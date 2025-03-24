from game import messages
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
    def __init__(self, _game, broadcast_fn):
        self._game = _game
        self.broadcast_fn = broadcast_fn

    async def change_state(self, data):
        await self._game.add_connected_player(data)
        await self.broadcast_fn(messages.player_joined_message(data))
        return messages.ok_response()

    async def not_allowed(self, data):
        raise ActionNotAllowed("Something is very wrong")