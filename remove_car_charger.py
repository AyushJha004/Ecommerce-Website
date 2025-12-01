from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def remove_car_charger():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    # Remove Car Charger product
    result = products_collection.delete_one({"name": "Car Charger"})
    
    if result.deleted_count > 0:
        print("Car Charger product removed successfully")
    else:
        print("Car Charger product not found")
    
    # Show remaining products
    remaining_products = products_collection.count_documents({})
    print(f"Remaining products: {remaining_products}")

if __name__ == "__main__":
    remove_car_charger()