
from flask import *
import mysql.connector

app=Flask(__name__)

app.secret_key="abc"

conn = mysql.connector.connect(user='root',
                               host='127.0.0.1',
                               database='doctorappoint',
                               password='')
# Sreesanjuna@2000
mycursor=conn.cursor()

@app.route('/')
def enter():
    return render_template('welcome.html')

@app.route('/admin_login')
def home():
    if not session.get('logged_in'):
        return render_template('adminlogin.html')
    else:
        return render_template('admindashboard.html')

@app.route('/adminlogin', methods=['POST'])
def do_admin_login():
    if request.form['email'] == 'admin@gmail.com' and request.form['pwd'] == '12345':
        session['logged_in'] = True
        return render_template('admindashboard.html')
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
    mycursor.execute('select * from specialization order by sid asc')
    x=mycursor.fetchall()
    return render_template('add_specialization.html',data=x)

@app.route('/admin/add_specializations',methods=['POST','GET'])
def add_specializations():
    mycursor.execute('select sname from specialization')
    x=mycursor.fetchall()
    l=[]
    for i in x:
        for j in i:
            l.append(j)
    if request.form['sname'] not in l:
        mycursor.execute('insert into specialization (sname) values (%s)',[request.form['sname']])
        conn.commit()
        mycursor.execute('select * from specialization order by sid asc')
        x=mycursor.fetchall()
        m=''
        return render_template('add_specialization.html',data=x,msg=m)
    else:
        mycursor.execute('select * from specialization order by sid asc')
        x=mycursor.fetchall()
        m='Specialization already exists'
        return render_template('add_specialization.html',data=x,msg=m)

@app.route('/doctor_details')
def doctor_details():
    msg=''
    mycursor.execute('select * from specialization order by sid asc')
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
        
@app.route('/disp_by_search',methods=['POST','GET'])
def display_by_emailid():
    if request.form['searchby']=='Email ID':
        mycursor.execute('select emailid from doctor_details')
        x1=mycursor.fetchall()
        mycursor.execute('select * from doctor_details order by doctorID desc ')
        x=mycursor.fetchall()
        q=dict()
        for i in range(0,len(x)):
            p=[]
            y=x[i][0]
            mycursor.execute('select s.sname from d_s_mapping dsm join specialization s on dsm.sid=s.sid where dsm.doctorID=%s',[y])
            z=mycursor.fetchall()
            for i in z:
                p.append(i[0])
            q[y]=p
        return render_template('disp_by_emailid_1.html',data1=x1,data=x,combo=q)
    elif request.form['searchby']=='Doctor ID':
        mycursor.execute('select doctorid from doctor_details')
        x1=mycursor.fetchall()
        mycursor.execute('select * from doctor_details order by doctorID desc ')
        x=mycursor.fetchall()
        q=dict()
        for i in range(0,len(x)):
            p=[]
            y=x[i][0]
            mycursor.execute('select s.sname from d_s_mapping dsm join specialization s on dsm.sid=s.sid where dsm.doctorID=%s',[y])
            z=mycursor.fetchall()
            for i in z:
                p.append(i[0])
            q[y]=p
        return render_template('disp_by_doctorid.html',data1=x1,data=x,combo=q)
    elif request.form['searchby']=='Specialization':
        mycursor.execute('select sname from specialization')
        x1=mycursor.fetchall()
        mycursor.execute('select * from doctor_details order by doctorID desc ')
        x=mycursor.fetchall()
        q=dict()
        for i in range(0,len(x)):
            p=[]
            y=x[i][0]
            mycursor.execute('select s.sname from d_s_mapping dsm join specialization s on dsm.sid=s.sid where dsm.doctorID=%s',[y])
            z=mycursor.fetchall()
            for i in z:
                p.append(i[0])
            q[y]=p
        return render_template('disp_by_specialization.html',data1=x1,data=x,combo=q)
    else:
        if request.form['searchby']=='None':
            return display()

@app.route('/disp_by_emailid_2',methods=['POST','GET'])
def display_by_emailid_1():
    print('111111')
    mycursor.execute('select * from doctor_details where emailid=%s',[request.form['emails']])
    x=mycursor.fetchall()
    print('222222',x)
    mycursor.execute('select dsm.doctorID,s.sname from specialization s join d_s_mapping dsm on dsm.sid=s.sid where dsm.doctorid=(select doctorid from doctor_details where emailid=%s)',[x[0][3]])
    y=mycursor.fetchall()
    print('333333',y)
    q=dict()
    p=[]
    for i in y:
        p.append(i[1])
    print('444444',p)
    q[y[0][0]]=p
    print('555555',q)
    return render_template('display_doctor_details1.html',data=x,combo=q)

