from app import db, login_manager
from flask_login import UserMixin
from .product import Cart
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Cart', backref='buyer')
    duration = db.Column(db.Integer, default=0)
    image = db.Column(db.String(256), default='actor.png')
    banner = db.Column(db.String(256), default='white.png')
    applications = db.relationship('JobApplication', backref='user', lazy=True)
    status = db.Column(db.String(10), default='offline')
    last_seen = db.Column(db.DateTime)
    socket_id = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.now())
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    jobs_page_visible = db.Column(db.Boolean, default=True)


class LeaderboardList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    rank = db.Column(db.Integer, default=0)
    
