import socket
import threading
import sys


class ChatServer:

    def __init__(self, host='localhost', port=5541):
        self.clients = []
        self.host = host
        self.port = port
        self.server_socket = None
        self.command_handling_thread = None
        self.client_handling_thread = None

    def command_handling(self):
        while True:

            user_input = input('Waiting for server communications...\n')

            if user_input == "list":
                # List all connected users with their info
                for client in self.clients:
                    if client.online:
                        print("Name: {}\nIP: {}".format(client.name, client.address))
            else:
                pass

    def client_handling(self, new_client):
        try:
            # Receive the first 1024 bytes as client's nickname and define it
            sentence = new_client.client_socket.recv(1024)
            new_client.name = sentence
            identification_msg = bytes("Client {} has logged in.".format(new_client.name), encoding="utf8")
            print(identification_msg)
            new_client.client_socket.send(identification_msg)  # Send to the client the login confirmation

            # Send client login confirmation to every connected client with an open socket
            for client in self.clients:
                if client.online:
                    client.client_socket.send(identification_msg)

            # Non stop receiving sentences from the client socket and resending it to all the clients
            while True:
                message = new_client.client_socket.recv(1024)
                serv_response = bytes("{} -> {}".format(new_client.name, message), encoding="utf8")
                print(serv_response.decode(encoding="utf-8"))

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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Open a new socket stream
        self.server_socket.bind((self.host, self.port))  # Bind the new socket to a specific HOST & IP
        self.server_socket.listen(1)  # Let the server accept new connections
        # Create and start new thread to handle server commands
        self.command_handling_thread = threading.Thread(target=self.command_handling)
        self.command_handling_thread.start()

        # Keep main thread in a infinite loop listening for new connections
        while True:
            client_socket, address = self.server_socket.accept()
            print("Incoming connection accepted")

            # Create a new object and thread to handle the communication between the server and the new client
            new_client = Client(client_socket, "undefined", True, address)
            self.clients.append(new_client)  # We add the Client's object to a common pool
            self.client_handling_thread = threading.Thread(target=self.client_handling, args=(new_client,))
            self.client_handling_thread.start()


class Client:

    def __init__(self, client_socket, name, online, address):
        self.client_socket = client_socket
        self.name = name
        self.online = online
        self.address = address


if __name__ == "__main__":
    port = int(input("Port to connect:\n"))
    chat_server = ChatServer(port=port)
    chat_server.run()
