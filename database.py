import os

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    connection = psycopg2.connect(
        DATABASE_URL
    )

    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # =========================================================
    # 1. POSITIVE EXECUTIONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positive_executions (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            what_i_did TEXT NOT NULL,
            old_pattern_defeated TEXT,
            what_worked TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =========================================================
    # 2. OLD PATTERNS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            id SERIAL PRIMARY KEY,
            old_pattern TEXT NOT NULL,
            counter_thought TEXT NOT NULL,
            my_response TEXT,
            next_execution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =========================================================
    # 3. GROWTH EXECUTIONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS growth_executions (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            why_i_want_to_try TEXT,
            action TEXT NOT NULL,
            experience TEXT,
            what_i_learned TEXT,
            would_repeat BOOLEAN DEFAULT FALSE,
            next_growth_execution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =========================================================
    # 4. NEXT / RE-EXECUTIONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS next_executions (
            id SERIAL PRIMARY KEY,
            execution_type TEXT NOT NULL,
            source_id INTEGER,
            action TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()

    cursor.close()
    connection.close()


def get_dict_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)