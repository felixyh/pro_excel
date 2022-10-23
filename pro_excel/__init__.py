from flask import Flask, render_template, request, url_for, redirect, flash, session
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.utils import secure_filename
import os
import xlrd
from flask_bootstrap import Bootstrap

## create db

db = SQLAlchemy()

class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    price = db.Column(db.String(10))

    def __init__(self, name, author, price):
        self.name = name
        self.author = author
        self.price = price

### create app

def create_app():

    app = Flask(__name__)

    Bootstrap(app)

    def auth(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if 'username' in session:
                logsuccessmsg =  f'Logged in as {session["username"]}'
                return func(*args, **kwargs)
            flash('You are not logged in')
            return redirect(url_for('login'))
        return inner

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        account = request.form['account']
        password = request.form['password']

        if account == 'felix' and password == 'novirus':
            session['username'] = request.form.get('account')
            return redirect('/index')
        flash('Accout name or password is wrong, please try again!')
        return render_template('login.html')

    @app.route('/logout')
    @auth
    def logout():
        # remove the suername from the session if it's there
        session.pop('username', None)
        return redirect(url_for('index'))

    @app.route('/')
    @app.route('/index')
    @auth
    def index():
        return render_template('index.html', account_name=session['username'], books = Books.query.all())

    # 增加
    @app.route('/new_book', methods = ['GET', 'POST'])
    @auth
    def new_book():
        if request.method == 'POST':
            if not request.form['name'] or not request.form['author'] or not request.form['price']:
                flash('Please enter all the fields', 'error')
            else:
                book = Books(request.form['name'], request.form['author'],
                    request.form['price'])
                
                db.session.add(book)
                db.session.commit()
                flash('Record was successfully added')
                return redirect(url_for('index'))
        return render_template('new_book.html')


    # @app.route('/delete')
    # @auth
    # def delete():
    #     bname = request.args['name']
    #     book = Books.query.filter_by(name=bname).first_or_404()
    #     db.session.delete(book)
    #     db.session.commit()
    #     return redirect('/index')

    # 删除
    @app.route('/delete/<int:id>')
    @auth
    def delete(id):
        book = Books.query.filter_by(id=id).first_or_404()
        db.session.delete(book)
        db.session.commit()
        return redirect('/index')

    # 修改
    @app.route('/modify', methods=['GET', 'POST'])
    @auth
    def modify():
        id = request.args['id']
        book = Books.query.filter_by(id=int(id)).first_or_404()
        if request.method == 'POST':
            book.author = request.form['author']
            book.price = request.form['price']
            db.session.commit()
            return redirect(url_for('index'))
        name = book.name
        author = book.author
        price = book.price
        return render_template('modify.html', name=name, author=author, price=price)

    # 查询
    @app.route('/search', methods=['GET', 'POST'])
    @auth
    def search():
        name = request.form['name']
        return render_template('search.html', name=name, books=Books.query.filter_by(name=name).all())
        
        
    @app.route('/upload_excel', methods = ['GET', 'POST'])
    @auth
    def upload_excel():
        if request.method == 'POST':
            f = request.files['file']
            print(request.files)
            f_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(f_path)

            # read excel file with xlrd module
            wb = xlrd.open_workbook(f_path)
            ws = wb.sheets()[0]

            for row_number in range(ws.nrows):
                row_values = ws.row_values(row_number)
                book = Books(row_values[0], row_values[1], row_values[2])
                db.session.add(book)
            db.session.commit()
            flash('excel data imported into database successfully!')

            # remove the uploaded excel file
            os.remove(f_path)

            return redirect(url_for('index'))

        return render_template('upload_excel.html')

    @app.route('/testbootstrap/<name>')
    def testbootstrap(name):
        return render_template('test_bootstrap.html', name=name)
    
    return app

