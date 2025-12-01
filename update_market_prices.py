from pymongo import MongoClient
from datetime import datetime
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def update_to_market_prices():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    # Market prices in INR (realistic Indian market prices)
    market_prices = {
        "iPhone 15 Pro": 134900,
        "Samsung 4K TV": 45999,
        "AirPods Pro": 24900,
        "Nike Running Shoes": 8995,
        "Levi's Jeans": 3499,
        "Cotton T-Shirt": 799,
        "Coffee Maker": 4999,
        "Blender": 2999,
        "Dining Table": 15999,
        "Python Programming Book": 1299,
        "Bluetooth Speaker": 2499,
        "Yoga Mat": 1199,
        "Basketball": 1499,
        "Camping Tent": 8999,
        "Electric Toothbrush": 3999,
        "Face Moisturizer": 1899,
        "Car Phone Mount": 599,
        "Car Charger": 399,
        "Laptop Pro": 89999,
        "Wireless Mouse": 1299,
        "Mechanical Keyboard": 7999
    }
    
    updated_count = 0
    for product_name, price in market_prices.items():
        result = products_collection.update_one(
            {"name": product_name},
            {"$set": {"price": price}}
        )
        if result.modified_count > 0:
            updated_count += 1
            print(f"Updated {product_name}: Rs.{price:,}")
    
    print(f"\nUpdated {updated_count} products with market prices")
    
    # Show all current prices
    print("\nCurrent product prices:")
    products = list(products_collection.find())
    for product in products:
        print(f"{product['name']}: Rs.{product['price']:,.2f}")

if __name__ == "__main__":
    update_to_market_prices()