"""
Logging Configuration for API Service
Integrates with the shared structured logger
"""

import sys
import os
from pathlib import Path

# Add the shared utils to Python path if needed
shared_utils_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "shared" / "utils" / "src"
if shared_utils_path.exists():
    sys.path.insert(0, str(shared_utils_path))

try:
    from structured_logger import create_logger, LogLevel
    
    # Create API service logger
    api_logger = create_logger(
        "api-service", 
        version="1.0.0",
        min_level=LogLevel.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else LogLevel.INFO
    )
    
except ImportError:
    # Fallback to basic logging if structured logger not available
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    class FallbackLogger:
        def __init__(self, name):
            self.logger = logging.getLogger(name)
        
        def debug(self, message, context=None):
            self.logger.debug(f"{message} {context or ''}")
        
        def info(self, message, context=None):
            self.logger.info(f"{message} {context or ''}")
        
        def warning(self, message, context=None, error=None):
            self.logger.warning(f"{message} {context or ''}")
        
        def error(self, message, context=None, error=None):
            self.logger.error(f"{message} {context or ''}")
        
        def critical(self, message, context=None, error=None):
            self.logger.critical(f"{message} {context or ''}")
        
        def child(self, context):
            return self
        
        def request_started(self, method, path, context=None):
            import uuid
            request_id = str(uuid.uuid4())
            self.info(f"Request started: {method} {path}", context)
            return request_id
        
        def request_completed(self, request_id, status_code, duration, context=None):
            self.info(f"Request completed: {status_code} ({duration:.2f}s)", context)
    
    api_logger = FallbackLogger("api-service") 