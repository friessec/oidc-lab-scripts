from testplan.base import BaseTest

class OpTest(BaseTest):
    def __init__(self, profapi):
        super().__init__(profapi, "op")
