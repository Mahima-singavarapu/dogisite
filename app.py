from flask import Flask,render_template,request,url_for,flash,redirect,session
from flask_session import Session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mahima@codegnan'
mydb = mysql.connector.connect(host='localhost',user='root',password='Admin',db='forfa')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phno = request.form['phoneNo']
        password= request.form['password']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('insert into register(user_name,email,phno,password) values(%s,%s,%s,%s)',[username,email,phno,password])
        mydb.commit()
        cursor.close()
        flash("You've successfully registered")
        return redirect(url_for('login'))
    else:
        return render_template('registration.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        email = request.form['email']
        password= request.form['password']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where email=%s',[email])
        count = cursor.fetchone()[0]
        if count == 0:
            flash('Sorry email is not registered, Please register')
            return redirect(url_for('register'))
        else:
            cursor.execute('select email,password from register where email=%s',[email])
            data = cursor.fetchone()
            email_sql = data[0]
            password_sql = data[1]
            cursor.close()
            if password == password_sql:
                session['user'] = email
                if not session.get('user'):
                    session[user] = {}
                flash('Login successful')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password')
                return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('success.html')
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    return redirect(url_for('login'))


app.run(debug=True, use_reloader=True)