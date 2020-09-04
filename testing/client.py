import base64
import json
import socket
from urllib.parse import urlparse, quote

from time import sleep


class ReplaceCommand:
    def __init__(self):
        self.type = "request"
        self.action = "querySearchReplace"
        #self.uri = "site/authorize"
        self.uri = "mitreid-server/oidc-server/authorize"
        self.keyVal = {}

    def replaceKeyVal(self, key, value):
        self.keyVal[key] = quote(value)

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

ip, port = "localhost", 8042


def command(cmd):
    data = json.dumps(cmd)
    client(ip, port, data)

TestData="https://mitreid-server/oidc-server/authorize?scope=openid+profile&response_type=code&redirect_uri=https%3A%2F%2Fevilrp.professos%2F29UwVyVD6y8%2Fcallback&state=TEouYMYDFcHy46rW_LbE6e2MLDTPqIYPUPJAHFdP3rw&nonce=zZk79HrChtcrTekKZAw8BECGe8hMNWgonKUk07kCAUM&client_id=ed419096-3b8c-4767-83ff-8c4f4d581585"


def queryReplaceCommand(requestUri, command):
    parse = urlparse(requestUri)

    # Check if url same
    if command.uri != parse.netloc+parse.path:
        print('{}{}'.format(parse.netloc, parse.path))
        return None

    querys = parse.query.split("&")
    new_query = []
    for query in querys:
        key, value = query.split('=')
        print(command.keyVal)
        if key in command.keyVal:
            print(key)
            value = command.keyVal.get(key)
        query = key + '=' + quote(value)
        new_query.append(query)

    new_query = "&".join(new_query)
    return parse._replace(query=new_query).geturl()


if __name__ == "__main__":
    cmd = ReplaceCommand()
    cmd.replaceKeyVal("redirect_uri", '<script></script>')

    jsonStr = json.dumps(cmd.__dict__)
    print(jsonStr)

    newRequest = queryReplaceCommand(TestData, cmd)
    print(newRequest)



    #command({'type': 'request', 'search': base64.b64encode('honestOP'.encode('ascii')).decode('ascii'), 'replace':  base64.b64encode('attackOP'.encode('ascii')).decode('ascii')})
    #sleep(2)
    #command({'type': 'response', 'search':  base64.b64encode('honestRP'.encode('ascii')).decode('ascii'), 'replace':  base64.b64encode('attackRP'.encode('ascii')).decode('ascii')})
    #sleep(4)
    #command({'type': 'clear'})

