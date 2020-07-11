#!/usr/bin/env python3

import os
import sys
import argparse


from testplan.op import OpTest
from testplan.rp import RpTest


professos_url = "http://localhost:8888/api"
#professos_url = "https://openid.professos/api"

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
    parser.add_argument('--export', action='store_true',
                        default=False,
                        help='export result to file')
    parser.add_argument('--test', help="A comma separated list of tests which should run", type=lambda x: x.split(','))
    args = parser.parse_args()

    print(args.test)

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

    if args.test:
        obj.run(run_test=args.test, export_results=args.export)
    else:
        obj.run(export_results=args.export)
