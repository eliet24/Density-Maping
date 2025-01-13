import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from starlette.responses import FileResponse
from fastapi.responses import FileResponse

app = FastAPI(debug=True)  # Enable debug mode for better error details
app.mount("/static", StaticFiles(directory="."), name="static")  # Serve static files under /static

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models
class Location(BaseModel):
    latitude: float
    longitude: float
    name: str
    location_type: str
    project_code: str

class Project(BaseModel):
    name: str
    address: str
    code: str

# SQLite Database Initialization
DATABASE_FILE = "locations.db"

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Create locations table if it doesn't exist
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
    # Create projects table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def serve_project_registration():
    """Serve the project_registration.html file."""
    return FileResponse("project_registration.html")

@app.get("/index/")
async def serve_index():
    """Serve the index.html file."""
    return FileResponse("index.html")

@app.get("/download_db/")
async def download_db():
    """Provide the SQLite database file for download."""
    return FileResponse("locations.db", media_type="application/octet-stream", filename="locations.db")


# Serve the index.html file directly for the root URL
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/save_location/")
async def save_location(location: Location):
    """Save location data to the locations table."""
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

@app.post("/save_project/")
async def save_project(project: Project):
    """Save project data to the projects table."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, address, code) VALUES (?, ?, ?)",
            (project.name, project.address, project.code)
        )
        conn.commit()
        conn.close()
        return {"message": "Project saved successfully"}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}

@app.get("/get_latest_project_code/")
async def get_latest_project_code():
    """Retrieve the latest project_code from the projects table."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM projects ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            return {"project_code": result[0]}
        else:
            return {"error": "No project found"}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

