from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re    # re is used for validating the email and username 

import pymysql

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

#### Connect database using pymysql using this string
conn = pymysql.connect(
    'localhost',
    'root',
    'Shivam123',
    'pythonlogin'
)

#### Enter your MySQLdb database connection details below
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Shivam123'
# app.config['MYSQL_DB'] = 'pythonlogin'

### Intialize MySQL
# mysql = MySQL(app)

@app.route('/pythonlogin', methods = ['GET', 'POST'])
def login():
    msg = ''

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor(pymysql.cursors.DictCursor)  ### DictCursor is used for fetch data from database in the form of dict instead of tuple

        #### Connect database using MySQLdb using this string
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))

        # Fetch one record and return result
        account = cursor.fetchone()
        # print(account)
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            ## return to homepage
            return redirect(url_for('home'))
        else:
            msg = "Incorrect useranme/password!"

    return render_template('index.html', msg = msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods = ['GET', 'POST'])
def register():
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        ### create cursor using MySQLdb/pymysql 
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = conn.cursor(pymysql.cursors.DictCursor) 
        cursor.execute("SELECT * FROM accounts WHERE username= %s", (username,))
        account = cursor.fetchone()
        
        ## IF Account exists show error
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()

            msg = 'You have successfully registered!'


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"

    return render_template('register.html', msg = msg)

@app.route('/pythonlogin/home')
def home():
    ## check if user is loggedin
    if 'loggedin' in session:
        
        return render_template('home.html', username = session['username'])

    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    ## check if user is loggedin
    if 'loggedin' in session:
        ### create cursor using MySQLdb/pymysql 
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = conn.cursor(pymysql.cursors.DictCursor) 
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account = account)
        
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True)