from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def fix_product_images():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    # Working product images from reliable sources
    product_images = {
        "iPhone 15 Pro": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
        "Samsung 4K TV": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=400&fit=crop",
        "AirPods Pro": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop",
        "Nike Running Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
        "Levi's Jeans": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop",
        "Cotton T-Shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
        "Coffee Maker": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop",
        "Blender": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=400&fit=crop",
        "Dining Table": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop",
        "Python Programming Book": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop",
        "Bluetooth Speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
        "Yoga Mat": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop",
        "Basketball": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=400&fit=crop",
        "Camping Tent": "https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=400&h=400&fit=crop",
        "Electric Toothbrush": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=400&h=400&fit=crop",
        "Face Moisturizer": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop",
        "Car Phone Mount": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "Car Charger": "https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=400&h=400&fit=crop",
        "Laptop Pro": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop",
        "Wireless Mouse": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop",
        "Mechanical Keyboard": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=400&fit=crop"
    }
    
    updated_count = 0
    for product_name, image_url in product_images.items():
        result = products_collection.update_one(
            {"name": product_name},
            {"$set": {"image": image_url}}
        )
        if result.modified_count > 0:
            updated_count += 1
            print(f"Fixed image for: {product_name}")
    
    print(f"\nFixed {updated_count} products with working images")

if __name__ == "__main__":
    fix_product_images()