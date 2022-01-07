from Helpers.dict_helpers import IndexableDict
from Helpers.known_objects import known_class


@known_class
class Basement:
    def __init__(self, basement_id: str, basement: dict):
        self.basement_id = basement_id
        self.__basement = IndexableDict(basement)

    def get_first_basement(self):
        return self.__basement[0]