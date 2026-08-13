from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE: str
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://localhost:3000"]
    
    # JWT Configuration
    JWT_SECRET: str = "your_jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