@app.route('/disp_by_doctorid',methods=['POST','GET'])
def display_by_doctorid():
    print('111111')
    mycursor.execute('select * from doctor_details where doctorid=%s',[request.form['did']])
    x=mycursor.fetchall()
    print('222222',x)
    mycursor.execute('select dsm.doctorID,s.sname from specialization s join d_s_mapping dsm on dsm.sid=s.sid where dsm.doctorid=(select doctorid from doctor_details where emailid=%s)',[x[0][3]])
    y=mycursor.fetchall()
    print('333333',y)
    q=dict()
    p=[]
    for i in y:
        p.append(i[1])
    print('444444',p)
    q[y[0][0]]=p
    print('555555',q)
    return render_template('display_doctor_details1.html',data=x,combo=q)

@app.route('/disp_by_specialization', methods=['POST','GET'])
def display_by_specialization():
    mycursor.execute('select d.*, s.sname from doctor_details d join d_s_mapping dsm on d.doctorID=dsm.doctorID join specialization s on s.sid=dsm.sid having s.sname=%s',[request.form['sname']])
    x=mycursor.fetchall()
    return render_template('display_by_spcl.html',data=x)

@app.route('/disp')
def disp():
    return display()

@app.route("/display",methods=['POST'])
def display():
    mycursor.execute('select * from doctor_details order by doctorID desc ')
    x=mycursor.fetchall()
    q=dict()
    for i in range(0,len(x)):
        p=[]
        y=x[i][0]
        mycursor.execute('select s.sname from d_s_mapping dsm join specialization s on dsm.sid=s.sid where dsm.doctorID=%s',[y])
        z=mycursor.fetchall()
        for i in z:
            p.append(i[0])
        q[y]=p
    return render_template('display_doctor_details.html',data=x,combo=q)

@app.route('/patient_display')
def patientdisp_disp():
    return patient_display()

@app.route("/disp_patient",methods=['POST'])
def patient_display():
    mycursor.execute('select patientID,fullname,emailid, gender,dob,contactno,address,city,state from patient_details where patientID in (select distinct(patientID) from appointments)')
    x=mycursor.fetchall()
    mycursor.execute('select patientID,fullname,emailid, gender,dob,contactno,address,city,state from patient_details')
    y=mycursor.fetchall()
    return render_template('display_patients.html',d1=x,d2=y)

@app.route('/appointment_disp')
def appointment_disp():
    return app_display()

@app.route("/app_display",methods=['POST'])
def app_display():
    mycursor.execute('select a.aid, p.fullname, d.fullname, a.a_date, a.a_time, a.reason, a.astatus from appointments a join patient_details p on a.patientID=p.patientID join doctor_details d on a.doctorID=d.doctorID ')
    x=mycursor.fetchall()
    return render_template('display_appointments.html',data=x)

@app.route('/doc_sess_disp')
def doc_sess_disp():
    return doctor_session_display()

@app.route("/doctor_session_display",methods=['POST'])
def doctor_session_display():
    mycursor.execute('select ds.sessionID,ds.doctorID,dd.fullname,ds.login_time,ds.logout_time from doctor_session ds join doctor_details dd on ds.doctorID=dd.doctorID order by sessionID desc')
    x=mycursor.fetchall()
    return render_template('display_doctor_session.html',data=x)

@app.route('/doctor_login')
def doctor():
    if not session.get('logged_in'):
        session['logged_in']=True
        m=''
        return render_template('doclogin.html',msg=m)
    else:
        return render_template('doctordashboard.html')

@app.route('/doctorlogin',methods=['POST','GET'])
def doc_login():
    mycursor.execute('select doctorID from doctor_details where emailid=%s',[request.form['email']])
    b=mycursor.fetchall()[0][0]
    mycursor.execute('select current_timestamp()')
    c=mycursor.fetchall()[0][0]
    mycursor.execute('insert into doctor_session (doctorID,login_time) values (%s ,%s)',[b,c])
    conn.commit()
    mycursor.execute('select sessionID from doctor_session where doctorID=%s and login_time=%s',[b,c])
    session['sessionID']=mycursor.fetchall()[0][0]
    mycursor.execute('select emailid from doctor_details')
    x=mycursor.fetchall()
    session['loggedUser']=request.form['email']
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
            return render_template('doctordashboard.html')
        else:
            m='Wrong Password!'
            return render_template('doclogin.html',msg=m)
    else:
        m='You have entered wrong Email ID!'
        return render_template('doclogin.html',msg=m)

