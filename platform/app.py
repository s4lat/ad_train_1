from flask import Flask, request, json, render_template
from flask_apscheduler import APScheduler
from db import db, init_db, Service, Flag, CheckSystem
from config import CONFIG
from subprocess import Popen
import os, re, warnings

warnings.filterwarnings("ignore")


app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

init_db(db)

@scheduler.task('interval', id='checker', seconds=CONFIG["ROUND_DURATION"])
def check_all():
    db.connect()
    check_system = CheckSystem.select()[0]
    check_system.is_checking = True
    check_system.save()

    procs = []
    for team in CONFIG["TEAMS"]:
        team = CONFIG["TEAMS"][team]
        procs.append(Popen(["python3", "check_all.py", team["ip"], team["token"]]))

    for p in procs:
        p.wait()

    check_system.round += 1
    check_system.is_checking = False
    check_system.save()
    db.close()


@app.route("/")
def index():
    db.connect(db)

    check_system = CheckSystem.select()[0]
    IS_CHECKING, CURRENT_ROUND = check_system.is_checking, check_system.round

    if IS_CHECKING or CURRENT_ROUND == 0:
        return ('<head><meta charset="utf-8"><meta http-equiv="refresh" content="5">' +
            '<title> AD_SCOREBOARD</title></head>' + 'Updating scoreboard, please wait...')

    services = Service.select()
    scoreboard = []
    for team in CONFIG["TEAMS"]:
        team_services = []
        score = 0
        for s in services.where(Service.team == team):
            score += s.fp * (s.up_rounds/CURRENT_ROUND)
            team_services.append(s)

        scoreboard.append({"name" : team, "score" : score, "services" : tuple(team_services)})

    scoreboard = sorted(scoreboard, key=lambda team: team["score"])[::-1]

    db.close()
    return render_template("scoreboard.html", scoreboard=scoreboard, CURRENT_ROUND=CURRENT_ROUND)

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

        msg = ""
        matched = re.match(CONFIG["FLAG_FORMAT"], flag)
        if not matched:
            msg = "Wrong flag"
            continue

        result = Flag.select().where(Flag.flag == flag)
        if not result.exists():
            msg = "Flag not in database!"
            continue

        result = result.get()
        if result.team_token == token:
            msg = "It's your own flag!"
        elif CURRENT_ROUND - result.creation_round > CONFIG["FLAG_LIFETIME"] / CONFIG["ROUND_DURATION"]:
            msg = "Flag is expired!"
        elif result.submited:
            msg = "Already submitted!"
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

            defense_s = result.service
            defense_s.fp = max(0, defense_s.fp - delta_fp)
            defense_s.lost += 1
            defense_s.save()

            attack_s = Service.get((Service.team == CONFIG["TOKEN2TEAM"][token]) & 
                (Service.name == result.service.name))
            attack_s.fp += delta_fp;
            attack_s.submited += 1;
            attack_s.save()

            result.submited = True
            result.save()
            msg = "The flag is accepted! You received %s points." % delta_fp

        resp.append({"flag" : flag, "msg" : msg})

    return app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run("0.0.0.0", 80)
