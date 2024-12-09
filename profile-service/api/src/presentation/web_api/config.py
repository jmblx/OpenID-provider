import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")
