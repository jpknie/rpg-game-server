class GameState:
    def __init__(self):
        self.players = []

class GameStateManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def add_player(self, player):
        self.game_state.players.append(player)

    def remove_player(self, player):
        self.game_state.players.remove(player)

    def get_players(self):
        return self.game_state.players

class Game:
    def __init__(self, max_players=1):
        game_state = GameState()
        self.game_state_manager = GameStateManager(game_state)

    async def add_connected_player(self, websocket):
        self.game_state_manager.add_player(websocket)

    async def remove_connected_player(self, websocket):
        self.game_state_manager.remove_player(websocket)

    async def get_connected_players(self):
        return self.game_state_manager.get_players()