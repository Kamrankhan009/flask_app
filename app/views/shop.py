from app import app,db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import Product,Cart
import os
from ..confing import basedir
from uuid import uuid4


cart = []

@app.route("/shop", methods = ['GET','POST'])
def shop():
    products=Product.query.all()
    return render_template('shop.html',user=current_user,products=products)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST' and 'image' in request.files:
    # Get form data
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']
        # Save the image to a specific location or process it as needed
        filename = str(uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
        
        image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/products", filename))
        new_product=Product(title=title,description=description,price=price,image=f'{filename}')
        db.session.add(new_product)
        db.session.commit()
        # ...

        # Redirect to a success page or another route
        return redirect(url_for('shop'))

    return render_template('add_product.html',user=current_user)

@app.route("/products/<int:id>", methods = ['GET','POST'])
def one_product(id):
    product=Product.query.filter_by(id=id).first()
    return render_template('one_product.html',user=current_user,product=product)


@app.route('/cart')
@login_required
def cart():
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    user_id = current_user.id

    # Query the Cart table to get all cart items for the current user
    cart_items = Cart.query.filter_by(uid=user_id).all()

    # Calculate the total amount
    total_amount = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount, user=current_user)

@app.route('/cart_count')
def cart_count():
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    count = 0
    if current_user.is_authenticated:
        # Query the Cart table for the count of items for the current user
        count = Cart.query.filter_by(uid=current_user.id).count()

    return jsonify({'count': count})


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    user_id = current_user.id
    quantity = int(request.form['quantity'])

    # Check if the item is already in the cart for the user
    cart_item = Cart.query.filter_by(uid=user_id, itemid=item_id).first()

    if cart_item:
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += quantity
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'})
    else:
        # If the item is not in the cart, create a new Cart object
        cart_item = Cart(uid=user_id, itemid=item_id, quantity=quantity)

        # Save the Cart object to the database
        db.session.add(cart_item)
        db.session.commit()

    return jsonify({'message': 'Item added to cart successfully'})




@app.route('/delete_from_cart/<int:cart_item_id>', methods=['POST'])
def delete_from_cart(cart_item_id):
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    user_id = current_user.id

    # Query the Cart table for the cart item to delete
    cart_item = Cart.query.filter_by(uid=user_id, id=cart_item_id).first()

    if cart_item:
        # Delete the cart item from the database
        db.session.delete(cart_item)
        db.session.commit()

    return redirect('/cart')  # Redirect back to the cart page