from testplan.base import BaseTest

class RpTest(BaseTest):
    def __init__(self, profapi):
        super().__init__(profapi, "rp", "mitreid-client")
