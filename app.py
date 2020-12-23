from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

#----------------Database------------------
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

#------------------------------------------



@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile', methods=["POST", "GET"])
def profile():
    username = None
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            session['email'] = email
            session['first_name'] = first_name
            session['last_name'] = last_name

            flash('User Settings was Updated!')
        else:
            if "username" in session:
                username = session['username']
        return render_template('profile.html', email=email, username=username) #payload probably better here. To load data when a get is called
    else:
        return redirect(url_for('login'))

@app.route('/table')
def table():
    if 'email' in session:
        return render_template('table.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        session['email'] = email
        return redirect(url_for('index'))
    else:
        if 'email' in session:
            flash('Already Signed In!')
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        found_user = users.query.filter_by(email=email).first()
        if found_user:
            session[]
        else:
            usr = users(first_name, last_name, email)
            db.session.add(usr)
            db.session.commit()
        flash('Account Created!')
        return redirect(url_for('login'))
    else:
        if 'email' in session:
            flash('Already Signed In!')
            return redirect(url_for('index'))
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Successfully Logged Out!')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        email = request.form['email']
        flash('Password Reset Link Sent!')
        return redirect(url_for('login'))
    else:
        return render_template('forgot-password.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
