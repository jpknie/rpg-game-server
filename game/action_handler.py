from multiprocessing.forkserver import connect_to_new_process

from game import messages
from game.Game import GamePhase
from game.exceptions import ActionNotAllowed


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class ActionHandler:
    def __init__(self, game, connection_manager):
        self.game = game
        self.connection_manager = connection_manager

    async def register_connection(self, connection):
        await self.connection_manager.add_connection(connection)

    async def on_player_joined(self, data):
        player_id = data['player_id']
        player_name = data['player_name']
        # Populate tentative player data here, for example player name etc.
        player_data = {'player_name': player_name}
        await self.game.add_connected_player(player_id, player_data)
        await self.connection_manager.broadcast_all_but(player_id, messages.player_joined_message(data))
        if await self.game.has_max_players():
            await self.game.transition_to_character_creation()
            await self.connection_manager.broadcast_all(messages.state_transition(GamePhase.CHARACTER_CREATION))
        # else should return error message

        return messages.ok_response()

    async def not_allowed(self, data):
        raise ActionNotAllowed("Something is very wrong")