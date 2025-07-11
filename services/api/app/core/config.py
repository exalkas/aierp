"""
Configuration settings for Greek ERP/CRM API Service
Handles environment variables and Greek business requirements
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings with Greek business configuration"""
    
    # Application
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    SECRET_KEY: str = Field(env="SECRET_KEY")
    
    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    
    # Security
    JWT_SECRET_KEY: str = Field(env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS and Security
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
        env="CORS_ORIGINS"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    
    # Greek Business Configuration
    DEFAULT_VAT_RATE: float = Field(default=0.24, env="DEFAULT_VAT_RATE")  # 24% standard Greek VAT
    REDUCED_VAT_RATE_1: float = Field(default=0.13, env="REDUCED_VAT_RATE_1")  # 13% reduced rate
    REDUCED_VAT_RATE_2: float = Field(default=0.06, env="REDUCED_VAT_RATE_2")  # 6% super reduced rate
    ZERO_VAT_RATE: float = Field(default=0.00, env="ZERO_VAT_RATE")  # 0% for exports/exemptions
    
    GREEK_CURRENCY: str = Field(default="EUR", env="GREEK_CURRENCY")
    GREEK_LOCALE: str = Field(default="el_GR", env="GREEK_LOCALE")
    DEFAULT_TIMEZONE: str = Field(default="Europe/Athens", env="DEFAULT_TIMEZONE")
    
    # AADE (Greek Tax Authority) Integration
    AADE_BASE_URL: str = Field(default="https://mydata-dev.azure-api.net", env="AADE_BASE_URL")
    AADE_SUBSCRIPTION_KEY: Optional[str] = Field(default=None, env="AADE_SUBSCRIPTION_KEY")
    AADE_TIMEOUT_SECONDS: int = Field(default=30, env="AADE_TIMEOUT_SECONDS")
    AADE_ENABLE_SANDBOX: bool = Field(default=True, env="AADE_ENABLE_SANDBOX")
    
    # File Storage
    FILE_STORAGE_PATH: str = Field(default="./storage/files", env="FILE_STORAGE_PATH")
    MAX_FILE_SIZE_MB: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    ALLOWED_FILE_EXTENSIONS: List[str] = Field(
        default=[".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".xls", ".xlsx"],
        env="ALLOWED_FILE_EXTENSIONS"
    )
    
    # Email Configuration
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = Field(default=True, env="SMTP_USE_TLS")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60, env="RATE_LIMIT_WINDOW_SECONDS")
    
    # Company Isolation
    MAX_COMPANIES_PER_USER: int = Field(default=1, env="MAX_COMPANIES_PER_USER")
    REQUIRE_COMPANY_IN_JWT: bool = Field(default=True, env="REQUIRE_COMPANY_IN_JWT")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_EXTENSIONS", pre=True)
    def assemble_file_extensions(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings() 