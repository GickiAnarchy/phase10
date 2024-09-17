import asyncio
import json
from collections import defaultdict
import uuid

from cclass import Client

from game.game import Game 

clients = defaultdict(dict)  # Dictionary to store clients by ID

def get_clients():
    return clients

async def handle_client(reader, writer):
    client_id = json.loads(await reader.readuntil(b'\n')).get('client_id')  # Get client-generated ID
    
    if client_id and client_id["type"] == "register":
        client = Client(reader, writer)  # Create Client object
        client.set_server_id(uuid.uuid4())  # Assign server-assigned ID
        clients[client_id] = client
        print(f"Client {client_id} (server ID: {client.server_id}) connected")
    elif client_id["type"] == "lobbyinfo":
        await send_message_to_client({"type":"lobbyinfo","id":client_id["client_id"]})
    else:
        print("Client registration failed. No client ID sent.")
        writer.close()
        await writer.wait_closed()
        return

async def send_message_to_client(client_id, message):
    if client_id in clients:
        await clients[client_id].send_message(message)
    else:
        print(f"Client {client_id} not found")

# ... game logic (update game state, determine next player, validate moves, etc.)
# This logic would use the `clients` dictionary to broadcast updates
# and send messages to specific clients based on their ID.

async def handle_game_over(winner_id):
    # Send game over message to all clients
    await send_message_to_client(winner_id, {"type": "game_over", "winner": winner_id})
    for client_id, client in clients.items():
        if client_id != winner_id:
            await send_message_to_client(client_id, {"type": "game_over", "winner": winner_id})

async def handle_disconnect(client):
    del clients[client.id]  # Remove client from dictionary
    # Broadcast disconnect message to other clients (optional)

async def run():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run())
