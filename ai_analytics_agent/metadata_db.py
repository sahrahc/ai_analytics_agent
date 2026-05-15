from contextlib import contextmanager
from psycopg2 import pool
from config import settings

# Initialize pool variable
_pool = None


def init_pool():
    """Initializes the global connection pool."""
    global _pool
    if _pool is None:
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.postgress_conn_params["host"],
            port=settings.postgress_conn_params["port"],
            database=settings.postgress_conn_params["database"],
            user=settings.postgress_conn_params["user"],
            password=settings.postgress_conn_params["password"],
        )


@contextmanager
def get_connection():
    """Context manager to borrow/return connections safely."""
    if _pool is None:
        init_pool()

    # Explicitly catch initialization failures
    if _pool is None:
        raise RuntimeError(
            "Semantic Metadata Postgres database connection pool failed to initialize."
        )

    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)  # Always return connection


def close_pool():
    if _pool:
        _pool.closeall()
