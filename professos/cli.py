#!/usr/bin/env python3


from professos.testplan.op import OpTest

professos_url = "http://localhost:8888/api/"





if __name__ == '__main__':
    print("[*] Professos CLI started")

    op = OpTest(professos_url)

    op.create_test()

