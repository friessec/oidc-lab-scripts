from testplan.base import BaseTest

class OpTest(BaseTest):
    def __init__(self, profapi, configname):
        super().__init__(profapi, "op", configname)
