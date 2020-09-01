import socket
import threading
import socketserver

from time import sleep


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)
        print(self.server.controller.text)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, host_port_tuple, streamhandler, controller):
        super().__init__(host_port_tuple, streamhandler)
        self.controller = controller


class Controller(object):
    def __init__(self):
        self.text = "Hello"


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


#    def request(self, flow: http.HTTPFlow) -> None:
#        #ctx.log.info("Request: {}".format(self.controller.text))


#    def response(self, flow: http.HTTPFlow) -> None:
#        pass

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
            sleep(1)
    finally:
        prof.done()
