from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import os

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def setup_database():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        
        print(f"Connected to MongoDB: {MONGODB_URI}")
        print(f"Database: {MONGODB_DB}")
        
        # Drop existing collections if they exist (optional - remove if you want to keep existing data)
        # db.products.drop()
        # db.orders.drop()
        
        # Create Products Collection
        products_collection = db['products']
        
        # Create indexes for products collection
        products_collection.create_index([("name", ASCENDING)], unique=True)  # Unique product names
        products_collection.create_index([("price", ASCENDING)])
        products_collection.create_index([("stock", ASCENDING)])
        products_collection.create_index([("created_at", DESCENDING)])
        
        # Create validation schema for products
        db.command({
            "collMod": "products",
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["name", "price", "stock", "created_at"],
                    "properties": {
                        "name": {
                            "bsonType": "string",
                            "description": "Product name is required and must be a string"
                        },
                        "price": {
                            "bsonType": ["double", "int"],
                            "minimum": 0,
                            "description": "Price must be a positive number"
                        },
                        "description": {
                            "bsonType": "string",
                            "description": "Product description must be a string"
                        },
                        "stock": {
                            "bsonType": "int",
                            "minimum": 0,
                            "description": "Stock must be a non-negative integer"
                        },
                        "image": {
                            "bsonType": "string",
                            "description": "Image URL must be a string"
                        },
                        "created_at": {
                            "bsonType": "date",
                            "description": "Created date is required"
                        }
                    }
                }
            },
            "validationLevel": "strict",
            "validationAction": "error"
        })
        
        # Create Orders Collection
        orders_collection = db['orders']
        
        # Create indexes for orders collection
        orders_collection.create_index([("created_at", DESCENDING)])
        orders_collection.create_index([("status", ASCENDING)])
        orders_collection.create_index([("total", DESCENDING)])
        
        # Create validation schema for orders
        db.command({
            "collMod": "orders",
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["items", "total", "status", "created_at"],
                    "properties": {
                        "items": {
                            "bsonType": "array",
                            "minItems": 1,
                            "items": {
                                "bsonType": "object",
                                "required": ["product_id", "quantity", "price"],
                                "properties": {
                                    "product_id": {
                                        "bsonType": "string",
                                        "description": "Product ID is required"
                                    },
                                    "quantity": {
                                        "bsonType": "int",
                                        "minimum": 1,
                                        "description": "Quantity must be at least 1"
                                    },
                                    "price": {
                                        "bsonType": ["double", "int"],
                                        "minimum": 0,
                                        "description": "Price must be positive"
                                    }
                                }
                            },
                            "description": "Items array is required and must contain at least one item"
                        },
                        "total": {
                            "bsonType": ["double", "int"],
                            "minimum": 0,
                            "description": "Total must be a positive number"
                        },
                        "status": {
                            "bsonType": "string",
                            "enum": ["pending", "processing", "shipped", "delivered", "cancelled"],
                            "description": "Status must be one of the allowed values"
                        },
                        "created_at": {
                            "bsonType": "date",
                            "description": "Created date is required"
                        }
                    }
                }
            },
            "validationLevel": "strict",
            "validationAction": "error"
        })
        
        print("Database setup completed successfully!")
        print("\nCollections created:")
        print("- products (with validation and indexes)")
        print("- orders (with validation and indexes)")
        
        print("\nProducts collection constraints:")
        print("- name: required, unique, string")
        print("- price: required, positive number")
        print("- stock: required, non-negative integer")
        print("- description: optional, string")
        print("- image: optional, string")
        print("- created_at: required, date")
        
        print("\nOrders collection constraints:")
        print("- items: required, array with at least 1 item")
        print("- total: required, positive number")
        print("- status: required, enum (pending, processing, shipped, delivered, cancelled)")
        print("- created_at: required, date")
        
        # Insert sample data
        insert_sample_data(products_collection, orders_collection)
        
    except Exception as e:
        print(f"Database setup failed: {e}")

def insert_sample_data(products_collection, orders_collection):
    try:
        # Sample products
        sample_products = [
            {
                "name": "Laptop Pro",
                "price": 1299.99,
                "description": "High-performance laptop for professionals",
                "stock": 10,
                "image": "/placeholder.svg?height=300&width=300",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Wireless Mouse",
                "price": 29.99,
                "description": "Ergonomic wireless mouse",
                "stock": 50,
                "image": "/placeholder.svg?height=300&width=300",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Mechanical Keyboard",
                "price": 149.99,
                "description": "RGB mechanical gaming keyboard",
                "stock": 25,
                "image": "/placeholder.svg?height=300&width=300",
                "created_at": datetime.utcnow()
            }
        ]
        
        # Insert products if they don't exist
        for product in sample_products:
            existing = products_collection.find_one({"name": product["name"]})
            if not existing:
                products_collection.insert_one(product)
                print(f"Inserted sample product: {product['name']}")
        
        print("\nSample data inserted successfully!")
        
    except Exception as e:
        print(f"Sample data insertion failed: {e}")

if __name__ == "__main__":
    setup_database()