from contextlib import contextmanager
import psycopg_pool
from langgraph.checkpoint.postgres import PostgresSaver
from config import load_env
import os

# ==== Cargar variable ====
load_env()
DB_URI = os.environ['DB_URI']

# ==== Memoria ====
@contextmanager
def memory_checkpointer():
    with psycopg_pool.ConnectionPool(conninfo=DB_URI) as pool:
        checkpointer = PostgresSaver(pool)
        yield checkpointer