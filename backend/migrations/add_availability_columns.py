import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to Python path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

# Load environment variables
load_dotenv(os.path.join(parent_dir, '.env'))

from sqlalchemy import create_engine, JSON
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('migration_debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL not found in environment variables")
    sys.exit(1)

def check_database_connection(engine):
    """Test database connection"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

def get_existing_columns(connection):
    """Get list of existing columns in restaurants table"""
    try:
        result = connection.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'restaurants' 
            AND COLUMN_NAME IN ('availability', 'booked_slots')
        """))
        existing_columns = {row[0] for row in result}
        logger.info(f"Existing columns found: {existing_columns}")
        return existing_columns
    except SQLAlchemyError as e:
        logger.error(f"Error checking existing columns: {str(e)}")
        raise

def add_column(connection, column_name):
    """Add a new column to the restaurants table"""
    try:
        connection.execute(text(f"""
            ALTER TABLE restaurants
            ADD COLUMN {column_name} JSON
        """))
        logger.info(f"Successfully added {column_name} column")
    except SQLAlchemyError as e:
        logger.error(f"Error adding {column_name} column: {str(e)}")
        raise

def update_existing_rows(connection):
    """Update existing rows with empty arrays"""
    try:
        result = connection.execute(text("""
            UPDATE restaurants 
            SET availability = '[]', booked_slots = '[]'
            WHERE availability IS NULL OR booked_slots IS NULL
        """))
        logger.info(f"Updated {result.rowcount} rows with empty arrays")
    except SQLAlchemyError as e:
        logger.error(f"Error updating existing rows: {str(e)}")
        raise

def migrate():
    logger.info("Starting migration process")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        logger.debug(f"Database URL: {DATABASE_URL}")
        
        # Check database connection
        if not check_database_connection(engine):
            return
        
        # Connect to the database
        with engine.connect() as connection:
            # Get existing columns
            existing_columns = get_existing_columns(connection)
            
            # Add availability column if it doesn't exist
            if 'availability' not in existing_columns:
                add_column(connection, 'availability')
            
            # Add booked_slots column if it doesn't exist
            if 'booked_slots' not in existing_columns:
                add_column(connection, 'booked_slots')
            
            # Update existing rows
            update_existing_rows(connection)
            
            # Commit the changes
            connection.commit()
            logger.info("Migration completed successfully!")
            
    except SQLAlchemyError as e:
        logger.error(f"Migration failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during migration: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        logger.error(f"Migration script failed: {str(e)}")
        sys.exit(1) 