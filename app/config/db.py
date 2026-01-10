import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
import certifi # FIX: Import certifi

# Use find_dotenv() to ensure the .env file is found even if running from a subfolder
load_dotenv(find_dotenv())

MONGO_URI = os.getenv("MONGO_URI")
# The second argument provides a default string if "DB_NAME" is None
DB_NAME = os.getenv("DB_NAME", "ai_summarizer") 

# FIX: Pass tlsCAFile=certifi.where() to trust Atlas certificates on Windows
client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
# This is likely where the TypeError occurred: db = client[None]
db = client[DB_NAME]