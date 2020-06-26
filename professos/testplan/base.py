import requests, json


class BaseTest(object):

    def __init__(self, profapi, target):
        self.profapi = profapi
        self.target = target
        self.testId = ""
        self.testObj = None
        self.initialized = False

    def create(self):
        url = self.profapi + '/' + self.target + '/create-test-object'
        response = requests.post(url)
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        response_json = json.loads(response.text)
        self.testId = response_json["TestId"]
        self.testObj = response_json
#        for i in response_json:
#            print(i)
        print("Create new test plan: TestId={}".format(self.testId))

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
        url = self.profapi + '/' + self.target + '/' + self.testId + '/config'
        header = {"Content-Type": "application/json"}
        #header = {"Content-type": "application/json"}
        jsonFile = open("config/op/mitreid-server/professos.json", "r+")
        jsoncfg=json.load(jsonFile)

        payload = self.testObj["TestConfig"]
        payload.update(jsoncfg)

        response = requests.post(url, json=payload, headers=header)
        if response.status_code != 200:
            raise requests.RequestException('POST {} Error {}'.format(url, response.status_code))
        print("Updated config: {}".format(json.dumps(payload, indent=4)))


    def learn(self):
        url = self.profapi + '/' + self.target + '/' + self.testId + '/learn'
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
