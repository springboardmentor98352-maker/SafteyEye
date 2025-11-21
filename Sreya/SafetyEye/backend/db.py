# backend/db.py
import sqlite3
from pathlib import Path
from typing import Any, Dict, List
from contextlib import contextmanager
import threading

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / 'detections.db'

# Thread-local storage for connections
_local = threading.local()

def get_conn():
    """Get a thread-local database connection."""
    if not hasattr(_local, 'conn') or _local.conn is None:
        _local.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
    return _local.conn

@contextmanager
def get_db():
    """Context manager for database operations."""
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def init_db():
    """Initialize database schema."""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                camera TEXT DEFAULT 'cam1',
                class TEXT,
                conf REAL,
                x1 REAL,
                y1 REAL,
                x2 REAL,
                y2 REAL,
                image_path TEXT,
                violation_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create index for faster queries
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_detections_ts ON detections(ts DESC)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_detections_violation ON detections(violation_type)
        ''')
    print(f"[DB] Initialized database at {DB_PATH}")

def insert_detection(row: Dict[str, Any]) -> int:
    """Insert a new detection record."""
    with get_db() as conn:
        cursor = conn.execute('''
            INSERT INTO detections (ts, camera, class, conf, x1, y1, x2, y2, image_path, violation_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row.get('ts'),
            row.get('camera', 'cam1'),
            row.get('class'),
            row.get('conf'),
            row.get('x1'),
            row.get('y1'),
            row.get('x2'),
            row.get('y2'),
            row.get('image_path'),
            row.get('violation_type')
        ))
        return cursor.lastrowid

def fetch_recent(limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch recent detections."""
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM detections ORDER BY ts DESC LIMIT ?', 
        (limit,)
    ).fetchall()
    return [dict(r) for r in rows]

def stats_over_time() -> List[Dict[str, Any]]:
    """Get detection counts grouped by hour."""
    conn = get_conn()
    rows = conn.execute('''
        SELECT substr(ts, 1, 13) as hour, count(*) as cnt 
        FROM detections 
        GROUP BY hour 
        ORDER BY hour DESC 
        LIMIT 24
    ''').fetchall()
    return [dict(r) for r in reversed(rows)]

def counts_by_violation() -> List[Dict[str, Any]]:
    """Get counts grouped by violation type."""
    conn = get_conn()
    rows = conn.execute('''
        SELECT violation_type, count(*) as cnt 
        FROM detections 
        WHERE violation_type IS NOT NULL AND violation_type != ''
        GROUP BY violation_type 
        ORDER BY cnt DESC
    ''').fetchall()
    return [dict(r) for r in rows]

def get_detection_by_id(detection_id: int) -> Dict[str, Any] | None:
    """Fetch a single detection by ID."""
    conn = get_conn()
    row = conn.execute(
        'SELECT * FROM detections WHERE id = ?', 
        (detection_id,)
    ).fetchone()
    return dict(row) if row else None

def delete_old_detections(days: int = 30) -> int:
    """Delete detections older than specified days."""
    with get_db() as conn:
        cursor = conn.execute('''
            DELETE FROM detections 
            WHERE created_at < datetime('now', ?)
        ''', (f'-{days} days',))
        return cursor.rowcount