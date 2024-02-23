from app import app, db
from flask import render_template,jsonify,request, url_for, session, redirect
from flask_login import current_user
import stripe
from ..models import Cart, ball_management, color_management, speed_management, Ordered_items, Product


popup_text = "hello world"
money_back = "No Money back, check if you are agree"
color = "red"
@app.route("/success")
def success():
    user_data = session['shipping_address']
    # country,f_name, l_name, company,address,city,postal_code,phone_number, amount
    car_data = Cart.query.filter_by(uid = current_user.id).all()    
    for data in car_data:
        order = Ordered_items(
            user_id = current_user.id,
            item_id = data.itemid,
            quantity = data.quantity,
            country = user_data['country'],
            first_name = user_data['f_name'],
            last_name = user_data['l_name'],
            company = user_data['company'],
            address = user_data['address'],
            city = user_data['city'],
            postal_code = user_data['postal_code'],
            phone_number = user_data['phone_number'],
            amount = user_data['amount']
        )
        db.session.add(order)
        db.session.delete(data)
        db.session.commit()
    return render_template("success.html", user=current_user)


@app.route("/change_popup", methods=['GET', 'POST'])
def change_popup():
    global popup_text
    if request.method == "POST":
        popup_text = request.form.get('popup')
    return render_template("dashboard/popup.html", user = current_user)


@app.route("/money_back", methods = ["GET", 'POST'])
def money_back():
    global money_back
    global color
    if request.method == 'POST':
        money_back = request.form.get("text")
        color = request.form.get('color')        
    return render_template("dashboard/money_back.html", user = current_user)


@app.route('/cart_payment_form')
def cart_payment_form():
    amount = request.args.get('amount')
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    
    try:
        user_data = session['shipping_address']
    except:
        user_data = ""
  
    return render_template('cart_payment_form.html', amount=amount, user=current_user, count = count, user_data = user_data, text = popup_text, money_back = money_back, color = color)


@app.route('/donate_form')
def donate_form():
    min_amount = request.args.get('min_amount')
    # Render the donate_form.html template with the min_amount value
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
    return render_template('donate_form.html', min_amount=min_amount, user=current_user, count = count,
                            color1 = color1,
                           ball_speed = speed_of_ball.speed,
                           balls = int(balls.number))


@app.route("/process_payment", methods=["POST"])
def process_payment():
    # Retrieve the payment method ID from the form data
    payment_method = request.json.get("payment_method")
  
    # Retrieve the user information from the form data
    name = request.json.get("name")
    email = request.json.get("email")
    amount = request.json.get('amount')
    
    print(request.json)
    print(amount)
  
    try:
        # Create a payment intent and confirm it
        intent = stripe.PaymentIntent.create(
            amount=int(request.json.get("amount")) * 100,  # Convert amount to cents
            currency="usd",
            payment_method=payment_method,
            confirm=True,
            description=f"Donation from {name} ({email})"
        )
        
        print("done")
        # Handle successful payment
        
    except Exception as e:
        # Handle payment error
        print(e)
    
    return jsonify({"success": True})


@app.route('/payment_address', methods = ['GET', 'POST'])
def payment_address():

    amount = request.args.get('amount')
    try:
        user_address = session['shipping_address']
    except:
        user_address = ""

    if request.method == 'POST': 
        country = request.form.get("country")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        company = request.form.get("company")
        address = request.form.get("address")
        city = request.form.get("city")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")
        amount = request.form.get('amount')

        print(amount)
        
        session['shipping_address'] = {
                'country': country,
                'f_name': f_name,
                'l_name': l_name,
                'company': company,
                'address': address,
                'city': city,
                'postal_code': postal_code,
                'phone_number':phone,
                'amount': amount
            }
        print(session['shipping_address'])
        

        return redirect(f"/cart_payment_form?amount={amount.strip()}")
    return render_template("payment_address.html", user = current_user, amount = amount, user_address = user_address)
    


@app.route('/process_payment_cart', methods=['POST'])
def process_payment_cart():
    try:
        # Retrieve the payment amount from the request
        payment_amount = request.form.get('payment-amount')        
        copen = request.form.get('copen')

        if copen == "1234":
            payment_amount -= 100
        # Create a payment intent with Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(payment_amount) * 100),  # Stripe requires amount in cents
            currency='usd',
            payment_method_types=['card']
        )

        # Return the payment intent client secret to the client
        print(payment_intent.client_secret)
        print(payment_intent)
        return payment_intent.client_secret
    
    except Exception as e:
        print(e)
        return str(e)