from multiprocessing.forkserver import connect_to_new_process

from game import messages
from game.Game import GamePhase, TileType
from game.character import Thief, Paladin, Cleric, Barbarian, CharacterFactory
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
        if self.game.game_state_manager.get_game_phase() == GamePhase.IN_GAME:
            raise ActionNotAllowed("Game is already started")

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

    async def on_player_move(self, data):
        player_id = data['player_id']
        direction = data['direction']
        player_is_on = await self.game.move_player(player_id, direction)
        if player_is_on == TileType.TRAP:
            # Decrease HP by some amount
            pass

        return messages.ok_response()

    async def on_character_select(self, data):
        """Character is just simple Thief, Paladin, Mage, Cleric"""
        player_id = data['player_id']
        character_name = data['character_name']
        selected_character = CharacterFactory.create(character_name)
        await self.game.select_character(data['player_id'], selected_character)
        self.game.game_state_manager.add_all_into_inventory(player_id, selected_character.get_inventory())
        # def add_into_inventory(self, player_id, item: Item)
        await self.connection_manager.broadcast_all(messages.player_selected_character(character_name, player_id))

        # if characters are selected for everyone game should start
        if await self.game.characters_checked():
            await self.game.transition_to_game()
            await self.connection_manager.broadcast_all(messages.state_transition(GamePhase.IN_GAME))

        return messages.ok_response()

    async def on_get_inventory(self, data):
        player_id = data['player_id']
        items = self.game.game_state_manager.get_inventory(player_id)
        return messages.player_inventory(items)

    async def not_allowed(self, data):
        raise ActionNotAllowed("Something is very wrong")