from Helpers.dict_helpers import IndexableDict
from Helpers.known_objects import known_class
from itertools import chain


@known_class
class Armory:
    def __init__(self, name, weapons, armor):
        self.name = name
        self.known_weapons = IndexableDict(weapons)
        self.known_armor = IndexableDict(armor)

    def __iter__(self):
        return chain(self.known_weapons, self.known_armor)