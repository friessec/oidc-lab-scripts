import json
import threading
import socketserver

from time import sleep


class Intercept():
    def __init__(self, search, replace):
        self.search = search
        self.replace = replace


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cmd = json.loads(data)

        if cmd.get("type") == 'clear':
            self.server.controller.clear()
        elif cmd.get("type") == 'request':
            intercept = Intercept(cmd.get('search'), cmd.get('replace'))
            self.server.controller.requestInterceptor = intercept
        elif cmd.get("type") == 'response':
            intercept = Intercept(cmd.get('search'), cmd.get('replace'))
            self.server.controller.responseInterceptor = intercept

        response = bytes("OK", 'ascii')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, host_port_tuple, streamhandler, controller):
        super().__init__(host_port_tuple, streamhandler)
        self.controller = controller


class Controller(object):
    def __init__(self):
        self.__requestInterceptor = []
        self.__responseInterceptor = []

    def clear(self):
        self.__requestInterceptor.clear()
        self.__responseInterceptor.clear()

    @property
    def requestInterceptor(self):
        return self.__requestInterceptor

    @requestInterceptor.setter
    def requestInterceptor(self, value):
        self.__requestInterceptor.append(value)

    @property
    def responseInterceptor(self):
        return self.__responseInterceptor

    @responseInterceptor.setter
    def responseInterceptor(self, value):
        self.__responseInterceptor.append(value)


class ProfessosEnhancer(object):

    def __init__(self) -> None:
        print("Init Server")
        self.controller = Controller()
        self.server = None
        self.finished = True

    def running(self):
        if self.server is not None:
            print("Server is already running")
            return
        HOST, PORT = "0.0.0.0", 8042
        self.server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, self.controller)
        ip, port = self.server.server_address

        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Enhancer listens on {}:{}".format(ip,port))

    def request(self):
        for intercept in self.controller.requestInterceptor:
            print(intercept.search, intercept.replace)

    def response(self):
        for intercept in self.controller.responseInterceptor:
            print(intercept.search, intercept.replace)

    def done(self):
        if self.server is not None:
            self.server.shutdown()
            self.server = None
        print("Finish")


if __name__ == "__main__":
    prof = ProfessosEnhancer()
    try:
        prof.running()
        while(prof.finished):
            sleep(3)
            print("============ REQUESTS =============")
            prof.request()
            print("============ RESPONSE =============")
            prof.response()
    finally:
        prof.done()
