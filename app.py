from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user


app = Flask(__name__)
app.secret_key = "test" #Change Secret key to something complex maybe look up!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return users.query.filter_by(user_id=user_id).first()


#----------------Database------------------
db = SQLAlchemy(app)

class users(UserMixin, db.Model):
    user_id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

#------------------------------------------

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash('Already Signed In!', 'alert alert-warning alert-dismissible fade show')
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            session.permanent = True
            email = request.form['email']
            password = request.form['password']
            remember = True if request.form.get('remember') else False
            print(remember)

            found_user = users.query.filter_by(email=email).first()

            if not found_user or not check_password_hash(found_user.password, password):
                flash('Incorrect Username or Password.', 'alert alert-danger alert-dismissible fade show')
                return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

                # if the above check passes, then we know the user has the right credentials

            session['email'] = email
            login_user(found_user, remember=remember)
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        flash('Already Signed In!', 'alert alert-warning alert-dismissible fade show')
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['password']

            found_user = users.query.filter_by(email=email).first()
            if found_user:
                flash('Email Already in Use. Sign In.', 'alert alert-danger alert-dismissible fade show')
                return redirect(url_for('login'))
            else:
                usr = users(first_name, last_name, email, password=generate_password_hash(password, method='sha256'))
                db.session.add(usr)
                db.session.commit()
                flash('Account Created!', 'alert alert-primary alert-dismissible fade show')
            return redirect(url_for('login'))
        else:
            return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    logout_user()
    flash('Successfully Logged Out!', 'alert alert-primary alert-dismissible fade show')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')#, first_name=current_user.first_name)


@app.route('/profile', methods=["POST", "GET"]) #Load from database
@login_required
def profile():
    email = current_user.email
    first_name = current_user.first_name
    last_name = current_user.last_name

    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        found_user = users.query.filter_by(email=email).first()
        if found_user is not None and found_user.email != current_user.email:
            flash(u'Email Already in Use.', 'alert alert-danger alert-dismissible fade show')
        else:
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            db.session.commit()
            flash(u'User Settings was Updated!', 'alert alert-primary alert-dismissible fade show')


    #Load from database into session. Use session instead of db wherever u can Sanjay.
    return render_template('profile.html', email=email, first_name=first_name, last_name=last_name) #payload probably better here. To load data when a get is called

@app.route('/table')
@login_required
def table():
    return render_template('table.html')

@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password():
    #NEED PASSWORD RESETTER
    if request.method == "POST":
        email = request.form['email']
        flash('Password Reset Link Sent!', 'alert alert-primary alert-dismissible fade show')
        return redirect(url_for('login'))
    else:
        return render_template('forgot-password.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
