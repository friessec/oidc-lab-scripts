import requests
import json
import time
import os
import base64
from bs4 import BeautifulSoup
from datetime import datetime

class BaseTest(object):

    def __init__(self, profapi, target_type, target_name):
        self.profapi = profapi
        self.target_type = target_type
        self.target_name = target_name
        self.testId = ""
        self.testObj = None
        self.staticCfg = None
        self.initialized = False

    def create(self):
        url = self.profapi + '/' + self.target_type + '/create-test-object'
        response = ""
        testID = None

        staticConfig = "config/" + self.target_type + "/" + self.target_name + "/statictest.json"
        if os.path.exists(staticConfig):
            staticFile = open("config/" + self.target_type + "/" + self.target_name + "/statictest.json", "r+")
            self.staticCfg = json.load(staticFile)
            testID = self.staticCfg['testId']

        if testID:
            header = {"Content-type": "application/x-www-form-urlencoded"}
            payload = "test_id=" + testID
            response = requests.post(url, data=payload, headers=header)
        else:
            response = requests.post(url)
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        response_json = json.loads(response.text)
        self.testId = response_json["TestId"]
        self.testObj = response_json

        print("Create new test plan: TestId = {}".format(self.testId))

    def clean(self):
        if len(self.testId) == 0 or not self.initialized:
            return
        url = self.profapi + '/delete-test-object'
        header = {"Content-type": "application/x-www-form-urlencoded"}
        payload = "test_id=" + self.testId
        response = requests.post(url, data=payload, headers=header)
        if response.status_code != 200 and response.status_code != 204:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        print("Delete test plan ID: {}".format(self.testId))

    def set_config(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/config'
        header = {"Content-Type": "application/json"}
        jsonFile = open("config/" + self.target_type + "/" + self.target_name + "/professos.json", "r+")
        jsoncfg=json.load(jsonFile)

        payload = self.testObj["TestConfig"]
        payload.update(jsoncfg)

        response = requests.post(url, json=payload, headers=header)
        if response.status_code != 200 and response.status_code != 204:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        print("Updated config: {}".format(json.dumps(payload, indent=4)))

    def get_config(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/config'
        header = {"Content-Type": "application/json"}

        response = requests.get(url, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('GET {} Error {}'.format(url, response.status_code))
        print("{}".format(json.dumps(response.json(), indent=4)))

    def learn(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/learn'
        header = {"Content-type": "application/json"}

        jsonFile = open("config/" + self.target_type + "/" + self.target_name + "/professos.json", "r+")
        jsoncfg = json.load(jsonFile)

        payload = self.testObj["TestConfig"]
        payload.update(jsoncfg)

        print("Learn: {}".format(json.dumps(payload, indent=4)))

        response = requests.post(url, json=payload, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        self.initialized = True

    def runAllTests(self):
        skip_tests = None
        if self.staticCfg and self.staticCfg['skipTests'] != "":
            skip_tests = [int(x) for x in self.staticCfg['skipTests'].split(",")]

        for i, item in enumerate(self.testObj["TestReport"]["TestStepResult"]):
            if skip_tests:
                if i not in skip_tests:
                    self.runTest(i)
                else:
                    print('='*80)
                    print("Skip Test [{}]: {}".format(i, self.testObj["TestReport"]["TestStepResult"][i]['StepReference']['Name']))
            else:
                self.runTest(i)

    def runTest(self, id, screenshot=False):
        print('='*80)
        testStep = self.testObj["TestReport"]["TestStepResult"][id]

        test = testStep['StepReference']['Name']

        print("Run Test Step [{}]: {}".format(id, test), end='')

        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/test/' + test
        header = {"Content-type": "application/json"}

        response = requests.post(url, headers=header)
        if response.status_code != 200:
            print()
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        result = response.json()
        result_status = result['Result']
        print(" - {}".format(result_status))
        if screenshot:
            # print("{}".format(json.dumps(result['LogEntry'], indent=4)))
            cnt = 0
            for entry in result['LogEntry']:
                if entry["Screenshot"]:
                    cnt += 1
                    directory = "results/" + self.target_type + "/" + self.target_name
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open("{}/screenshot{}.png".format(directory, cnt), "wb") as file:
                        file.write(base64.b64decode(entry["Screenshot"]["Data"]))

        if result_status != 'PASS':
            for entry in result['LogEntry']:
                date = time.localtime(entry['Date'])
                print("{}: {}".format(time.strftime("%H:%M:%S", date), entry['Text']))
                if entry["CodeBlock"]:
                    print("{}".format(json.dumps(entry['CodeBlock'], indent=2)))
                if entry["HttpRequest"]:
                    print("{}".format(json.dumps(entry['HttpRequest'], indent=2)))
                if entry["HttpResponse"]:
                    print("{}".format(json.dumps(entry['HttpResponse'], indent=2)))
                print('-' * 80)

    def export_result(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/export'
        header = {"Content-Type": "application/json"}

        response = requests.get(url, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('GET {} Error {}'.format(url, response.status_code))
        xml_response = BeautifulSoup(response.content, "xml").prettify()

        directory = "results/" + self.target_type + "/" + self.target_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open (directory + "/result-" + datetime.now().isoformat(timespec='minutes') + ".xml", "w") as file:
            file.write(xml_response)

    def run(self, export_results=False, run_test=None, screenshot=False):
        try:
            self.create()
            if self.staticCfg:
                self.set_config()
            else:
                self.learn()
            if run_test:
                for i in run_test:
                    self.runTest(int(i), screenshot=screenshot)
            else:
                self.runAllTests()
            if export_results:
                self.export_result()
        except requests.RequestException as e:
            print("Received error from Professos")
            print(str(e))
        finally:
            self.clean()
