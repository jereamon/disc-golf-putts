import os
from peewee import Model, CharField, IntegerField, \
    ForeignKeyField, DateTimeField
from playhouse.db_url import connect
from werkzeug.security import generate_password_hash, check_password_hash

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///putting_db.db'))
# backup_db = connect(os.environ.get('DATABASE_URL', 'sqlite:///putting_db_backup.db'))


class User(Model):
    username = CharField(primary_key=True)
    password_hash = CharField()
    email = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    class Meta:
        database = db


class PuttSesh(Model):
    """
    Fields include the date and time, as well as the number of putters used.
    """
    # user = ForeignKeyField(User, field=User.username, on_delete='CASCADE')
    date = DateTimeField()
    no_putters = IntegerField()

    class Meta:
        database = db


class PuttSeshTemp(Model):
    """
    Will include the foreignKeyField I want to add and will temporarily
    store the existing data.
    """
    user = ForeignKeyField(User, on_delete='CASCADE')
    date = DateTimeField()
    no_putters = IntegerField()

    class Meta:
        database = db


class Putt(Model):
    putt_sesh = ForeignKeyField(PuttSesh, on_delete='CASCADE')
    putts_made = IntegerField()
    distance = IntegerField()

    class Meta:
        database = db
