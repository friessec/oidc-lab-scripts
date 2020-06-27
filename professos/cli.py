#!/usr/bin/env python3
import requests

from testplan.op import OpTest

professos_url = "http://localhost:8888/api"
#professos_url = "https://openid.professos/api"

if __name__ == '__main__':
    print("[*] Professos CLI started")

    op = OpTest(professos_url)

    try:
        op.create()
        #op.set_config()
        op.learn()
        op.runAllTests()
        #op.runTest(0)
    except requests.RequestException as e:
        print("Received error from Professos")
        print(str(e))
    finally:
        op.clean()

