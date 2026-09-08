import sqlite3
from pathlib import Path

from app.config import SQLITE_PATH
from app.models import Advisory


def _get_connection():
    db_path = Path(SQLITE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(db_path)


def init_db():
    conn = _get_connection()

    # Crop-specific weather advisory rules
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crop_advisories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT NOT NULL,
            hazard TEXT NOT NULL,
            recommendation TEXT NOT NULL
        )
    """)

    # General disaster/weather safety protocols
    conn.execute("""
        CREATE TABLE IF NOT EXISTS disaster_protocols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hazard TEXT NOT NULL,
            protocol TEXT NOT NULL
        )
    """)

    # User interaction logs
    conn.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT NOT NULL,
            language TEXT,
            location TEXT,
            crop TEXT,
            intent TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed crop advisories only when the table is empty
    crop_count = conn.execute(
        "SELECT COUNT(*) FROM crop_advisories"
    ).fetchone()[0]

    if crop_count == 0:
        crop_data = [
            (
                "cotton",
                "heavy_rain",
                "Ensure proper field drainage and avoid waterlogging."
            ),
            (
                "cotton",
                "heatwave",
                "Provide adequate irrigation and monitor crop stress."
            ),
            (
                "cotton",
                "low_rainfall",
                "Provide supplemental irrigation and monitor soil moisture."
            ),
            (
                "wheat",
                "heavy_rain",
                "Improve drainage and protect harvested grain from moisture."
            ),
            (
                "wheat",
                "coldwave",
                "Protect the crop from frost and monitor for cold injury."
            ),
            (
                "rice",
                "heavy_rain",
                "Maintain drainage and monitor fields for prolonged waterlogging."
            ),
            (
                "rice",
                "heatwave",
                "Maintain adequate water levels and monitor crop stress."
            ),
            (
                "sugarcane",
                "heavy_rain",
                "Maintain drainage and inspect fields for waterlogging."
            ),
            (
                "sugarcane",
                "high_wind",
                "Secure vulnerable plants and monitor for lodging."
            ),
            (
                "groundnut",
                "heavy_rain",
                "Improve drainage to reduce prolonged soil moisture."
            ),
            (
                "groundnut",
                "heatwave",
                "Maintain irrigation and monitor the crop for heat stress."
            ),
            (
                "groundnut",
                "dry_spell",
                "Consider delaying sowing until adequate rainfall is expected."
            ),
            (
                "maize",
                "heavy_rain",
                "Improve field drainage to prevent waterlogging and crop damage."
            ),
        ]

        conn.executemany(
            """
            INSERT INTO crop_advisories
            (crop, hazard, recommendation)
            VALUES (?, ?, ?)
            """,
            crop_data,
        )

    # Seed disaster protocols only when the table is empty
    protocol_count = conn.execute(
        "SELECT COUNT(*) FROM disaster_protocols"
    ).fetchone()[0]

    if protocol_count == 0:
        protocol_data = [
            (
                "flood",
                "Move to safer elevated areas and follow official emergency instructions."
            ),
            (
                "heatwave",
                "Stay hydrated, reduce heat exposure, and follow local advisories."
            ),
            (
                "cyclone",
                "Secure property, avoid exposed areas, and follow official warnings."
            ),
            (
                "high_wind",
                "Secure loose objects and avoid unnecessary outdoor exposure."
            ),
            (
                "coldwave",
                "Protect vulnerable people, livestock, and sensitive crops from cold."
            ),
        ]

        conn.executemany(
            """
            INSERT INTO disaster_protocols
            (hazard, protocol)
            VALUES (?, ?)
            """,
            protocol_data,
        )

    conn.commit()
    conn.close()


def get_advisory(crop: str, hazard: str):
    conn = _get_connection()

    row = conn.execute(
        """
        SELECT crop, hazard, recommendation
        FROM crop_advisories
        WHERE LOWER(crop) = LOWER(?)
          AND LOWER(hazard) = LOWER(?)
        LIMIT 1
        """,
        (crop, hazard),
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return Advisory(
        crop=row[0],
        hazard=row[1],
        recommendation=row[2],
    )


def list_known_crops():
    conn = _get_connection()

    rows = conn.execute(
        """
        SELECT DISTINCT crop
        FROM crop_advisories
        ORDER BY crop
        """
    ).fetchall()

    conn.close()

    return [row[0] for row in rows]


def get_disaster_protocol(hazard: str):
    conn = _get_connection()

    row = conn.execute(
        """
        SELECT hazard, protocol
        FROM disaster_protocols
        WHERE LOWER(hazard) = LOWER(?)
        LIMIT 1
        """,
        (hazard,),
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "hazard": row[0],
        "protocol": row[1],
    }


def list_disaster_protocols():
    conn = _get_connection()

    rows = conn.execute(
        """
        SELECT hazard, protocol
        FROM disaster_protocols
        ORDER BY hazard
        """
    ).fetchall()

    conn.close()

    return [
        {
            "hazard": row[0],
            "protocol": row[1],
        }
        for row in rows
    ]


def log_query(
    message,
    language=None,
    location=None,
    crop=None,
    intent=None,
    response=None,
    user_id=None,
):
    conn = _get_connection()

    conn.execute(
        """
        INSERT INTO query_logs
        (
            user_id,
            message,
            language,
            location,
            crop,
            intent,
            response
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            message,
            language,
            location,
            crop,
            intent,
            response,
        ),
    )

    conn.commit()
    conn.close()


def get_query_logs(limit=50):
    conn = _get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            user_id,
            message,
            language,
            location,
            crop,
            intent,
            response,
            created_at
        FROM query_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "user_id": row[1],
            "message": row[2],
            "language": row[3],
            "location": row[4],
            "crop": row[5],
            "intent": row[6],
            "response": row[7],
            "created_at": row[8],
        }
        for row in rows
    ]
