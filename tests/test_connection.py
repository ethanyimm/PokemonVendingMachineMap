import sys
import os

# Add project root to sys.path before importing backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.database import get_db_connection


def test_database_connection():
    """Test that we can connect to the database"""
    print("Testing database connection...")
    connection = get_db_connection()
    if connection:
        print("✅ SUCCESS: Connected to database!")
        connection.close()
        return True
    else:
        print("❌ FAILED: Could not connect to database")
        return False


if __name__ == "__main__":
    test_database_connection()
