from game.Item import Dagger

# These are the templates for the characters or "the beginning attributes so to say"
# Characters has different stats like AP (Action Points, inventory etc)
# These are the "templates" what kind of inventory, AP and stats the final character has, these are copied over to real
# Player character
# For example if player chooses "Thief", then his inventory is populated with Dagger (by calling get_inventory())
class Character:
    def __init__(self):
        self.ap = None

class Thief(Character):
    def __init__(self):
        super().__init__()
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory
        self.ap = 4 # Thief has 4 action points in the beginning
        self.hp = 10

    def get_inventory(self):
        return self.inventory

    def get_ap(self):
        return self.ap

    def get_hp(self):
        return self.hp

class Paladin(Character):
    def __init__(self):
        super().__init__()
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory
        self.ap = 4 # Thief has 4 action points in the beginning

    def get_inventory(self):
        return self.inventory

    def get_ap(self):
        return self.ap

    def get_hp(self):
        return self.hp


class Cleric(Character):
    def __init__(self):
        super().__init__()
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory
        self.ap = 4 # Thief has 4 action points in the beginning
        self.hp = 10

    def get_inventory(self):
        return self.inventory

    def get_ap(self):
        return self.ap

    def get_hp(self):
        return self.hp


class Barbarian(Character):
    def __init__(self):
        super().__init__()
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory
        self.ap = 4 # Thief has 4 action points in the beginning
        self.hp = 10

    def get_inventory(self):
        return self.inventory

    def get_ap(self):
        return self.ap

    def get_hp(self):
        return self.hp

class Mage(Character):
    def __init__(self):
        super().__init__()
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory
        self.ap = 4 # Thief has 4 action points in the beginning
        self.hp = 8

    def get_inventory(self):
        return self.inventory

    def get_ap(self):
        return self.ap

    def get_hp(self):
        return self.hp

class CharacterFactory:
    _character_classes = {
        "Thief": Thief,
        "Paladin": Paladin,
        "Cleric": Cleric,
        "Barbarian": Barbarian,
        "Mage": Mage
    }

    @classmethod
    def create(cls, character_name):
        if character_name not in cls._character_classes:
            raise ValueError(f"Unknown character class: {character_name}")
        return cls._character_classes[character_name]()