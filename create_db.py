import sqlite3

# Conectar a SQLite (crea el archivo si no existe)
conn = sqlite3.connect("marketing_campaigns.db")
cursor = conn.cursor()

# Crear la tabla campaigns

cursor.execute("""
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY,
    campaign_type TEXT,
    channel TEXT,
    topic TEXT,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    total_count INTEGER,
    ab_test BOOLEAN,
    warmup_mode BOOLEAN,
    hour_limit INTEGER,
    subject_length INTEGER, 
    subject_with_personalization BOOLEAN,
    subject_with_deadline BOOLEAN,
    subject_with_emoji BOOLEAN,
    subject_with_bonuses BOOLEAN,
    subject_with_discount BOOLEAN,
    subject_with_saleout BOOLEAN,
    is_test BOOLEAN,
    position INTEGER
)
""")

# Crear la tabla client_first_purchase_date
cursor.execute("""
CREATE TABLE IF NOT EXISTS client_first_purchase_date (
    client_id INTEGER PRIMARY KEY,
    first_purchase_date DATE
)
""")

# Crear la tabla holidays
cursor.execute("""
CREATE TABLE IF NOT EXISTS holidays (
    date DATE PRIMARY KEY,
    holiday TEXT
)
""")

# Crear la tabla messages_demo
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages_demo (
    id INTEGER PRIMARY KEY,
    message_id TEXT,
    campaign_id TEXT,
    message_type TEXT,
    client_id TEXT,
    channel TEXT,
    category TEXT,
    platform TEXT,
    email_provider TEXT,
    stream TEXT,
    date TIMESTAMP,
    sent_at TIMESTAMP,
    is_opened BOOLEAN,
    opened_first_time_at TIMESTAMP,
    opened_last_time_at TIMESTAMP,
    is_clicked BOOLEAN,
    clicked_first_time_at TIMESTAMP,
    clicked_last_time_at TIMESTAMP,
    is_unsubscribed BOOLEAN,
    unsubscribed_at TIMESTAMP,
    is_hard_bounced BOOLEAN,
    hard_bounced_at TIMESTAMP,
    is_soft_bounced BOOLEAN,
    soft_bounced_at TIMESTAMP,
    is_complained BOOLEAN,
    complained_at TIMESTAMP,
    is_blocked BOOLEAN,
    blocked_at TIMESTAMP,
    is_purchased BOOLEAN,
    purchased_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
    FOREIGN KEY (client_id) REFERENCES client_first_purchase_date (client_id)
)
""")

conn.commit()
conn.close()

print("✅ Base de datos y tablas creadas con éxito.")
