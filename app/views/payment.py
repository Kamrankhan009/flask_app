from app import app, db
from flask import render_template,jsonify,request, url_for
from flask_login import current_user
import stripe
from ..models import Cart


@app.route("/success")
def success():
    print("don")
    return render_template("success.html", user=current_user)



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
    return render_template('cart_payment_form.html', amount=amount, user=current_user, count = count)


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
    return render_template('donate_form.html', min_amount=min_amount, user=current_user, count = count)

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



@app.route('/process_payment_cart', methods=['POST'])
def process_payment_cart():
    try:
        # Retrieve the payment amount from the request
        payment_amount = request.form.get('payment-amount')
        address = request.form.get('address')
        zip = request.form.get('zip')
        city = request.form.get('city')
        state = request.form.get('state')

        
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