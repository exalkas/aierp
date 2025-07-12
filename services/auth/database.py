"""
Database connection for Authentication Service
Connects to the same database as API service to access User and Company models
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
import logging
from typing import AsyncGenerator

from config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Convert PostgreSQL URL to asyncpg format
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Create async database engine
engine = create_async_engine(
    database_url,
    poolclass=StaticPool if "sqlite" in database_url else None,
    echo=settings.ENVIRONMENT == "development"
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create base class for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database dependency injection
    Provides async database session for endpoints
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_database():
    """
    Initialize database connection
    Called at service startup
    """
    try:
        # Test database connection
        from sqlalchemy import text
        async with engine.begin() as connection:
            result = await connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

async def close_database():
    """
    Close database connections
    Called at service shutdown
    """
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}") 