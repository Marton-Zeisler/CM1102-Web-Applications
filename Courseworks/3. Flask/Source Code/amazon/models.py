from amazon import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref="product", lazy=True)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __repr__(self):
        return f"Comment('{self.title}', '{self.comment}')"

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    priceTotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Basket('{self.user_id}', '{self.product_id}'), '{self.priceTotal}') "

class BasketObject():
    product = Product()
    basket = Basket()

    def __init__(self, product, basket):
        self.product = product
        self.basket = basket

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __repr__(self):
        return f"Wishlist('{self.user_id}', '{self.product_id}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    priceTotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}')"

class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_title = db.Column(db.String(100), nullable=False)
    priceTotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}')"