#!/usr/bin/env python3
import requests
import os

from testplan.op import OpTest
from testplan.rp import RpTest


professos_url = "http://localhost:8888/api"
#professos_url = "https://openid.professos/api"


def testhandler(testobj):
    try:
        testobj.create()
        #testobj.set_config()
        testobj.learn()
        testobj.runAllTests()
        #testobj.runTest(0)
        testobj.export_result()
    except requests.RequestException as e:
        print("Received error from Professos")
        print(str(e))
    finally:
        testobj.clean()


if __name__ == '__main__':
    print("[*] Professos CLI started")

#    obj = OpTest(professos_url)
    obj = RpTest(professos_url)
    testhandler(obj)


