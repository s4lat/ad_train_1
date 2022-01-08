import re
from typing import Dict, List

pattern = re.compile(r'[A-Za-z0-9_=\-]{1,45}')


def validate_units(unit_description: Dict[str, List[str]]):
    if len(unit_description) > 2:
        raise ValueError()
    for key, value in unit_description.items():
        if re.fullmatch(pattern, key) is None:
            raise ValueError()
        for arg in value:
            if len(value) > 5:
                raise ValueError()
            if re.fullmatch(pattern, arg) is None:
                raise ValueError()
    return True


def validate_requests(request_description):
    if len(request_description) > 5:
        raise ValueError()
    for item in request_description:
        if re.fullmatch(pattern, item) is None:
            raise ValueError()
    return True
