import sqlite3
import os
import stat

class DatabaseConnector:
    DB_PATH = "instance/Taxi_database.db"

    @classmethod
    def get_connection(cls):
        try:
            # Ensure instance directory exists with proper permissions
            instance_dir = os.path.dirname(cls.DB_PATH)
            if not os.path.exists(instance_dir):
                os.makedirs(instance_dir, mode=0o777)
            
            # If database file exists, ensure it has proper permissions
            if os.path.exists(cls.DB_PATH):
                # Make the file readable and writable by all
                os.chmod(cls.DB_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            
            conn = sqlite3.connect(cls.DB_PATH, timeout=20)  # Added timeout for busy database
            conn.row_factory = sqlite3.Row
            
            # Set journal mode to WAL for better concurrency
            cursor = conn.cursor()
            cursor.execute('PRAGMA journal_mode=WAL')
            cursor.close()
            
            return conn
        except PermissionError as e:
            print(f"Permission denied: {str(e)}")
            print(f"Current file permissions: {oct(os.stat(cls.DB_PATH).st_mode)}")
            print(f"Please check permissions for: {cls.DB_PATH}")
            raise
        except sqlite3.Error as e:
            print(f"Database connection error: {str(e)}")
            raise

    @classmethod
    def execute_query(cls, query, params=None):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"Query execution error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
