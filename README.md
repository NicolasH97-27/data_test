Airbnb Search System with FastAPI & Typesense

Project Overview:

This project is a search system for Airbnb listings, using:
FastAPI for the REST API.
SQLite as the database.
Typesense as the Vector Database for efficient search queries.
Docker for containerization.

The system allows:
✅ Full CRUD operations on the listings.
✅ Efficient full-text search using Typesense.
✅ REST API with FastAPI.
✅ SQLite database for structured data storage.

python -m venv datenv
source datenv/Scripts/activate     # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Docker for Typesense

Make sure Docker is running, then start Typesense:
docker-compose up -d

5️⃣ Run the FastAPI App

uvicorn fastapi_app:app --reload

Try the API with Swagger UI:👉 http://127.0.0.1:8000/docs

