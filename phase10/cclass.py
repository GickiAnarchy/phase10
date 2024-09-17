import uuid

class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.client_id = str(uuid.uuid4())  # Generate unique ID for the client
        self.server_id = None  # Store server-assigned ID

    def set_server_id(self, server_id):
        self.server_id = server_id
