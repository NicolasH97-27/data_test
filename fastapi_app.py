from fastapi import FastAPI, Query, HTTPException
import requests
import sqlite3
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Configuración de Typesense
TYPESENSE_API_KEY = "48fe8dc-2d51-4e61-ba9f-057e835c0e77"
TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

DB_PATH = "./airbnb_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class Listing(BaseModel):
    id: int
    name: str
    host_id: int
    host_name: str
    neighbourhood: str
    latitude: float
    longitude: float
    room_type: str
    price: int
    minimum_nights: int

class Calendar(BaseModel):
    listing_id: int
    date: str
    available: str
    price: Optional[int] = None

class Review(BaseModel):
    listing_id: int
    id: int
    date: str
    reviewer_id: int
    reviewer_name: str
    comments: str


@app.get("/listings")
def get_all_listings():
    """Obtener todos los listings de la base de datos."""
    conn = get_db_connection()
    listings = conn.execute("SELECT * FROM listings LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in listings]

@app.get("/listings/{id}")
def get_listing(id: int):
    conn = get_db_connection()
    listing = conn.execute("SELECT * FROM listings WHERE id = ?", (id,)).fetchone()
    conn.close()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found.")
    return dict(listing)

@app.post("/listings")
def create_listing(listing: Listing):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO listings (id, name, host_id, host_name, neighbourhood, latitude, longitude, room_type, price, minimum_nights)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (listing.id, listing.name, listing.host_id, listing.host_name, listing.neighbourhood, 
              listing.latitude, listing.longitude, listing.room_type, listing.price, listing.minimum_nights))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Listing with this ID already exists.")
    finally:
        conn.close()
    return {"message": "Listing created successfully."}

@app.put("/listings/{id}")
def update_listing(id: int, listing: Listing):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE listings SET name = ?, host_id = ?, host_name = ?, neighbourhood = ?, latitude = ?, longitude = ?,
        room_type = ?, price = ?, minimum_nights = ? WHERE id = ?
    """, (listing.name, listing.host_id, listing.host_name, listing.neighbourhood, listing.latitude, 
          listing.longitude, listing.room_type, listing.price, listing.minimum_nights, id))
    conn.commit()
    conn.close()
    return {"message": "Listing updated successfully."}

@app.delete("/listings/{id}")
def delete_listing(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM listings WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Listing deleted successfully."}


@app.get("/calendar")
def get_calendar():
    conn = get_db_connection()
    calendar = conn.execute("SELECT * FROM calendar LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in calendar]

@app.post("/calendar")
def create_calendar_entry(entry: Calendar):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calendar (listing_id, date, available, price)
        VALUES (?, ?, ?, ?)
    """, (entry.listing_id, entry.date, entry.available, entry.price))
    conn.commit()
    conn.close()
    return {"message": "Calendar entry created successfully."}


@app.get("/reviews")
def get_reviews():
    conn = get_db_connection()
    reviews = conn.execute("SELECT * FROM reviews LIMIT 50").fetchall()
    conn.close()
    return [dict(row) for row in reviews]

@app.post("/reviews")
def create_review(review: Review):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (listing_id, id, date, reviewer_id, reviewer_name, comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (review.listing_id, review.id, review.date, review.reviewer_id, review.reviewer_name, review.comments))
    conn.commit()
    conn.close()
    return {"message": "Review created successfully."}

