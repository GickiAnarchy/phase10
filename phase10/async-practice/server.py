import asyncio
import json
from asyncio import StreamWriter

from common import Client


"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                    M A I N
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""


async def main():
    # Start the server at host:port
    try:
        server = await asyncio.start_server(handle_client, "127.0.0.1", 8899)
        async with server:
            print("Server Listening")
            await server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")

"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                S E R V E R
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""

clients_list = []
"""
    Saving and loading players
"""

async def handle_client(reader, writer):
    """
    Called when a client connects to host:port.
    """
    c_id = None #initialize c_id for the client_id
    try:
        while True:
            # Continuously check for messages from the client
            data = await reader.read(2048)
            if not data:
                break

            # Decode the message
            message_json = data.decode()
            message = json.loads(message_json)

            try:
                # Get the client_id
                c_id = message["client_id"]  # always include the client_id
            except Exception as e:
                print(e)

            try:
                # Get the type of message. Which is sent from the client.
                msg_type = message["type"]
            except Exception as e:
                print(f"There is no 'type' value in the message.\n{e}")
                break

            # Perform action here base on the message type.
            match msg_type:
                case "register":
                    # Register the client in the CLIENTS dictionary
                    new_client = Client(reader, writer)
                    new_client.make_client_id()
                    new_client.set_client_id(message["client_id"])
                    clients_list.append(new_client)

                    # Create the response back to the client and send
                    rep = {"type": "success", "client_id": c_id} # Message to send back to the client
                    rep_e = json.dumps(rep) # Encode with the GameEncoder
                    writer.write(rep_e.encode()) # Send to client
                    print(f"Message received: Registered Client {c_id}")
                    print(f"Registered Client Count: {len(clients_list)}")
                    await writer.drain() # Clear the write buffer

                case "get_clients":
                    ids = clients_list
                    rep = {
                        "type":msg_type,
                        "client_id": c_id,
                        "response": ids
                    }
                    # Create the response back to the client and send
                    rep_e = json.dumps(rep)  # Encode with the GameEncoder
                    writer.write(rep_e.encode())  # Send to client
                    await writer.drain()  # Clear the write buffer

                case _:
                    print(f"Type:{msg_type} is not recognized by the server")

    finally:
        if c_id and c_id in clients_list:
            clients_list.remove(c_id)
        writer.close()



#   Games Management
async def broadcast_game(gamestate, gclients):
    pass
    '''msg = {
        "type":"update",
        "gamestate":gamestate
    }
    for c in gclients:
        try:
            msg = json.dumps(msg)
            c.writer.write(msg.encode())
            print(f"Sending Game Update to : {c.client_id}")
            await c.writer.drain()
        except Exception as e:
            print(e)'''


if __name__ == "__main__":
    asyncio.run(main())
