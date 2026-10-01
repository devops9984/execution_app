from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_tables, get_connection


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Execution App",
    version="1.0.0"
)


# =========================================================
# CORS
# Allows frontend running on localhost:5500
# to communicate with FastAPI
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


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
def create_positive_execution(
    execution: PositiveExecution
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO positive_executions
        (
            title,
            what_i_did,
            old_pattern_defeated,
            what_worked
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            execution.title,
            execution.what_i_did,
            execution.old_pattern_defeated,
            execution.what_worked
        )
    )

    connection.commit()

    execution_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Positive execution created successfully",
        "id": execution_id
    }


@app.get("/positive-executions")
def get_positive_executions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM positive_executions
        ORDER BY created_at DESC
        """
    )

    executions = cursor.fetchall()

    connection.close()

    return [
        dict(execution)
        for execution in executions
    ]


# =========================================================
# 2. OLD PATTERNS
# =========================================================

@app.post("/patterns")
def create_pattern(
    pattern: Pattern
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO patterns
        (
            old_pattern,
            counter_thought,
            my_response,
            next_execution
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            pattern.old_pattern,
            pattern.counter_thought,
            pattern.my_response,
            pattern.next_execution
        )
    )

    connection.commit()

    pattern_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Pattern created successfully",
        "id": pattern_id
    }


@app.get("/patterns")
def get_patterns():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM patterns
        ORDER BY created_at DESC
        """
    )

    patterns = cursor.fetchall()

    connection.close()

    return [
        dict(pattern)
        for pattern in patterns
    ]


# =========================================================
# 3. GROWTH EXECUTIONS
# =========================================================

@app.post("/growth-executions")
def create_growth_execution(
    execution: GrowthExecution
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
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
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            execution.title,
            execution.why_i_want_to_try,
            execution.action,
            execution.experience,
            execution.what_i_learned,
            execution.would_repeat,
            execution.next_growth_execution
        )
    )

    connection.commit()

    execution_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Growth execution created successfully",
        "id": execution_id
    }


@app.get("/growth-executions")
def get_growth_executions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM growth_executions
        ORDER BY created_at DESC
        """
    )

    executions = cursor.fetchall()

    connection.close()

    return [
        dict(execution)
        for execution in executions
    ]


# =========================================================
# 4. NEXT / RE-EXECUTIONS
# =========================================================

@app.post("/next-executions")
def create_next_execution(
    execution: NextExecution
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO next_executions
        (
            execution_type,
            source_id,
            action,
            reason,
            status
        )
        VALUES (?, ?, ?, ?, 'pending')
        """,
        (
            execution.execution_type,
            execution.source_id,
            execution.action,
            execution.reason
        )
    )

    connection.commit()

    execution_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Next execution created successfully",
        "id": execution_id
    }


@app.get("/next-executions")
def get_next_executions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM next_executions
        ORDER BY created_at DESC
        """
    )

    executions = cursor.fetchall()

    connection.close()

    return [
        dict(execution)
        for execution in executions
    ]


# =========================================================
# PENDING NEXT EXECUTIONS
# =========================================================

@app.get("/next-executions/pending")
def get_pending_executions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM next_executions
        WHERE status = 'pending'
        ORDER BY created_at ASC
        """
    )

    executions = cursor.fetchall()

    connection.close()

    return [
        dict(execution)
        for execution in executions
    ]


# =========================================================
# COMPLETE NEXT EXECUTION
# =========================================================

@app.put("/next-executions/{execution_id}/complete")
def complete_execution(
    execution_id: int
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM next_executions
        WHERE id = ?
        """,
        (execution_id,)
    )

    execution = cursor.fetchone()

    if execution is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    cursor.execute(
        """
        UPDATE next_executions
        SET
            status = 'completed',
            completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (execution_id,)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Execution completed successfully",
        "id": execution_id
    }


# =========================================================
# DELETE NEXT EXECUTION
# =========================================================

@app.delete("/next-executions/{execution_id}")
def delete_next_execution(
    execution_id: int
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM next_executions
        WHERE id = ?
        """,
        (execution_id,)
    )

    execution = cursor.fetchone()

    if execution is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    cursor.execute(
        """
        DELETE FROM next_executions
        WHERE id = ?
        """,
        (execution_id,)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Next execution deleted successfully",
        "id": execution_id
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()


    # Positive executions

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM positive_executions
        """
    )

    positive_count = cursor.fetchone()["count"]


    # Patterns

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM patterns
        """
    )

    pattern_count = cursor.fetchone()["count"]


    # Growth executions

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM growth_executions
        """
    )

    growth_count = cursor.fetchone()["count"]


    # Pending executions

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM next_executions
        WHERE status = 'pending'
        """
    )

    pending_count = cursor.fetchone()["count"]


    # Completed executions

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM next_executions
        WHERE status = 'completed'
        """
    )

    completed_count = cursor.fetchone()["count"]


    connection.close()


    return {

        "positive_executions": positive_count,

        "patterns": pattern_count,

        "growth_executions": growth_count,

        "pending_next_executions": pending_count,

        "completed_executions": completed_count

    }