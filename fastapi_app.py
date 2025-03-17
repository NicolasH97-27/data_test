from fastapi import FastAPI, Query, HTTPException
import requests
import sqlite3
from pydantic import BaseModel
import os
from dotenv import load_dotenv

app = FastAPI()

# 📌 Configurar conexión con Typesense
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")

if not TYPESENSE_API_KEY:
    raise ValueError("La API key de Typesense no está configurada correctamente.")

TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

# 📌 Configurar conexión con SQLite
DB_PATH = "airbnb_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 📌 Modelos para cada tabla
class Campaign(BaseModel):
    id: int
    campaign_type: str
    channel: str
    topic: str
    started_at: str
    finished_at: str
    total_count: int
    ab_test: str
    warmup_mode: str
    hour_limit: int
    subject_length: int
    subject_with_personalization: str
    subject_with_deadline: str
    subject_with_emoji: str
    subject_with_bonuses: str
    subject_with_discount: str
    subject_with_saleout: str
    is_test: str
    position: int

class ClientFirstPurchase(BaseModel):
    client_id: int
    first_purchase_date: str

class Holiday(BaseModel):
    date: str
    holiday: str

class Message(BaseModel):
    id: int
    message_id: int
    campaign_id: int
    message_type: str
    client_id: int
    channel: str
    category: str
    platform: str
    email_provider: str
    stream: str
    date: str
    sent_at: str
    is_opened: int
    opened_first_time_at: str
    opened_last_time_at: str
    is_clicked: int
    clicked_first_time_at: str
    clicked_last_time_at: str
    is_unsubscribed: int
    unsubscribed_at: str
    is_hard_bounced: int
    hard_bounced_at: str
    is_soft_bounced: int
    soft_bounced_at: str
    is_complained: int
    complained_at: str
    is_blocked: int
    blocked_at: str
    is_purchased: int
    purchased_at: str
    created_at: str
    updated_at: str

# 📌 ENDPOINTS PARA CRUD (Todas las tablas)

## ✅ 1️⃣ - Obtener registros

@app.get("/campaigns")
def get_campaigns():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM campaigns LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in data]

@app.get("/clients")
def get_clients():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM client_first_purchase_date LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in data]

@app.get("/holidays")
def get_holidays():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM holidays LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in data]

@app.get("/messages")
def get_messages():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM messages_demo LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in data]

## ✅ 2️⃣ - Buscar en Typesense

@app.get("/search")
def search_campaigns(
    q: str = Query("*", description="Search query"),
    topic: str = Query(None, description="Filter by topic"),
    channel: str = Query(None, description="Filter by channel"),
    max_count: int = Query(None, description="Maximum total_count"),
    sort_by_count: bool = Query(False, description="Sort results by total_count ascending")
):
    """Buscar campañas en Typesense con filtros."""
    filters = []
    if topic:
        filters.append(f"topic:={topic}")
    if channel:
        filters.append(f"channel:={channel}")
    if max_count:
        filters.append(f"total_count:<{max_count}")

    filter_by = " && ".join(filters) if filters else None

    params = {
        "q": q,
        "query_by": "campaign_type,topic",
        "filter_by": filter_by,
        "sort_by": "total_count:asc" if sort_by_count else None,
    }
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(f"{TYPESENSE_HOST}/collections/campaigns/documents/search", 
                            headers=HEADERS, params=params)
    return response.json()

## ✅ 3️⃣ - Crear un nuevo registro

@app.post("/campaigns")
def create_campaign(campaign: Campaign):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO campaigns VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (campaign.id, campaign.campaign_type, campaign.channel, campaign.topic, campaign.started_at,
              campaign.finished_at, campaign.total_count, campaign.ab_test, campaign.warmup_mode,
              campaign.hour_limit, campaign.subject_length, campaign.subject_with_personalization,
              campaign.subject_with_deadline, campaign.subject_with_emoji, campaign.subject_with_bonuses,
              campaign.subject_with_discount, campaign.subject_with_saleout, campaign.is_test, campaign.position))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Campaign with this ID already exists.")
    finally:
        conn.close()
    return {"message": "Campaign created successfully."}

## ✅ 4️⃣ - Actualizar un registro

@app.put("/campaigns/{id}")
def update_campaign(id: int, campaign: Campaign):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE campaigns SET campaign_type = ?, channel = ?, topic = ?, started_at = ?, finished_at = ?, 
        total_count = ?, ab_test = ?, warmup_mode = ?, hour_limit = ?, subject_length = ?, 
        subject_with_personalization = ?, subject_with_deadline = ?, subject_with_emoji = ?, 
        subject_with_bonuses = ?, subject_with_discount = ?, subject_with_saleout = ?, is_test = ?, 
        position = ? WHERE id = ?
    """, (campaign.campaign_type, campaign.channel, campaign.topic, campaign.started_at,
          campaign.finished_at, campaign.total_count, campaign.ab_test, campaign.warmup_mode,
          campaign.hour_limit, campaign.subject_length, campaign.subject_with_personalization,
          campaign.subject_with_deadline, campaign.subject_with_emoji, campaign.subject_with_bonuses,
          campaign.subject_with_discount, campaign.subject_with_saleout, campaign.is_test, campaign.position, id))
    conn.commit()
    conn.close()
    return {"message": "Campaign updated successfully."}

## ✅ 5️⃣ - Eliminar un registro

@app.delete("/campaigns/{id}")
def delete_campaign(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM campaigns WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Campaign deleted successfully."}
