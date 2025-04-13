# db.py
# Provides a reusable database connection interface for PostgreSQL.
# This module can be imported by any part of the application that needs to execute SQL queries.

import psycopg2
from app.config import DB_URI

def get_connection():
    """
    Returns a new connection to the PostgreSQL database.
    The caller is responsible for closing the connection.
    """
    return psycopg2.connect(DB_URI)

def get_cursor():
    """
    Returns a cursor and connection pair for executing queries.
    Caller must close both cursor and connection after use.
    """
    conn = get_connection()
    cursor = conn.cursor()
    return cursor, conn
