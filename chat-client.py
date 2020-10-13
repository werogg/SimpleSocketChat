import socket
import threading
import sys


class ChatClient:

    def __init__(self, host="localhost", port=5541):
        self.host = host
        self.port = port
        self.client_socket = None
        self.sentence = ""

    def open_socket(self):
        # Open and define a new socket stream via internet
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))  # Connect the socket to the desired HOST & IP
        self.sentence = bytes(input("Type your nickname:\n"), encoding="utf8")  # First input will be the client's nick
        self.client_socket.send(self.sentence)  # Send the sentence via socket
        srv_response = self.client_socket.recv(1024)  # Receive the server response in a 1024 bytes sentence
        print("Server {}:{} responded: {}".format(self.host, self.port, srv_response))

    def communication_handling(self):
        try:
            # Non stop receiving and printing server responses
            while True:
                srv_response = self.client_socket.recv(1024)
                print(srv_response.decode())
        except socket.error:
            sys.exit(-1)

    def run(self):
        self.open_socket()
        receiving_thread = threading.Thread(target=self.communication_handling)  # Open thread for server communication
        receiving_thread.start()

        try:
            while True:
                self.sentence = bytes(input(""), encoding="utf8")  # Get user input and encode it to bytes
                self.client_socket.send(self.sentence)  # Send the sentence via socket
        except socket.error:
            sys.exit(-1)


if __name__ == "__main__":
    port = int(input("Port to connect:\n"))
    chat_client = ChatClient(port=port)
    chat_client.run()