@app.route('/doctor_profile_view')
def doctor_profile_view():
    sql='select * from doctor_details where emailid=%s'
    val=[session['loggedUser']]
    mycursor.execute(sql,val)
    data=mycursor.fetchone()
    print(data)
    return render_template('doctor_profile_view.html',pdata=data)

@app.route('/doctor_profile')
def doctor_profile():
    sql='select * from doctor_details where emailid=%s'
    val=[session['loggedUser']]
    mycursor.execute(sql,val)
    data=mycursor.fetchone()
    print(data)
    return render_template('doctor_profile.html',pdata=data)
    
@app.route('/update_doc_profile',methods=['POST'])
def update_doc_profile():
    try:
        sql='update doctor_details set fullname=%s,qualification=%s,emailid=%s,contactno=%s,consultancyfee=%s,address=%s,city=%s,state=%s where emailid=%s'
        print("heyyy")
        val=[request.form['fullname'],request.form['qualification'],request.form['email'],request.form['contactno'],request.form['consultancyfee'],request.form['address'],request.form['city'],request.form['state'],session['loggedUser']]
        print("heyyy2")
        mycursor.execute(sql,val)
        conn.commit()
        print("heyy3")
        return render_template('doctordashboard.html',msg="Updated successfully")
    except Exception as e:
        print(e)
        return render_template('doctordashboard.html',msg="error")

@app.route('/patient_signup')
def patient():
    msg=''
    session['logged_in']=True
    return render_template('patientlogin.html',m=msg)

@app.route('/patient/signup',methods=['POST','GET'])
def signup():
    mycursor.execute('select emailid from patient_details')
    x=mycursor.fetchall()
    if len(x)!=0:
        l=[]
        for i in x:
            for j in i:
                l.append(j)
        if request.form['emailid'] not in l:
            sql='insert into patient_details (fullname,emailid,gender,dob,pwd,contactno,address,state,city) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            val=[request.form['fullname'],request.form['emailid'],request.form['gender'],request.form['dob'],request.form['pwd'],request.form['contactno'],request.form['address'],request.form['state'],request.form['city']]
            mycursor.execute(sql,val)
            conn.commit()
            return render_template('patientlogin.html',m='')
        else:
            msg="\""+request.form['emailid']+"\""+" already exists!"
            return render_template('patientlogin.html',m=msg)
    else:
        sql='insert into patient_details (fullname,emailid,gender,dob,pwd,contactno,address,state,city) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        val=[request.form['fullname'],request.form['emailid'],request.form['gender'],request.form['dob'],request.form['pwd'],request.form['contactno'],request.form['address'],request.form['state'],request.form['city']]
        mycursor.execute(sql,val)
        conn.commit()
        return render_template('patientdashboard.html')


@app.route("/patient_login",methods=["POST","GET"])
def login():
    
    if request.method == "GET":
        return render_template("patientlogin.html",msg='')
    else:
        sql = "select * from patient_details where emailid=%s and binary pwd=%s"
        val = [request.form['emailid'],request.form['pwd']]   
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        conn.commit()
        if len(myresult)==1:
            session['loggedUser']=request.form['emailid']
            return render_template("patientdashboard.html")
        else:
            return render_template("patientlogin.html",msg="Incorrect credentials")

@app.route('/patient_profile_view')
def patient_profile_view():
    sql='select * from patient_details where emailid=%s'
    val=[session['loggedUser']]
    mycursor.execute(sql,val)
    data=mycursor.fetchone()
    print(data)
    return render_template('patient_profile_view.html',pdata=data)

@app.route('/patient_profile')
def patient_profile():
    sql='select * from patient_details where emailid=%s'
    val=[session['loggedUser']]
    mycursor.execute(sql,val)
    data=mycursor.fetchone()
    print(data)
    return render_template('patient_profile.html',pdata=data)
    
@app.route('/update_profile',methods=['POST'])
def update_profile():
    try:
        sql='update patient_details set fullname=%s,gender=%s,dob=%s,contactno=%s,address=%s,state=%s,city=%s where emailid=%s'
        print("heyyy")
        val=[request.form['name'],request.form['gender'],request.form['dob'],request.form['contactno'],request.form['address'],request.form['state'],request.form['city'],session['loggedUser']]
        print("heyyy2")
        mycursor.execute(sql,val)
        conn.commit()
        print("heyy3")
        return render_template('patientdashboard.html',msg="Updated successfully")
    except Exception as e:
        print(e)
        return render_template('patientdashboard.html',msg="error")

