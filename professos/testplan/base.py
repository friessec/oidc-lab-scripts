import requests, json


#url = ""
#payload = {"number": 12524}
#header = {"Content-type": "application/x-www-form-urlencoded",}
#response_decoded_json = requests.post(url, data=payload, headers=header)


class BaseTest(object):

    def __init__(self, profapi, target):
        self.profapi = profapi
        self.target = target
        self.testId = ""
        self.testObj = None

    def create_test(self):
        response = requests.post(self.profapi + self.target + '/create-test-object')
        if response.status_code != 200:
            raise Exception('GET /{}/create-test-object {}'.format(self.target, response.status_code))
        response_json = json.loads(response.text)
        self.testId = response_json["TestId"]
        print(self.testId)
        self.testObj = response_json


