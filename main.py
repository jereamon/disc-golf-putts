import os
import datetime
import random
from functools import wraps
import averaging_functions as af
from flask import Flask, render_template, request, redirect, url_for, session
from flask import json
from model import PuttSesh, Putt, User
from peewee import DoesNotExist

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()



distances = [18, 21, 24, 27, 30, 33]\



def get_putt_distance(get_or_post):
    """
    Returns an integer to set the next putting distance depending on whether a
    session is in progress and the selection of random or incrementing
    distances.
    """
    if session.get('session_dist_select', None) != None:
        if get_or_post == 'get':
            if session.get('distance', None) == None:
                if session.get('session_dist_select', None) == 'rand-dist':
                    session['distance'] = random.randint(0, len(distances) - 1)
                else:
                    session['distance'] = 0
        else:
            if session.get('session_dist_select', None) == 'rand-dist':
                session['distance'] = random.randint(0, len(distances) - 1)
            else:
                if session.get('distance') + 1 > len(distances)-1:
                    session['distance'] = 0
                else:
                    session['distance'] = session.get('distance') + 1

        return distances[session.get('distance')]
    else:
        return None


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

    current_user = User.get(User.username == session.get('logged_in_user'))
    all_time_avgs = af.get_avg(current_user, 'ALL_TIME')
    today_avgs = af.get_avg(current_user)

    # return render_template('home.jinja2', all_time_avgs=sorted(all_time_avgs),
    #                        today_avgs=sorted(today_avgs))
    return render_template('home.jinja2', all_time_avgs=all_time_avgs,
                           today_avgs=today_avgs)


@app.route('/puttsesh/new', methods=['GET', 'POST'])
@login_required
def new_puttsesh():
    if request.method == "POST":
        no_putters = request.form['no-putters']
        # specifies whether to increment putting distance or have random distances
        if (request.form['session_dist_select'] == 'rand-dist') or \
                (request.form['session_dist_select'] == 'inc-dist'):
            session['session_dist_select'] = request.form['session_dist_select']

        # This is necessary because the heroku server is set to UTC
        current_time = datetime.datetime.now() - datetime.timedelta(hours=7)
        # current_time = datetime.datetime.now()
        current_user = session.get('logged_in_user')

        new_puttsesh = PuttSesh(
            user=current_user, date=current_time, no_putters=no_putters)
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
            session.pop('session_dist_select', None)
            session.pop('current_sesh_id')
            return redirect(url_for('home'))

    distance = get_putt_distance('get')

    current_user = User.get(User.username == session.get('logged_in_user'))
    all_time_avgs = af.get_avg(current_user, 'ALL_TIME')
    today_avgs = af.get_avg(current_user)
    return render_template('current_puttsesh.jinja2', distance=distance,
                           today_avgs=today_avgs, all_time_avgs=all_time_avgs,
                           no_putters=current_session.no_putters)


@app.route('/puttsesh/view')
@login_required
def view_puttsesh():
    all_sessions = PuttSesh.select().order_by(PuttSesh.date.desc())
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
    if request.form.get('distance'):
        distance = request.form.get('distance')
    else:
        distance = distances[session.get('distance')]
    new_putt = Putt(putt_sesh=session['current_sesh_id'], putts_made=putts_made,
                    distance=distance)
    save_code = new_putt.save()

    current_user = User.get(User.username == session.get('logged_in_user'))
    all_time_avgs=af.get_avg(current_user, 'all_time')
    today_avgs = af.get_avg(current_user)

    distance = get_putt_distance('post')

    return json.dumps({'status': 'OK', 'distance': distance,
                       'save_code': save_code, 'today_avgs': today_avgs,
                       'all_time_avgs': all_time_avgs})


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
def login(error=None):
    if request.method == 'POST':
        session.pop('error', None)
        # session.pop('logged_in_user', None)
        if request.form['action'] == 'Log In':
            try:
                login_user = User.get(User.username == request.form['username'].lower())
            except DoesNotExist:
                session['error'] = f"{request.form['username']} could not be found!"
                return redirect(url_for('login'))
            if login_user.check_password(request.form['password']):
                session['logged_in_user'] = login_user.username

                session.permanent = True

                return redirect(url_for('home'))
            session['error'] = "Password Incorrect!"
        else:
            session.pop('logged_in_user', None)

    login_stat = session.get('logged_in_user', None)
    return render_template('login.jinja2', login_stat=login_stat)


@app.template_filter('strparsetime')
def string_parse_time_filter(value, date_format):
    return datetime.datetime.strptime(value, date_format)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6789))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(host='0.0.0.0', port=port)
