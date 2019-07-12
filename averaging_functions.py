from collections import OrderedDict
from datetime import datetime, timedelta
from flask import session
from model import PuttSesh, Putt, User


def get_session_avg(session):
    """
    Takes a session object and returns the putting averages for that session.
    """
    # Takes a session object as an argument. Finds all putts corresponding to
    # that session and orders them by their Putt.distance.
    session_putts = Putt.select().where(Putt.putt_sesh == session).order_by(Putt.distance)

    session_putt_avgs = OrderedDict()
    putt_individual_avg = OrderedDict()

    # Loops the putts for the current session.
    for putt in session_putts:
        # if the current putt's distance is already in the previously defined
        # OrderedDict we append to the list for that key. Otherwise we create a
        # list for that key using the current putts values: putts_made / no_putters
        if putt_individual_avg.get(putt.distance, None):
            putt_individual_avg[putt.distance].append(
                putt.putts_made / session.no_putters)
        else:
            putt_individual_avg[putt.distance] = [
                putt.putts_made / session.no_putters]

    for putt_avg in putt_individual_avg:
        session_putt_avgs[putt_avg] = sum(
            putt_individual_avg[putt_avg]) / len(putt_individual_avg[putt_avg])

    return session_putt_avgs



def get_avg(current_user, all_time=None):
    """
    Retrieves all sessions for a user for the day and returns the putt averages
    for those sessions.
    """
    # First, get a datetime.today corrected to equal PST
    today_utc_corrected = (datetime.today() -
                           timedelta(hours=7)).date()

    # If the all_time variable is specified we get every puttsesh. Otherwise
    # we just get the sessions that match today's date.
    if all_time:
        users_sessions = PuttSesh().select().where(PuttSesh.user == current_user)
    else:
        users_sessions = PuttSesh().select().where(PuttSesh.user == current_user and
                                                   PuttSesh.date >= today_utc_corrected)

    # Create OrderedDicts to maintain low to high distance averages.
    session_avgs = OrderedDict()
    putt_avgs = OrderedDict()

    for session in users_sessions:
        # this will be an ordered dict containing the averages for an individual
        # session. Keys will be distances, values floats.
        session_avgs_return = get_session_avg(session)

        # Loop the returned OrderedDict, first; check if distance is already in
        # the predefined session_avgs OrderedDict
        # If the distance is not in the dict create a list with the current loop
        # iterations value in it.
        # Otherwise append to the list corresponding to the current distance
        # with the current loop iterations value.
        for distance in session_avgs_return:
            if session_avgs.get(distance):
                session_avgs[distance].append(session_avgs_return[distance])
            else:
                session_avgs[distance] = [session_avgs_return[distance]]
        # Finally, we'll have an OrderedDict where keys are distances and values
        # are a list of averages for that distance.

    # Finally we'll loop our populated dict and find the average of the list of
    # averages stored as values in it.
    for distance in session_avgs:
        putt_avgs[distance] = int(
            round((sum(session_avgs[distance]) / len(session_avgs[distance])), 2) * 100)

    return putt_avgs
