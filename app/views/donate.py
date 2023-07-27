
from app import app, db
from flask import render_template,jsonify,request, url_for
from flask_login import current_user
import stripe
from ..models import Cart

@app.route('/donate')
def donate():
    try:
        count = Cart.query.filter_by(uid=current_user.id).count()
    except:
        count = 0
    return render_template('donate.html', user=current_user, count = count)


@app.route('/donate-url')
def donate_url():
    min_amount = request.args.get('min_amount')
    # Generate the URL for the donate_form page based on the min_amount value
    donate_url = url_for('donate_form', min_amount=min_amount)
    return jsonify(url=donate_url)
