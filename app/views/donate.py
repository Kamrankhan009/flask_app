
from app import app, db
from flask import render_template,jsonify,request, url_for
from flask_login import current_user
import stripe
from ..models import Cart, color_management, speed_management, ball_management

@app.route('/donate')
def donate():
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    color1 = color_management.query.filter_by(class_name = "Donate_background_ball").first()
    speed_of_ball = speed_management.query.filter_by(page_name= "Donate_ball_speed").first()
    balls = ball_management.query.filter_by(class_name = "Donate").first()
    return render_template('donate.html', user=current_user,
                           count = count,
                           color1 = color1,
                           ball_speed = speed_of_ball.speed,
                           balls = int(balls.number))


@app.route('/donate-url')
def donate_url():
    min_amount = request.args.get('min_amount')
    # Generate the URL for the donate_form page based on the min_amount value
    donate_url = url_for('donate_form', min_amount=min_amount)
    return jsonify(url=donate_url)
