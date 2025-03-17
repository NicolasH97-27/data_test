import requests
import sqlite3
import json


TYPESENSE_API_KEY = "tu_api_key_segura"
TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}


COLLECTIONS = {
    "airbnb_listings": {
        "table": "listings",
        "fields": ["id", "name", "host_id", "host_name", "neighbourhood", "latitude", "longitude", "room_type", "price", "minimum_nights"]
    },
    "airbnb_calendar": {
        "table": "calendar",
        "fields": ["listing_id", "date", "available", "price"]
    },
    "airbnb_reviews": {
        "table": "reviews",
        "fields": ["id", "listing_id", "date", "reviewer_name", "comments"]
    },
}


BATCH_SIZE = 100

def get_db_connection():
    """Conectar a la base de datos SQLite."""
    conn = sqlite3.connect("airbnb_data.db")
    conn.row_factory = sqlite3.Row
    return conn

def fetch_data(table, fields):
    """Obtener datos de una tabla específica."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT {', '.join(fields)} FROM {table} LIMIT 10"  
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def load_data_to_typesense():
    """Carga los datos en Typesense por lotes para evitar bloqueos."""
    for collection, config in COLLECTIONS.items():
        print(f"🚀 Cargando datos en la colección '{collection}' desde la tabla '{config['table']}'...")
        
        # Obtener los datos de la base de datos
        data = fetch_data(config["table"], config["fields"])
        
        if not data:
            print(f"⚠️ No hay datos para cargar en '{collection}'")
            continue
        
        # Enviar datos en batches pequeños
        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i : i + BATCH_SIZE]
            
            response = requests.post(
                f"{TYPESENSE_HOST}/collections/{collection}/documents/import",
                headers=HEADERS,
                data=json.dumps(batch)
            )
            
            print(f"✅ Batch {i // BATCH_SIZE + 1} en '{collection}' cargado: {response.status_code}")

if __name__ == "__main__":
    load_data_to_typesense()
    print("🎉 ¡Carga de datos completada!")
