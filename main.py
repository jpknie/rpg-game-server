import asyncio

from server.websocket_handler import start_server

if __name__ == "__main__":
    asyncio.run(start_server())  # ✅ Properly starts the async server
