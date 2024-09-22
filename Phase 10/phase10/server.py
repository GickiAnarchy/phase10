import asyncio
import json


class Phase10Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store connected clients
        self.game_state = GameState()  # Create a game state object

    async def handle_client(self, reader, writer):
        client_id = await reader.readuntil(b'\n').decode()  # Read client ID
        self.clients[client_id] = (reader, writer)  # Add client to dictionary
        print(f"Client {client_id} connected")
        await self.send_message(client_id, {"type": "connected"})  # Send connection confirmation

        while True:
            try:
                data = await reader.readuntil(b'\n').decode()  # Read incoming message
                if not data:
                    break  # Handle disconnection
                message = json.loads(data)
                await self.handle_message(client_id, message)  # Process message
            except json.JSONDecodeError:
                print(f"Error decoding message from {client_id}")
                break  # Handle invalid JSON

        del self.clients[client_id]
        await self.game_state.handle_disconnect(client_id)  # Update game state on disconnect
        print(f"Client {client_id} disconnected")

    async def handle_message(self, client_id, message):
        message_type = message.get("type")  # Extract message type

        if message_type == "register":
            # Handle player registration logic (assign name, etc.)
            await self.game_state.register_player(client_id, message.get("name"))
        elif message_type == "play_card":
            # Validate card play and update game state
            await self.game_state.play_card(client_id, message.get("card"))
        elif message_type == "draw_card":
            # Handle card draw logic and update game state
            await self.game_state.draw_card(client_id)
        elif message_type == "check_phase":
            # Check player's phase completion and send response
            is_complete = self.game_state.check_phase(client_id)
            await self.send_message(client_id, {"type": "phase_check", "complete": is_complete})
        else:
            print(f"Unknown message type: {message_type} from {client_id}")

    async def send_message(self, client_id, message):
        data = json.dumps(message).encode() + b'\n'
        reader, writer = self.clients.get(client_id)  # Get writer object for the client
        if writer:
            await writer.write(data)
        else:
            print(f"Client {client_id} not found for sending message")

    async def broadcast(self, message):
        # Send message to all connected clients (except sender for some messages)
        for client_id, (reader, writer) in self.clients.items():
            if message.get("sender") != client_id:  # Avoid sending to the sender (optional)
                await writer.write(json.dumps(message).encode() + b'\n')

    async def serve(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server listening on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

class GameState:
    # Implement game state logic here (deck, discard pile, player hands, phases, etc.)
    # Handle player registration, card play, drawing, phase checking, disconnection handling, etc.
    # Update game state based on received messages and game rules.
    # Send appropriate responses to clients based on game state changes and validations.
    pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = Phase10Server("localhost", 8888)  # Replace with desired host and port
    loop.run_until_complete(server.serve())
    loop.close()