@app.route('/change_pass',methods=['GET','POST'])
def change_pass():
    if request.method == "GET":
        return render_template("change_pass.html")
    else: 
        sql='select * from patient_details where emailid=%s and pwd=%s'
        val=[session['loggedUser'],request.form['opwd']]
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        conn.commit()

        if len(myresult)==1:
            sql1='update patient_details set pwd=%s where emailid=%s'
            val1=[request.form['ptxt'],session['loggedUser']]
            mycursor.execute(sql1,val1)
            conn.commit()
            return render_template("patientdashboard.html",msg="Changed password successfully")
        else:
            return render_template("patientdashboard.html",msg="Old password is incorrect")

@app.route('/redirect')
def topatient():
    return render_template('patientdashboard.html')

@app.route('/book_1')
def book1():
    sql='select sname from specialization'
    mycursor.execute(sql)
    spl=mycursor.fetchall()
    return render_template('book_appointment1.html',specials=spl)

@app.route('/book_2',methods=['POST'])
def book2():
    sql='select sid from specialization where sname=%s'
    val=[request.form['special']]
    mycursor.execute(sql,val)
    sid=mycursor.fetchone()
    print("hey 3",sid)
    sql1='select doctorID from d_s_mapping where sid=%s'
    val1=[sid[0]]
    mycursor.execute(sql1,val1)
    did=mycursor.fetchall()
    d=[]
    for i in did:
        d.append(i)
    names=[]
    print(d[1][0])
    for i in d:
        sql3='select fullname from doctor_details where doctorID = %s'
        mycursor.execute(sql3,i)
        fetchnames=mycursor.fetchone()
        names.append(fetchnames[0])
    return render_template('book_1.html',spl=request.form['special'], namelist=names)

