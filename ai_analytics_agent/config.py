import os
from dotenv import load_dotenv

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# -----------------------------------
# Config
# Single session, this code is not
# configured for multi-threading or
#   multiple concurrent executions.
# -----------------------------------

load_dotenv()


class AppSettings:
    # Environment variables
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
    SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
    PRIVATE_KEY_PATH = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    PRIVATE_KEY_PASSPHRASE = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")

    if not all(
        [
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_USER,
            SNOWFLAKE_WAREHOUSE,
            SNOWFLAKE_DATABASE,
            SNOWFLAKE_SCHEMA,
            SNOWFLAKE_ROLE,
            PRIVATE_KEY_PATH,
            PRIVATE_KEY_PASSPHRASE,
        ]
    ):
        raise Exception(
            "Missing one or more required environment variables for Snowflake connection."
        )

    # Load private key
    with open(PRIVATE_KEY_PATH or "", "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=(PRIVATE_KEY_PASSPHRASE or "").encode(),
            backend=default_backend(),
        )

    # Convert private key to DER format required by Snowflake
    private_key = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # postgress connection
    # Fetch configurations safely from the OS environment
    postgress_conn_params = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    # pgvector embedding configuration
    EMBEDDING_DIMENSION = 384  # all-MiniLM-L6-v2 output size
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Create a single global configuration object
settings = AppSettings()
