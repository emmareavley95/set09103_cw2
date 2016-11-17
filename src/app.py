from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def root():
  if request.method == 'POST':
    print request.form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    return render_template('index.html', username=username, email=email), 200
  else:
    return render_template('home.html')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'simon_AWT':
      error = 'Incorrect Username or Password, Please try again.'
    else:
      return redirect(url_for('index'))
  return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
