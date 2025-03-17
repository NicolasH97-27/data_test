import pandas as pd
import sqlite3

DB_PATH = "marketing_campaigns.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

datasets = {
    "campaigns": "kaggle_dataset/campaigns.csv",
    "client_first_purchase_date": "kaggle_dataset/client_first_purchase_date.csv",
    "holidays": "kaggle_dataset/holidays.csv",
    "messages_demo": "kaggle_dataset/messages-demo.csv"
}

for table, file in datasets.items():
    print(f"📥 Cargando datos en {table} desde {file} ...")
    
    df = pd.read_csv(file, dtype=str) 


    for col in df.columns:
        if "date" in col or "at" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce").astype(str)  
        elif df[col].str.replace('.', '', 1).str.isnumeric().all():  
            df[col] = df[col].astype(float)
        elif df[col].str.isnumeric().all():  
            df[col] = df[col].astype(int)

   
    values = [tuple(row) for row in df.to_records(index=False)]

    # Crear placeholders dinámicos para SQLite
    placeholders = ", ".join(["?"] * len(df.columns))


    query = f"INSERT OR REPLACE INTO {table} VALUES ({placeholders})"

    try:
        cursor.executemany(query, values)  # Inserción en batch
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"⚠️ Error en la tabla {table}: {e}")

conn.close()
print("✅ Datos cargados exitosamente en SQLite.")
