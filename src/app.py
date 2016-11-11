from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def root():
  if request.method == 'POST':
    print request.form
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    return render_template('index.html', name=name, email=email), 200
  else:
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
