import os
import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv

load_dotenv()

class SessionManager:
    def __init__(self):
        self.db_path = "sessions.db"  # Use SQLite database file
        self.init_db()

    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn

    def init_db(self):
        """Initialize database tables if they don't exist"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                citations TEXT,
                selected_text TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=24)  # 24-hour session timeout

        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (session_id, user_id, created_at, updated_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_id, datetime.utcnow(), datetime.utcnow(), expires_at))

        conn.commit()
        cursor.close()
        conn.close()

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM sessions WHERE session_id = ? AND expires_at > ?
        """, (session_id, datetime.utcnow()))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return dict(result) if result else None

    def save_message(self, session_id: str, role: str, content: str,
                    citations: Optional[List[Dict[str, Any]]] = None,
                    selected_text: Optional[str] = None):
        """Save a message to the session"""
        message_id = str(uuid.uuid4())

        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Convert citations to JSON string for SQLite
        import json
        citations_json = json.dumps(citations) if citations else None

        cursor.execute("""
            INSERT INTO messages (message_id, session_id, role, content, timestamp, citations, selected_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (message_id, session_id, role, content, datetime.utcnow(),
              citations_json, selected_text))

        # Update session's updated_at timestamp
        cursor.execute("""
            UPDATE sessions SET updated_at = ? WHERE session_id = ?
        """, (datetime.utcnow(), session_id))

        conn.commit()
        cursor.close()
        conn.close()

    def get_session_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get message history for a session"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT role, content, timestamp, citations, selected_text
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Parse JSON citations back to objects
        import json
        history = []
        for row in results:
            row_dict = dict(row)
            # Parse citations JSON string back to object
            if row_dict['citations']:
                try:
                    row_dict['citations'] = json.loads(row_dict['citations'])
                except (json.JSONDecodeError, TypeError):
                    row_dict['citations'] = None
            history.append(row_dict)

        return history