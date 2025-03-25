from game.exceptions import ActionNotAllowed


class GameState:
    def __init__(self):
        self.players = {}

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

    def get_players(self):
        return self.game_state.players

class Game:
    def __init__(self, max_players=1):
        game_state = GameState()
        self.game_state_manager = GameStateManager(game_state)

    async def add_connected_player(self, player_id, player_data):
        self.game_state_manager.add_player(player_id, player_data)

    async def remove_connected_player(self, websocket):
        self.game_state_manager.remove_player(websocket)

    async def get_connected_players(self):
        return self.game_state_manager.get_players()