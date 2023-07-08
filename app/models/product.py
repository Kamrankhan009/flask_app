from app import db





class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description= db.Column(db.String(300))
    price = db.Column(db.Float)
    image = db.Column(db.String(256))
    in_cart = db.relationship("Cart", backref="item")


class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	itemid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=1)