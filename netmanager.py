import socket

class NetworkManager:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.client_socket = None
        self.connected = False

    def connect(self, host, port):
        self.socket.connect((host, port))
        self.connected = True

    def accept_connection(self):
        self.client_socket, addr = self.socket.accept()
        self.connected = True

    def send_data(self, data):
        self.client_socket.send(data)

    def receive_data(self):
        data = self.client_socket.recv(1024)
        return data

    def close(self):
        self.socket.close()


MESSAGE_TYPES = [
    "CONNECT",
    "DISCONNECT",
    "CARD_DRAWN"]
    "CARD_PLAYED",
    "PHASE_COMPLETED",
    "GAME_OVER"]

class Message:
    def __init__(self, type, data):
        self.type = type
        self.data = data

