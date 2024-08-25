
import asyncio


class Client:
    def __init__(self, reader, writer, name):
        self.reader = readergc
        self.writer = writer
        self.name = name


addr = "localhost"

async def connect_and_send_message(message):
    reader, writer = await asyncio.open_connection(addr, 8888)
    writer.write(message.encode())
    await writer.drain()
    data = await reader.readuntil(b'\n')
    print(f"Received: {data.decode()}")
    writer.close()

asyncio.run(connect_and_send_message('Hello from client'))
