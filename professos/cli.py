#!/usr/bin/env python3

import requests, json

professos_url = "http://localhost:8888/api/"


def createTest(target="op"):
    resp = requests.post(professos_url + target + '/create-test-object')
    print(resp.text)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('GET /{}/create-test-object {}'.format(target, resp.status_code))



if __name__ == '__main__':
    print("[*] Professos CLI started")
    createTest()

