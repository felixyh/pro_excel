from flask import Flask, render_template

from .views.bp_test import bp_test

from .config import Config


def create_app():
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/login', )
    def login():
        return render_template('login.html')

    app.register_blueprint(bp_test, url_prefix='/usr')
    

    return app