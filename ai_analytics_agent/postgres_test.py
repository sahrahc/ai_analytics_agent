import os
from dotenv import load_dotenv
import psycopg2
from config import settings

# Load environment variables from the .env file
load_dotenv()


def test_connection():

    try:
        # 2. Establish the connection using a context manager
        with psycopg2.connect(
            host=settings.conn_params["host"],
            port=settings.conn_params["port"],
            database=settings.conn_params["database"],
            user=settings.conn_params["user"],
            password=settings.conn_params["password"],
        ) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()

            # Guard clause: Ensure data was actually returned
            if db_version is not None:
                print("✅ Connection successful!")
                print(f"PostgreSQL Version: {db_version[0]}")

    except Exception as error:
        print("❌ Connection failed!")
        print(f"Error details: {error}")

    finally:
        # Clean up
        cursor.close()
        connection.close()


if __name__ == "__main__":
    test_connection()
