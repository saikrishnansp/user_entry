import os
from typing import Any
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime, timezone
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient # Makes your db performace effective!

app = FastAPI()
load_dotenv()

# Password hashing context (bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add this block — allows your frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],
)

# User model with password included
class User(BaseModel):      
    username: str
    email: str
    password: str  # plain password from request

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(MONGO_URI)
db = client["mydatabase"]          # database name
users_collection = db["users"]     # collection name

# Helper: hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 1xx: Informational
# 2xx: Success
# 3xx: Redirection
# 4xx: Client Error
# 5xx: Server Error

# POST: Create user
@app.post("/users/")
async def create_user(user: User):
    try:

        # Check if username already exists
        existing_user = await users_collection.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Build dict without plain password
        user_dict = user.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hash_password(user.password)
        user_dict["created_at"] = datetime.now(timezone.utc)

        # Insert into MongoDB
        result = await users_collection.insert_one(user_dict)

        # Return safe response (NEVER return plain password!)
        return {
            "id": str(result.inserted_id),
            "message": "New Record registered",
            "username": user.username,
            "email": user.email,
            "created_at": user_dict["created_at"].isoformat() + "Z"
        }
    
    except HTTPException:
        # Raise if any unknow error appear.
        raise
    except Exception as e:
        # Log the real error
        print(f"Error creating user: {e}")
        # Return proper HTTP error
        raise HTTPException(status_code=500, detail="Failed to create user")
    
# Update a user profile         
@app.put("/users/{username}")
async def update_user(username: str, user: User):
    try:
        # Step 1: Check if user exists
        existing_user = await users_collection.find_one({"username": username})
        if not existing_user:
            raise HTTPException(status_code=404, detail="Create a new user")

        # Step 2: Build update dict (exclude plain password)
        update_data = user.model_dump(exclude={"password"})
        update_data["hashed_password"] = hash_password(user.password)
        update_data["updated_at"] = datetime.now(timezone.utc)

        # Step 3: Update in MongoDB
        result = await users_collection.update_one(
            {"username": username},
            {"$set": update_data} # Only update these fields, keep the rest exactly as-is, safe way to update the monodb
        ) 
# Operator,What it does,Example use
# $set,Change specific fields,Update email/password
# $inc,Add to a number,"{""$inc"": {""coins"": 100}}"
# $push,Add item to array,Add item to wishlist
# $pull,Remove item from array,Remove banned user
# $unset,Delete a field completely,Remove old data


        # Step 4: Check if actually updated
        if result.modified_count == 1:
            return {
                "message": "User updated successfully",
                "username": user.username,
                "email": user.email,
                "updated_at": update_data["updated_at"].isoformat() + "Z"
            }
        else:
            return {"message": "No changes detected — data already up to date"}

    except HTTPException:
        raise  # re-raise known errors
    except Exception as e:
        print(f"Update failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")