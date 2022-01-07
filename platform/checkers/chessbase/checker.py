#!/usr/bin/env python3.7

from .api import Api
from uuid import uuid4
from requests.exceptions import RequestException

PORT = 8284

OK = 101
CORRUPT = 102
MUMBLE = 103
DOWN = 104
CHECKER_ERROR = 110

def randomize() -> str:
    return str(uuid4())


def check(ip):
    hostname = "%s:8284" % ip
    api = Api()
    try:
        rand_uuid = api.add_new_chess_unit(hostname, randomize(), randomize())
        if len(rand_uuid) > 0:
            return {"status": OK}
    except RequestException as e:
        return {"status": DOWN, "error": "Can't connect to host."}
    except Exception as e:
        return {"status": MUMBLE, "error": "Bad proto"}



def put(ip, flag):
    hostname = "%s:8284" % ip
    api = Api()
    try:
        unit_name = randomize()
        id_of_basement = api.add_new_chess_unit(hostname, unit_name, flag)
        armory_id = randomize()
        new_armory_id = api.add_armory_unit(hostname, armory_id)
        result = api.add_unit_to_chess(hostname, unit_name, new_armory_id)
        last_50_objects = api.get_latest_objects(hostname, 50)
        if "Armory" not in str(api.object_info(hostname, unit_name)):
            return {"status" : MUMBLE, "error" : "Bad object"}
        if unit_name not in last_50_objects or result not in last_50_objects or armory_id not in last_50_objects:
            return {"status" : MUMBLE, "error" : "bad objects listing"}
        if result != unit_name:
            return {"status" : MUMBLE, "error" : "bad object id after adding"}
        if armory_id != new_armory_id:
            return {"status" : MUMBLE, "error" : "bad object id after adding"}
        return {"status" : OK, "flag_id" : "%s.%s" % (unit_name, id_of_basement)}
    except RequestException as e:
        return {"status" : DOWN, "error" : "timeout"}
    except Exception as e:
        return {"status" : MUMBLE, "error" : "bad proto"}



def get(ip, flag_id, flag):
    hostname = "%s:8284" % ip
    api = Api()
    try:
        addr, secret = flag_id.strip().split(".")
        try:
            resulting_info = api.basement_info(hostname, addr, secret)
            if flag in resulting_info:
                return {"status": OK}
            else:
                return {"status": CORRUPT, "error" : "bad flag"}
        except Exception as e:
            return {"status" : CORRUPT, "error" : "can't reach flag"}
    except RequestException as e:
        print(e)
        return {"status" : DOWN, "error" : "seems to be down"}
    except Exception as e:
        return {"status" : MUMBLE, "error" : "bad proto"}
