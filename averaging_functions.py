from collections import OrderedDict
from datetime import datetime, timedelta
from flask import session
from model import PuttSesh, Putt, User


def get_session_avg(session):
    """
    Takes a session object and returns the putting averages for that session.
    """
    pass
    session_putts = Putt.select().where(Putt.putt_sesh == session).order_by(Putt.distance)

    putt_avgs = OrderedDict()
    putt_individual_avg = OrderedDict()

    for putt in session_putts:
        # print(f"In get_session_avgs for loop putt.putts_made = {putt.putts_made} session.no_putters = {session.no_putters} distance = {putt.distance}")
        if putt_individual_avg.get(putt.distance, None):
            putt_individual_avg[putt.distance].append(
                putt.putts_made / session.no_putters)
        else:
            putt_individual_avg[putt.distance] = [
                putt.putts_made / session.no_putters]

    # print(f"In get_session_avgs putt_indiviual_avgs = {putt_individual_avg}")
    for putt_avg in putt_individual_avg:
        putt_avgs[putt_avg] = sum(
            putt_individual_avg[putt_avg]) / len(putt_individual_avg[putt_avg])

    # print(f"In get_session_avgs putt_avgs = {putt_avgs}")
    return putt_avgs


def get_avg(current_user, all_time=None):
    """
    Retrieves all sessions for a user for the day and returns the putt averages
    for those sessions.
    """
    today_utc_corrected = (datetime.today() -
                           timedelta(hours=7)).date()

    if all_time:
        users_sessions = PuttSesh().select().where(PuttSesh.user == current_user)
    else:
        users_sessions = PuttSesh().select().where(PuttSesh.user == current_user and
                                                   PuttSesh.date >= today_utc_corrected)

    session_avgs = OrderedDict()
    today_putt_avgs = OrderedDict()
    for session in users_sessions:
        session_avgs_return = get_session_avg(session)

        for distance in session_avgs_return:
            if session_avgs.get(distance):
                session_avgs[distance].append(session_avgs_return[distance])
            else:
                session_avgs[distance] = [session_avgs_return[distance]]

    for distance in session_avgs:
        today_putt_avgs[distance] = int(
            round((sum(session_avgs[distance]) / len(session_avgs[distance])), 2) * 100)

    return today_putt_avgs
