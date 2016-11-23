import sqlite3
import os

from flask import Flask, g, render_template, url_for, request, redirect, session, flash, abort
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sGJeN21Z]=6RmK='
db_location = 'var/wish_db.db'

def required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorator

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
      db = sqlite3.connect(db_location)
      g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
      db.close()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('var/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods=['GET','POST'])
def root():
 # db = get_db()
 # db.cursor().execute('insert into users values ("emma", "emma.reavley95@gmail.com", "dijon78")')
 # db.commit()

  if request.method == 'POST':
    print request.form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    return render_template('index.html', username=username, email=email), 200
  else:
    return render_template('home.html')

@app.route('/index')
@required
def index():
  db = get_db()
  cur = db.execute('select title, quantity, price, details from wishlists order by wish desc')
  wishlists = [dict(title=row[0], quantity=row[1], price=row[2], details=row[3]) for row in cur.fetchall()]
  db.close()
  return render_template('index.html', wishlists=wishlists)

@app.route('/add', methods=['GET','POST'])
def add():
  if not session.get('logged_in'):
      abort(401)
  db = get_db()
  db.execute('INSERT INTO wishlists (title,quantity,price,details) VALUES(?,?,?,?)', 
            [request.form['title'], request.form['quantity'], request.form['price'], request.form['details']])
  db.commit()
  session['wish_added'] = True
  flash('Your wish has been added to your list')
  return redirect(url_for('index'))

@app.route('/remove')
def remove():
  session.pop('wish_added', None)
  flash('Your wish has been removed from your list')
  return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'simon_AWT':
      error = 'Incorrect Username or Password, Please try again.'
    else:
      session['logged_in'] = True
      flash('Welcome! You can now send your wishlist to Santa')
      return redirect(url_for('index'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('Successful log out')
  return redirect(url_for('root'))

@app.errorhandler(404)
def page_not_found(error):
  return "We couldn't answer your request. Please try again later or this page might not exist. </br> Please, check your URL", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
