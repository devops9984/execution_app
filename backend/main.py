from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_tables, get_connection, get_dict_cursor


# =========================================================
# APP
# =========================================================

app = FastAPI(title="Execution App")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
# POSITIVE EXECUTIONS
# =========================================================

@app.post("/positive-executions")
def create_positive_execution(execution: PositiveExecution):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO positive_executions
            (
                title,
                what_i_did,
                old_pattern_defeated,
                what_worked
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                execution.title,
                execution.what_i_did,
                execution.old_pattern_defeated,
                execution.what_worked
            )
        )

        execution_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "message": "Positive execution created successfully",
            "id": execution_id
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


@app.get("/positive-executions")
def get_positive_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        cursor.execute(
            """
            SELECT *
            FROM positive_executions
            ORDER BY created_at DESC
            """
        )

        executions = cursor.fetchall()

        return executions

    finally:

        cursor.close()
        connection.close()


# =========================================================
# PATTERNS
# =========================================================

@app.post("/patterns")
def create_pattern(pattern: Pattern):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # 1. SAVE PATTERN
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO patterns
            (
                old_pattern,
                counter_thought,
                my_response,
                next_execution
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                pattern.old_pattern,
                pattern.counter_thought,
                pattern.my_response,
                pattern.next_execution
            )
        )

        pattern_id = cursor.fetchone()[0]


        # -------------------------------------------------
        # 2. AUTOMATICALLY CREATE NEXT EXECUTION
        # -------------------------------------------------

        if (
            pattern.next_execution
            and pattern.next_execution.strip()
        ):

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
                VALUES (%s, %s, %s, %s, 'pending')
                RETURNING id
                """,
                (
                    "pattern",
                    pattern_id,
                    pattern.next_execution,
                    "Next execution from pattern interruption"
                )
            )

            next_execution_id = cursor.fetchone()[0]

        else:

            next_execution_id = None


        # -------------------------------------------------
        # 3. COMMIT
        # -------------------------------------------------

        connection.commit()


        return {
            "message": "Pattern created successfully",
            "id": pattern_id,
            "next_execution_id": next_execution_id
        }


    except Exception:

        connection.rollback()
        raise


    finally:

        cursor.close()
        connection.close()


@app.get("/patterns")
def get_patterns():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        cursor.execute(
            """
            SELECT *
            FROM patterns
            ORDER BY created_at DESC
            """
        )

        patterns = cursor.fetchall()

        return patterns

    finally:

        cursor.close()
        connection.close()


# =========================================================
# GROWTH EXECUTIONS
# =========================================================

@app.post("/growth-executions")
def create_growth_execution(execution: GrowthExecution):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # 1. SAVE GROWTH EXECUTION
        # -------------------------------------------------

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
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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

        execution_id = cursor.fetchone()[0]


        # -------------------------------------------------
        # 2. AUTOMATICALLY CREATE NEXT GROWTH EXECUTION
        # -------------------------------------------------

        if (
            execution.next_growth_execution
            and execution.next_growth_execution.strip()
        ):

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
                VALUES (%s, %s, %s, %s, 'pending')
                RETURNING id
                """,
                (
                    "growth",
                    execution_id,
                    execution.next_growth_execution,
                    "Next execution from growth execution"
                )
            )

            next_execution_id = cursor.fetchone()[0]

        else:

            next_execution_id = None


        # -------------------------------------------------
        # 3. COMMIT
        # -------------------------------------------------

        connection.commit()


        return {
            "message": "Growth execution created successfully",
            "id": execution_id,
            "next_execution_id": next_execution_id
        }


    except Exception:

        connection.rollback()
        raise


    finally:

        cursor.close()
        connection.close()


@app.get("/growth-executions")
def get_growth_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        cursor.execute(
            """
            SELECT *
            FROM growth_executions
            ORDER BY created_at DESC
            """
        )

        executions = cursor.fetchall()

        return executions

    finally:

        cursor.close()
        connection.close()


