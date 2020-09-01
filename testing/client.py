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
    command({'type': 'request', 'search': 'honestOP', 'replace': 'attackOP'})
    sleep(2)
    command({'type': 'response', 'search': 'honestRP', 'replace': 'attackRP'})
    sleep(4)
    command({'type': 'clear'})

