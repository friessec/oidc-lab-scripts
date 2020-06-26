import requests, json


class BaseTest(object):

    def __init__(self, profapi, target):
        self.profapi = profapi
        self.target = target
        self.testId = ""
        self.testObj = None
        self.initialized = False

    def create(self):
        response = requests.post(self.profapi + self.target + '/create-test-object')
        if response.status_code != 200:
            raise requests.RequestException('POST /{}/create-test-object {}'.format(self.target, response.status_code))
        response_json = json.loads(response.text)
        self.testId = response_json["TestId"]
        self.testObj = response_json
#        for i in response_json:
#            print(i)
        print("Create new test plan: TestId={}".format(self.testId))

    def clean(self):
        if len(self.testId) == 0 or not self.initialized:
            return
        header = {"Content-type": "application/x-www-form-urlencoded"}
        payload = "test_id=" + self.testId
        response = requests.post(self.profapi + '/delete-test-object', data=payload, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('POST /delete-test-object {}'.format(response.status_code))
        print("Delete test plan ID: {}".format(self.testId))

    def learn(self):
        header = {"Content-type": "application/json"}
        payload = self.testObj["TestConfig"]
        #print(payload)
        response = requests.post(self.profapi + self.target + '/learn', data=payload, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('POST /{}/learn {}'.format(self.target, response.status_code))
        print(response)
        self.initialized = True
