from enum import Enum

from game.exceptions import ActionNotAllowed

class GamePhase(Enum):
    WAITING_FOR_PLAYERS = "Waiting for players"
    CHARACTER_CREATION = "Character creation"
    IN_GAME = "In game"
    GAME_OVER = "Game over"


class GameState:
    def __init__(self, game_phase=GamePhase.WAITING_FOR_PLAYERS):
        self.players = {}
        self.game_phase = game_phase

class GameStateManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def add_player(self, player_id, player_data):
        if player_id not in self.game_state.players.keys():
            self.game_state.players[player_id] = player_data
        else:
            raise ActionNotAllowed(f"Player already registered with id: {player_id}")

    def remove_player(self, player):
        self.game_state.players.remove(player)

    def set_game_phase(self, phase):
        self.game_state.game_phase = phase

    def set_character(self, player_id, character):
        self.game_state.players[player_id]['character'] = character

    def get_players(self):
        return self.game_state.players

class Game:
    def __init__(self, max_players=1):
        game_state = GameState()
        self.max_players = max_players
        self.game_state_manager = GameStateManager(game_state)

    async def add_connected_player(self, player_id, player_data):
        self.game_state_manager.add_player(player_id, player_data)

    async def remove_connected_player(self, websocket):
        self.game_state_manager.remove_player(websocket)

    async def select_character(self, player_id, character):
        self.game_state_manager.set_character(player_id, character)

    async def get_connected_players(self):
        return self.game_state_manager.get_players()

    async def has_max_players(self):
        return len(self.game_state_manager.get_players()) == self.max_players

    async def transition_to_character_creation(self):
        self.game_state_manager.game_state.phase = GamePhase.CHARACTER_CREATION

