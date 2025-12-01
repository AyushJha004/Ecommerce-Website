from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def update_prices():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    # Update all product prices by multiplying by 80
    result = products_collection.update_many(
        {},
        {"$mul": {"price": 80}}
    )
    
    print(f"Updated {result.modified_count} products")
    
    # Show updated prices
    products = list(products_collection.find())
    for product in products:
        print(f"{product['name']}: ₹{product['price']:.2f}")

if __name__ == "__main__":
    update_prices()