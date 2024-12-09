"""
Test suite for Database functionality
"""
import unittest
import os
import sqlite3
from pathlib import Path
from modules.database import initialize_database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_db_dir = Path('test_database')
        self.test_db_dir.mkdir(exist_ok=True)
        self.original_cwd = os.getcwd()
        os.chdir(self.test_db_dir)

    def test_database_initialization(self):
        """Test that the database is initialized correctly"""
        conn = initialize_database()
        self.assertIsInstance(conn, sqlite3.Connection)
        
        # Check if database file was created
        self.assertTrue(Path('database/my_pyqt_app.db').exists())
        
        # Check if tables were created
        cursor = conn.cursor()
        tables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [table[0] for table in tables]
        self.assertIn('settings', table_names)
        
        conn.close()

    def test_database_connection_error(self):
        """Test database initialization with invalid path"""
        # Create a file where the database directory should be
        Path('database').touch()
        
        with self.assertRaises(Exception) as context:
            initialize_database()
        
        self.assertIn("Failed to initialize database", str(context.exception))
        
        # Clean up
        Path('database').unlink()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        if self.test_db_dir.exists():
            for file in self.test_db_dir.glob('**/*'):
                if file.is_file():
                    file.unlink()
            for dir in reversed(list(self.test_db_dir.glob('**/*'))):
                if dir.is_dir():
                    dir.rmdir()
            self.test_db_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
