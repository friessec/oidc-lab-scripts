import base64
import json
import socket
from urllib.parse import urlparse, quote

from time import sleep


class CMDDef:
    TYPE_CLEAR = "clear"
    TYPE_REQUEST = "request"

    QUERY_SEARCH_REPLACE = "querySearchReplace"

class ClearCommand:
    def __init__(self):
        self.type = CMDDef.TYPE_CLEAR


class ReplaceCommand:
    def __init__(self):
        self.type = CMDDef.TYPE_REQUEST
        self.action = CMDDef.QUERY_SEARCH_REPLACE
        self.uri = ""
        self.keyVal = {}

    def replaceKeyVal(self, key, value):
        self.keyVal[key] = quote(value)


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))


def command(cmd):
    data = json.dumps(cmd.__dict__)
    client(ip, port, data)


ip, port = "localhost", 8042

if __name__ == "__main__":
    cmd = ReplaceCommand()
    cmd.replaceKeyVal("redirect_uri", '<script>"42"</script>')

    command(cmd)
    sleep(4)
    command(ClearCommand())


