"""
Database module for PyQt6ify Pro.
"""

import os
import sqlite3
from loguru import logger
from modules.config.config import Config

class Database:
    """Database class for PyQt6ify Pro."""

    def __init__(self, config: Config):
        """Initialize the database."""
        self.config = config
        self.db_path = os.path.join(os.path.dirname(__file__), 'pyqt6ify.db')
        self.connection = None
        self.cursor = None

        # Initialize database
        self.init_db()

    def init_db(self):
        """Initialize the database connection and tables."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

            # Create tables if they don't exist
            self.create_tables()

            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")

    def create_tables(self):
        """Create database tables."""
        try:
            # Create settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')

            # Create themes table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS themes (
                    name TEXT PRIMARY KEY,
                    data TEXT
                )
            ''')

            self.connection.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
