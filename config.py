import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///insurance.db")
    DEBUG = os.getenv("DEBUG", True)
    
    # Security Configurations
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour expiry
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
