# websocket_handler.py
import websockets
import json

from websockets.legacy.server import WebSocketServerProtocol

from game import messages
from game.Game import Game
from game.action_handler import ActionHandler
from game.exceptions import ActionNotAllowed
from server.connection_manager import ConnectionManager
from server.event_dispatcher import EventDispatcher

connected_players = set()
game = Game()
event_dispatcher = EventDispatcher(game)

connection_manager = ConnectionManager()
action_handler = ActionHandler(game, connection_manager)

event_dispatcher.register_event('player_join', action_handler.change_state)
event_dispatcher.register_event('not_allowed', action_handler.not_allowed)


async def websocket_handler(websocket: WebSocketServerProtocol):

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            payload = data.get('payload')

            try:
                # This is special case and handled here
                if action == "player_join":
                    await connection_manager.add_connection(websocket, payload['player_id'])
                    print(f"Player connected! Total: {len(connection_manager.get_connections())}")

                response = await event_dispatcher.dispatch(action, payload)
                await connection_manager.send_to(websocket, response)

            except ActionNotAllowed as e:
                print("ActionNotAllowed: ", e)
                await websocket.send(json.dumps(messages.action_not_allowed()))
                #await connection_manager.send_to(websocket, messages.action_not_allowed())

    except websockets.exceptions.ConnectionClosed:
        await connection_manager.remove_connection(websocket)

    finally:
        await connection_manager.remove_connection(websocket)
        #await game.remove_connected_player(websocket)


async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8080)
    print(f"Server listening on ws://0.0.0.0:8080")
    await server.wait_closed()

