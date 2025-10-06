import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # MySQL database configuration with PyMySQL driver
    database_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/moviedb")
    
    # Convert Railway MySQL URL to PyMySQL format if needed
    if database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False