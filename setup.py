from datetime import datetime, timedelta
from model import db, PuttSesh, Putt, User, PuttSeshTemp, PuttTemp

db.connect()

# db.drop_tables([PuttSesh, Putt])
# db.create_tables([PuttSesh, Putt])

##########################################
# ↓ used to implement new puttsesh table
##########################################
db.drop_tables([PuttSeshTemp])
db.create_tables([PuttSeshTemp, PuttTemp])

my_user = User.get(User.username == 'jereamon')

for old_sesh in PuttSesh.select():
    sesh_putts = Putt.select().where(Putt.putt_sesh == old_sesh)

    temp_sesh = PuttSeshTemp(user=my_user, date=old_sesh.date, no_putters=old_sesh.no_putters)
    temp_sesh.save()

    for putt in sesh_putts:
        temp_putt = PuttTemp(putt_sesh=temp_sesh, putts_made=putt.putts_made, distance=putt.distance)
        temp_putt.save()

db.drop_tables([Putt])
db.drop_tables([PuttSesh])
db.create_tables([PuttSesh, Putt])

for temp_sesh in PuttSeshTemp.select():
    sesh_putts = PuttTemp.select().where(PuttTemp.putt_sesh == temp_sesh)

    updated_sesh = PuttSesh(user=my_user, date=temp_sesh.date, no_putters=temp_sesh.no_putters)
    updated_sesh.save()

    for putt in sesh_putts:
        updated_putt = Putt(putt_sesh=updated_sesh, putts_made=putt.putts_made, distance=putt.distance)
        updated_putt.save()
#############################################
# ↑ used to implement new puttsesh table
#############################################

# new_puttsesh = PuttSesh(date=(datetime.now() - timedelta(hours=7)), no_putters=20)
# new_puttsesh.save()
# old_puttsesh = PuttSesh(date='2019-06-28', no_putters=20)
# old_puttsesh.save()

# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=18)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=10, distance=21)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=24)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=27)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=30)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=33)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=10, distance=21)
# new_putt.save()
# new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=18)
# new_putt.save()

# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=5, distance=18)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=2, distance=21)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=20, distance=24)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=20, distance=27)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=7, distance=30)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=20, distance=33)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=10, distance=21)
# old_putt.save()
# old_putt = Putt(putt_sesh=old_puttsesh, putts_made=5, distance=18)
# old_putt.save()