# =========================================================
# NEXT EXECUTIONS
# =========================================================

@app.post("/next-executions")
def create_next_execution(execution: NextExecution):

    connection = get_connection()
    cursor = connection.cursor()

    try:

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
            VALUES (%s, %s, %s, %s, 'pending')
            RETURNING id
            """,
            (
                execution.execution_type,
                execution.source_id,
                execution.action,
                execution.reason
            )
        )

        execution_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "message": "Next execution created successfully",
            "id": execution_id
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


@app.get("/next-executions")
def get_next_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        cursor.execute(
            """
            SELECT *
            FROM next_executions
            ORDER BY created_at DESC
            """
        )

        executions = cursor.fetchall()

        return executions

    finally:

        cursor.close()
        connection.close()


# =========================================================
# PENDING NEXT EXECUTIONS
# =========================================================

@app.get("/next-executions/pending")
def get_pending_executions():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        cursor.execute(
            """
            SELECT *
            FROM next_executions
            WHERE status = 'pending'
            ORDER BY created_at ASC
            """
        )

        executions = cursor.fetchall()

        return executions

    finally:

        cursor.close()
        connection.close()


# =========================================================
# COMPLETE NEXT EXECUTION
# =========================================================

@app.put("/next-executions/{execution_id}/complete")
def complete_execution(execution_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # CHECK EXECUTION EXISTS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM next_executions
            WHERE id = %s
            """,
            (execution_id,)
        )

        execution = cursor.fetchone()


        if execution is None:

            raise HTTPException(
                status_code=404,
                detail="Execution not found"
            )


        # -------------------------------------------------
        # MARK AS COMPLETED
        # -------------------------------------------------

        cursor.execute(
            """
            UPDATE next_executions
            SET
                status = 'completed',
                completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (execution_id,)
        )


        connection.commit()


        return {
            "message": "Execution completed successfully",
            "id": execution_id
        }


    except HTTPException:

        connection.rollback()
        raise


    except Exception:

        connection.rollback()
        raise


    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE NEXT EXECUTION
# =========================================================

@app.delete("/next-executions/{execution_id}")
def delete_next_execution(execution_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # CHECK EXECUTION EXISTS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM next_executions
            WHERE id = %s
            """,
            (execution_id,)
        )

        execution = cursor.fetchone()


        if execution is None:

            raise HTTPException(
                status_code=404,
                detail="Execution not found"
            )


        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        cursor.execute(
            """
            DELETE FROM next_executions
            WHERE id = %s
            """,
            (execution_id,)
        )


        connection.commit()


        return {
            "message": "Next execution deleted successfully",
            "id": execution_id
        }


    except HTTPException:

        connection.rollback()
        raise


    except Exception:

        connection.rollback()
        raise


    finally:

        cursor.close()
        connection.close()


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # POSITIVE COUNT
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM positive_executions
            """
        )

        positive_count = cursor.fetchone()[0]


        # -------------------------------------------------
        # PATTERN COUNT
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patterns
            """
        )

        pattern_count = cursor.fetchone()[0]


        # -------------------------------------------------
        # GROWTH COUNT
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM growth_executions
            """
        )

        growth_count = cursor.fetchone()[0]


        # -------------------------------------------------
        # PENDING COUNT
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM next_executions
            WHERE status = 'pending'
            """
        )

        pending_count = cursor.fetchone()[0]


        # -------------------------------------------------
        # COMPLETED COUNT
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM next_executions
            WHERE status = 'completed'
            """
        )

        completed_count = cursor.fetchone()[0]


        # -------------------------------------------------
        # RETURN DASHBOARD
        # -------------------------------------------------

        return {
            "positive_executions": positive_count,
            "patterns": pattern_count,
            "growth_executions": growth_count,
            "pending_next_executions": pending_count,
            "completed_executions": completed_count
        }


    finally:

        cursor.close()
        connection.close()