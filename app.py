from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "test"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/table')
def table():
    if 'user' in session:
        return render_template('table.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form['email']
        session['user'] = user
        return redirect(url_for('index'))
    else:
        if 'user' in session:
            flash('Already Signed In!')
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        #Check it post data is valid
        flash('Account Created!')
        return redirect(url_for('login'))
    else:
        if 'user' in session:
            flash('Already Signed In!')
            return redirect(url_for('index'))
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully Logged Out!')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        user = request.form['email']
        flash('Password Reset Link Sent!')
        return redirect(url_for('login'))
    else:
        return render_template('forgot-password.html')

if __name__ == '__main__':
    app.run(debug=True)
