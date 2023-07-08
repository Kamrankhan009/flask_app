from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User

@app.route("/", methods = ['GET','POST'])
def home():
    return render_template('home.html',user=current_user)
