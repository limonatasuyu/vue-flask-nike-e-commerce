from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable = True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),  unique = True, nullable = False)
    price = db.Column(db.Integer)
    isForMen = db.Column(db.Boolean)
    isForWomen = db.Column(db.Boolean)   
    sizesOnStock = db.Column(db.String(80), nullable = True)

class ProductsBought(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    productId = db.Column(db.Integer, nullable = False)
    userId = db.Column(db.Integer, nullable = False)
    size = db.Column(db.Integer, nullable = False)


class ProductsInBag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    productId = db.Column(db.Integer, nullable = False)
    userId = db.Column(db.Integer, nullable = False)
    size = db.Column(db.Integer, nullable = False)

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sessionId = db.Column(db.String(80), unique = True, nullable = False)
    userId = db.Column(db.Integer, nullable = False)
