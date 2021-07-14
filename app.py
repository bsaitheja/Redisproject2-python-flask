from flask import Flask, render_template, request
import sqlite3
import textwrap
import pyodbc
import time
import os
import redis
import hashlib
import pickle

app = Flask(__name__)


driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'assign1server'
database_name = 'assignment1'
server = 'tcp:database.windows.net,1433'
username = "saitheja"
password = "9705004946S@i"

r = redis.Redis(host='saitheja.redis.cache.windows.net',
                port=6380, db=0, password='UIO8izHCadRdL+fe6T5L04jCo+0JUMua4N0QIX2wbAw=',ssl=True)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/q5')
def q5():
   return render_template('q5.html')

@app.route('/q5b')
def q5b():
   return render_template('q5b.html')

@app.route('/q6')
def q6():
   return render_template('q6.html')


@app.route('/q8')
def q8():
   return render_template('q8.html')

@app.route('/q7')
def q7():
   return render_template('q7.html')

@app.route('/q7b')
def q7b():
   return render_template('q7b.html')


@app.route('/q8b')
def q8b():
   return render_template('q8b.html')

@app.route('/q6b')
def q6b():
   return render_template('q6b.html')

@app.route('/all', methods=['POST','GET'])
def fulllist():

    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select  state,year,votes,party from presidentialvotes "
    t1=time.time()
    crsr.execute(querry)
    rows=crsr.fetchall()
    t2=time.time()
    total=t2-t1
    cnxx.close()
    return render_template("list.html",rows = rows,time=total)

@app.route('/p5', methods=['POST','GET'])
def p5():
    y1=request.form['y1']
    y2=request.form['y2']
    v1=request.form['v1']
    v2=request.form['v2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' and votes between '"+v1+"' and '"+v2+"'"
    t1=time.time()
    crsr.execute(querry)
    rows=crsr.fetchall()
    t2=time.time()
    total=t2-t1
    cnxx.close()
    return render_template("list.html",rows = rows,time=total)

@app.route('/p5b', methods=['POST','GET'])
def p5b():
    y1=request.form['y1']
    y2=request.form['y2']
    v1=request.form['v1']
    v2=request.form['v2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select top(2) state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' and votes between '"+v1+"' and '"+v2+"' ORDER BY VOTES ASC"
    querry1="Select top(2) state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' and votes between '"+v1+"' and '"+v2+"' ORDER BY VOTES DESC"
    t1=time.time()
    crsr.execute(querry)
    rows=crsr.fetchall()
    crsr.execute(querry1)
    rows1=crsr.fetchall()
    t2=time.time()
    total=t2-t1
    cnxx.close()
    return render_template("newrecord.html",rows = rows,rows1=rows1,time=total)

@app.route('/p6', methods=['POST','GET'])
def p6():
    y1=request.form['y1']
    y2=request.form['y2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select party,state,SUM(votes) from presidentialvotes where year between '"+y1+"' and '"+y2+"' GROUP BY party,state"
    t1=time.time()
    crsr.execute(querry)
    rows=crsr.fetchall()
    t2=time.time()
    total=t2-t1
    cnxx.close()
    return render_template("o6.html",rows = rows,time=total)


@app.route('/p6b', methods=['POST','GET'])
def p6b():
    y1=request.form['y1']
    y2=request.form['y2']
    n=request.form['n']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select top ("+n+") party,state,SUM(votes),RAND() from presidentialvotes where year between '"+y1+"' and '"+y2+"' GROUP BY RAND(),party,state"
    t1=time.time()
    crsr.execute(querry)
    rows=crsr.fetchall()
    t2=time.time()
    total=t2-t1
    cnxx.close()
    return render_template("o6.html",rows = rows,time=total)



@app.route('/p7', methods=['POST','GET'])
def p7():
    
    y1=request.form['y1']
    y2=request.form['y2']
    v1=request.form['v1']
    v2=request.form['v2']
    n=int(request.form['n'])
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' and votes between '"+v1+"' and '"+v2+"'"
    hash = hashlib.sha224(querry.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,n):
        if(r.get(key)):
            pass
        else:
            crsr.execute(querry)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("l2.html",rows=data,n=n,time = total)

@app.route('/p7b', methods=['POST','GET'])
def p7b():
    
    y1=request.form['y1']
    y2=request.form['y2']
    n=int(request.form['n'])
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' "
    hash = hashlib.sha224(querry.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,n):
        if(r.get(key)):
            pass
        else:
            crsr.execute(querry)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("l2.html",rows=data,n=n,time = total)

@app.route('/p8', methods=['POST','GET'])
def p8():
    
    y1=request.form['y1']
    y2=request.form['y2']
    v1=request.form['v1']
    v2=request.form['v2']
    n=int(request.form['n'])
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' and votes between '"+v1+"' and '"+v2+"'"
    hash = hashlib.sha224(querry.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,n):
            crsr.execute(querry)
            data = crsr.fetchall()
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("l2.html",rows=data,n=n,time = total)

@app.route('/p8b', methods=['POST','GET'])
def p8b():
    
    y1=request.form['y1']
    y2=request.form['y2']
    n=int(request.form['n'])
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select state,year,votes,party from presidentialvotes where year between '"+y1+"' and '"+y2+"' "
    hash = hashlib.sha224(querry.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,n):
            crsr.execute(querry)
            data = crsr.fetchall()
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("l2.html",rows=data,n=n,time = total)





if __name__ == '__main__':
    app.debug=True
    app.run()
    