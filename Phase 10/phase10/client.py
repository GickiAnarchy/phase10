import asyncio
import json

from clientclass import Client


async def main():
    # Server connection details
    host = "localhost"  # Replace with server's IP or hostname
    port = 8888  # Replace with server's port

    # Create a Client instance
    client = Client(host, port)

    # Connect to the server asynchronously
    await client.connect()

    # Get player name from user input (optional)
    player_name = input("Enter your player name: ")

    # Send a registration message to the server
    registration_message = {"type": "register", "name": player_name}
    await client.send_message(registration_message)

    # Continuously receive and handle messages from the server
    while True:
        try:
            message = await client.receive_message()
            message_type = message.get("type")

            if message_type == "connected":
                print("Connected to server!")
            elif message_type == "phase_check":
                is_complete = message.get("complete")
                if is_complete:
                    print("Congratulations! You completed your current phase.")
                else:
                    print("Your current phase is not complete yet.")
                # Handle displaying hand, playing cards, drawing cards, etc. (based on game logic)
            else:
                print(f"Received message from server: {message}")
        except json.JSONDecodeError:
            print("Error decoding message from server")
            break  # Handle invalid JSON
        except ConnectionError:
            print("Connection to server lost")
            break  # Handle connection errors

    # Close the connection when done
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())