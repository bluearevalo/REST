from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

@app.route("/products")
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]) 

@app.route("/products/<int:id>")
def get_product(id):
    product = Product.query.get(id)
    return jsonify(product.to_dict())

@app.route("/products", methods=["POST"]) 
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"], 
        price=data["price"],
        quantity=data["quantity"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict())

if __name__ == "__main__":
    app.run(debug=True, port=5000)