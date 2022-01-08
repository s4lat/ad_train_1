from checkers.notebook import checker as nch
from checkers.chessbase import checker as bch
from checkers.pastetrash import checker as pch
from config import CONFIG
from db import db, init_db, Service, Flag
import rstr, sys

OK = 101
NO_FLAG = 102
MUMBLE = 103
NO_CONNECT = 104

CHECKERS = [nch, bch, pch]

ROUND = int(sys.argv[1])
ip = sys.argv[2]
team_token = sys.argv[3]



db.connect()

for checker in CHECKERS:
    service = Service.get((Service.ip == ip) & (Service.port == checker.PORT))

    #CHECKING
    result = checker.check(ip)
    if result["status"] != OK:
        service.status = result["status"]
        service.error = result["error"]
        service.save()
        continue

    #PUTTING & GETTING
    for i in range(CONFIG["FLAGS_PER_ROUND"]):
        #Putting
        flag = rstr.xeger(CONFIG["FLAG_FORMAT"])
        result = checker.put(ip, flag)
        if result["status"] != OK:
            service.status = result["status"]
            service.error = result["error"]
            service.save()
            break

        #Getting
        flag_id = result["flag_id"]
        result = checker.get(ip, flag_id, flag)

        if result["status"] != OK:
            service.status = result["status"]
            service.error = result["error"]
            service.save()
            break

        Flag.create(flag=flag, flag_id=flag_id, team_token=team_token,
            service=service, creation_round=ROUND)

    service.status = result["status"]
    if service.status == OK:
        service.up_rounds += 1
        service.error = ""
    else:
        service.error = result["error"]

    service.save()

db.close()