import os

class Config:
    SECRET_KEY = os.environ.get("ACCESS_TOKEN_SECRET") or "fallback-secret-key"
    
    # Database Config
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "testdb")
    
    # SQLAlchemy URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Config
    JWT_ALGORITHM = "HS256"
