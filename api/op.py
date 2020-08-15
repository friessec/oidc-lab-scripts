from api.rest import Rest


class OpTest(Rest):
    def __init__(self, profapi, configname):
        super().__init__(profapi, "op", configname)
