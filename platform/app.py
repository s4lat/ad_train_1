from flask import Flask, request, json
from flask_apscheduler import APScheduler
from db import db, init_db, Service, Flag
from config import CONFIG
import os, subprocess, re

IS_CHECKING = False
CURRENT_ROUND = None
SCOREBOARD = []

app = Flask(__name__)
init_db(db)

if (os.path.isfile("./shared/current_round")):
    with open("./shared/current_round", "r") as f:
        CURRENT_ROUND = int(f.read())
else:
    with open("./shared/current_round", "w") as f:
        CURRENT_ROUND = 0
        f.write("0")

def check_all():
    global CURRENT_ROUND, IS_CHECKING

    IS_CHECKING = True
    result = subprocess.run(["python3", "check_all.py", str(CURRENT_ROUND)])
    CURRENT_ROUND += 1

    with open("./shared/current_round", "w") as f:
        f.write(str(CURRENT_ROUND))

    IS_CHECKING = False


@app.route("/")
def index():
    if IS_CHECKING or CURRENT_ROUND == 0:
        return "Updating scoreboard, please wait..."

    db.connect(db)
    services = Service.select()
    resp = "ROUND: %s<br>" % CURRENT_ROUND
    for service in services:
        SLA = (service.up_rounds/CURRENT_ROUND) * 100
        resp = resp + "\t%s | %s | %s | %0.2f | %0.3f | %s<br>" % (service.name, service.ip, 
            service.status, SLA, service.fp, service.error)
    
    db.close()
    return resp

@app.route("/submit", methods=["PUT"])
def submit():
    global SCOREBOARD
    token = request.headers.get('X-Team-Token')
    teams_tokens = [team["token"] for team in CONFIG["TEAMS"].values()]
    if token not in teams_tokens:
        return "Bad token"

    if not request.json:
        return "You forgot flags json"

    resp = []
    for i, flag in enumerate(request.json):
        if i > 50:
            break

        matched = re.match(CONFIG["FLAG_FORMAT"], flag)
        if not matched:
            resp.append("Wrong flag")
            continue

        result = Flag.select().where(Flag.flag == flag)
        
        if not result.exists():
            resp.append("Flag not in database!")
            continue

        result = result.get()
        if result.team_token == token:
            resp.append("It's your own flag!")
            continue
        elif CURRENT_ROUND - result.creation_round > 5:
            resp.append("Flag is expired!")
        elif result.submited:
            resp.append("Already submitted!")
        else:
            services = Service.select()
            scoreboard = []
            for team in CONFIG["TEAMS"]:
                score = 0
                for s in services.where(Service.team == team):
                    score += s.fp
                scoreboard.append([team, score])

            scoreboard = sorted(scoreboard, key=lambda team: team[1])
            SCOREBOARD = scoreboard

            attack_N = None
            for i, (name, score) in enumerate(scoreboard):
                if CONFIG["TOKEN2TEAM"][token] == team:
                    attack_N = i
                    break

            defense_N = None
            for i, (name, score) in enumerate(scoreboard):
                if CONFIG["TOKEN2TEAM"][result.team_token] == name:
                    defense_N = i
                    break

            N = len(CONFIG["TEAMS"])
            delta_fp = pow(N, min(1, (N - defense_N)/(N - attack_N)))
            result.service.fp = max(0, result.service.fp - delta_fp)
            result.service.save()

            attack_s = Service.get((Service.team == CONFIG["TOKEN2TEAM"][token]) & 
                (Service.name == result.service.name))
            attack_s.fp += delta_fp;
            attack_s.save()

            result.submited = True
            result.save()
            resp.append("The flag is accepted! You received %s points." % delta_fp)

    return app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.add_job(func=check_all, trigger='interval', id='checker', seconds=30)
    scheduler.start()
    app.run("0.0.0.0", 80)