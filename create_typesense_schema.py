import requests

TYPESENSE_API_KEY = "48fe8dc-2d51-4e61-ba9f-057e835c0e77"
TYPESENSE_HOST = "http://localhost:8108"
HEADERS = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

collections = [
    {
        "name": "airbnb_listings",
        "fields": [
            {"name": "id", "type": "int32"},
            {"name": "name", "type": "string"},
            {"name": "host_id", "type": "int32"},
            {"name": "host_name", "type": "string"},
            {"name": "neighbourhood", "type": "string"},
            {"name": "latitude", "type": "float"},
            {"name": "longitude", "type": "float"},
            {"name": "room_type", "type": "string"},
            {"name": "price", "type": "int32", "sort": True},
            {"name": "minimum_nights", "type": "int32"}
        ]
    },
    {
        "name": "airbnb_calendar",
        "fields": [
            {"name": "listing_id", "type": "int32"},
            {"name": "date", "type": "string"},
            {"name": "available", "type": "string"},
            {"name": "price", "type": "string"}
        ]
    },
    {
        "name": "airbnb_reviews",
        "fields": [
            {"name": "id", "type": "int32"},
            {"name": "listing_id", "type": "int32"},
            {"name": "date", "type": "string"},
            {"name": "reviewer_id", "type": "int32"},
            {"name": "reviewer_name", "type": "string"},
            {"name": "comments", "type": "string"}
        ]
    }
]

for schema in collections:
    COLLECTION_NAME = schema["name"]
    
    # Verificar si la colección ya existe
    response = requests.get(f"{TYPESENSE_HOST}/collections/{COLLECTION_NAME}", headers=HEADERS)
    
    if response.status_code == 200:
        print(f"⚠️ La colección '{COLLECTION_NAME}' ya existe. No es necesario crearla.")
    else:
        print(f"⚠️ La colección '{COLLECTION_NAME}' no existía, se creará desde cero.")
        response = requests.post(f"{TYPESENSE_HOST}/collections", headers=HEADERS, json=schema)
        if response.status_code == 201:
            print(f"✅ Colección '{COLLECTION_NAME}' creada en Typesense.")
        else:
            print(f"❌ Error al crear la colección '{COLLECTION_NAME}':", response.json())
