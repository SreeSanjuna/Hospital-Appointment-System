
from msvcrt import LK_LOCK
from flask import *
app=Flask(__name__)

@app.route('/')
def hey():
    l=[(1,'qwe'),(2,'ert'),(3,'qgdf'),(4,'mko'),(5,'lop')]
    return render_template('checkboxes.html',data=l)

@app.route('/um',methods=['POST'])
def hi():
    print('Entered')
    print(request.form.getlist('myval'))
    return render_template('cb1.html')



app.run()
