from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

try:
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    orders_collection = db['orders']
    baskets_collection = db['baskets']
    users_collection = db['users']

    print("Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/cart/<user_id>')
def cart_page(user_id):
    return render_template('cart.html', user_id=user_id)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = list(products_collection.find())
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        product = {
            'name': data.get('name'),
            'price': float(data.get('price')),
            'description': data.get('description'),
            'stock': int(data.get('stock', 0)),
            'image': data.get('image', '/placeholder.svg?height=300&width=300'),
            'created_at': datetime.utcnow()
        }
        result = products_collection.insert_one(product)
        product['_id'] = str(result.inserted_id)
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.json
        items = data.get('items', [])
        
        # Calculate total and validate stock using numpy
        prices = np.array([item['price'] for item in items])
        quantities = np.array([item['quantity'] for item in items])
        total = float(np.sum(prices * quantities))
        
        # Update product stock
        for item in items:
            products_collection.update_one(
                {'_id': ObjectId(item['product_id'])},
                {'$inc': {'stock': -item['quantity']}}
            )
        
        order = {
            'items': items,
            'total': total,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        result = orders_collection.insert_one(order)
        return jsonify({'order_id': str(result.inserted_id), 'total': total}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/basket/<user_id>', methods=['GET'])
def get_basket(user_id):
    try:
        basket = baskets_collection.find_one({'user_id': user_id})
        if not basket:
            return jsonify({'items': [], 'total': 0})
        
        # Get product details for each item
        items_with_details = []
        total = 0
        for item in basket.get('items', []):
            product = products_collection.find_one({'_id': ObjectId(item['product_id'])})
            if product:
                item_total = item['quantity'] * product['price']
                items_with_details.append({
                    'product_id': str(product['_id']),
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': item['quantity'],
                    'item_total': item_total
                })
                total += item_total
        
        return jsonify({'items': items_with_details, 'total': total})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/basket/<user_id>/add', methods=['POST'])
def add_to_basket(user_id):
    try:
        data = request.json
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        # Check if product exists and has enough stock
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        if product['stock'] < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Update or create basket
        basket = baskets_collection.find_one({'user_id': user_id})
        if basket:
            # Check if item already in basket
            item_found = False
            for item in basket['items']:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    item_found = True
                    break
            if not item_found:
                basket['items'].append({'product_id': product_id, 'quantity': quantity})
            
            baskets_collection.update_one(
                {'user_id': user_id},
                {'$set': {'items': basket['items'], 'updated_at': datetime.utcnow()}}
            )
        else:
            baskets_collection.insert_one({
                'user_id': user_id,
                'items': [{'product_id': product_id, 'quantity': quantity}],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
        
        return jsonify({'message': 'Item added to basket'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/basket/<user_id>/clear', methods=['DELETE'])
def clear_basket(user_id):
    try:
        baskets_collection.delete_one({'user_id': user_id})
        return jsonify({'message': 'Basket cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/basket/<user_id>/purchase', methods=['POST'])
def purchase_selected_items(user_id):
    try:
        data = request.json
        selected_items = data.get('selected_items', [])
        address = data.get('address', {})
        payment_method = data.get('payment_method', '')
        
        if not selected_items:
            return jsonify({'error': 'No items selected'}), 400
        if not address or not payment_method:
            return jsonify({'error': 'Address and payment method required'}), 400
        
        # Get basket
        basket = baskets_collection.find_one({'user_id': user_id})
        if not basket:
            return jsonify({'error': 'Basket not found'}), 404
        
        # Prepare order items and calculate total
        order_items = []
        total = 0
        
        for selected_item in selected_items:
            product_id = selected_item['product_id']
            quantity = selected_item['quantity']
            
            # Get product details
            product = products_collection.find_one({'_id': ObjectId(product_id)})
            if not product:
                return jsonify({'error': f'Product {product_id} not found'}), 404
            if product['stock'] < quantity:
                return jsonify({'error': f'Insufficient stock for {product["name"]}'}), 400
            
            item_total = product['price'] * quantity
            order_items.append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })
            total += item_total
        
        # Update product stock
        for item in order_items:
            products_collection.update_one(
                {'_id': ObjectId(item['product_id'])},
                {'$inc': {'stock': -item['quantity']}}
            )
        
        # Get buyer info
        buyer = users_collection.find_one({'_id': ObjectId(user_id)})
        buyer_info = {
            'user_id': user_id,
            'name': f"{buyer['firstName']} {buyer['lastName']}" if buyer else 'Unknown',
            'email': buyer['email'] if buyer else 'Unknown',
            'phone': buyer.get('phone', 'Not provided') if buyer else 'Unknown'
        }
        
        # Create order
        order = {
            'buyer_info': buyer_info,
            'items': order_items,
            'total': total,
            'address': address,
            'payment_method': payment_method,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        result = orders_collection.insert_one(order)
        
        # Remove purchased items from basket
        remaining_items = []
        for basket_item in basket['items']:
            purchased = False
            for selected_item in selected_items:
                if basket_item['product_id'] == selected_item['product_id']:
                    if basket_item['quantity'] > selected_item['quantity']:
                        basket_item['quantity'] -= selected_item['quantity']
                        remaining_items.append(basket_item)
                    purchased = True
                    break
            if not purchased:
                remaining_items.append(basket_item)
        
        if remaining_items:
            baskets_collection.update_one(
                {'user_id': user_id},
                {'$set': {'items': remaining_items, 'updated_at': datetime.utcnow()}}
            )
        else:
            baskets_collection.delete_one({'user_id': user_id})
        
        return jsonify({
            'order_id': str(result.inserted_id),
            'total': total,
            'message': 'Order placed successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already registered'}), 400
        
        user = {
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': email,
            'phone': data.get('phone'),
            'password': data.get('password'),  # In production, hash this!
            'created_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user)
        return jsonify({
            'message': 'Account created successfully',
            'user_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            return jsonify({
                'message': 'Login successful',
                'user_id': str(user['_id']),
                'name': f"{user['firstName']} {user['lastName']}"
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        products = list(products_collection.find())
        prices = np.array([p['price'] for p in products])
        stocks = np.array([p['stock'] for p in products])
        
        stats = {
            'total_products': len(products),
            'avg_price': float(np.mean(prices)) if len(prices) > 0 else 0,
            'total_stock': int(np.sum(stocks)),
            'price_range': {
                'min': float(np.min(prices)) if len(prices) > 0 else 0,
                'max': float(np.max(prices)) if len(prices) > 0 else 0
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
