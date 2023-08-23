from app import db





class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description= db.Column(db.String(300))
    price = db.Column(db.Float)
    image = db.Column(db.String(256))
    quantity = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    in_cart = db.relationship("Cart", backref="item")
    in_stock = db.Column(db.Boolean, default=True)


class Product_offer(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      p_id = db.Column(db.Integer)
      price = db.Column(db.Integer)
      title = db.Column(db.Integer)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    itemid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, nullable=False, default=1)


class color_management(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     color = db.Column(db.String(255))
     class_name = db.Column(db.String(255))


class speed_management(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     speed = db.Column(db.Integer, default=50)
     page_name = db.Column(db.String(255), nullable = False)


class text_management(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     English_text = db.Column(db.Text, nullable = False)
     Arabic_text = db.Column(db.Text, nullable = False)
     page_name = db.Column(db.String(255))


class ball_management(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     number = db.Column(db.Integer, nullable = False, default = 120)
     class_name = db.Column(db.String(255), nullable = False)