from pymongo import MongoClient, ASCENDING
import os

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'ecommerce')

def setup_users_collection():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    users_collection = db['users']
    
    # Create unique index on email
    users_collection.create_index([("email", ASCENDING)], unique=True)
    
    # Create validation schema for users
    db.command({
        "collMod": "users",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email", "password", "created_at"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "First name is required"
                    },
                    "lastName": {
                        "bsonType": "string", 
                        "description": "Last name is required"
                    },
                    "email": {
                        "bsonType": "string",
                        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                        "description": "Valid email is required"
                    },
                    "phone": {
                        "bsonType": "string",
                        "description": "Phone number"
                    },
                    "password": {
                        "bsonType": "string",
                        "minLength": 6,
                        "description": "Password must be at least 6 characters"
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
    
    print("Users collection setup completed!")
    print("- Unique index on email")
    print("- Validation schema applied")

if __name__ == "__main__":
    setup_users_collection()