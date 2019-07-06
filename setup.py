from datetime import datetime, timedelta
from model import db, PuttSesh, Putt, User
from dateutil.relativedelta import relativedelta

db.connect()

# db.drop_tables([PuttSesh, Putt])
# db.create_tables([PuttSesh, Putt])

##########################################
# ↓ used to implement new puttsesh table
##########################################
# db.drop_tables([PuttSeshTemp])
# db.drop_tables([PuttTemp])
# db.create_tables([PuttSesh, Putt])

my_user = User.get(User.username == 'admin')
#############################################
# ↑ used to implement new puttsesh table
#############################################

for i in range(14):
    new_puttsesh = PuttSesh(user=my_user, date=(datetime.now() - relativedelta(months=i)), no_putters=20)
    new_puttsesh.save()

    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=18)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=10, distance=21)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=24)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=27)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=30)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=20, distance=33)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=10, distance=21)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=18)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=1, distance=18)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=6, distance=21)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=2, distance=24)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=27)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=4, distance=30)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=19, distance=33)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=10, distance=21)
    new_putt.save()
    new_putt = Putt(putt_sesh=new_puttsesh, putts_made=15, distance=18)
    new_putt.save()

# new_puttsesh = PuttSesh(date=(datetime.now() - timedelta(hours=2)), no_putters=20)
# new_puttsesh.save()
# old_puttsesh = PuttSesh(date='2019-06-28', no_putters=20)
# old_puttsesh.save()



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
