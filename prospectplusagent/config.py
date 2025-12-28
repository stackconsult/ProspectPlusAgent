"""Configuration management for ProspectPlusAgent."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # App Configuration
    app_name: str = "ProspectPlusAgent"
    app_version: str = "1.0.0"
    environment: str = "production"
    debug: bool = False
    port: int = 8080
    host: str = "0.0.0.0"
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./prospectplus.db"
    
    # Security
    secret_key: str = "change-this-in-production-to-a-secure-random-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["*"]
    
    # Agent Configuration
    default_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Vector Store
    vector_store_path: str = "./data/chroma"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
