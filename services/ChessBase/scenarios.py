from object_storage import storage, save_db_once
from chess_unit import ChessUnit
from Entitites.basement import Basement
from Entitites.armory import Armory
from uuid import uuid4
from Helpers.known_objects import is_known_object, get_class_by_name
from itertools import islice
from typing import Dict, List


def get_uuid() -> str:
    return str(uuid4())


def add_new_unit(object_props: Dict[str, List[str]]):
    for object_name, object_values in object_props.items():
        if is_known_object(object_name):
            spawned_class = get_class_by_name(object_name)
            unit_name = object_values[0]
            if unit_name in storage:
                raise LookupError(f"{unit_name} already exists")
            if spawned_class is ChessUnit:
                basement_id = get_uuid()
                unit = spawned_class(
                    unit_name, Basement(basement_id, {"store": object_values[1:]}))
                storage.add_object(unit_name, unit)
                return basement_id
            if spawned_class is Armory:
                unit = spawned_class(
                    unit_name,
                    {"axes": object_values[1]},
                    {"helmets": object_values[2]}
                )
                storage.add_object(unit_name, unit)
                return unit_name
    raise ValueError("bad request")


def add_inner_unit_to_chess_unit(name1, name2):
    if name1 in storage and name2 in storage:
        chess_unit: ChessUnit = storage[name1]
        secondary_unit = storage[name2]
        chess_unit.add(secondary_unit)
        return chess_unit.name
    raise ValueError("unknown objects provided")


def print_object_info(name):
    if name in storage:
        return str(storage[name])
    raise ValueError("unknown_object_provided")


def get_basement_info(name, access_key):
    if name in storage:
        if storage[name][0].basement_id == access_key:
            return storage[name][0].get_first_basement()
        return str(storage[name])
    raise ValueError("unknown basement")


def get_window_of_objects(index_from, index_to):
    if abs(index_from - index_to) < 100 and index_from >= 0 and index_to >= 0:
        return list(islice(storage.keys(), max(index_from, 0), index_to))
    raise ValueError("bad amount of objects")


def get_last_index():
    return len(storage)


def save_final_version_of_db():
    save_db_once()