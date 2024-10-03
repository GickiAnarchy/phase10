#!/usr/bin/env python

import uuid


class Client:
    def __init__(self, reader=None, writer=None):
        self.reader = reader
        self.writer = writer
        self.client_id = None

    def set_client_id(self, client_id):
        self.client_id = client_id

    def make_client_id(self):
        self.client_id =  str(uuid.uuid4())

    def __dict__(self):
        return {
            "reader": self.reader,
            "writer": self.writer,
            "client_id": self.client_id
        }
