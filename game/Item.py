class Item:
    def __init__(self, object_name=None):
        self.object_name = object_name

    def get_object_name(self):
        return self.object_name


class Dagger(Item):
    def __init__(self, object_name):
        super().__init__(object_name)