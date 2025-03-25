from game.Game import GamePhase


def player_joined_message(data):
    return {"action": "player_joined", "payload": data}

def player_selected_character(character, player_id):
    return {"action": "player_selected_character", "payload": {"player_id": player_id, "character": character}}

def state_transition(game_phase: GamePhase):
    return {"action": "game_phase_changed", "payload": game_phase.name}

def ok_response():
    return {"status": "ok"}

def action_not_allowed():
    return {"status": "action not allowed"}

