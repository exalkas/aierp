"""
Comprehensive Structured Logging System for Python Services
Supports multilingual applications with proper error tracking
Compatible with PowerShell (no unicode icons)
"""

import logging
import json
import time
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Union
from enum import Enum
import sys
import os


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class StructuredLogger:
    """
    Structured logger with Greek ERP/CRM specific context
    Provides consistent logging across all Python services
    """
    
    def __init__(self, service_name: str, version: str = "1.0.0", min_level: LogLevel = LogLevel.INFO):
        self.service_name = service_name
        self.version = version
        self.min_level = min_level
        self.correlation_id = str(uuid.uuid4())
        
        # Configure Python logging
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(min_level.value)
        
        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(min_level.value)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on minimum level"""
        return level.value >= self.min_level.value
    
    def _create_log_entry(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None,
        duration: Optional[float] = None
    ) -> Dict[str, Any]:
        """Create structured log entry"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.name,
            "message": message,
            "service": self.service_name,
            "version": self.version,
            "correlation_id": self.correlation_id,
            "context": context or {}
        }
        
        if error:
            entry["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            }
        
        if duration is not None:
            entry["performance"] = {
                "duration_ms": round(duration * 1000, 2),
                "memory_mb": self._get_memory_usage()
            }
        
        return entry
    
    def _get_memory_usage(self) -> Optional[float]:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return round(process.memory_info().rss / 1024 / 1024, 2)
        except ImportError:
            return None
    
    def _output_log(self, entry: Dict[str, Any]) -> None:
        """Output log entry to console and external services"""
        level = LogLevel[entry["level"]]
        
        # PowerShell-compatible output (no unicode icons)
        prefix = f"[{entry['timestamp']}] [{entry['level']}] [{entry['service']}]"
        message = f"{prefix} {entry['message']}"
        
        # Add context if present
        if entry.get("context"):
            context_str = json.dumps(entry["context"], default=str)
            message += f" Context: {context_str}"
        
        # Log using Python's logging system
        if level == LogLevel.DEBUG:
            self.logger.debug(message)
        elif level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(message)
        
        # In production, send to external logging service
        if os.getenv("ENVIRONMENT") == "production":
            self._send_to_logging_service(entry)
    
    def _send_to_logging_service(self, entry: Dict[str, Any]) -> None:
        """Send log entry to external logging service"""
        try:
            # Example: Send to ELK stack, Datadog, etc.
            # Implementation depends on your logging infrastructure
            pass
        except Exception:
            # Fail silently to avoid logging loops
            pass
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message"""
        if self._should_log(LogLevel.DEBUG):
            entry = self._create_log_entry(LogLevel.DEBUG, message, context)
            self._output_log(entry)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log info message"""
        if self._should_log(LogLevel.INFO):
            entry = self._create_log_entry(LogLevel.INFO, message, context)
            self._output_log(entry)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None, error: Optional[Exception] = None) -> None:
        """Log warning message"""
        if self._should_log(LogLevel.WARNING):
            entry = self._create_log_entry(LogLevel.WARNING, message, context, error)
            self._output_log(entry)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None, error: Optional[Exception] = None) -> None:
        """Log error message"""
        if self._should_log(LogLevel.ERROR):
            entry = self._create_log_entry(LogLevel.ERROR, message, context, error)
            self._output_log(entry)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None, error: Optional[Exception] = None) -> None:
        """Log critical message"""
        if self._should_log(LogLevel.CRITICAL):
            entry = self._create_log_entry(LogLevel.CRITICAL, message, context, error)
            self._output_log(entry)
    
    def time_operation(self, operation_name: str, context: Optional[Dict[str, Any]] = None):
        """Context manager for timing operations"""
        class TimerContext:
            def __init__(self, logger, operation_name, context):
                self.logger = logger
                self.operation_name = operation_name
                self.context = context or {}
                self.start_time = None
            
            def __enter__(self):
                self.start_time = time.time()
                self.logger.debug(f"Starting: {self.operation_name}", self.context)
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                duration = time.time() - self.start_time
                if exc_type:
                    self.logger.error(
                        f"Failed: {self.operation_name}",
                        {**self.context, "duration_ms": round(duration * 1000, 2)},
                        exc_val
                    )
                else:
                    self.logger.info(
                        f"Completed: {self.operation_name}",
                        {**self.context, "duration_ms": round(duration * 1000, 2)}
                    )
        
        return TimerContext(self, operation_name, context)
    
    def request_started(self, method: str, path: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Log request start and return request ID"""
        request_id = str(uuid.uuid4())
        self.info(f"Request started: {method} {path}", {
            **(context or {}),
            "request_id": request_id,
            "method": method,
            "path": path
        })
        return request_id
    
    def request_completed(
        self,
        request_id: str,
        status_code: int,
        duration: float,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log request completion"""
        self.info(f"Request completed: {status_code}", {
            **(context or {}),
            "request_id": request_id,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2)
        })
    
    def auth_success(self, user_id: str, method: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log successful authentication"""
        self.info(f"Authentication successful: {method}", {
            **(context or {}),
            "user_id": user_id,
            "auth_method": method
        })
    
    def auth_failure(self, email: str, reason: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log authentication failure"""
        self.warning(f"Authentication failed: {reason}", {
            **(context or {}),
            "email": email,
            "failure_reason": reason
        })
    
    def business_operation(self, operation: str, entity: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log business operation"""
        self.info(f"Business operation: {operation} {entity}", {
            **(context or {}),
            "operation": operation,
            "entity": entity
        })
    
    def greek_compliance(self, event: str, entity: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log Greek compliance event"""
        self.info(f"Greek compliance: {event}", {
            **(context or {}),
            "compliance_event": event,
            "entity": entity
        })
    
    def database_operation(self, operation: str, table: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log database operation"""
        self.debug(f"Database: {operation} {table}", {
            **(context or {}),
            "db_operation": operation,
            "table": table
        })
    
    def child(self, additional_context: Dict[str, Any]) -> 'StructuredLogger':
        """Create child logger with additional context"""
        child = StructuredLogger(self.service_name, self.version, self.min_level)
        child.correlation_id = self.correlation_id
        
        # Store additional context for all log calls
        original_create_entry = child._create_log_entry
        
        def enhanced_create_entry(level, message, context=None, error=None, duration=None):
            enhanced_context = {**additional_context, **(context or {})}
            return original_create_entry(level, message, enhanced_context, error, duration)
        
        child._create_log_entry = enhanced_create_entry
        return child


# Global logger instances
def create_logger(service_name: str, version: str = "1.0.0", min_level: LogLevel = LogLevel.INFO) -> StructuredLogger:
    """Create a new structured logger instance"""
    return StructuredLogger(service_name, version, min_level)


# Default loggers for services
auth_logger = create_logger("auth-service")
api_logger = create_logger("api-service")
files_logger = create_logger("files-service")
integrations_logger = create_logger("integrations-service")


# Decorator for automatic function logging
def log_function_call(logger: StructuredLogger, log_args: bool = False):
    """Decorator to automatically log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            context = {"function": func.__name__}
            if log_args:
                context["args"] = str(args)
                context["kwargs"] = str(kwargs)
            
            with logger.time_operation(f"Function: {func.__name__}", context):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Exception handler for FastAPI
def log_exception(logger: StructuredLogger, exc: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """Log exception with full context"""
    logger.error(f"Unhandled exception: {type(exc).__name__}", context, exc) 