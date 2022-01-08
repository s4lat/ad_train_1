from Helpers.known_objects import known_class


@known_class
class ChessUnit:
    def __init__(self, name: str, basement):
        self.name: str = name
        self.__constructions = [basement]

    def add(self, construction):
        self.__constructions.append(construction)

    def __getitem__(self, item):
        return self.__constructions[item]

    def __str__(self):
        armory_inner_fields = []
        for construction in self.__constructions[1:]:
            construction_info = [type(construction).__name__]
            armory_inner_fields.append(construction_info)
            try:
                for inner_field in construction:
                    if hasattr(inner_field, "__dict__"):
                        construction_info.append(inner_field.__dict__)
                    else:
                        construction_info.append(inner_field)
            except:
                pass
        return str(armory_inner_fields)