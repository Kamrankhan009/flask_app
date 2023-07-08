from flask import Flask
from .confing import Config, basedir
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import send_from_directory
import stripe

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = f"{basedir}/uploads"
migrate = Migrate(app,db,compare_type=True)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
stripe.api_key = "sk_test_51NP8SlAG1w1CkJgYFgkbdMIxkodAty9Q1ZgGQWQ4KU5fwJmb3Y8SpUZZzxWRt5YTOoKOPk3QEhslbqbToguYMHVI00Gpd7r6T1"

@app.route('/uploads/users/<filename>')
def uploaded_users_images(filename):
    return send_from_directory('uploads/users', filename)

@app.route('/uploads/product/<filename>')
def uploaded_product_images(filename):
    return send_from_directory('uploads/products', filename)

@app.route('/uploads/resumes/<filename>')
def uploaded_resumes(filename):
    return send_from_directory('uploads/resumes', filename)

from .views import *
from .models import *
