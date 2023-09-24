from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carts.db'

db = SQLAlchemy(app)

class CartItem(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

@app.route("/cart/<int:user_id>")
def get_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in items])

@app.route("/cart/<int:user_id>/add/<int:product_id>")
def add_to_cart(user_id, product_id):
    resp = requests.get(f"http://localhost:5000/products/{product_id}")
    item = CartItem(user_id=user_id, product_id=product_id, quantity=1)    
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()) 

@app.route("/cart/<int:user_id>/remove/<int:product_id>")  
def remove_from_cart(user_id, product_id):
    CartItem.query.filter_by(user_id=user_id, product_id=product_id).delete()
    db.session.commit()
    return jsonify({"message": "Item removed from cart"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)