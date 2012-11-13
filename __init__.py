"""
Handles requests
"""

from forms import GameForm, LoginForm, RegistrationForm
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from functools import wraps
from settings import DATABASE, DEBUG, SECRET_KEY, USERNAME, PASSWORD
from user import User 
import sqlite3
import os.path
from game_logic import *

CONFIGURATION_FILE = 'game_config.txt'

# database configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = ( 
'\xa5\xee\xd4\x1a\\\x8aQ\xa4\x1a\xa5\x9f\xe3\xdeT=\xb5\xbd\xa6\x93\xb3\x9a' )

# adapted from http://flask.pocoo.org/snippets/8/
def access_denied():

    '''What to do when user does not have proper credentials'''

    flash('To access that page, please log in first')
    return redirect(url_for('login', next = request.path))

def requires_login(f):

    '''Decorator to be applied to actions that require login.'''

    @wraps(f)
    def decorated(*args, **kwargs):
       if not 'logged_in' in session:
           return access_denied()
       return f(*args, **kwargs)
    return decorated

def connect_db():
    
    '''Establishes database connection'''

    return sqlite3.connect(app.config['DATABASE']) 

@app.teardown_request
def teardown_request(exception):

    '''Handle teardown requests'''

    g.db.close()

@app.before_request
def before_request():
    
    '''Opens log file and connects to DB prior to requests'''

    g.db = connect_db()
    f = open("log.txt", 'a')
    f.write(request.url + '\n')
    f.close()

def login_user(userid):
    
    '''Logs user in.  Called following verified authentication'''

    session['logged in'] = True 
    session['user_id'] = userid 

@app.route("/register", methods=["GET", "POST"])
def register():
    
    '''Renders registration page'''

    reg_form = RegistrationForm(request.form)
    if request.method == 'POST': 
        username = reg_form.username.data
        password = reg_form.password.data
        userid = new_game(username, password, g.db) 
        cur  = g.db.execute('select location, id, username, password '   \
                            'from players '      \
                            'where id=?', (userid,) 
                            )
        location, userid, fetched_u, fetched_p = cur.fetchone()
        if username == fetched_u and password == fetched_p:
            session['logged_in'] = True 
            session['user_id'] = userid 
            flash('Logged In')
            return redirect(url_for("index")) 
        else:
            flash('just be yourself')
    return render_template("register.html", 
                                          reg_form = reg_form )

@app.route("/login", methods=["GET", "POST"])
def login():
    
    '''Renders login page'''

    login_form = LoginForm(request.form)
    if request.method == 'POST': 
        username = login_form.username.data
        password = login_form.password.data
        cur  = g.db.execute('select id, username, password '   \
                            'from players '      \
                            'where id=?', (1,) 
                            )
        userid, fetched_u, fetched_p = cur.fetchone()
        if username == fetched_u and password == fetched_p:
            session['logged_in'] = True 
            session['user_id'] = userid 
            flash('Logged In')
            return redirect(url_for("index")) 
        else:
            flash('just be yourself')
    return render_template("login.html", login_form = login_form,
                                           )
@app.route('/', methods=['GET', 'POST'])
@requires_login
def index():

    '''Renders main page'''

    game_form = GameForm(request.form)
    inp = game_form.inp.data
    if request.method=='POST':
        if not game_over(g.db, session['user_id']):
            play(inp, g.db, session['user_id']) 
    out = get_history(g.db, session['user_id']) 
    return render_template('main.html', game_form=game_form, history = out)


