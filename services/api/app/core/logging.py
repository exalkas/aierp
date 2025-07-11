"""
Logging configuration for Greek ERP/CRM API Service
Comprehensive logging setup for audit trails and compliance
"""

import logging
import logging.config
import sys
from pathlib import Path

from .config import settings


def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": settings.LOG_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "audit": {
                "format": "%(asctime)s - AUDIT - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "level": settings.LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": sys.stdout
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "filename": "logs/api.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "audit_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "audit",
                "filename": "logs/audit.log",
                "maxBytes": 52428800,  # 50MB
                "backupCount": 10,
                "encoding": "utf-8"
            }
        },
        "loggers": {
            "": {  # Root logger
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "audit": {  # Audit logger
                "level": "INFO",
                "handlers": ["audit_file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "error_file"],
                "propagate": False
            },
            "fastapi": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "sqlalchemy.engine": {
                "level": "WARNING",  # Reduce SQL query logging in production
                "handlers": ["file"],
                "propagate": False
            }
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    logger.info(f"Environment: {settings.ENVIRONMENT}") 