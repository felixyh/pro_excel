import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '_5#y2L"F4Q8z\n\xec]/'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'book.sqlite')
    UPLOAD_FOLDER = os.path.join(basedir, 'upload/')
