from app import app, db
from flask import render_template, request,redirect,url_for,flash
from ..models.user import User
from werkzeug.security import generate_password_hash
import uuid

@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already registered", category="error")
        else:

            if email == "mmalallh22@gmail.com":
                new_user = User(username=username, email=email, password=password, is_active=True, is_admin=True)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created", category="success")
                return redirect(url_for("login"))
            else:
                new_user = User(username=username, email=email, password=password,is_active=True)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created", category="success")
                return redirect(url_for("login"))
    return render_template('register.html')
