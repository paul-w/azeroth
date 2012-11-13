''' Initial configuration of database '''

from __future__ import with_statement
from __init__ import app
from contextlib import closing
from settings import DB_SCHEMA, DATABASE
import sqlite3

CONFIGURATION_FILE = 'game_config.txt'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def default_users(db):
    db.cursor().execute(
              'insert into players ' 
              '(location, username, password, history) values ' 
              '(?, ?, ?, ?)' ,
              ['start', 'default','user', 'welcome to azeroth']   )

def setup(db):
    f = open(CONFIGURATION_FILE, 'r').read().split('\n')
    print "file", f
    for line in f:
        print line
        s = line.split(' ')
        table = s[0]
        print table
        if table == 'path':
            right = s[1]
            left = s[2]
            db.execute(
                'insert into paths (right, left) values (?, ?)', (right, left))
            db.commit()
            print 'inserted into paths'
            path_id, = db.execute(
                'select id from paths where right=? and left=?', (right, left)).fetchone()
            db.commit() 
            for i in xrange(3, len(s)):
                required_item = s[i]
                db.execute(
                        'insert into requirements (item, path) values (?, ?)', 
                        (required_item, path_id))
                db.commit()
        if table == 'item':
            name = s[1]
            loc = s[2]
            db.execute(
                    'insert into items (location, name) values (?, ?)',
                    (loc, name))
            db.commit()
            print db.execute(
            'select name from items').fetchall()

def print_setup(db): 
     cur = db.execute(
            'select id, right, left from paths')
     s =  cur.fetchall() 
     print 'fetched paths', s
     cur = db.execute(
            'select name, location from items')
     s =  cur.fetchall() 
     print 'items', s
     cur = db.execute(
            'select id, item, path from requirements')
     s =  cur.fetchall() 
     print 'requirements', s

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(DB_SCHEMA) as f:
            db.cursor().executescript(f.read()) 
            setup(db) 
            print_setup(db)
            default_users(db)
        db.commit()

init_db()
