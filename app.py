from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# --- Initial System Setup ---
# Here we define the core settings of the application.
app = Flask(__name__)

# The SECRET_KEY is used to encrypt session cookies and keep user data safe.
app.config['SECRET_KEY'] = "minha_chave_321"

# This defines where our database file will be stored (a local SQLite file).
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

# --- Security and Database Initialization ---
# login_manager: Responsible for handling user sessions (login/logout).
login_manager = LoginManager()

# db: Our interface to talk to the database using Python objects.
db = SQLAlchemy(app)

# Connecting the login manager to our app and defining where to go if access is denied.
login_manager.init_app(app)
login_manager.login_view = "login" 

# CORS: Allows external browsers or tools (like Swagger) to interact with this API.
CORS(app) 

### Data Models
class User(db.Model, UserMixin):
    """ Represents the customers. Stores credentials and links to their shopping cart. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref="user", lazy=True)

class Product(db.Model):
    """ Represents the items available for sale in the store. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    """ Links a user to the specific products they intend to buy. """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
   
# --- Authentication Logic ---
@login_manager.user_loader
def load_user(user_id):
    """ Helper function to reload the user object from the ID stored in the session. """
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    """ Authenticates the user and starts a secure session. """
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()

    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "Logged in successfully"})
        
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    """ Ends the current user session. """
    logout_user()
    return jsonify({"message": "Logout successfully"})

# --- Product Management (Catalog) ---

@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    """ Adds a new item to the store's inventory. """
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'] , description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': "Product added successfully"}), 200
    return jsonify({'message': "Invalid product data"}), 400

@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    """ Permanently removes a product from the database. """
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': "Product deleted successfully"}), 200
    return jsonify({'message': "Product not found"}), 404

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    """ Retrieves full information about a single product. """
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Product not found"}), 404

@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    """ Updates details of an existing product. """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data: product.name = data['name']
    if 'price' in data: product.price = data['price']
    if 'description' in data: product.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route("/api/products", methods=["GET"])
def get_products():
    """ Lists all products currently in the store. """
    products = Product.query.all()
    product_list = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    return jsonify(product_list), 200

# --- Shopping Cart Workflow ---

@app.route("/api/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """ Adds a chosen product to the logged-in user's cart. """
    user = User.query.get(int(current_user.id))
    product = Product.query.get(int(product_id))

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Item added to the cart successfully"}), 200
    return jsonify({"message": "Failed to add item to the cart"}), 400

@app.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_from_cart(product_id):
    """ Removes a specific item from the user's cart. """
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item removed from the cart successfully"}), 200
    return jsonify({"message": "Failed to remove item"}), 400

@app.route("/api/cart", methods=["GET"])
@login_required
def view_cart():
    """ Shows all items inside the current user's shopping cart. """
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        cart_content.append({
            "id": item.id,
            "product_name": product.name,
            "product_price": product.price
        })
    return jsonify(cart_content), 200

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    """ Completes the purchase and clears the user's cart. """
    user = User.query.get(int(current_user.id))
    for item in user.cart:
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Checkout successful. Cart cleared"}), 200

if __name__ == '__main__':
    app.run(debug=True)