import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "asdsdasdasdasdasdaas" #os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True



