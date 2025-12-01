from pymongo import MongoClient
from datetime import datetime
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def add_diverse_products():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    products = [
        # Electronics
        {"name": "iPhone 15 Pro", "price": 999.99, "description": "Latest Apple smartphone", "stock": 15, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Samsung 4K TV", "price": 799.99, "description": "55-inch Smart TV", "stock": 8, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "AirPods Pro", "price": 249.99, "description": "Wireless noise-canceling earbuds", "stock": 30, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Clothing
        {"name": "Nike Running Shoes", "price": 129.99, "description": "Comfortable athletic footwear", "stock": 40, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Levi's Jeans", "price": 79.99, "description": "Classic denim jeans", "stock": 25, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Cotton T-Shirt", "price": 19.99, "description": "Basic cotton t-shirt", "stock": 60, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Home & Kitchen
        {"name": "Coffee Maker", "price": 89.99, "description": "12-cup programmable coffee maker", "stock": 12, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Blender", "price": 59.99, "description": "High-speed blender", "stock": 18, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Dining Table", "price": 299.99, "description": "Wooden dining table for 4", "stock": 5, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Books & Media
        {"name": "Python Programming Book", "price": 39.99, "description": "Learn Python programming", "stock": 20, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Bluetooth Speaker", "price": 49.99, "description": "Portable wireless speaker", "stock": 35, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Sports & Outdoors
        {"name": "Yoga Mat", "price": 24.99, "description": "Non-slip exercise mat", "stock": 45, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Basketball", "price": 29.99, "description": "Official size basketball", "stock": 22, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Camping Tent", "price": 149.99, "description": "4-person waterproof tent", "stock": 7, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Beauty & Personal Care
        {"name": "Electric Toothbrush", "price": 79.99, "description": "Rechargeable sonic toothbrush", "stock": 28, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Face Moisturizer", "price": 34.99, "description": "Daily hydrating cream", "stock": 50, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        
        # Automotive
        {"name": "Car Phone Mount", "price": 19.99, "description": "Dashboard phone holder", "stock": 40, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
        {"name": "Car Charger", "price": 14.99, "description": "Dual USB car charger", "stock": 55, "image": "/placeholder.svg?height=300&width=300", "created_at": datetime.utcnow()},
    ]
    
    for product in products:
        try:
            existing = products_collection.find_one({"name": product["name"]})
            if not existing:
                products_collection.insert_one(product)
                print(f"Added: {product['name']}")
        except Exception as e:
            print(f"Error adding {product['name']}: {e}")
    
    print(f"\nTotal products in database: {products_collection.count_documents({})}")

if __name__ == "__main__":
    add_diverse_products()