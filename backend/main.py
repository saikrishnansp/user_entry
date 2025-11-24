from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load .env file (make sure you have MONGO_URI inside it)
load_dotenv()

app = FastAPI()

# Password hashing context (bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model with password included
class User(BaseModel):
    username: str
    email: str
    password: str  # plain password from request

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["mydatabase"]          # database name
users_collection = db["users"]     # collection name

# Helper: hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# POST: Create user
@app.post("/users/")
async def create_user(user: User):
    # Build dict without plain password
    user_dict = user.dict(exclude={"password"})
    # Add hashed password field
    user_dict["hashed_password"] = hash_password(user.password)

    # Insert into MongoDB
    result = await users_collection.insert_one(user_dict)

    # Return safe response (no password)
    return {
        "id": str(result.inserted_id),
        "username": user.username,
        "email": user.email
    }
