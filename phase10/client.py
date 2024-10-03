import asyncio
import json

from common import Client


async def connect(cl:Client):
    client=cl
    client.reader, client.writer = await asyncio.open_connection("127.0.0.1", 8888)
    client.make_client_id()  # Client creates the client_id
    return client

async def send_message(client: Client, message: dict):
    writer = client.writer
    message_json = json.dumps(message)
    writer.write(message_json.encode())
    await writer.drain()

async def main(c = Client()):
    client = await connect(c)

    while True:
        message_dict = {
            "type": "register",
            "client_id": client.client_id
        }

        await send_message(client, message_dict)

        data = await client.reader.read(1024)
        message_json = data.decode()
        message_dict = json.loads(message_json)
        print(f"Received: {message_dict}")

        client.writer.close()
        await client.writer.wait_closed()


def run_main():
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())