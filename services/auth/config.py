"""
Authentication Service Configuration
Connects to same database as API service for user authentication
"""

import os
from typing import List


class Settings:
    """Simple settings class that reads from environment variables"""
    
    def __init__(self):
        # Service Information
        self.SERVICE_NAME = "greek-erp-auth"
        self.VERSION = "1.0.0"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        
        # Database Configuration (shared with API service)
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL", 
            "postgresql://erp_admin_315:replace_with_local_database_password@localhost:5432/erp_maritime_hellenic_4007"
        )
        
        # JWT Configuration
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
        self.JWT_ALGORITHM = "HS256"
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        
        # Security Settings
        self.SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
        self.MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        self.PASSWORD_RESET_EXPIRE_HOURS = int(os.getenv("PASSWORD_RESET_EXPIRE_HOURS", "24"))
        self.EMAIL_VERIFICATION_EXPIRE_HOURS = int(os.getenv("EMAIL_VERIFICATION_EXPIRE_HOURS", "48"))
        
        # CORS Configuration
        cors_origins = os.getenv("CORS_ORIGINS", "")
        if cors_origins:
            if cors_origins.startswith('[') and cors_origins.endswith(']'):
                # Parse JSON-like format
                cors_origins = cors_origins.strip('[]')
                self.CORS_ORIGINS = [item.strip().strip('"\'') for item in cors_origins.split(',') if item.strip()]
            else:
                # Parse comma-separated
                self.CORS_ORIGINS = [item.strip() for item in cors_origins.split(',') if item.strip()]
        else:
            self.CORS_ORIGINS = [
                "http://localhost:3000",
                "http://localhost:3001", 
                "http://localhost:3002",
                "http://localhost:3003",
                "http://localhost:3004"
            ]
        
        self.ALLOWED_HOSTS = ["*"]
        
        # Service Ports
        self.AUTH_SERVICE_PORT = int(os.getenv("AUTH_SERVICE_PORT", "8001"))
        
        # API Service Integration
        self.API_SERVICE_URL = os.getenv("API_SERVICE_URL", "http://localhost:8000")
        
        # Email Configuration (for password reset)
        self.SMTP_HOST = os.getenv("SMTP_HOST", "")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
        self.SMTP_TLS = os.getenv("SMTP_TLS", "true").lower() == "true"
        self.FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@erp-system.gr")
        
        # Greek Localization
        self.DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Europe/Athens")
        self.DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "el")
        self.DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "EUR")


# Global settings instance
settings = Settings() 