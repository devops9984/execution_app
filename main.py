from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import create_tables, get_connection, get_dict_cursor


app = FastAPI(title="Execution App")


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

create_tables()


# =========================================================
# DATA MODELS
# =========================================================

class PositiveExecution(BaseModel):
    title: str
    what_i_did: str
    old_pattern_defeated: str | None = None
    what_worked: str | None = None


class Pattern(BaseModel):
    old_pattern: str
    counter_thought: str
    my_response: str | None = None
    next_execution: str | None = None


class GrowthExecution(BaseModel):
    title: str
    why_i_want_to_try: str | None = None
    action: str
    experience: str | None = None
    what_i_learned: str | None = None
    would_repeat: bool = False
    next_growth_execution: str | None = None


class NextExecution(BaseModel):
    execution_type: str
    source_id: int | None = None
    action: str
    reason: str | None = None


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Execution App is running!",
        "status": "success"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# 1. POSITIVE EXECUTIONS
# =========================================================

@app.post("/positive-executions")
def create_positive_execution(execution: PositiveExecution):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO positive_executions
        (
            title,
            what_i_did,
            old_pattern_defeated,
            what_worked
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (
        execution.title,
        execution.what_i_did,
        execution.old_pattern_defeated,
        execution.what_worked
    ))

    execution_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Positive execution created successfully",
        "id": execution_id
    }


@app.get("/positive-executions")
def get_positive_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    cursor.execute("""
        SELECT *
        FROM positive_executions
        ORDER BY created_at DESC
    """)

    executions = cursor.fetchall()

    cursor.close()
    connection.close()

    return executions


# =========================================================
# 2. OLD PATTERNS
# =========================================================

@app.post("/patterns")
def create_pattern(pattern: Pattern):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO patterns
        (
            old_pattern,
            counter_thought,
            my_response,
            next_execution
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (
        pattern.old_pattern,
        pattern.counter_thought,
        pattern.my_response,
        pattern.next_execution
    ))

    pattern_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Pattern created successfully",
        "id": pattern_id
    }


@app.get("/patterns")
def get_patterns():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    cursor.execute("""
        SELECT *
        FROM patterns
        ORDER BY created_at DESC
    """)

    patterns = cursor.fetchall()

    cursor.close()
    connection.close()

    return patterns


# =========================================================
# 3. GROWTH EXECUTIONS
# =========================================================

@app.post("/growth-executions")
def create_growth_execution(execution: GrowthExecution):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO growth_executions
        (
            title,
            why_i_want_to_try,
            action,
            experience,
            what_i_learned,
            would_repeat,
            next_growth_execution
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        execution.title,
        execution.why_i_want_to_try,
        execution.action,
        execution.experience,
        execution.what_i_learned,
        execution.would_repeat,
        execution.next_growth_execution
    ))

    execution_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Growth execution created successfully",
        "id": execution_id
    }


@app.get("/growth-executions")
def get_growth_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    cursor.execute("""
        SELECT *
        FROM growth_executions
        ORDER BY created_at DESC
    """)

    executions = cursor.fetchall()

    cursor.close()
    connection.close()

    return executions


# =========================================================
# 4. NEXT / RE-EXECUTIONS
# =========================================================

@app.post("/next-executions")
def create_next_execution(execution: NextExecution):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO next_executions
        (
            execution_type,
            source_id,
            action,
            reason,
            status
        )
        VALUES (%s, %s, %s, %s, 'pending')
        RETURNING id
    """, (
        execution.execution_type,
        execution.source_id,
        execution.action,
        execution.reason
    ))

    execution_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Next execution created successfully",
        "id": execution_id
    }


@app.get("/next-executions")
def get_next_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    cursor.execute("""
        SELECT *
        FROM next_executions
        ORDER BY created_at DESC
    """)

    executions = cursor.fetchall()

    cursor.close()
    connection.close()

    return executions


# =========================================================
# PENDING NEXT EXECUTIONS
# =========================================================

@app.get("/next-executions/pending")
def get_pending_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    cursor.execute("""
        SELECT *
        FROM next_executions
        WHERE status = 'pending'
        ORDER BY created_at ASC
    """)

    executions = cursor.fetchall()

    cursor.close()
    connection.close()

    return executions


# =========================================================
# COMPLETE EXECUTION
# =========================================================

@app.put("/next-executions/{execution_id}/complete")
def complete_execution(execution_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM next_executions
        WHERE id = %s
    """, (execution_id,))

    execution = cursor.fetchone()

    if execution is None:

        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    cursor.execute("""
        UPDATE next_executions
        SET
            status = 'completed',
            completed_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (execution_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Execution completed successfully",
        "id": execution_id
    }


# =========================================================
# DELETE / RESET NEXT EXECUTION
# =========================================================

@app.delete("/next-executions/{execution_id}")
def delete_next_execution(execution_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM next_executions
        WHERE id = %s
    """, (execution_id,))

    execution = cursor.fetchone()

    if execution is None:

        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    cursor.execute("""
        DELETE FROM next_executions
        WHERE id = %s
    """, (execution_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Next execution deleted successfully",
        "id": execution_id
    }


# =========================================================
# DASHBOARD SUMMARY
# =========================================================

@app.get("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM positive_executions
    """)
    positive_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM patterns
    """)
    pattern_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM growth_executions
    """)
    growth_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM next_executions
        WHERE status = 'pending'
    """)
    pending_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM next_executions
        WHERE status = 'completed'
    """)
    completed_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "positive_executions": positive_count,
        "patterns": pattern_count,
        "growth_executions": growth_count,
        "pending_next_executions": pending_count,
        "completed_executions": completed_count
    }