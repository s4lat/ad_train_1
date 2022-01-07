from checkers.notebook import checker as nch
from config import CONFIG
from db import db, init_db, Service, Flag
import rstr, sys

OK = 101
NO_FLAG = 102
MUMBLE = 103
NO_CONNECT = 104

CHECKERS = [nch, ]
STATUS = {101 : "OK", 102 : "CORRUPT", 103 : "MUMBLE", 104 : "DOWN"}

ROUND = int(sys.argv[1])

db.connect()
for name, team in CONFIG["TEAMS"].items():
    ip = team["ip"]

    for checker in CHECKERS:
        service = Service.get((Service.ip == ip) & (Service.port == checker.PORT))

        #CHECKING
        result = checker.check(ip)
        # print(name, ip, result["status"])
        if result["status"] != OK:
            # print(service.ip)
            service.status = result["status"]
            service.error = result["error"]
            service.save()
            continue

        #PUTTING & GETTING
        for i in range(5):
            #Putting
            flag = rstr.xeger(CONFIG["FLAG_FORMAT"])
            result = checker.put(ip, flag)
            if result["status"] != OK:
                service.status = result["status"]
                service.error = result["error"]
                service.save()
                break

            #Getting
            flag_id, key = result["flag_id"], result["key"]
            flag_id = flag_id + "." + key
            result = checker.get(ip, flag_id, flag)

            if result["status"] != OK:
                service.status = result["status"]
                service.error = result["error"]
                service.save()
                break

            Flag.create(flag=flag, flag_id=flag_id, team_token=team["token"],
                service=service, creation_round=ROUND)

        service.status = result["status"]
        if service.status == OK:
            service.up_rounds += 1
            service.error = ""
        else:
            service.error = result["error"]

        service.save()

db.close()