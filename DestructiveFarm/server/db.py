from peewee import *

db = SqliteDatabase('db.sqlite')

class User(Model):
    username = CharField()
    pwd = CharField()

    class Meta:
        database = db

class Paste(Model):
    file_name = CharField()
    owner = ForeignKeyField(User, backref='pastes')

    class Meta:
        database = db

db.connect()
db.create_tables([User, Paste])
db.close()