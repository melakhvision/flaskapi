from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

### Create an instance of flask
app = Flask(__name__)


db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


#Create a model for our table

class Product(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(15), nullable=False)
    price= db.Column(db.Float, nullable=False)
    category= db.Column(db.String(15), nullable=False)


    def __init__(self, name, price, category) :
        self.name=name
        self.price=price
        self.category=category
    
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'price', 'category')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

##MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/product'

##SQLITE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/product/add', methods=['POST'])
def add_product():
    _json = request.json
    name = _json['name']
    price = _json['price']
    category = _json['category']
    new_product = Product(name=name, price=price, category=category)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "the product has been added "})



@app.route('/product', methods=['GET'])
def get_product():
    products = []
    data = Product.query.all()
    products = products_schema.dump(data)
    return jsonify(products)


@app.route('/product/<id>', methods=['GET'])
def product_byid(id):
    product = Product.query.get(id)
    data = product_schema.dump(product)
    return jsonify(data)

@app.route('/product/delete/<id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify(f"Error: the product doesn't exist")
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "the product has been deleted"})

@app.route('/product/edit/<id>', methods=['POST'])
def edit_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify ({"error": "the prodcut doesn't exist"})
    _json = request.json
    product.name = _json['name']
    product.price =_json['price']
    product.category= _json['category']
    db.session.commit()
    return jsonify({"message": "the product has been edited"})

if __name__ == "__main__":
    app.run(debug=True)