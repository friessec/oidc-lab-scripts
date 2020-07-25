#!/usr/bin/env python3

import http.server
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="results", **kwargs)


def start_server(address="127.0.0.1", port=8000):
    with socketserver.TCPServer((address, port), Handler) as httpd:
        print("Server started at: http://{}:{}".format(address,port))
        httpd.serve_forever()


if __name__ == '__main__':
    print("[*] Start server")
    start_server()
