#!/usr/bin/env python3
import requests
import os
import sys
import argparse


from testplan.op import OpTest
from testplan.rp import RpTest


professos_url = "http://localhost:8888/api"
#professos_url = "https://openid.professos/api"


def testhandler(testobj):
    try:
        testobj.create()
        testobj.set_config()
        #testobj.learn()
        testobj.get_config()
        #testobj.runAllTests()
        testobj.runTest(0)
        #testobj.export_result()
    except requests.RequestException as e:
        print("Received error from Professos")
        print(str(e))
    finally:
        testobj.clean()


if __name__ == '__main__':
    print("[*] Professos CLI started")

    parser = argparse.ArgumentParser(description='Professos command line interface.')
    parser.add_argument('config', type=str, help='Configuration to run')
    parser.add_argument('--op', action='store_true',
                    default=False,
                    help='op tests')
    parser.add_argument('--rp', action='store_true',
                        default=False,
                        help='rp tests')
    args = parser.parse_args()

    if args.rp == args.op:   # xor
        print("Choose OP or RP tests")
        sys.exit(-1)


    if not os.path.exists("config/" + "op/" if args.op else "rp/" + args.config ):
        print("No configuration found for: ", args.config)
        sys.exit(-1)

    if args.op:
        obj = OpTest(professos_url, args.config)
    else:
        obj = RpTest(professos_url, args.config)
    testhandler(obj)


