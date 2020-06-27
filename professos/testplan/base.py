import requests
import json
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime

class BaseTest(object):

    def __init__(self, profapi, target_type, target_name):
        self.profapi = profapi
        self.target_type = target_type
        self.target_name = target_name
        self.testId = ""
        self.testObj = None
        self.initialized = False

    def create(self):
        url = self.profapi + '/' + self.target_type + '/create-test-object'
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
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        print("Updated config: {}".format(json.dumps(payload, indent=4)))

    def get_config(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/config'
        header = {"Content-Type": "application/json"}

        response = requests.get(url, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('GET {} Error {}'.format(url, response.status_code))
        print(response.content)

    def learn(self):
        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/learn'
        header = {"Content-type": "application/json"}
        jsonFile = open("config/op/mitreid-server/professos.json", "r+")
        jsoncfg=json.load(jsonFile)

        payload = self.testObj["TestConfig"]
        payload.update(jsoncfg)

        print("Learn: {}".format(json.dumps(payload, indent=4)))

        response = requests.post(url, json=payload, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        self.initialized = True

    def runAllTests(self):
        for i, item in enumerate(self.testObj["TestReport"]["TestStepResult"]):
            self.runTest(i)

    def runTest(self, id):
        print('='*80)
        testStep = self.testObj["TestReport"]["TestStepResult"][id]

        test = testStep['StepReference']['Name']

        print("Run Test Step: {}".format(test), end='')

        url = self.profapi + '/' + self.target_type + '/' + self.testId + '/test/' + test
        header = {"Content-type": "application/json"}

        response = requests.post(url, headers=header)
        if response.status_code != 200:
            print()
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        result = response.json()
        result_status = result['Result']
        print(" - {}".format(result_status))
#        print("{}".format(json.dumps(result['LogEntry'], indent=4)))
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
        print(xml_response)

        with open (directory + "/result-" + datetime.now().isoformat(timespec='minutes') + ".xml", "w") as file:
            file.write(xml_response)
