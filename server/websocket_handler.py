# websocket_handler.py
import websockets
import json

from websockets.legacy.server import WebSocketServerProtocol

from game import messages
from game.Game import Game
from game.action_handler import ActionHandler
from game.exceptions import ActionNotAllowed
from server.event_dispatcher import EventDispatcher

connected_players = set()
game = Game()
event_dispatcher = EventDispatcher(game)

async def broadcast_all(message):
    for conn in connected_players:
        await conn.send(json.dumps(message))


action_handler = ActionHandler(game, broadcast_all)

event_dispatcher.register_event('change_state', action_handler.change_state)
event_dispatcher.register_event('not_allowed', action_handler.not_allowed)

async def websocket_handler(websocket: WebSocketServerProtocol):
    """WebSocket connection handler."""
    print(f"Player connected! Total: {len(game.game_state_manager.get_players())}")
    connected_players.add(websocket)

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            payload = data.get('payload')
            try:
                response = await event_dispatcher.dispatch(action, payload)
                await websocket.send(json.dumps(response))
            except ActionNotAllowed as e:
                await websocket.send(json.dumps(messages.action_not_allowed()))
    except websockets.exceptions.ConnectionClosed:
        print("Player disconnected")
    finally:
        connected_players.remove(websocket)
        await game.remove_connected_player(websocket)


async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8080)
    print(f"Server listening on ws://0.0.0.0:8080")
    await server.wait_closed()

