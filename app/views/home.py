from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User, Cart

@app.route("/", methods = ['GET','POST'])
def home():
    try:
        count = Cart.query.filter_by(uid=current_user.id).count()
    except:
        count = 0
    return render_template('home.html',user=current_user, count = count)
