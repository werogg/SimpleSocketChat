import socket
import threading
import sys


class ChatClient:

    def __init__(self, host="localhost", port=5542):
        self.host = host
        self.port = port
        self.client_socket = None
        self.sentence = ""

    def open_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.sentence = bytes(input("Type your nickname:\n"), encoding="utf8")
        self.client_socket.send(self.sentence)
        srv_response = self.client_socket.recv(1024)
        print("Server {}:{} responded: {}".format(self.host, self.port, srv_response))

    def communication_handling(self):
        try:
            while True:
                srv_response = self.client_socket.recv(1024)
                print(srv_response)
        except socket.error:
            sys.exit(-1)

    def run(self):
        self.open_socket()
        receiving_thread = threading.Thread(target=self.communication_handling)
        receiving_thread.start()

        try:
            while True:
                self.sentence = bytes(input(""), encoding="utf8")
                self.client_socket.send(self.sentence)
        except socket.error:
            sys.exit(-1)


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.run()
