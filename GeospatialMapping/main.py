import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(debug=True)  # Enable debug mode for better error details

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model
class Location(BaseModel):
    latitude: float
    longitude: float
    name: str
    location_type: str
    project_code: str

# SQLite Database Initialization
DATABASE_FILE = "locations.db"

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            name TEXT NOT NULL,
            location_type TEXT NOT NULL,
            project_code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()

@app.post("/save_location/")
async def save_location(location: Location):
    print(location)  # This will print the data received
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO locations (latitude, longitude, name, location_type, project_code) VALUES (?, ?, ?, ?, ?)",
            (location.latitude, location.longitude, location.name, location.location_type, location.project_code)
        )
        conn.commit()
        conn.close()
        return {"message": "Location saved successfully"}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}
