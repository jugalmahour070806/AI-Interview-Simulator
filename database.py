
import sqlite3

DB_NAME = "interview_data.db"


def create_table():
    """Create database table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            question TEXT,
            answer TEXT,
            confidence_score REAL,
            accuracy_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_interview_result(
    role, question, answer,
    confidence_score=0, accuracy_score=0
):
    """Save interview answer and scores."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interview_results
        (role, question, answer, confidence_score, accuracy_score)
        VALUES (?, ?, ?, ?, ?)
    """, (
        role, question, answer,
        confidence_score, accuracy_score
    ))

    conn.commit()
    conn.close()


def get_interview_results():
    """Fetch all saved interview results."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM interview_results
        ORDER BY created_at DESC
    """)

    results = cursor.fetchall()
    conn.close()

    return results
