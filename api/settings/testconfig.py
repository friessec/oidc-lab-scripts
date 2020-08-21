import os
import json


class TestConfig(object):

    def __init__(self):
        self.discovery = True
        self.dynamic = True

    def loadJson(self, file):
        if not os.path.exists(file):
            return None
        with open(file, 'r') as jsonData:
            data = json.load(jsonData)
            self.testId = data['testId']
            self.skipTests = data['skipTests']
            self.disable_dynamic = data['disable_dynamic']


if __name__ == "__main__":
    cfg = TestConfig()
    cfg.loadJson("../../config/rp/angular-auth-oidc/statictest.json")

    print(cfg.discovery)
    print(cfg.testId)
    print(cfg.skipTests)