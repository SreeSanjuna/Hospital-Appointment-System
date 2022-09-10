from flask import *
app = Flask(__name__)

app.secret_key="abc"

@app.route('/')
def enter():
    return render_template('welcome.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('adminlogin.html')
    else:
        return "Hello Admin!  <a href=\"/logout\">Logout</a>"

@app.route('/adminlogin', methods=['POST'])
def do_admin_login():
    if request.form['email'] == 'admin@gmail.com' and request.form['pwd'] == '12345':
        session['logged_in'] = True
        return render_template('als.html')
    elif request.form['email'] != 'admin@gmail.com':
        print('Wrong username!')
        return home()
    else:
        print('Wrong Password')
        return home()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

app.run()