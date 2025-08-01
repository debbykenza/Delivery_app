import os
from pydantic_settings import BaseSettings 
from typing import Optional
from dotenv import load_dotenv 

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_HOURS : int = 24
    SUPABASE_DB_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()