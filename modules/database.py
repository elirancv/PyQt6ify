import sqlite3
from loguru import logger
import os
from pathlib import Path

def initialize_database():
    """
    Initialize the SQLite database connection and create necessary tables.
    
    Returns:
        sqlite3.Connection: Database connection object
    
    Raises:
        Exception: If database initialization fails
    """
    try:
        # Create database directory if it doesn't exist
        db_dir = Path('database')
        db_dir.mkdir(exist_ok=True)
        
        # Create database connection
        db_path = db_dir / 'my_pyqt_app.db'
        conn = sqlite3.connect(str(db_path))
        logger.info(f"Connected to database: {db_path}")
        
        # Create tables if they don't exist
        with conn:
            cursor = conn.cursor()
            
            # Example table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            
            # Add more table creation statements as needed
            
        logger.info("Database initialization completed successfully")
        return conn
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise Exception(f"Failed to initialize database: {str(e)}")

def main():
    """Legacy main function, kept for backwards compatibility."""
    try:
        return initialize_database()
    except Exception as e:
        logger.error(f"Database main function failed: {str(e)}")
        return None

if __name__ == '__main__':
    main()
