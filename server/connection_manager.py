import json
from argparse import Action

from game.exceptions import ActionNotAllowed


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def broadcast_all(self, message):
        for conn in self.connections.values():
            await conn.send(json.dumps(message))

    async def broadcast_all_but(self, player_id, message):
        for k, conn in ((k, conn) for k, conn in self.connections.items() if k != player_id):
            await conn.send(json.dumps(message))

    async def send_to(self, connection, message):
        if connection in self.connections.values():
            await connection.send(json.dumps(message))

    async def add_connection(self, websocket, player_id):
        if player_id not in self.connections.keys():
            self.connections[player_id] = websocket
        else:
            raise ActionNotAllowed(f"Player already connected with id {player_id}")

    async def get_connection(self, player_id):
        if player_id in self.connections.keys():
            return self.connections[player_id]
        else:
            return None

    async def remove_connection(self, websocket):
        player_id = next((k for k, v in self.connections.items() if v == websocket), None)
        if player_id:
            del self.connections[player_id]
            print(f"Player {player_id} disconnected.")

    def get_connections(self):
        return self.connections