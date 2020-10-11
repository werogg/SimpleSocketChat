import socket
import threading
import sys


class ChatServer:

    def __init__(self, host='localhost', port=5542):
        self.clients = []
        self.host = host
        self.port = port
        self.server_socket = None
        self.command_handling_thread = None
        self.client_handling_thread = None

    def command_handling(self):
        while True:

            user_input = input('Waiting for commands...\n')

            if user_input == "list":
                for client in self.clients:
                    if client.online:
                        print("Name: {}\nIP: {}".format(client.name, client.address))
            elif user_input == "exit":
                self.close()
            else:
                pass

    def client_handling(self, new_client):
        try:
            sentence = new_client.client_socket.recv(1024)
            new_client.name = sentence
            identification_msg = bytes("Client {} has logged in.".format(new_client.name), encoding="utf8")
            print(identification_msg)
            new_client.client_socket.send(identification_msg)

            for client in self.clients:
                if client.online:
                    client.client_socket.send(identification_msg)

            while True:
                message = new_client.client_socket.recv(10242)
                serv_response = bytes("{} -> {}".format(new_client.name, message), encoding="utf8")
                print(serv_response)

                for client in self.clients:
                    if client.online:
                        client.client_socket.send(serv_response)

        except socket.error:
            sys.exit(-1)

    def close(self):
        for client in self.clients:
            client.client_socket.close()
        self.server_socket.close()
        sys.exit(0)

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.command_handling_thread = threading.Thread(target=self.command_handling)
        self.command_handling_thread.start()

        while True:
            client_socket, address = self.server_socket.accept()
            print("incoming connection accepted")
            new_client = Client(client_socket, "undefined", True, address)
            self.clients.append(new_client)
            self.client_handling_thread = threading.Thread(target=self.client_handling, args=(new_client,))
            self.client_handling_thread.start()


class Client:

    def __init__(self, client_socket, name, online, address):
        self.client_socket = client_socket
        self.name = name
        self.online = online
        self.address = address


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.run()
