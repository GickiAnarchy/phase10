import asyncio
import json

from common import Client

clients = {}


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message_json = data.decode()
        message = json.loads(message_json)

        type = None

        try:
            type = message["type"]
        except:
            print("There is no 'type' value in the message.")
            break
        if type == "register":
            new_client = Client(reader,writer)
            new_client.set_client_id(message["client_id"])

            c_id = message["client_id"]
            clients[c_id] = json.dumps(new_client)

            print(f"Received message: {message}")
            writer.write(b"Message received: Registered Client {c_id}")
            await writer.drain()

async def main():
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 8888
    )

    async with server:
        print("Server Listening")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())