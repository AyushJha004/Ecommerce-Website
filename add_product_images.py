from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def add_product_images():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    products_collection = db['products']
    
    # Real product images from the internet
    product_images = {
        "iPhone 15 Pro": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-1inch-naturaltitanium?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692895703229",
        "Samsung 4K TV": "https://images.samsung.com/is/image/samsung/p6pim/in/ua55au7700klxl/gallery/in-uhd-4k-smart-tv-au7700-ua55au7700klxl-531217828?$650_519_PNG$",
        "AirPods Pro": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1660803972361",
        "Nike Running Shoes": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/99486859-0ff3-46b4-949b-2d16af2ad421/custom-nike-dunk-high-by-you-shoes.png",
        "Levi's Jeans": "https://lsco.scene7.com/is/image/lsco/005010114-front-pdp-lse?fmt=jpeg&qlt=70&resMode=bisharp&fit=crop,1&op_usm=0.6,0.6,8&wid=2000&hei=1840",
        "Cotton T-Shirt": "https://assets.ajio.com/medias/sys_master/root/20230629/Yp8j/649d0e42eebac147fc0f3eef/-473Wx593H-466346435-white-MODEL.jpg",
        "Coffee Maker": "https://m.media-amazon.com/images/I/61+XaXEOIPL._SL1500_.jpg",
        "Blender": "https://m.media-amazon.com/images/I/61Ks8YLTYOL._SL1500_.jpg",
        "Dining Table": "https://ii1.pepperfry.com/media/catalog/product/s/h/1100x1210/sheesham-wood-dining-table---honey-finish-by-mudramark-sheesham-wood-dining-table---honey-finish-by-m-qvkieh.jpg",
        "Python Programming Book": "https://m.media-amazon.com/images/I/71-++hbbERL._SL1500_.jpg",
        "Bluetooth Speaker": "https://m.media-amazon.com/images/I/61NBdu1YNQL._SL1500_.jpg",
        "Yoga Mat": "https://m.media-amazon.com/images/I/71zKzXgkKkL._SL1500_.jpg",
        "Basketball": "https://m.media-amazon.com/images/I/81QF1NYPORL._SL1500_.jpg",
        "Camping Tent": "https://m.media-amazon.com/images/I/81xYzjjMOzL._SL1500_.jpg",
        "Electric Toothbrush": "https://m.media-amazon.com/images/I/61Jn7MfOzgL._SL1500_.jpg",
        "Face Moisturizer": "https://m.media-amazon.com/images/I/51VjHtKoOyL._SL1080_.jpg",
        "Car Phone Mount": "https://m.media-amazon.com/images/I/61xGGqNdBzL._SL1500_.jpg",
        "Car Charger": "https://m.media-amazon.com/images/I/61Hn8EXHPUL._SL1500_.jpg",
        "Laptop Pro": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697311054290",
        "Wireless Mouse": "https://m.media-amazon.com/images/I/61mpMH5TzkL._SL1500_.jpg",
        "Mechanical Keyboard": "https://m.media-amazon.com/images/I/81bC7khGJeL._SL1500_.jpg"
    }
    
    updated_count = 0
    for product_name, image_url in product_images.items():
        result = products_collection.update_one(
            {"name": product_name},
            {"$set": {"image": image_url}}
        )
        if result.modified_count > 0:
            updated_count += 1
            print(f"Updated image for: {product_name}")
    
    print(f"\nUpdated {updated_count} products with real images")

if __name__ == "__main__":
    add_product_images()