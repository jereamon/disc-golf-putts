import os
from peewee import Model, CharField, IntegerField, \
    ForeignKeyField, DateTimeField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///putting_db.db'))


class PuttSesh(Model):
    """
    Fields include the date and time, as well as the number of putters used.
    """
    date = DateTimeField()
    no_putters = IntegerField()

    class Meta:
        database = db


class Putt(Model):
    putt_sesh = ForeignKeyField(PuttSesh)
    putts_made = IntegerField()
    distance = IntegerField()

    class Meta:
        database = db
