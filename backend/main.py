import os
from typing import Any
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime, timezone
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
# Load .env file (make sure you have MONGO_URI inside it)
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

# POST: Create user
@app.post("/users/")
async def create_user(user: User):
    try:
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

    except Exception as e:
        # Log the real error
        print(f"Error creating user: {e}")
        # Return proper HTTP error
        raise HTTPException(status_code=500, detail="Failed to create user")