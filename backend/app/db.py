import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.schemas import CampaignCreate, LeadCreate

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "aura.db"


def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                idea TEXT NOT NULL,
                city TEXT NOT NULL,
                company TEXT NOT NULL,
                package_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT '',
                service TEXT NOT NULL,
                source TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Nuevo',
                created_at TEXT NOT NULL
            );
            """
        )


def create_campaign(payload: CampaignCreate, package: dict):
    created_at = datetime.now().isoformat(timespec="seconds")
    name = package["campaign_name"]
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO campaigns (name, idea, city, company, package_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                payload.idea,
                payload.city,
                payload.company,
                json.dumps(package, ensure_ascii=False),
                created_at,
            ),
        )
        campaign_id = cursor.lastrowid
    return {
        "id": campaign_id,
        "name": name,
        "idea": payload.idea,
        "city": payload.city,
        "company": payload.company,
        "package": package,
        "created_at": created_at,
    }


def list_campaigns():
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, idea, city, company, created_at FROM campaigns ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_campaign(campaign_id: int):
    with connect() as conn:
        row = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    if not row:
        return None
    data = dict(row)
    data["package"] = json.loads(data.pop("package_json"))
    data["flyer_url"] = f"/media/flyer_{campaign_id}.svg"
    return data


def create_lead(payload: LeadCreate):
    created_at = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO leads (name, phone, email, service, source, notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'Nuevo', ?)
            """,
            (
                payload.name,
                payload.phone,
                payload.email,
                payload.service,
                payload.source,
                payload.notes,
                created_at,
            ),
        )
        lead_id = cursor.lastrowid
    return {
        "id": lead_id,
        **payload.model_dump(),
        "status": "Nuevo",
        "created_at": created_at,
    }


def list_leads():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def update_lead_status(lead_id: int, status: str):
    with connect() as conn:
        conn.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    return dict(row) if row else None


def get_dashboard():
    with connect() as conn:
        campaigns = conn.execute("SELECT COUNT(*) AS total FROM campaigns").fetchone()["total"]
        leads = conn.execute("SELECT COUNT(*) AS total FROM leads").fetchone()["total"]
        won = conn.execute(
            "SELECT COUNT(*) AS total FROM leads WHERE status = 'Ganado'"
        ).fetchone()["total"]
        recent_campaigns = conn.execute(
            "SELECT id, name, city, created_at FROM campaigns ORDER BY id DESC LIMIT 5"
        ).fetchall()

    conversion = round((won / leads * 100), 1) if leads else 0
    return {
        "campaigns": campaigns,
        "leads": leads,
        "won": won,
        "conversion": conversion,
        "recent_campaigns": [dict(row) for row in recent_campaigns],
    }
