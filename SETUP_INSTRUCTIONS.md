# Flask MongoDB Ecommerce Store - Setup Guide

A beautiful, simple ecommerce store built with Flask, HTML, CSS, and MongoDB.

## Prerequisites

- Python 3.8+ installed
- MongoDB Atlas account or local MongoDB installation
- A web browser
- Text editor (optional, for customization)

## Step-by-Step Setup

### Step 1: Extract/Navigate to Project

If you downloaded as ZIP, extract it first:
\`\`\`bash
cd ecommerce-store
\`\`\`

### Step 2: Create Python Virtual Environment

\`\`\`bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

You should see `(venv)` at the start of your terminal line.

### Step 3: Install Python Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

This installs Flask, PyMongo, and NumPy.

### Step 4: Set Up MongoDB

#### Option A: MongoDB Atlas (Cloud - Recommended for beginners)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a FREE account
3. Create a new Project
4. Create a Cluster (select FREE tier)
5. Wait for cluster to deploy (2-3 minutes)
6. Click "Connect"
7. Choose "Drivers" and select "Python 3.6 or later"
8. Copy the connection string (looks like: `mongodb+srv://username:password@cluster0.abc123.mongodb.net/`)
9. Replace `username`, `password`, and database name

#### Option B: Local MongoDB (Advanced)

1. Download: https://www.mongodb.com/try/download/community
2. Install and start MongoDB
3. Connection string: `mongodb://localhost:27017`

### Step 5: Create Environment File

Create a `.env` file in the root directory (same folder as app.py):

\`\`\`
MONGODB_URI=mongodb+srv://username:password@cluster0.abc123.mongodb.net/ecommerce
MONGODB_DB=ecommerce
FLASK_ENV=development
\`\`\`

**Important:** Replace `username`, `password`, and `cluster0.abc123` with your actual credentials!

### Step 6: Add Sample Products

Create `seed_data.py` in the root directory and paste this:

\`\`\`python
from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
products = db['products']

# Clear existing products
products.delete_many({})

# Add sample products
sample_products = [
    {
        'name': 'Premium Wireless Headphones',
        'price': 199.99,
        'description': 'High-quality audio with noise cancellation',
        'stock': 45,
        'image': 'https://via.placeholder.com/300x300?text=Headphones'
    },
    {
        'name': 'Luxury Watch',
        'price': 599.99,
        'description': 'Elegant Swiss-made timepiece',
        'stock': 12,
        'image': 'https://via.placeholder.com/300x300?text=Watch'
    },
    {
        'name': 'Designer Sunglasses',
        'price': 299.99,
        'description': 'UV protection with premium style',
        'stock': 38,
        'image': 'https://via.placeholder.com/300x300?text=Sunglasses'
    },
    {
        'name': 'Leather Wallet',
        'price': 149.99,
        'description': 'Genuine Italian leather construction',
        'stock': 60,
        'image': 'https://via.placeholder.com/300x300?text=Wallet'
    },
    {
        'name': 'Smart Ring',
        'price': 399.99,
        'description': 'Track health and notifications',
        'stock': 25,
        'image': 'https://via.placeholder.com/300x300?text=SmartRing'
    },
    {
        'name': 'Premium Camera',
        'price': 1299.99,
        'description': '4K mirrorless professional camera',
        'stock': 8,
        'image': 'https://via.placeholder.com/300x300?text=Camera'
    },
]

result = products.insert_many(sample_products)
print(f"✓ Added {len(result.inserted_ids)} products to MongoDB!")
client.close()
\`\`\`

Save the file, then run:

\`\`\`bash
python seed_data.py
\`\`\`

You should see: `✓ Added 6 products to MongoDB!`

### Step 7: Run the Application

\`\`\`bash
python app.py
\`\`\`

You should see:
\`\`\`
✓ Connected to MongoDB
 * Running on http://127.0.0.1:5000
\`\`\`

### Step 8: Open in Browser

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: **http://localhost:5000**
3. Enjoy your beautiful ecommerce store!

## What You'll See

- **Hero Section**: Eye-catching banner with shop now button
- **Statistics Dashboard**: Shows total products, average price, items in stock, price range
- **Product Grid**: Beautiful product cards with images, descriptions, prices
- **Shopping Cart**: Add items to cart and place orders
- **Footer**: Company info and links

## How to Customize

### Add Your Own Products

Edit `seed_data.py` and add more items to `sample_products` list:

\`\`\`python
{
    'name': 'Your Product Name',
    'price': 99.99,
    'description': 'Product description here',
    'stock': 50,
    'image': 'https://your-image-url.com/image.jpg'
}
\`\`\`

Run `python seed_data.py` again.

### Change Styling

Open `templates/index.html` and modify the CSS in the `<style>` section:
- Colors: Change `--primary`, `--accent`, `--white`, etc. in `:root`
- Fonts: Update `--font-primary`
- Sizes: Adjust padding, margins, font-sizes as needed

### Change Store Name

In `templates/index.html`, find and replace:
- "LUXE STORE" in the header
- "Premium Shopping Experience" in hero section
- Other text as desired

## Troubleshooting

### Error: "Connection refused"
**Solution:** 
- Check MongoDB is running (Atlas: verify internet connection; Local: start MongoDB service)
- Verify `.env` file has correct MONGODB_URI
- Test connection with MongoDB Compass

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Make sure virtual environment is activated:
\`\`\`bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
\`\`\`

Then run: `pip install -r requirements.txt`

### Products not showing on webpage
**Solution:**
1. Run seed script: `python seed_data.py`
2. Refresh browser (Ctrl+F5)
3. Check browser console (F12) for errors
4. Check server console for error messages

### Port 5000 already in use
**Solution:** Edit `app.py`, change last line to:
\`\`\`python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
\`\`\`

Then visit `http://localhost:5001`

### Products load but display is broken
**Solution:**
- Check browser console (F12) for JavaScript errors
- Clear browser cache (Ctrl+Shift+Delete)
- Make sure placeholder images work

## Project Structure

\`\`\`
.
├── app.py                          # Flask backend & API
├── templates/
│   └── index.html                  # Beautiful UI & JavaScript
├── requirements.txt                # Python dependencies
├── seed_data.py                    # Add sample products (create this)
└── .env                            # Environment variables (create this)
\`\`\`

## Key Features

✅ Responsive design (works on mobile, tablet, desktop)
✅ Real-time statistics with NumPy
✅ MongoDB data persistence
✅ Shopping cart with local storage
✅ Order processing
✅ Beautiful premium design
✅ No build process needed

## Next Steps

1. **Customize**: Edit store name, colors, products
2. **Add Payment**: Integrate Stripe for real transactions
3. **Add Images**: Replace placeholder URLs with real product images
4. **Deploy**: Host on Heroku, Railway, or PythonAnywhere
5. **Add Authentication**: User accounts and order history

## Deployment (Optional)

### Deploy to Heroku

1. Create account at https://www.heroku.com
2. Install Heroku CLI
3. Run:
   \`\`\`bash
   heroku login
   heroku create your-app-name
   git push heroku main
   \`\`\`
4. Set environment variables in Heroku dashboard

## Support

- Flask docs: https://flask.palletsprojects.com/
- MongoDB docs: https://docs.mongodb.com/
- Python docs: https://docs.python.org/3/

---

**Congratulations!** You now have a fully functional ecommerce store with MongoDB! 🎉
