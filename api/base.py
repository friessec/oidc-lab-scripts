import requests
import json
import time
import os
import base64
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


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

    def expose_discovery(self, id=0):
        testStep = self.testObj["TestReport"]["TestStepResult"][id]

        test = testStep['StepReference']['Name']
        #print("Expose discovery for Test: {}".format(test))
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/expose/' + test

        response = requests.post(url)
        if response.status_code != 200 and response.status_code != 204:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))

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

        result = response.json()
        if result["TestStepResult"]["Result"] != "PASS":
            print("Learn failed: {}".format(json.dumps(response.json(), indent=4)))
            raise requests.RequestException("Test Failed")



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

    def runTest(self, id):
        if self.staticCfg and self.staticCfg.get("preExpose"):
            self.expose_discovery(id)
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
        #print("{}".format(json.dumps(result, indent=4)))
        #print("{}".format(json.dumps(result['LogEntry'], indent=4)))
        directory = "results/" + self.target_type + "/" + self.target_name + "/test" + str(id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        for path in Path(directory).glob("*"):
            if path.is_file():
                path.unlink()

        with open("{}/result.json".format(directory), "w") as file:
            file.write(json.dumps(result['LogEntry'], indent=4))

        cnt = 0
        for entry in result['LogEntry']:
            if entry["Screenshot"]:
                cnt += 1
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
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/export-json'
        header = {"Content-Type": "application/json"}

        response = requests.get(url, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('GET {} Error {}'.format(url, response.status_code))

        directory = "results/" + self.target_type + "/" + self.target_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + "/result-" + datetime.now().isoformat(timespec='minutes') + ".json", "w") as file:
            json.dump(response.json(), file)

    def run(self, export_results=False, run_test=None):
        try:
            self.create()
            if self.staticCfg and self.staticCfg["disable_dynamic"]:
                self.set_config()
                if self.target_type == "rp":
                    self.expose_discovery(0)
            else:
                #self.set_config()
                self.learn()
            if run_test:
                for i in run_test:
                    self.runTest(int(i))
            else:
                self.runAllTests()
            if export_results:
                self.export_result()
        except requests.RequestException as e:
            print("Received error from Professos")
            print(str(e))
        finally:
            self.clean()

    def prepare(self):
        try:
            self.create()
            if self.staticCfg and self.staticCfg["disable_dynamic"]:
                self.set_config()
            self.expose_discovery(0)
        except requests.RequestException as e:
            print("Received error from Professos")
            print(str(e))