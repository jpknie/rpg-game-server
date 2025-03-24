class EventDispatcher:
    def __init__(self, game):
        self.game = game
        self.events = {}

    def register_event(self, event_type, handler):
        if event_type not in self.events:
            self.events[event_type] = handler

    async def dispatch(self, event_type, data):
        return await self.events[event_type](data)
