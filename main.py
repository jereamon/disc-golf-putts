import os
import datetime
import random
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from flask import json
from model import PuttSesh, Putt, User

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()


distances = [18, 21, 24, 27, 30, 33]


def get_averages():
    """ Returns a tuple of all time and today's putting averages. """

    putt_avgs = {}
    current_user = User.get(User.username == session.get('logged_in_user'))
    # all_sessions = PuttSesh.select().where(PuttSesh.user == current_user)

    for record in PuttSesh.select().where(PuttSesh.user == current_user):
        print(record)

    for distance in distances:
        temp_list = []
        for putt in Putt.select().where(Putt.distance == distance):
            no_putters = putt.putt_sesh.no_putters
            temp_list.append(putt.putts_made / no_putters)
        try:
            putt_avgs[distance] = int(
                round((sum(temp_list) / len(temp_list)), 2) * 100)
        except:
            putt_avgs[distance] = 0
    putt_avgs['18-33'] = int(round((sum(putt_avgs.values()) /
                                    len(putt_avgs.values())), 2))

    today_putt_avgs = {}
    for distance in distances:
        temp_list = []
        for putt in Putt.select().where(Putt.distance == distance):
            # The first if is for local dev 2nd is for heroku server utc time.
            # if putt.putt_sesh.date.date() == datetime.datetime.today().date():
            if putt.putt_sesh.date.date() == (datetime.datetime.today() - datetime.timedelta(hours=7)).date():
                no_putters = putt.putt_sesh.no_putters
                temp_list.append(round((putt.putts_made / no_putters), 2))
        try:
            today_putt_avgs[distance] = int(round(
                (sum(temp_list) / len(temp_list)), 2) * 100)
        except:
            today_putt_avgs[distance] = 0
    today_putt_avgs['18-33'] = int(round(sum(today_putt_avgs.values()) /
                                         len(today_putt_avgs.values()), 2))

    return (putt_avgs, today_putt_avgs)


def get_putt_distance(get_or_post):
    """
    Returns an integer to set the next putting distance depending on whether a
    session is in progress and the selection of random or incrementing
    distances.
    """
    if get_or_post == 'get':
        if session.get('distance', None) == None:
            if session.get('rand_or_no', None) == 'rand-dist':
                session['distance'] = random.randint(0, len(distances) - 1)
            else:
                session['distance'] = 0
    else:
        if session.get('rand_or_no', None) == 'rand-dist':
            session['distance'] = random.randint(0, len(distances) - 1)
        else:
            if session.get('distance') + 1 > len(distances)-1:
                session['distance'] = 0
            else:
                session['distance'] = session.get('distance') + 1

    return distances[session.get('distance')]


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in_user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    # if not login_check():
    #     return redirect(url_for('login'))

    putt_avgs, today_putt_avgs = get_averages()

    return render_template('home.jinja2', putt_avgs=putt_avgs,
                           today_putt_avgs=today_putt_avgs)


@app.route('/puttsesh/new', methods=['GET', 'POST'])
@login_required
def new_puttsesh():
    if request.method == "POST":
        no_putters = request.form['no-putters']
        # specifies whether to increment putting distance or have random distances
        session['rand_or_no'] = request.form['rand-or-no']

        # This is necessary because the heroku server is set to UTC
        current_time = datetime.datetime.now() - datetime.timedelta(hours=7)
        current_user = session.get('logged_in_user')
        # current_time = datetime.datetime.now()
        new_puttsesh = PuttSesh(user=current_user, date=current_time, no_putters=no_putters)
        new_puttsesh.save()
        session['current_sesh_id'] = new_puttsesh.id

        return redirect(url_for('current_puttsesh', sesh_id=session.get('current_sesh_id')))

    return render_template('new_puttsesh.jinja2')


@app.route('/puttsesh/current/<sesh_id>', methods=['GET', 'POST'])
@login_required
def current_puttsesh(sesh_id):
    current_session = PuttSesh.select().where(PuttSesh.id == sesh_id).get()

    if request.method == "POST":
        if request.form['action'] == 'End Putting Session':
            session.pop('distance', None)
            session.pop('rand_or_no', None)
            session.pop('current_sesh_id')
            return redirect(url_for('home'))

    distance = get_putt_distance('get')
    putt_avgs, today_putt_avgs = get_averages()
    return render_template('current_puttsesh.jinja2', distance=distance,
                           today_putt_avgs=today_putt_avgs,
                           no_putters=current_session.no_putters)


@app.route('/puttsesh/view')
@login_required
def view_puttsesh():
    all_sessions = PuttSesh.select()
    return render_template('view_puttsesh.jinja2', all_sessions=all_sessions)


@app.route('/puttsesh/view/<sesh_id>', methods=['GET', 'POST'])
@login_required
def view_puttsesh_single(sesh_id):
    if request.method == "POST":
        if request.form.get('puttsesh-id'):
            puttsesh_id = request.form.get('puttsesh-id')
            session_to_del = PuttSesh.select().where(PuttSesh.id == puttsesh_id).get()

            session_to_del.delete_instance(session_to_del)

            return redirect(url_for('view_puttsesh'))
        if request.form.get('putt-id'):
            putt_id = request.form.get('putt-id')
            putt_to_del = Putt.select().where(Putt.id == putt_id).get()

            putt_to_del.delete_instance(putt_to_del)
    single_session = PuttSesh.select().where(PuttSesh.id == sesh_id).get()
    associated_putts = Putt.select().where(Putt.putt_sesh == single_session)

    return render_template('view_puttsesh_single.jinja2',
                           single_session=single_session,
                           putts=associated_putts)


@app.route('/save_putt', methods=['POST'])
@login_required
def save_putt():
    putts_made = request.form.get('no_putts')
    new_putt = Putt(putt_sesh=session['current_sesh_id'], putts_made=putts_made,
                    distance=distances[session.get('distance')])
    save_code = new_putt.save()
    # new_putt_id = new_putt.id

    distance = get_putt_distance('post')

    return json.dumps({'status': 'OK', 'distance': distance,
                       'save_code': save_code})


@app.route('/update_putt', methods=['POST'])
@login_required
def update_putt():
    putt_id = request.form['putt_id']
    no_putters = request.form['no_putters']
    new_value = request.form['new_value']

    putt_to_update = Putt.select().where(Putt.id == putt_id).get()
    putt_to_update.putts_made = new_value
    putt_to_update.save()

    return json.dumps({'status': 'OK', 'putt_id': putt_id,
                       'new_value': new_value,
                       'no_putters': no_putters})


@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        # session.pop('logged_in_user', None)
        if request.form['action'] == 'Log In':
            login_user = User.get(User.username == request.form['username'])
            if login_user.check_password(request.form['password']):
                session['logged_in_user'] = login_user.username
                return redirect(url_for('home'))
        else:
            session.pop('logged_in_user', None)

    login_stat = session.get('logged_in_user', None)
    return render_template('login.jinja2', login_stat=login_stat)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6789))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(host='0.0.0.0', port=port)
