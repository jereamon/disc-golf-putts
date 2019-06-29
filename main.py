import os
import datetime
import random
from flask import Flask, render_template, request, redirect, url_for, session
from model import PuttSesh, Putt

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()

distances = [18, 21, 24, 27, 30, 33]


def get_averages():
    putt_avgs = {}
    for distance in distances:
        temp_list = []
        for putt in Putt.select().where(Putt.distance == distance):
            no_putters = putt.putt_sesh.no_putters
            temp_list.append(putt.putts_made / no_putters)
        try:
            putt_avgs[distance] = round((sum(temp_list) / len(temp_list)), 2)
        except:
            putt_avgs[distance] = 0
    putt_avgs['18-33'] = round((sum(putt_avgs.values()) /
                                len(putt_avgs.values())), 2)

    today_putt_avgs = {}
    for distance in distances:
        temp_list = []
        for putt in Putt.select().where(Putt.distance == distance):
            if putt.putt_sesh.date.date() == datetime.datetime.today().date():
                no_putters = putt.putt_sesh.no_putters
                temp_list.append(round((putt.putts_made / no_putters), 2))
        try:
            today_putt_avgs[distance] = round(
                (sum(temp_list) / len(temp_list)), 2)
        except:
            today_putt_avgs[distance] = 0
    today_putt_avgs['18-33'] = round(sum(today_putt_avgs.values()) /
                                     len(today_putt_avgs.values()), 2)

    return (putt_avgs, today_putt_avgs)


@app.route('/')
def home():
    putt_avgs, today_putt_avgs = get_averages()

    return render_template('home.jinja2', putt_avgs=putt_avgs,
                           today_putt_avgs=today_putt_avgs)


@app.route('/puttsesh/new', methods=['GET', 'POST'])
def new_puttsesh():
    if request.method == "POST":
        no_putters = request.form['no-putters']
        # specifies whether to increment putting distance or have random distances
        session['rand_or_no'] = request.form['rand-or-no']

        # This is necessary because the heroku server is set to UTC
        current_time = datetime.datetime.now() - datetime.timedelta(hours=7)
        # current_time = datetime.datetime.now()
        new_puttsesh = PuttSesh(date=current_time, no_putters=no_putters)
        new_puttsesh.save()
        session['current_sesh_id'] = new_puttsesh.id

        return redirect(url_for('putt'))

    return render_template('new_puttsesh.jinja2')


@app.route('/puttsesh/view')
def view_puttsesh():
    all_sessions = PuttSesh.select()
    return render_template('view_puttsesh.jinja2', all_sessions=all_sessions)


@app.route('/puttsesh/view/<sesh_id>', methods=['GET', 'POST'])
def view_puttsesh_single(sesh_id):
    single_session = PuttSesh.select().where(PuttSesh.id == sesh_id).get()
    associated_putts = Putt.select().where(Putt.putt_sesh == single_session)

    return render_template('view_puttsesh_single.jinja2', single_session=single_session, putts=associated_putts)


@app.route('/putt', methods=['GET', 'POST'])
def putt():
    if request.method == "POST":
        if request.form['action'] == 'End Putting Session':
            session.pop('distance', None)
            session.pop('rand_or_no', None)
            return redirect(url_for('home'))

        new_putt = Putt(putt_sesh=session['current_sesh_id'], putts_made=request.form.get(
            'no_putts'), distance=distances[session.get('distance')])
        new_putt.save()

        if session.get('rand_or_no', None) == 'rand-dist':
            distance = random.choice(distances)
        else:
            if session.get('distance', None) != None:
                if session.get('distance') + 1 > len(distances)-1:
                    session['distance'] = 0
                else:
                    session['distance'] = session.get('distance') + 1
                distance = session.get('distance')
            else:
                session['distance'] = 0

            distance = distances[session.get('distance')]

        putt_avgs, today_putt_avgs = get_averages()
        return render_template('putt.jinja2', distance=distance, today_putt_avgs=today_putt_avgs)

    if session.get('rand_or_no', None) == 'rand-dist':
        distance = random.choice(distances)
    else:
        session['distance'] = 0

    distance = distances[session.get('distance')]

    # distance = 0
    putt_avgs, today_putt_avgs = get_averages()
    return render_template('putt.jinja2', distance=distance, today_putt_avgs=today_putt_avgs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6789))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port)
