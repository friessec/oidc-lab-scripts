from api.rest import Rest


class RpTest(Rest):
    def __init__(self, profapi, configname):
        super().__init__(profapi, "rp", configname)
