import sqlite3


DATABASE_NAME = "execution_app.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # =========================================================
    # 1. POSITIVE EXECUTIONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positive_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            why_i_want_to_try TEXT,
            action TEXT NOT NULL,
            experience TEXT,
            what_i_learned TEXT,
            would_repeat INTEGER DEFAULT 0,
            next_growth_execution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =========================================================
    # 4. NEXT / RE-EXECUTIONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS next_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_type TEXT NOT NULL,
            source_id INTEGER,
            action TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =========================================================
    # SAVE CHANGES
    # =========================================================

    connection.commit()
    connection.close()