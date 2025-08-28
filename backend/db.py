from psycopg2.pool import SimpleConnectionPool
import psycopg2, os

_POOL: SimpleConnectionPool | None = None

def init_pool():
    global _POOL
    if _POOL:
        return _POOL
    _POOL = SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host="127.0.0.1",
        port=5432,
        user="vhub",
        password="password123",
        dbname="cmu_db",
        connect_timeout=5,
    )
    return _POOL

def get_conn():
    pool = init_pool()
    return pool.getconn()

def put_conn(conn):
    pool = init_pool()
    pool.putconn(conn)
