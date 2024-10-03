# server:
#
# import asyncio
#
# async def handle_client(reader, writer):
#     while True:
#         data = await reader.read(1024)
#         if not data:
#             break
#         message = data.decode()
#         print(f"Received message: {message}")
#         writer.write(b"Message received")
#         await writer.drain()
#
# async def main():
#     server = await asyncio.start_server(
#         handle_client, "127.0.0.1", 8888
#     )
#
#     async with server:
#         await server.serve_forever()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
# server2:
#
# import asyncio
#
# async def handle_client(reader, writer):
#     while True:
#         data = await reader.read(1024)
#         if not data:
#             break
#         message_json = data.decode()
#         message_dict = json.loads(message_json)
#         print(f"Received message: {message_dict}")
#         writer.write(b"Message received")
#         await writer.drain()
#
# async def main():
#     server = await asyncio.start_server(
#         handle_client, "127.0.0.1", 8888
#     )
#
#     async with server:
#         await server.serve_forever()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
# client:
#
# import asyncio
#
# async def main():
#     reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
#
#     while True:
#         message = input("Enter a message: ")
#         writer.write(message.encode())
#         await writer.drain()
#
#         data = await reader.read(1024)
#         print(f"Received: {data.decode()}")
#
#     writer.close()
#     await writer.wait_closed()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
#
# client 2:
#
# import asyncio
# import json
#
# from common import Client
#
# async def send_message(client: Client, message: dict):
#     """Sends a dictionary message to the server through the provided Client object."""
#     writer = client.writer
#     message_json = json.dumps(message)
#     writer.write(message_json.encode())
#     await writer.drain()
#
# async def main():
#     reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
#     client = Client(reader, writer)
#
#     while True:
#         message_dict = {
#             "key1": "value1",
#             "key2": 123
#         }  # Replace with your desired dictionary
#
#         await send_message(client, message_dict)
#
#         data = await reader.read(1024)
#         message_json = data.decode()
#         message_dict = json.loads(message_json)
#         print(f"Received: {message_dict}")
#
#     writer.close()
#     await writer.wait_closed()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
#
# BACKUPS:
#
# server:
#
# ###/usr/bin/env python
#
# import asyncio
# import json
# import pickle
# from types import new_class
#
# from common import Client
#
# clients = {}
#
#
# async def handle_client(reader, writer):
#     while True:
#         data = await reader.read(1024)
#         if not data:
#             break
#         message_json = data.decode()
#         message = json.loads(message_json)
#         print(f"Received message: {message}")
#         print(type(message))
#
#         try:
#             typ = message["type"]
#         except Exception as e:
#             print(f"{e}")
#         client = Client(reader, writer)
#
#         if typ == "register":
#             new_client = pickle.loads(message["client"])
#             # new_client.set_client_id([message["client_id"]])
#             clients[new_client.client_id] = new_client
#
#             ret_msg = {
#                 "reply": "GOOD",
#                 "client_id": new_client.client_id,
#                 "say": "ACKKKKKKKKK"
#             }
#
#             writer.write(ret_msg)
#             await writer.drain()
#         else:
#             for k, v in clients.items():
#                 if message["client_id"] == k:
#                     client = v
#
#         if typ == "disconnect":
#             del clients[client.client_id]
#
#             print(f"Received disconnect message: {message}")
#             writer.write(b"Message received")
#             await writer.drain()
#
#
# async def main():
#     server = await asyncio.start_server(
#         handle_client, "127.0.0.1", 8888
#     )
#
#     async with server:
#         await server.serve_forever()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
#
# client:
#
# #!/usr/bin/env python
#
# import asyncio
# import json
# import pickle
#
# from common import Client
#
#
# CLIENT = Client()
#
#
#
# async def send_message(message: dict):
#     writer = CLIENT.writer
#     message_json = json.dumps(message)
#     writer.write(message_json.encode())
#     await writer.drain()
#
#
#
# async def main(client = None):
#     reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
#
#     if client is None:
#         CLIENT = Client(reader, writer)
#     else:
#         CLIENT = client
#         CLIENT.reader = reader
#         CLIENT.writer = writer
#
#     CLIENT.client_id = CLIENT.make_client_id()
#
#     message = {
#         "type": "register",
#         "client_id": CLIENT.client_id,
#         "client": {pickle_client(CLIENT)}
#     }
#     await send_message(message)
#
#     data = await reader.read(1024)
#     m = data.decode()
#     print(f"Received: {m["say"]}")
#     writer.close()
#     await writer.wait_closed()
#
# def get_client():
#     return CLIENT
#
# def pickle_client(cl):
#     p_client = pickle.dumps(cl)
#     return p_client
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
# def run_client():
#     asyncio.run(main())
#
#
#
#
#
#
