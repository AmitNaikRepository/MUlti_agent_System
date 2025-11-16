"""
Configuration management for the Multi-Agent Orchestration System.
Loads environment variables and provides centralized configuration.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str
    openai_api_key: Optional[str] = None
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_enabled: bool = False
    
    # Database
    database_url: str = "sqlite:///./data/metrics.db"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    
    # Groq Model Configuration
    default_fast_model: str = "llama-3.1-8b-instant"  # Fast, cheap for simple tasks
    default_complex_model: str = "mixtral-8x7b-32768"  # More capable for complex tasks
    
    # Cost per 1M tokens (approximate, update based on Groq pricing)
    cost_per_1m_tokens_fast: float = 0.05
    cost_per_1m_tokens_complex: float = 0.24
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
