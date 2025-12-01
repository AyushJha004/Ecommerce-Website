from pymongo import MongoClient
import os

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def verify_database():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        
        print(f"Verifying database: {MONGODB_DB}")
        print("=" * 50)
        
        # Check collections
        collections = db.list_collection_names()
        print(f"Collections: {collections}")
        
        # Check products collection
        products_collection = db['products']
        product_count = products_collection.count_documents({})
        print(f"\nProducts collection: {product_count} documents")
        
        if product_count > 0:
            print("Sample products:")
            for product in products_collection.find().limit(3):
                print(f"  - {product['name']}: ${product['price']} (Stock: {product['stock']})")
        
        # Check orders collection
        orders_collection = db['orders']
        order_count = orders_collection.count_documents({})
        print(f"\nOrders collection: {order_count} documents")
        
        # Check indexes
        print(f"\nProducts indexes:")
        for index in products_collection.list_indexes():
            print(f"  - {index['name']}: {index.get('key', {})}")
        
        print(f"\nOrders indexes:")
        for index in orders_collection.list_indexes():
            print(f"  - {index['name']}: {index.get('key', {})}")
        
        print("\nDatabase verification completed!")
        
    except Exception as e:
        print(f"Database verification failed: {e}")

if __name__ == "__main__":
    verify_database()