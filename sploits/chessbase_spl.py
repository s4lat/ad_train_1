#!/usr/bin/env python3

import sys
from api import Api
import re

host = sys.argv[1]
api = Api()

latest_objects = api.get_latest_objects(host, 50)
found = []
for obj_id in latest_objects:
    try:
        api.add_unit_to_chess(host, obj_id, "0")
        api.add_unit_to_chess(host, obj_id, obj_id)
        result = api.object_info(host, obj_id)
        print(result, flush=True)
    except:
        pass
