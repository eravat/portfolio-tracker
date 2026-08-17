from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
