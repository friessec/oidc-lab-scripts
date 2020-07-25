from testplan.base import BaseTest

class RpTest(BaseTest):
    def __init__(self, profapi, configname):
        super().__init__(profapi, "rp", configname)
