import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

# Environment variables
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

PRIVATE_KEY_PATH =  os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
PRIVATE_KEY_PASSPHRASE = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")

print('SNOWFLAKE_ACCOUNT', SNOWFLAKE_ACCOUNT)
# Load private key
with open(PRIVATE_KEY_PATH, "rb") as key_file:
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=PRIVATE_KEY_PASSPHRASE.encode(),
        backend=default_backend(),
    )
print("key file: ", key_file)
# Convert private key to DER format required by Snowflake
private_key = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    account=SNOWFLAKE_ACCOUNT,
    private_key=private_key,
    authenticator="SNOWFLAKE_JWT",
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

cursor = conn.cursor()

try:
    query = """
    SELECT CURRENT_USER(), CURRENT_VERSION()
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:
        print(row)

finally:
    cursor.close()
    conn.close()