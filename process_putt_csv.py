""" Proccesses my disc golf putts csv from my google spreadsheet. """

from datetime import datetime
from model import db, User, PuttSesh, Putt

# db.drop_tables([PuttSesh, Putt])
# db.create_tables([PuttSesh, Putt])

with open('putt_averages.csv', 'r') as in_putt_file:
    in_putt_file_parsed = in_putt_file.read().split(",")

    single_putt_dict = {}
    for index, value in enumerate(in_putt_file_parsed):
        if '/' in value:
            if '\n' in value:
                single_putt_dict[value[1:]] = {"no_putters": in_putt_file_parsed[index + 1]}
                date = value[1::]
            else:
                single_putt_dict[value] = {"no_putters": in_putt_file_parsed[index + 1]}
                date = value
        elif "'" in value:
            distance = value
            single_putt_dict[date][value] = []
        elif '/' not in in_putt_file_parsed[index - 1] and value:
            # print(value)
            if "\n" in value:
                single_putt_dict[date][distance].append(value[:-2])
            else:
                single_putt_dict[date][distance].append(value)

user = User.get(User.username == 'jereamon')
for date in single_putt_dict:
    # print(date)
    save_date = datetime.strptime(date + '/2019 9:00AM', "%m/%d/%Y %I:%M%p")
    new_puttsesh = PuttSesh(user=user, date=save_date, no_putters=single_putt_dict[date]['no_putters'])
    new_puttsesh.save()
    for distance in single_putt_dict[date]:
        # print(repr(distance))
        if distance != "no_putters":
            for putt in single_putt_dict[date][distance]:
                if "\n" in distance:
                    distance = distance[1:]
                # print(repr(putt))
                new_putt = Putt(putt_sesh=new_puttsesh, putts_made=putt, distance=distance[:-1])
                new_putt.save()