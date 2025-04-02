from game.Game import GamePhase


def player_joined_message(data):
    return {"action": "player_joined", "payload": data}

def player_selected_character(character, player_id):
    return {"action": "player_selected_character", "payload": {"player_id": player_id, "character": character}}

def state_transition(game_phase: GamePhase):
    return {"action": "game_phase_changed", "payload": game_phase.name}

def game_world(game_world):
    return {"action": "game_world", "payload": game_world.to_dict()}

def player_inventory(items):
    object_names = []
    for item in items:
        object_names.append(item.get_object_name())
    return {"action": "player_inventory", "payload": {"items": object_names}}

def ok_response():
    return {"status": "ok"}

def action_not_allowed():
    return {"status": "action not allowed"}

