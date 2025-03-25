class Character:
    pass

class Thief(Character):
    pass

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