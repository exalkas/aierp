"""
Configuration settings for Greek ERP/CRM API Service
Handles environment variables and Greek business requirements
"""

import os
import json
from typing import List, Optional
from pathlib import Path

# Load .env file if it exists
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)


class Settings:
    """Application settings with Greek business configuration"""
    
    def __init__(self):
        # Application
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
        
        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
        self.DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
        self.DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))
        
        # Security
        self.JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        
        # CORS and Security - Handle both JSON array and comma-separated formats
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002")
        if cors_origins.startswith('[') and cors_origins.endswith(']'):
            # Handle JSON array format from .env file
            self.CORS_ORIGINS: List[str] = json.loads(cors_origins)
        else:
            # Handle comma-separated format
            self.CORS_ORIGINS: List[str] = [origin.strip() for origin in cors_origins.split(",")]
        
        allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
        if allowed_hosts.startswith('[') and allowed_hosts.endswith(']'):
            # Handle JSON array format from .env file
            self.ALLOWED_HOSTS: List[str] = json.loads(allowed_hosts)
        else:
            # Handle comma-separated format
            self.ALLOWED_HOSTS: List[str] = [host.strip() for host in allowed_hosts.split(",")]
        
        # Greek Business Configuration
        self.DEFAULT_VAT_RATE: float = float(os.getenv("DEFAULT_VAT_RATE", "0.24"))
        self.REDUCED_VAT_RATE_1: float = float(os.getenv("REDUCED_VAT_RATE_1", "0.13"))
        self.REDUCED_VAT_RATE_2: float = float(os.getenv("REDUCED_VAT_RATE_2", "0.06"))
        self.ZERO_VAT_RATE: float = float(os.getenv("ZERO_VAT_RATE", "0.00"))
        
        # Aegean Islands VAT rates (30% reduction)
        self.AEGEAN_STANDARD_VAT_RATE: float = float(os.getenv("AEGEAN_STANDARD_VAT_RATE", "0.17"))
        self.AEGEAN_REDUCED_VAT_RATE_1: float = float(os.getenv("AEGEAN_REDUCED_VAT_RATE_1", "0.09"))
        self.AEGEAN_REDUCED_VAT_RATE_2: float = float(os.getenv("AEGEAN_REDUCED_VAT_RATE_2", "0.04"))
        
        # Context-based VAT rates
        self.TAKEAWAY_COFFEE_VAT_RATE: float = float(os.getenv("TAKEAWAY_COFFEE_VAT_RATE", "0.13"))
        self.DINEIN_COFFEE_VAT_RATE: float = float(os.getenv("DINEIN_COFFEE_VAT_RATE", "0.24"))
        
        # VAT calculation settings
        self.VAT_CALCULATION_PRECISION: int = int(os.getenv("VAT_CALCULATION_PRECISION", "2"))
        self.ENABLE_DYNAMIC_VAT_CALCULATION: bool = os.getenv("ENABLE_DYNAMIC_VAT_CALCULATION", "true").lower() == "true"
        self.VAT_RULES_CACHE_TTL: int = int(os.getenv("VAT_RULES_CACHE_TTL", "3600"))
        
        self.GREEK_CURRENCY: str = os.getenv("GREEK_CURRENCY", "EUR")
        self.GREEK_LOCALE: str = os.getenv("GREEK_LOCALE", "el_GR")
        self.DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "Europe/Athens")
        
        # AADE (Greek Tax Authority) Integration
        self.AADE_BASE_URL: str = os.getenv("AADE_BASE_URL", "https://mydata-dev.azure-api.net")
        self.AADE_SUBSCRIPTION_KEY: Optional[str] = os.getenv("AADE_SUBSCRIPTION_KEY")
        self.AADE_TIMEOUT_SECONDS: int = int(os.getenv("AADE_TIMEOUT_SECONDS", "30"))
        self.AADE_ENABLE_SANDBOX: bool = os.getenv("AADE_ENABLE_SANDBOX", "true").lower() == "true"
        
        # File Storage
        self.FILE_STORAGE_PATH: str = os.getenv("FILE_STORAGE_PATH", "./storage/files")
        self.MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        
        file_extensions = os.getenv("ALLOWED_FILE_EXTENSIONS", ".pdf,.jpg,.jpeg,.png,.doc,.docx,.xls,.xlsx")
        if file_extensions.startswith('[') and file_extensions.endswith(']'):
            # Handle JSON array format from .env file
            self.ALLOWED_FILE_EXTENSIONS: List[str] = json.loads(file_extensions)
        else:
            # Handle comma-separated format
            self.ALLOWED_FILE_EXTENSIONS: List[str] = [ext.strip() for ext in file_extensions.split(",")]
        
        # Email Configuration
        self.SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
        self.SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
        self.SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        
        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Rate Limiting
        self.RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
        
        # Company Isolation
        self.MAX_COMPANIES_PER_USER: int = int(os.getenv("MAX_COMPANIES_PER_USER", "1"))
        self.REQUIRE_COMPANY_IN_JWT: bool = os.getenv("REQUIRE_COMPANY_IN_JWT", "true").lower() == "true"


# Create global settings instance
settings = Settings() 