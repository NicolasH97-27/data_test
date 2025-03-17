import sqlite3

conn = sqlite3.connect("airbnb_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    host_id INTEGER,
    host_name TEXT,
    neighbourhood TEXT,
    latitude REAL,
    longitude REAL,
    room_type TEXT,
    price INTEGER,
    minimum_nights INTEGER
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS calendar (
    listing_id INTEGER,
    date TEXT,
    available TEXT,
    price TEXT,
    FOREIGN KEY (listing_id) REFERENCES listings (id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER,
    date TEXT,
    reviewer_id INTEGER,
    reviewer_name TEXT,
    comments TEXT,
    FOREIGN KEY (listing_id) REFERENCES listings (id)
)
""")

conn.commit()
conn.close()

print("✅ Base de datos creada con éxito.")
