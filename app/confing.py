import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "asdsdasdasdasdasdaas" #os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://GWYGL:KingofKuwait22@GWYGL.mysql.pythonanywhere-services.com/GWYGL$shopdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

