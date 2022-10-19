from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    @app.route('/index')
    def index():
        return 'hello, I am Flask running on code-server!'

    return app