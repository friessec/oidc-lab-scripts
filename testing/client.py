import base64
import json
import socket
from time import sleep


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

if __name__ == "__main__":
    command({'type': 'request', 'search': base64.b64encode('honestOP'.encode('ascii')).decode('ascii'), 'replace':  base64.b64encode('attackOP'.encode('ascii')).decode('ascii')})
    sleep(2)
    command({'type': 'response', 'search':  base64.b64encode('honestRP'.encode('ascii')).decode('ascii'), 'replace':  base64.b64encode('attackRP'.encode('ascii')).decode('ascii')})
    sleep(4)
    command({'type': 'clear'})

