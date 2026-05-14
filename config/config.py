import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("PATH_FRONTEND")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "test"
JWT_SECRET = os.getenv("JWT_SECRET")
GEMINIAI_KEY = os.getenv("GEMINIAI_API_KEY")
GEMINIAI_MODEL = os.getenv("GEMINIAI_MODEL")