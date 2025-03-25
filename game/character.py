from game.Item import Dagger


# Characters has different stats like AP (Action Points, inventory etc)
# These are the "templates" what kind of inventory, AP and stats the final character has, these are copied over to real
# Player character
# For example if player chooses "Thief", then his inventory is populated with Dagger (by calling get_inventory())
class Character:
    pass

class Thief(Character):
    def __init__(self):
        self.inventory = [Dagger("Dagger")] # Thief has dagger in the default inventory

    def get_inventory(self):
        return self.inventory

class Paladin(Character):
    pass

class Cleric(Character):
    pass

class Barbarian(Character):
    pass

class Mage(Character):
    pass

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