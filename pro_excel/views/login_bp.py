from flask import Blueprint
from flask import render_template, request, url_for, redirect, flash
from flask_session import Session

from functools import wraps

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

login_bp = Blueprint('login', __name__)


def auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'username' in session:
            logsuccessmsg =  f'Logged in as {session["username"]}'
            return func(*args, **kwargs)
        flash('You are not logged in')
        return redirect(url_for('login'))
    return inner

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    account = request.form['account']
    password = request.form['password']

    if account == 'felix' and password == 'novirus':
        session['username'] = request.form.get('user')
        return redirect('/index')
    flash('Accout name or password is wrong, please try again!')
    return render_template('login.html')

@login_bp.route('/logout')
@auth
def logout():
    # remove the suername from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))