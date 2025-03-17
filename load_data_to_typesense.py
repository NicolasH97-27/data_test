import sqlite3
import requests
import os
from dotenv import load_dotenv


# Configurar Typesense
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")

if not TYPESENSE_API_KEY:
    raise ValueError("La API key de Typesense no está configurada correctamente.")
TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

DB_PATH = "marketing_campaigns.db"

def load_table_to_typesense(table_name):
    """Carga datos de una tabla SQLite a Typesense."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"🚀 Cargando datos de {table_name} en Typesense...")

    # Obtener todos los datos de la tabla
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    # Convertir los datos en formato JSON para Typesense
    documents = []
    for row in rows:
        doc = {columns[i]: row[i] for i in range(len(columns))}
        documents.append(doc)

    # Insertar los datos en Typesense
    url = f"{TYPESENSE_HOST}/collections/{table_name}/documents/import"
    response = requests.post(url, headers=HEADERS, json=documents)

    if response.status_code == 200:
        print(f"✅ Datos de {table_name} cargados en Typesense.")
    else:
        print(f"❌ Error al cargar {table_name}: {response.json()}")

    conn.close()

# Cargar cada tabla en Typesense
for table in ["campaigns", "client_first_purchase_date", "holidays", "messages_demo"]:
    load_table_to_typesense(table)

print("🎉 Todos los datos han sido cargados en Typesense.")
