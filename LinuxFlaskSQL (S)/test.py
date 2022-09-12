
from flask import *
import mysql.connector

app=Flask(__name__)

app.secret_key="abc"

conn = mysql.connector.connect(user='root',
                               host='127.0.0.1',
                               database='doctorappoint',
                               password='Sreesanjuna@2000')

mycursor=conn.cursor()

# @app.route('/')
# def enter():
#     return render_template('welcome.html')

@app.route('/')
def enter():
    return render_template('Bootstrap.html')

@app.route('/admin_login')
def home():
    if not session.get('logged_in'):
        return render_template('adminlogin.html')
    else:
        # return "Hello Admin!  <br> <a href=\"/admin_logout\">Logout</a>"
        return render_template('als.html')

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

@app.route('/hi')
def frgtpwd():
    return render_template('forgotpwd.html')

@app.route('/specializations')
def specializations():
    mycursor.execute('select * from specialization')
    x=mycursor.fetchall()
    return render_template('add_specialization.html',data=x)

@app.route('/admin/add_specializations',methods=['POST','GET'])
def add_specializations():
    mycursor.execute('select emailid from doctor_details')
    x=mycursor.fetchall()
    print(x)
    l=[]
    for i in x:
        for j in i:
            l.append(j)
    if request.form['sname'] not in l:
        mycursor.execute('insert into specialization (sname) values (%s)',[request.form['sname']])
        conn.commit()
        mycursor.execute('select * from specialization')
        x=mycursor.fetchall()
        return render_template('add_specialization.html',data=x)

@app.route('/doctor_details')
def doctor_details():
    msg=''
    print('######')
    mycursor.execute('select * from specialization')
    d=mycursor.fetchall()
    return render_template('add_doctor_details.html',m=msg,data=d)


@app.route('/admin/add_doctor_details',methods=['POST','GET'])
def add_doctor_details():
    mycursor.execute('select emailid from doctor_details')
    x=mycursor.fetchall()
    l=[]
    for i in x:
        for j in i:
            l.append(j)
    if request.form['email'] not in l:
        sql='insert into doctor_details (fullname, qualification, emailid, contactno, consultancyfee, pwd, address, city, state) values (%s, %s, %s, %s, %s,%s, %s, %s, %s) '
        val=[request.form['fullname'],request.form['qualification'],request.form['email'],request.form['contactno'],request.form['consultancyfee'],request.form['pwd'],request.form['address'],request.form['city'],request.form['state']]
        mycursor.execute(sql,val)
        conn.commit()
        k=request.form.getlist('myval')
        mycursor.execute('select doctorID from doctor_details where emailid=%s',[request.form['email']])
        doctorid=mycursor.fetchall()[0][0]
        print
        for i in k:
            doctorid=int(doctorid)
            i=int(i)
            mycursor.execute('insert into d_s_mapping values (%s,%s) ',[i,doctorid])
            conn.commit()
        msg="Added " + request.form['fullname'] + " to the list of Doctors\'s in the Hospital."
        mycursor.execute('select * from specialization')
        d=mycursor.fetchall()
        return render_template('add_doctor_details.html',m=msg,data=d)
    else:
        msg="\""+request.form['email']+"\""+" already exists!"
        return render_template('add_doctor_details.html',m=msg)

@app.route("/display",methods=["POST"])
def display():
    mycursor.execute('select * from doctor_details order by doctorID desc ')
    x=mycursor.fetchall()
    return render_template('display_doctor_details.html',data=x)

@app.route('/doctor_login')
def doctor():
    if not session.get('logged_in'):
        session['logged_in']=True
        m=''
        return render_template('doclogin.html',msg=m)
    else:
        return render_template('dls.html')

@app.route('/doctorlogin',methods=['POST','GET'])
def doc_login():
    mycursor.execute('select emailid from doctor_details')
    x=mycursor.fetchall()
    l=[]
    for i in x:
        for j in i:
            l.append(j)
    if request.form['email'] in l:
        t=[request.form['email']]
        mycursor.execute('select pwd from doctor_details where emailid = %s',t)
        d=mycursor.fetchall()
        for i in d:
            for j in i:
                passwd=j
        if request.form['pwd']==passwd:
            session['logged_in'] = True
            return render_template('dls.html')
        else:
            m='Wrong Password!'
            return render_template('doclogin.html',msg=m)
    else:
        m='You have entered wrong Email ID!'
        return render_template('doclogin.html',msg=m)

@app.route("/admin_logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/doctor_logout")
def doc_logout():
    session['logged_in'] = False
    return doctor()

app.run()