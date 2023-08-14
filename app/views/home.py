from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User, Cart, color_management

@app.route("/", methods = ['GET','POST'])
def home():
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('home.html',user=current_user, count = count)

@app.route("/color_edit/<id>", methods = ['GET', 'POST'])
def color_edit(id):
    color = color_management.query.get(id)
    colors = color_management.query.all()
    if request.method == "POST":
        color_class = request.form.get('color_class')
        in_color = request.form.get('color')

        color.class_name = color_class
        color.color = in_color

        db.session.commit()
        return redirect("/edit_color")

    return render_template("edit_colors.html", user = current_user, update = True, color = color, colors = colors)


@app.route("/edit_color", methods = ['GET', 'POST'])
def edit_color():

    if request.method == "POST":
        color_class = request.form.get('color_class')
        color = request.form.get('color')

        add_color = color_management(
            class_name = color_class,
            color = color
        )

        db.session.add(add_color)
        db.session.commit()
    
    colors = color_management.query.all()
    return render_template("edit_colors.html", user = current_user, colors = colors)