
from flask import *
import mysql.connector

app=Flask(__name__)

app.secret_key="abc"

conn = mysql.connector.connect(user='root',
                               host='127.0.0.1',
                               database='doctorappoint',
                               password='Sreesanjuna@2000')

mycursor=conn.cursor()

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
        print('Wrong Email!')
        return render_template('admin_error_email.html')
    else:
        print('Wrong Password')
        return render_template('admin_error_password.html')

@app.route('/doctor_details')
def doctor_details():
    return render_template('doctor_details.html')


@app.route('/admin/add_doctor_details',methods=['POST','GET'])
def add_doctor_details():
    sql='insert into doctor_details (fullname, qualification, specialization, emailid, contactno, consultancyfee, pwd, address, city, state) values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s) '
    val=[request.form['fullname'],request.form['qualification'],request.form['specialization'],request.form['email'],request.form['contactno'],request.form['consultancyfee'],request.form['pwd'],request.form['address'],request.form['city'],request.form['state']]
    mycursor.execute(sql,val)
    conn.commit()
    # msg="Added " + request.form['fullname'] + "to the list of Doctors\'s in the Hospital."
    return render_template('added_doctor_details.html')

@app.route("/display",methods=["POST"])
def display():
    # sql = 'select * from doctor_details order by doctorID desc '
    # val = [session['loggedUser']]
    # mycursor.execute(sql,val)
    mycursor.execute('select * from doctor_details order by doctorID desc ')
    x=mycursor.fetchall()
    conn.close()
    print(x)
    return render_template('display_doctor_details.html',data=x)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

app.run()