import pandas as pd
import sqlite3

DB_PATH = "airbnb_data.db"


conn = sqlite3.connect(DB_PATH)

df_listings = pd.read_csv("kaggle_dataset/listings.csv")
df_listings.to_sql("listings", conn, if_exists="replace", index=False)

df_calendar = pd.read_csv("kaggle_dataset/calendar.csv")
df_calendar.to_sql("calendar", conn, if_exists="replace", index=False)

df_reviews = pd.read_csv("kaggle_dataset/reviews.csv")
df_reviews.to_sql("reviews", conn, if_exists="replace", index=False)

conn.close()

print("✅ Datos cargados en SQLite correctamente.")