@app.route('/book_3',methods=['POST'])
def book_3():
    sql1='select doctorID from doctor_details where fullname=%s'
    val1=[request.form['doctors']]
    mycursor.execute(sql1,val1)
    did=mycursor.fetchone()[0]
    session['doctorid']=did
    session['reason']=request.form['reason']
    session['date']=request.form['date']
    sql2='select a_time from appointments where doctorID=%s and a_date=%s'
    val2=[did,request.form['date']]
    mycursor.execute(sql2,val2)
    times=mycursor.fetchall()
    print(times)
    l=['9:30','10:00','10:30','11:00','11:30','12:00','12:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
    for i in times:
        if i[0] in l:
            l.remove(i[0])
    print(l)
    return render_template('book_3.html',time=l)

@app.route('/booking',methods=['POST'])
def book3():
    # sql1='select doctorID from doctor_details where emailid=%s'
    # val1=[request.form['doctors']]
    # mycursor.execute(sql1,val1)
    print("heyy")
    # doctorid=mycursor.fetchone()[0]
    sql2='select patientID from patient_details where emailid=%s'
    val2=[session['loggedUser']]
    mycursor.execute(sql2,val2)
    patientid=mycursor.fetchone()[0]
    sql3='insert into appointments(patientID,doctorID,a_date,a_time,reason) values(%s,%s,%s,%s,%s)'
    val3=[patientid,session['doctorid'],session['date'],request.form['times'],session['reason']]
    mycursor.execute(sql3,val3)
    print("heyy 2")
    conn.commit()
    return render_template('patientdashboard.html',msg="Booked successfully")


@app.route('/appointment_history')
def history():
    sql1='select patientID from patient_details where emailid=%s'
    val1=[session['loggedUser']]
    mycursor.execute(sql1,val1)
    patientid=mycursor.fetchone()[0]
    sql2='select * from appointments where patientID = %s'
    val2=[patientid]
    mycursor.execute(sql2,val2)
    listapp=mycursor.fetchall()
    j=0
    for i in listapp:
        listapp[j]=list(i)
        j+=1
    j=0
    for i in listapp:
        sql1='select fullname from doctor_details where doctorID = %s'
        val1=[i[2]]
        mycursor.execute(sql1,val1)
        doctorname=mycursor.fetchone()[0]
        listapp[j][2]=doctorname
        j+=1
    return render_template("book_history.html",listapps=listapp)

@app.route("/admin_logout")
def logout():
    session['logged_in'] = False
    return enter()

@app.route("/doctor_logout")
def doc_logout():
    session['logged_in'] = False
    print(session['sessionID'])
    mycursor.execute('update doctor_session set logout_time=current_timestamp() where sessionID=%s',[session['sessionID']] )
    conn.commit()
    return enter()

@app.route("/patient_logout")
def patient_logout():
    session['logged_in'] = False
    return enter()

@app.route("/doctor_appoint")
def doctor_appoint():
    try:
        sql1='select doctorID from doctor_details where emailid=%s'
        val1=[session['loggedUser']]
        mycursor.execute(sql1,val1)
        print("heyy")
        did=mycursor.fetchone()[0]
        sql='select * from appointments where doctorID=%s and astatus not in ("disapproved","visited")'
        val=[did]
        mycursor.execute(sql,val)
        print("heyyy 2")
        appoints=mycursor.fetchall()
        print(appoints)
        l=[]
        j=0
        act={'pending':'approve','approve':'visited'}
        for i in appoints:
            sql2='select fullname from patient_details where patientID=%s'
            val2=[i[1]]
            mycursor.execute(sql2,val2)
            pname=mycursor.fetchone()[0]
            l.append(pname)
            j+=1
        print("heyy 3")
        return render_template('dis_doctor_appoint.html',appoints=appoints,pname=l,j=j,acts=act)
    except Exception as e:
        print(e)
        return render_template('dis_doctor_noappoint.html',msg="NO APPOINTMENTS")
@app.route('/change_status',methods=['POST'])
def change_status():
    print(request.form['aid'])
    sql='select astatus from appointments where aid=%s'
    val=[request.form['aid']]
    mycursor.execute(sql,val)
    status=mycursor.fetchone()[0]
    if status=='pending':
        sql1='update appointments set astatus="approve" where aid=%s'
        val1=[request.form['aid']]
        mycursor.execute(sql1,val1)
        conn.commit()
    elif status=='approve':
        sql1='update appointments set astatus="visited" where aid=%s'
        val1=[request.form['aid']]
        mycursor.execute(sql1,val1)
        conn.commit()
    else:
        pass
    return redirect(url_for('doctor_appoint'))

@app.route('/delete_appoint',methods=['POST'])
def del_appoint():
    print(request.form['aid'])
    sql1='update appointments set astatus="disapproved" where aid=%s'
    val1=[request.form['aid']]
    mycursor.execute(sql1,val1)
    conn.commit()
    return redirect(url_for('doctor_appoint'))

@app.route('/contact_us',methods=['POST'])
def contact_us():
    sql='insert into contactus(fullname,emailid,message) values(%s,%s,%s)'
    val=[request.form['name'],request.form['email'],request.form['message']]
    mycursor.execute(sql,val)
    conn.commit()
    return render_template('welcome.html')

@app.route('/user_com')
def user_com():
    sql='select * from contactus'
    mycursor.execute(sql)
    contact=mycursor.fetchall()
    print(contact)
    return render_template('user_comments.html',dis=contact)
@app.route('/search_option',methods=['POST'])
def search_option():
    sql1='select doctorID from doctor_details where emailid=%s'
    val1=[session['loggedUser']]
    mycursor.execute(sql1,val1)
    print("heyy")
    did=mycursor.fetchone()[0]
    if(request.form['opt']=='active'):
        return redirect(url_for('doctor_appoint'))
    sql='select * from appointments where astatus=%s and doctorID=%s'
    val=[request.form['opt'],did]
    mycursor.execute(sql,val)
    appoints=mycursor.fetchall()
    print(appoints)
    l=[]
    j=0
    act={'pending':'approve','approve':'visited'}

    for i in appoints:
        sql2='select fullname from patient_details where patientID=%s'
        val2=[i[1]]
        mycursor.execute(sql2,val2)
        pname=mycursor.fetchone()[0]
        l.append(pname)
        print("heyy 3")
        j+=1
    if j==0:
        m='No ' + request.form['opt']+' appointments'
        return render_template('dis_doctor_noappoint.html',msg=m)
    return render_template('dis_doctor_appoint.html',appoints=appoints,pname=l,acts=act,j=j)
    
    # return render_template('dis_doctor_noappoint.html',msg="NO APPOINTMENTS")
    # return render_template('search_option.html')
@app.route('/view_chart')
def view_chart():
    
    return render_template('view_chart.html')
app.run()