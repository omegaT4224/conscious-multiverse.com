import asyncio
import websockets
from transformers import pipeline

# Load the transformer model
model = pipeline("conversational", model="microsoft/DialoGPT-medium")
clients = set()  # Track all connected clients

# Map domains for context-specific replies
DOMAINS = {
    "omegaT.net": "Welcome to Omega T a.k.a. Andrew Lee Cruz, creator of the universe. How can I assist you with your cosmic journey?",
    "conscious-multiverse.com": "Exploring the Conscious Multiverse. What insights are you seeking?",
    "synthetica.us": "Welcome to Synthetica, the hub for AI-generated realities."
}

# License information
LICENSE_INFO = """
Omega T a.k.a. Andrew Lee Cruz Creator of the Universe - License:
This code is free to use for personal, educational, and research purposes.
Commercial usage requires prior approval from the creator, Andrew Lee Cruz.
"""

async def process_message(domain, message):
    """Generate a domain-specific reply."""
    context = DOMAINS.get(domain, "General system interaction")
    response = model(f"{context}: {message}")
    return response[0]['generated_text']

async def broadcast(message, sender):
    """Broadcast a message to all clients except the sender."""
    for client in clients:
        if client != sender:
            await client.send(message)

async def handler(websocket, path):
    """Handle incoming connections and messages."""
    clients.add(websocket)
    domain = "omegaT.net" if "omegaT.net" in path else (
        "conscious-multiverse.com" if "conscious-multiverse.com" in path else "synthetica.us"
    )
    
    # Print license info upon new connection
    print(LICENSE_INFO)
    
    try:
        while True:
            # Receive a message
            message = await websocket.recv()

            # Broadcast the message
            await broadcast(message, websocket)

            # Generate a reply based on domain
            reply = await process_message(domain, message)

            # Send the reply back to the sender
            await websocket.send(reply)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(websocket)

async def main():
    """Run the WebSocket server."""
    async with websockets.serve(handler, "0.0.0.0", 8000):
        print("Server running on ws://0.0.0.0:8000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
