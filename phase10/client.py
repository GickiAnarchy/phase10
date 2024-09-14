import asyncio
import json

from game.game import Game

async def send_message(message):
    reader, writer = await asyncio.open_connection('localhost', 8888)
    print(f"Sending message: {message}")
    writer.write(json.dumps(message).encode() + b'\n')
    await writer.drain()
    data = await reader.readuntil(b'\n')
    try:
        Game().from_json(data.decode())
    except:
        print("idk")
    print(f"Received: {data.decode()}")
    writer.close()
    await writer.wait_closed()

async def main():
    while True:
        """
        m = input("Enter your message (or 'quit' to exit): ")
        if m.lower() == 'quit':
            break
        """
        message = {"type": 'join'}
        await send_message(message)



if __name__ == '__main__':
    asyncio.run(main())
