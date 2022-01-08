import typing

__known_classes = {}


def known_class(cls: typing.ClassVar):
    __known_classes[cls.__name__] = cls
    return cls


def is_known_object(name: str):
    return name in __known_classes


def get_class_by_name(name: str) -> typing.ClassVar:
    return __known_classes[name]

