#!/usr/bin/env python3
import requests

from professos.testplan.op import OpTest

professos_url = "http://localhost:8888/api/"

if __name__ == '__main__':
    print("[*] Professos CLI started")

    op = OpTest(professos_url)

    try:
        op.create()
        op.learn()
    except requests.RequestException as e:
        print("Received error from Professos")
        print(str(e))
    finally:
        op.clean()

