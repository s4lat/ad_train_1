from config import CONFIG
from peewee import *

db = SqliteDatabase('shared/data.db')

def init_db(db):
    db.connect()
    db.create_tables([Service, Flag])

    for name, team in CONFIG["TEAMS"].items():
        service = Service.get_or_create(name="notebook", ip=team["ip"], port=8616, team=name)

    db.close()

class Service(Model):
    name = CharField()
    ip = CharField()
    port = IntegerField()
    team = CharField()
    status = IntegerField(default=104)
    error = CharField(default="")
    up_rounds = IntegerField(default=0)
    fp =  FloatField(default=len(CONFIG["TEAMS"]))

    class Meta:
        database = db

class Flag(Model):
    flag = CharField(unique=True)
    flag_id = CharField()
    team_token = CharField()
    service = ForeignKeyField(Service, backref='flags')
    creation_round = IntegerField()
    submited = BooleanField(default=False)

    class Meta:
        database = db