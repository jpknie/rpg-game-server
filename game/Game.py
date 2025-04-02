from enum import Enum

from game.Item import Item
from game.exceptions import ActionNotAllowed
from game.game_world import GameWorld

class GamePhase(Enum):
    WAITING_FOR_PLAYERS="Waiting for players"
    CHARACTER_CREATION="Character creation"
    IN_GAME="In game"
    GAME_OVER="Game over"


class GameState:
    def __init__(self, game_phase=GamePhase.WAITING_FOR_PLAYERS):
        self.players = {}
        self.world = {}
        self.game_phase = game_phase
        self.game_world = GameWorld(10, 10)  # Example dimensions

class GameStateManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def add_player(self, player_id, player_data):
        if player_id not in self.game_state.players.keys():
            self.game_state.players[player_id] = player_data
            self.game_state.players[player_id]['inventory'] = []
            self.game_state.players[player_id]['stats'] = dict()
            self.game_state.players[player_id]['position'] = [0, 0]

        else:
            raise ActionNotAllowed(f"Player already registered with id: {player_id}")

    def set_player_position(self, player_id, position):
        self.game_state.players[player_id]['position'] = position
    
    def update_player_position(self, player_id, direction):
        if direction == "SW":
            self.game_state.players[player_id]['position'][0] -= 1
            self.game_state.players[player_id]['position'][1] -= 1
        elif direction == "S":
            self.game_state.players[player_id]['position'][1] -= 1
        elif direction == "SE":
            self.game_state.players[player_id]['position'][0] += 1
            self.game_state.players[player_id]['position'][1] -= 1
        elif direction == "E": 
            self.game_state.players[player_id]['position'][0] += 1
        elif direction == "NE": 
            self.game_state.players[player_id]['position'][0] += 1
            self.game_state.players[player_id]['position'][1] += 1
        elif direction == "N":  
            self.game_state.players[player_id]['position'][1] += 1
        elif direction == "NW": 
            self.game_state.players[player_id]['position'][0] -= 1
            self.game_state.players[player_id]['position'][1] += 1
        elif direction == "W":
            self.game_state.players[player_id]['position'][0] -= 1

    def remove_player(self, player):
        self.game_state.players.remove(player)

    def set_game_phase(self, phase):
        self.game_state.game_phase = phase

    def get_game_phase(self):
        return self.game_state.game_phase
    
    def get_game_world(self):
        return self.game_state.game_world
    
    def is_walkable(self, x, y):
        return self.game_state.game_world.is_walkable(x, y)
    
    def get_player_position(self, player_id):
        return self.game_state.players[player_id]['position']
    
    # Let's setup player positions at hard coded place for now for example [2, 2], [3, 3], [4, 4]...
    def setup_player_positions(self):
        for i, player in enumerate(self.game_state.players.values()):
            player['position'] = [i + 2, i + 2]

    def set_character(self, player_id, character):
        self.game_state.players[player_id]['character'] = character

    def get_players(self):
        return self.game_state.players

    def add_all_into_inventory(self, player_id, items):
        self.game_state.players[player_id]['inventory'].extend(items)

    def drop_from_inventory(self, player_id, item):
        if item in self.game_state.players[player_id]['inventory']:
            self.game_state.players[player_id]['inventory'].remove(item)
        else:
            raise ActionNotAllowed(f"Item {item} not found in inventory of player {player_id}")
        
    def add_into_inventory(self, player_id, item):
        if item not in self.game_state.players[player_id]['inventory']:
            self.game_state.players[player_id]['inventory'].append(item)
        else:
            raise ActionNotAllowed(f"Item {item} already in inventory of player {player_id}")

    def get_inventory(self, player_id):
        return self.game_state.players[player_id]['inventory']

class Game:
    def __init__(self, max_players=1):
        self.game_state = GameState()
        self.max_players = max_players
        self.game_state_manager = GameStateManager(self.game_state)

    def add_connected_player(self, player_id, player_data):
        self.game_state_manager.add_player(player_id, player_data)

    def remove_connected_player(self, player_id):
        self.game_state_manager.remove_player(player_id)

    def select_character(self, player_id, character):
        self.game_state_manager.set_character(player_id, character)

    def get_connected_players(self):
        return self.game_state_manager.get_players()

    def has_max_players(self):
        return len(self.game_state_manager.get_players()) == self.max_players

    def transition_to_character_creation(self):
        self.game_state_manager.game_state.phase = GamePhase.CHARACTER_CREATION

    def transition_to_game(self):
        self.game_state_manager.game_state.phase = GamePhase.IN_GAME

    def all_characters_selected(self):
        return all(player.get("character") for player in self.game_state.players.values())
    
    def add_all_into_inventory(self, player_id, items):
        self.game_state_manager.add_all_into_inventory(player_id, items)

    def move_player(self, player_id, direction):
        # 1) Check if player has enough action points to move
        # 2) Check for blockades (wall, or some object, or other player)
        # 3) If there's trap or pickable item just move on it and return the object or trap (or something)
        # self.game_state.world[]
        # self.game_world.is_walkable()
        if self.get_game_world().is_walkable(self.game_state_manager.get_player_position(player_id)[0], 
                                    self.game_state_manager.get_player_position(player_id)[1]):
            self.game_state_manager.update_player_position(player_id, direction)
        else:
            raise ActionNotAllowed(f"Player {player_id} cannot move to {direction}")
    
    def get_player_position(self, player_id):
        return self.game_state_manager.get_player_position(player_id)
    
    def get_game_world(self):
        return self.game_state_manager.get_game_world()

