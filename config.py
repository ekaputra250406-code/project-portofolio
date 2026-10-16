"""
Konfigurasi aplikasi Flask.
Load environment variables dari .env
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"