import requests
import os
from dotenv import load_dotenv
# Configuración de Typesense
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")

if not TYPESENSE_API_KEY:
    raise ValueError("La API key de Typesense no está configurada correctamente.")
TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

# Definir los esquemas para las colecciones en Typesense
schemas = [
    {
        "name": "campaigns",
        "fields": [
            {"name": "id", "type": "int32"},
            {"name": "campaign_type", "type": "string"},
            {"name": "channel", "type": "string"},
            {"name": "topic", "type": "string"},
            {"name": "started_at", "type": "string"},
            {"name": "finished_at", "type": "string"},
            {"name": "total_count", "type": "int32"},
            {"name": "ab_test", "type": "bool"},
            {"name": "is_test", "type": "bool"},
        ]
    },
    {
        "name": "client_first_purchase_date",
        "fields": [
            {"name": "client_id", "type": "int32"},
            {"name": "first_purchase_date", "type": "string"}
        ]
    },
    {
        "name": "holidays",
        "fields": [
            {"name": "date", "type": "string"},
            {"name": "holiday", "type": "string"}
        ]
    },
    {
        "name": "messages_demo",
        "fields": [
            {"name": "id", "type": "int32"},
            {"name": "message_id", "type": "int32"},
            {"name": "campaign_id", "type": "int32"},
            {"name": "message_type", "type": "string"},
            {"name": "client_id", "type": "int32"},
            {"name": "channel", "type": "string"},
            {"name": "is_opened", "type": "bool"},
            {"name": "is_clicked", "type": "bool"},
            {"name": "is_purchased", "type": "bool"},
        ]
    }
]

# Crear las colecciones en Typesense
for schema in schemas:
    collection_name = schema["name"]
    url = f"{TYPESENSE_HOST}/collections/{collection_name}"
    
    # Verificar si la colección ya existe
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"⚠️ La colección '{collection_name}' ya existe. Se omitirá la creación.")
    else:
        print(f"📌 Creando colección: {collection_name} ...")
        response = requests.post(f"{TYPESENSE_HOST}/collections", headers=HEADERS, json=schema)
        if response.status_code == 201:
            print(f"✅ Colección '{collection_name}' creada exitosamente.")
        else:
            print(f"❌ Error al crear la colección '{collection_name}': {response.json()}")

print("🚀 Esquema de Typesense configurado.")
