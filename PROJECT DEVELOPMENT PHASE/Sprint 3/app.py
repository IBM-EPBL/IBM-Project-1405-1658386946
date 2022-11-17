from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import random
from flask_mail import Mail, Message
import re
app=Flask(__name__)
app.secret_key = 'a'
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cad.customercareregistry@gmail.com'
app.config['MAIL_PASSWORD'] = 'kgcrmixpshgelork'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yfk83812;PWD=9sBGOJmQe079M30M",' ',' ')

@app.route('/')
def home():
        return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    msg=' '
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM USERS WHERE username = ? AND password = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        sqlone = "SELECT UESRTYPE FROM USERS WHERE USERNAME = "+"'"+username+"'"
        stmtone = ibm_db.exec_immediate(conn, sqlone)
        while ibm_db.fetch_row(stmtone) != False:
                usertype=ibm_db.result(stmtone, "UESRTYPE")
        if account:
            if(usertype=="admin"):
                 return render_template('admindashboard.html')
            else:
                 return render_template('dashboard.html')
        else:
            return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
        if request.method=='POST':
            fullname = request.form['fullname']
            username = request.form['username']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            password = request.form['password']
            usertype="user"
            queryone = "SELECT * FROM USERS WHERE username = ? "
            stmtone = ibm_db.prepare(conn,queryone)
            ibm_db.bind_param(stmtone,1,username)
            ibm_db.execute(stmtone)
            userexist = ibm_db.fetch_assoc(stmtone)
            querytwo = "SELECT * FROM USERS WHERE email = ? "
            stmtwo = ibm_db.prepare(conn,querytwo)
            ibm_db.bind_param(stmtwo,1,email)
            ibm_db.execute(stmtwo)
            emailexist = ibm_db.fetch_assoc(stmtwo)
            if emailexist:
                return render_template('signup.html')
            if userexist:
                return render_template('signup.html')
            else:
                insert_sql="INSERT INTO USERS VALUES(?, ?, ?, ?,?,?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,fullname)
                ibm_db.bind_param(prep_stmt,2,username)
                ibm_db.bind_param(prep_stmt,3,email)
                ibm_db.bind_param(prep_stmt,4,phonenumber)
                ibm_db.bind_param(prep_stmt,5,password)
                ibm_db.bind_param(prep_stmt,6,usertype)
                ibm_db.execute(prep_stmt)
                msg = Message('CAD-CustomerCareRegistry Account Created Successfully',sender ='cad.customercareregistry@gmail.com',recipients = [email])
                msg.body = ("Welcome to CAD-CustomerCareRegistry, your account was successfully registered with us."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n\n"+"With regard,"+"\n"+"CAD-CustomerCareRegistry")
                mail.send(msg)
                return render_template('login.html')

@app.route('/raiseticket',methods=['GET','POST'])
def raiseticket():
        if request.method=='POST':
                randomnum= (random.random())
                randomone = int(randomnum*1000000000)
                ticketid = ("CCR"+str(randomone))
                username=request.form['username']
                sql = "SELECT * FROM USERS WHERE USERNAME = "+"'"+username+"'"
                stmt = ibm_db.exec_immediate(conn, sql)
                while ibm_db.fetch_row(stmt) != False:
                    emailid=ibm_db.result(stmt, "EMAIL")                
                kequery = request.form['kequery']
                dequery = request.form['dequery']
                adminreply="to be updated"
                insert_sql="INSERT INTO TICKET VALUES(?, ?, ?, ?,?,?)"
                prep_stmt1=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt1,1,ticketid)
                ibm_db.bind_param(prep_stmt1,2,username)
                ibm_db.bind_param(prep_stmt1,3,emailid)
                ibm_db.bind_param(prep_stmt1,4,kequery)
                ibm_db.bind_param(prep_stmt1,5,dequery)
                ibm_db.bind_param(prep_stmt1,6,adminreply)
                ibm_db.execute(prep_stmt1)
                #msg = Message('CAD-CustomerCareRegistry Account Created Successfully',sender ='cad.customercareregistry@gmail.com',recipients = [email])
                #msg.body = ("Welcome to CAD-CustomerCareRegistry, your account was successfully registered with us."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n\n"+"With regard,"+"\n"+"CAD-CustomerCareRegistry")
                #mail.send(msg)
                return render_template('checkstatus.html')

@app.route('/status',methods=['GET','POST'])
def status():
        if request.method=='POST':
                ticketid=request.form['ticketid']
                sql = "SELECT * FROM TICKET WHERE TICKETID = "+"'"+ticketid+"'"
                stmt = ibm_db.exec_immediate(conn, sql)
                while ibm_db.fetch_row(stmt) != False:
                    username=ibm_db.result(stmt, "USERNAME")
                    emailid=ibm_db.result(stmt, "EMAILID")                
                    kequery=ibm_db.result(stmt, "KEQUERY")
                    dequery=ibm_db.result(stmt, "DEQUERY")
                    adminreply=ibm_db.result(stmt, "ADMINREPLY")
                #msg = Message('CAD-CustomerCareRegistry Account Created Successfully',sender ='cad.customercareregistry@gmail.com',recipients = [email])
                #msg.body = ("Welcome to CAD-CustomerCareRegistry, your account was successfully registered with us."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n\n"+"With regard,"+"\n"+"CAD-CustomerCareRegistry")
                #mail.send(msg)
                return render_template('status.html',tracking_id=trackingid,user_name=username,email_id=emailid,key_complaint=kequery,detailed_complaint=dequery,admin_reply=adminreply)

@app.route('/ticketreply',methods=['GET','POST'])
def ticketreply():
        if request.method=='POST':
                adminreply=request.form['adminreply']
                insert_sql="UPDATE TICKET SET ADMINREPLY=? WHERE TICKETID=?"
                prep_stmt1=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt1,1,adminreply)
                ibm_db.bind_param(prep_stmt1,2,ticketid)
                ibm_db.execute(prep_stmt1)
                #msg = Message('CAD-CustomerCareRegistry Account Created Successfully',sender ='cad.customercareregistry@gmail.com',recipients = [email])
                #msg.body = ("Welcome to CAD-CustomerCareRegistry, your account was successfully registered with us."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n\n"+"With regard,"+"\n"+"CAD-CustomerCareRegistry")
                #mail.send(msg)
                return render_template('admindashboard.html',tracking_id=trackingid,user_name=username,email_id=emailid,key_complaint=kequery,detailed_complaint=dequery,admin_reply=adminreply)
                
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/replyadmin')
def replyadmin():
        #return render_template('adminreply.html')
        if request.method=='POST':
                ticketid="123"
        return ticketid


@app.route('/ticket')
def ticket():
    return render_template('ticket.html')

@app.route('/checkstatus')
def checkstatus():
    return render_template('checkstatus.html')
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True, threaded=True)
