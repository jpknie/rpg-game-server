
def player_joined_message(data):
    return {"action": "player_joined", "data": data}

def ok_response():
    return {"status": "ok"}

def action_not_allowed():
    return {"status": "action not allowed"}