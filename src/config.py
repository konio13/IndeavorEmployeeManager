from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_AUTHENTICATION_KEY = os.getenv('API_AUTHENTICATION_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')