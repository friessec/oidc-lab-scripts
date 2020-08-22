import os
import json


class TestConfig(object):

    def __init__(self):
        self.discovery = True
        self.dynamic = True
        self.pre_expose = False
        self.test_id = ""
        self.skip_tests = ""


    def loadJson(self, file):
        if not os.path.exists(file):
            return None
        with open(file, 'r') as jsonData:
            data = json.load(jsonData)
            self.test_id = data.get('test_id', "")
            skipTests = data.get('skip_tests', "")
            if skipTests != "":
                self.skip_tests = [int(x) for x in skipTests.split(",")]
            self.discovery = data.get('discovery', True)
            self.dynamic = data.get('dynamic', True)
            self.pre_expose = data.get('pre_expose', True)


if __name__ == "__main__":
    cfg = TestConfig()
    cfg.loadJson("../../config/rp/angular-auth-oidc/config.json")

    print(cfg.discovery)
    print(cfg.test_id)
    print(cfg.skip_tests)
    print(cfg.dynamic)