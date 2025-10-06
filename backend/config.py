import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # MySQL database configuration with PyMySQL driver
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/moviedb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False