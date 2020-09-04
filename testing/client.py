import base64
import json
import socket
from urllib.parse import urlparse, quote

from time import sleep


class ClearCommand:
    def __init__(self):
        self.type = "clear"


class ReplaceCommand:
    def __init__(self):
        self.type = "request"
        self.action = "querySearchReplace"
        self.uri = ""
        self.keyVal = {}

    def replaceKeyVal(self, key, value):
        self.keyVal[key] = quote(value)

    def queryReplaceCommand(self, requestUri):
        parse = urlparse(requestUri)

        # Check if url same
        if self.uri != parse.netloc+parse.path:
            print('{}{}'.format(parse.netloc, parse.path))
            return None

        querys = parse.query.split("&")
        new_query = []
        for query in querys:
            key, value = query.split('=')
            print(self.keyVal)
            if key in self.keyVal:
                print(key)
                value = self.keyVal.get(key)
            query = key + '=' + quote(value)
            new_query.append(query)

        new_query = "&".join(new_query)
        return parse._replace(query=new_query).geturl()


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


