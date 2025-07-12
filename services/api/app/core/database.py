"""
Database configuration for Greek ERP/CRM System
Implements separate database per company architecture
"""

import logging
from typing import Dict, Optional
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import asyncio
import asyncpg

from .config import settings

logger = logging.getLogger(__name__)

# Base class for all models
Base = declarative_base()

# Database engines cache for company-specific databases
_engines: Dict[str, any] = {}
_session_makers: Dict[str, any] = {}

# Default metadata for schema creation
metadata = MetaData()


class DatabaseManager:
    """Manages separate databases per company with connection pooling"""
    
    def __init__(self):
        self.engines = {}
        self.session_makers = {}
        self.master_engine = None
        self.master_session_maker = None
    
    def get_master_engine(self):
        """Get the master database engine for company management"""
        if not self.master_engine:
            self.master_engine = create_engine(
                settings.DATABASE_URL,
                poolclass=QueuePool,
                pool_size=settings.DATABASE_POOL_SIZE,
                max_overflow=settings.DATABASE_MAX_OVERFLOW,
                pool_pre_ping=True,
                echo=settings.DEBUG
            )
            
            # Add event listeners for Greek character support
            @event.listens_for(self.master_engine, "connect")
            def set_unicode_charset(dbapi_connection, connection_record):
                if "postgresql" in settings.DATABASE_URL:
                    # Ensure UTF-8 encoding for Greek characters
                    with dbapi_connection.cursor() as cursor:
                        cursor.execute("SET CLIENT_ENCODING TO 'UTF8'")
                        cursor.execute("SET timezone = 'Europe/Athens'")
        
        return self.master_engine
    
    def get_master_session_maker(self):
        """Get the master database session maker"""
        if not self.master_session_maker:
            engine = self.get_master_engine()
            self.master_session_maker = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        
        return self.master_session_maker
    
    def get_company_database_url(self, company_id: str) -> str:
        """Generate database URL for a specific company"""
        base_url = settings.DATABASE_URL
        
        # For PostgreSQL, create database name with company ID
        if "postgresql" in base_url:
            # Extract base URL parts
            if "@" in base_url:
                protocol_auth, host_db = base_url.split("@", 1)
                if "/" in host_db:
                    host_port, _ = host_db.split("/", 1)
                    return f"{protocol_auth}@{host_port}/erp_company_{company_id}"
            
        # Fallback: append company ID to database name
        if base_url.endswith("/"):
            return f"{base_url}erp_company_{company_id}"
        else:
            return f"{base_url}_company_{company_id}"
    
    def get_company_engine(self, company_id: str):
        """Get database engine for specific company"""
        if company_id not in self.engines:
            company_db_url = self.get_company_database_url(company_id)
            
            self.engines[company_id] = create_engine(
                company_db_url,
                poolclass=QueuePool,
                pool_size=settings.DATABASE_POOL_SIZE // 2,  # Smaller pool per company
                max_overflow=settings.DATABASE_MAX_OVERFLOW // 2,
                pool_pre_ping=True,
                echo=settings.DEBUG
            )
            
            # Add event listeners for Greek character support
            @event.listens_for(self.engines[company_id], "connect")
            def set_unicode_charset(dbapi_connection, connection_record):
                if "postgresql" in company_db_url:
                    with dbapi_connection.cursor() as cursor:
                        cursor.execute("SET CLIENT_ENCODING TO 'UTF8'")
                        cursor.execute("SET timezone = 'Europe/Athens'")
            
            logger.info(f"Created database engine for company {company_id}")
        
        return self.engines[company_id]
    
    def get_company_session_maker(self, company_id: str):
        """Get session maker for specific company"""
        if company_id not in self.session_makers:
            engine = self.get_company_engine(company_id)
            self.session_makers[company_id] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        
        return self.session_makers[company_id]
    
    async def create_company_database(self, company_id: str) -> bool:
        """Create a new database for a company"""
        try:
            # Connect to master database to create new company database
            if "postgresql" in settings.DATABASE_URL:
                # Extract connection details
                base_url = settings.DATABASE_URL
                if "@" in base_url:
                    protocol_auth, host_db = base_url.split("@", 1)
                    auth_part = protocol_auth.split("://")[1]
                    user_pass = auth_part.split(":")
                    username = user_pass[0]
                    password = user_pass[1] if len(user_pass) > 1 else ""
                    
                    host_port = host_db.split("/")[0]
                    host = host_port.split(":")[0]
                    port = int(host_port.split(":")[1]) if ":" in host_port else 5432
                    
                    # Connect to PostgreSQL master database
                    conn = await asyncpg.connect(
                        host=host,
                        port=port,
                        user=username,
                        password=password,
                        database="postgres"  # Connect to default database
                    )
                    
                    db_name = f"erp_company_{company_id}"
                    
                    # Check if database exists
                    exists = await conn.fetchval(
                        "SELECT 1 FROM pg_database WHERE datname = $1", db_name
                    )
                    
                    if not exists:
                        # Create database with UTF-8 encoding for Greek characters
                        await conn.execute(f"""
                            CREATE DATABASE "{db_name}"
                            WITH ENCODING 'UTF8'
                            LC_COLLATE = 'el_GR.UTF-8'
                            LC_CTYPE = 'el_GR.UTF-8'
                            TEMPLATE = template0
                        """)
                        logger.info(f"Created database for company {company_id}")
                    
                    await conn.close()
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to create database for company {company_id}: {e}")
            return False
        
        return False
    
    @contextmanager
    def get_company_session(self, company_id: str):
        """Get database session for specific company with context management"""
        session_maker = self.get_company_session_maker(company_id)
        session = session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database manager instance
db_manager = DatabaseManager()

# Legacy support - will be deprecated
engine = None
SessionLocal = None


async def create_tables():
    """Create database tables for all registered companies"""
    try:
        # Import all models to register them with SQLAlchemy
        from ..models import (
            Company, User, BusinessEntity, Contact, Product, ProductCategory, 
            ProductAttribute, ProductAttributeValue, ProductVariant, 
            ProductInventory, Invoice, InvoiceItem
        )
        
        # Create master database tables first
        master_engine = db_manager.get_master_engine()
        Base.metadata.create_all(bind=master_engine)
        logger.info("Created master database tables")
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def get_master_db() -> Session:
    """Dependency to get master database session"""
    session_maker = db_manager.get_master_session_maker()
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


def get_company_db(company_id: str) -> Session:
    """Dependency to get company-specific database session"""
    with db_manager.get_company_session(company_id) as session:
        yield session


def get_db_for_company(company_id: str):
    """Helper function to get database session for a specific company"""
    return db_manager.get_company_session(company_id)


def get_db():
    """FastAPI dependency to get database session (uses master DB for now)"""
    session_maker = db_manager.get_master_session_maker()
    db = session_maker()
    try:
        yield db
    finally:
        db.close() 