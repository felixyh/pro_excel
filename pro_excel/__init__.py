from flask import Flask, render_template, request, url_for, redirect, flash

from .views.login_bp import login_bp

# from .config import Config


def create_app():

    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')


    app.register_blueprint(login_bp)
    

    return app