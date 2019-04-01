import os

from peewee import *

PATH = os.path.dirname(os.path.abspath(__file__))

db = SqliteDatabase(None)


class Igralec(Model):
    ime = CharField()
    rokovanj = IntegerField(default=0)
    ekipa = TextField()

    class Meta:
        database = db
