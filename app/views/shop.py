from app import app,db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import Product,Cart, Product_offer, color_management
import os
from ..confing import basedir
from uuid import uuid4


cart = []

@app.route("/shop", methods = ['GET','POST'])
def shop():
    products=Product.query.all()
    offer = Product_offer.query.all()

    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0

    color = color_management.query.filter_by(class_name = "Shop_background").first()
    return render_template('shop.html',user=current_user,products=products, offer = offer, count = count, color = color)


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
        new_product=Product(title=title,description=description,discount_price=price,image=f'{filename}')
        db.session.add(new_product)
        db.session.commit()
        # ...

        # Redirect to a success page or another route
        return redirect(url_for('shop'))
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('add_product.html',user=current_user, count = count)

@app.route("/products/<int:id>", methods = ['GET','POST'])
def one_product(id):
    product=Product.query.filter_by(id=id).first()
    offer = Product_offer.query.filter_by(p_id=id).order_by(Product_offer.price).all()
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('one_product.html',user=current_user,product=product, offer = offer, count = count)


@app.route('/cart')
@login_required
def cart():
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    user_id = current_user.id

    # Query the Cart table to get all cart items for the current user
    cart_items = Cart.query.filter_by(uid=user_id).all()

    # Calculate the total amount
    total_amount = sum(cart_item.price * cart_item.quantity for cart_item in cart_items)
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount, user=current_user, count = count)

@app.route('/cart_count')
def cart_count():
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    count = 0
    if current_user.is_authenticated:
        # Query the Cart table for the count of items for the current user
        count = Cart.query.filter_by(uid=current_user.id).all()

        all_count = 0
        for data in count:
            all_count += data.quantity
        count = all_count

    return jsonify({'count': count})


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Retrieve the current user ID (assuming you have a way to get the user ID)
    user_id = current_user.id
    quantity = int(request.form['quantity'])
    try:
        price = request.form['price']
    except:
        price = 0
    

    # Check if the item is already in the cart for the user
    cart_item = Cart.query.filter_by(uid=user_id, itemid=item_id).first()

    if cart_item:
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += quantity
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'})
    else:
        # If the item is not in the cart, create a new Cart object
        cart_item = Cart(uid=user_id, itemid=item_id, quantity=quantity, price=price)

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



@app.route("/update_products")
@login_required
def update_products():
    products=Product.query.all()
    color = color_management.query.filter_by(class_name = "update_products").first()
    return render_template("edit_products.html", user = current_user, products=products, color = color)


@app.route("/edit_product/<id>", methods = ['GET','POST'])
def edit_product(id):
    product = Product.query.get(id)
    offer = Product_offer.query.filter_by(p_id = id).all()
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']
        stock = bool(request.form.get('check', False))
        quantity = request.form.get('quantity')


        try:
            discount = int(request.form.get('discount'))
        except:
            discount = ""

        
        if not image:
            pass
        else:
        # Save the image to a specific location or process it as needed
            filename = str(uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
            image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/products", filename))
            product.image = filename
        

        if discount:
            product.discount = discount
            convert_to_d = discount/100
            discounted_price = int(product.discount_price) - (product.discount_price * convert_to_d)
            product.price = discounted_price

        product.title = title
        product.description = description
        
        product.discount_price = price
        product.quantity = quantity


        if stock:
            product.in_stock = False
        else:
            product.in_stock = True

        

        db.session.commit()

        return redirect(url_for('update_products'))
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template("add_product.html",user = current_user, product = product, edit = True, offer = offer, count = count)

@app.route("/delete_product/<id>")
@login_required
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/update_products")


@app.route('/product_offer', methods=['POST'])
def product_offer():
    data = request.get_json()
    id = data.get('id')
    title = data.get('name')
    price = data.get('email')


    print(title)
    add = Product_offer(p_id = id, price = price, title = title)

    db.session.add(add)
    db.session.commit()
    # Process the form data
    # ...
    # Return a response
    response = {'message': 'Product offer received successfully!'}
    return jsonify(response)


@app.route('/delete_offer/<id>/<Pid>')
def delete_offer(id, Pid):

    offr = Product_offer.query.get(id)

    db.session.delete(offr)
    db.session.commit()

    return redirect(f"/edit_product/{Pid}")




@app.route("/update_quantity/<item_id>", methods = ['GET', 'POST'])
def update_quantity(item_id):
    print(item_id)
    user_id = current_user.id

    # Query the Cart table to get all cart items for the current user

    new_quantity = int(request.json.get('quantity', 0))
    action2 = request.json.get('action')
    
    cart_data = Cart.query.get(item_id)
    product = Product.query.get(cart_data.itemid)

    if action2 == "increase":
        print("you are here.. 1")
        if product.quantity is not None:
            if int(product.quantity) > 0:
                print("you are here.. 2")
                cart_data.quantity = new_quantity
                product.quantity -= 1
                db.session.commit()
            else:
                
                new_quantity = new_quantity - 1
        else:
            print("you are here.. 4")
            cart_data.quantity = new_quantity
    else:
        print("you are here..  5")       
        if product.quantity is not None:
            cart_data.quantity = new_quantity
            product.quantity += 1
        else:
            cart_data.quantity = new_quantity

    db.session.commit()
    cart_items = Cart.query.filter_by(uid=user_id).all()
    # Calculate the total amount
    total_amount = sum(cart_item.price * cart_item.quantity for cart_item in cart_items)
    return jsonify({'total_amount': total_amount, 'quantity': new_quantity})
