from flask import Flask, request, json
from flask_apscheduler import APScheduler
from db import db, init_db, Service, Flag, CheckSystem
from config import CONFIG
import os, subprocess, re
import warnings

warnings.filterwarnings("ignore")


app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

init_db(db)

@scheduler.task('interval', id='checker', seconds=CONFIG["ROUND_DURATION"])
def check_all():
    check_system = CheckSystem.select()[0]
    check_system.is_checking = True
    check_system.save()

    result = subprocess.run(["python3", "check_all.py", str(check_system.round)])
    check_system.round += 1
    check_system.save()

    check_system.is_checking = False
    check_system.save()


@app.route("/")
def index():
    check_system = CheckSystem.select()[0]
    IS_CHECKING, CURRENT_ROUND = check_system.is_checking, check_system.round

    if IS_CHECKING or CURRENT_ROUND == 0:
        return "Updating scoreboard, please wait..."

    db.connect(db)
    services = Service.select()
    resp = "ROUND: %s<br>" % CURRENT_ROUND

    resp = resp + "SERVICES:<br>"
    for service in services:
        SLA = (service.up_rounds/CURRENT_ROUND) * 100
        resp = resp + "&nbsp&nbsp%s | %s | %s | %s | %0.2f | %0.3f | %s<br>" % (
            service.team, service.name, service.ip, service.status, 
            SLA, service.fp, service.error)
    
    db.close()

    services = Service.select()
    scoreboard = []
    for team in CONFIG["TEAMS"]:
        score = 0
        for s in services.where(Service.team == team):
            score += s.fp * (s.up_rounds/CURRENT_ROUND)
        scoreboard.append([team, score])

    scoreboard = sorted(scoreboard, key=lambda team: team[1])[::-1]

    resp = resp + "SCOREBOARD:<br>"

    for team in scoreboard:
        resp = resp + "&nbsp&nbsp%s: %0.4f<br>" % (team[0], team[1]) 

    return resp

@app.route("/submit", methods=["PUT"])
def submit():
    check_system = CheckSystem.select()[0]
    IS_CHECKING, CURRENT_ROUND = check_system.is_checking, check_system.round

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
        elif CURRENT_ROUND - result.creation_round > FLAG_LIFETIME / CONFIG["ROUND_DURATION"]:
            resp.append("Flag is expired!")
        elif result.submited:
            resp.append("Already submitted!")
        else:
            services = Service.select()
            scoreboard = []
            for team in CONFIG["TEAMS"]:
                score = 0
                for s in services.where(Service.team == team):
                    score += s.fp * (s.up_rounds/CURRENT_ROUND)
                scoreboard.append([team, score])

            scoreboard = sorted(scoreboard, key=lambda team: team[1])[::-1]

            attack_N = None
            for i, (name, score) in enumerate(scoreboard):
                if CONFIG["TOKEN2TEAM"][token] == name:
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
    app.run("0.0.0.0", 80)