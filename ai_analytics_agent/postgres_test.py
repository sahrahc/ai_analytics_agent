import os
from dotenv import load_dotenv
from ai_analytics_agent.metadata_db import get_connection

# Load environment variables from the .env file
load_dotenv()


def test_connection():

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("""SELECT table_name,  table_schema, table_type
FROM information_schema.tables 
""")
            result = cursor.fetchall()

            # print("\nTables in the database:", result)
            # Guard clause: Ensure data was actually returned
            # if db_version is not None:
            #    print("✅ Connection successful!")
            #    print(f"PostgreSQL Version: {db_version[0]}")


if __name__ == "__main__":
    test_connection()
