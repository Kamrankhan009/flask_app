from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User, Cart, color_management, speed_management, text_management, ball_management

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

    balls = ball_management.query.filter_by(class_name = "Home").first()
    speed = speed_management.query.filter_by(page_name="Home_page_text").first()
    text = text_management.query.filter_by(page_name = "Home_page_text").first()
    englishtext = "`" + text.English_text + "`"
    arabictext = "`" + text.Arabic_text + "`"
    color1 = color_management.query.filter_by(class_name = "Home_background_ball").first()
    speed_of_ball = speed_management.query.filter_by(page_name= "Home_ball_speed").first()
    return render_template('home.html',user=current_user, count = count,
                           speed = speed.speed,
                           balls = int(balls.number), 
                           arabictext=arabictext,
                           englishtext=englishtext, 
                           color1=color1,
                           ball_speed = speed_of_ball.speed)

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


@app.route("/speed_edit/<id>", methods = ['GET', 'POST'])
def speed_edit(id):
    speed = speed_management.query.get(id)
    speeds = speed_management.query.all()
    if request.method == "POST":
        speed_class = request.form.get('speed_class')
        speed_number = request.form.get('num')

        speed.page_name = speed_class
        speed.speed = speed_number

        db.session.commit()
        return redirect("/edit_speed")

    return render_template("edit_speed.html", user = current_user, update = True, speed = speed, speeds = speeds)


@app.route("/edit_speed", methods = ['GET', 'POST'])
def edit_speed():

    if request.method == "POST":
        speed_class = request.form.get('speed_class')
        speed_number = request.form.get('num')

        add_speed = speed_management(
            page_name = speed_class,
            speed = speed_number
        )

        db.session.add(add_speed)
        db.session.commit()
    
    speeds = speed_management.query.all()
    return render_template("edit_speed.html", user = current_user, speeds = speeds)



@app.route("/text_edit/<id>", methods = ['GET', 'POST'])
def text_edit(id):
    text = text_management.query.get(id)
    texts = text_management.query.all()
    if request.method == "POST":
        text_class = request.form.get('speed_class')
        # speed_number = request.form.get('num')
        english_text = request.form.get('english_text')
        arabic_text = request.form.get('arabic_text')

        text.page_name = text_class
        text.English_text = english_text
        text.Arabic_text = arabic_text
        db.session.commit()
        return redirect("/edit_text")

    return render_template("edit_text.html", user = current_user, update = True, text = text, texts = texts)


@app.route("/edit_text", methods = ['GET', 'POST'])
def edit_text():

    if request.method == "POST":
        text_class = request.form.get('speed_class')
        # speed_number = request.form.get('num')
        english_text = request.form.get('english_text')
        arabic_text = request.form.get('arabic_text')
        
        add_text = text_management(
            page_name = text_class,
            English_text = english_text,
            Arabic_text = arabic_text
        )

        db.session.add(add_text)
        db.session.commit()
    
    texts = text_management.query.all()
    return render_template("edit_text.html", user = current_user, texts = texts)



@app.route("/ball_edit/<id>", methods = ['GET', 'POST'])
def ball_edit(id):
    ball = ball_management.query.get(id)
    balls = ball_management.query.all()
    if request.method == "POST":
        ball_class = request.form.get('ball_class')
        number = request.form.get('num')

        ball.class_name = ball_class
        ball.number = number

        db.session.commit()
        return redirect("/edit_ball")

    return render_template("edit_ball.html", user = current_user, update = True, ball = ball, balls = balls)


@app.route("/edit_ball", methods = ['GET', 'POST'])
def edit_ball():

    if request.method == "POST":
        ball_class = request.form.get('ball_class')
        speed_number = request.form.get('num')

        add_speed = ball_management(
            class_name = ball_class,
            number = speed_number
        )

        db.session.add(add_speed)
        db.session.commit()
    
    balls = ball_management.query.all()
    return render_template("edit_ball.html", user = current_user, balls = balls)