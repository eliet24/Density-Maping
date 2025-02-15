import uvicorn
import random
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


@app.get("/get_locations/{project_code}")
async def get_locations(project_code: str):
    """Fetch all locations associated with a project code."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT latitude, longitude, name FROM locations WHERE project_code = ?",
            (project_code,)
        )
        rows = cursor.fetchall()
        conn.close()

        locations = [{"latitude": row[0], "longitude": row[1], "name": row[2]} for row in rows]
        return {"locations": locations}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}


@app.get("/generate_project_code/")
async def generate_project_code():
    """Generate a unique project code."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Fetch all existing codes
        cursor.execute("SELECT code FROM projects")
        existing_codes = {row[0] for row in cursor.fetchall()}
        conn.close()

        # Generate a random number between 1 and 999 that is not in existing codes
        while True:
            new_code = str(random.randint(1, 999)).zfill(3)  # Pad with zeros to maintain 3-digit format
            if new_code not in existing_codes:
                break

        return {"project_code": new_code}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}

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

        # Ensure name is always saved as an address, not lat/lng
        location_name = location.name.strip()
        if not location_name or location_name.lower() in ["unnamed location", "unknown address"]:
            location_name = "Unknown Address"

        cursor.execute(
            "INSERT INTO locations (latitude, longitude, name, location_type, project_code) VALUES (?, ?, ?, ?, ?)",
            (location.latitude, location.longitude, location_name, location.location_type, location.project_code)
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

@app.get("/get_project/{project_code}")
async def get_project(project_code: str):
    """Fetch project details by project code."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, address, code FROM projects WHERE code = ?", (project_code,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {"name": row[0], "address": row[1], "code": row[2]}
        else:
            return {"error": "Project not found."}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}


@app.post("/find_project/")
async def find_project(data: dict):
    """Find an existing project by name or code."""
    project_name = data.get("name", "").strip()
    project_code = data.get("code", "").strip()

    if not project_name and not project_code:
        return {"detail": "Either project name or project code must be provided."}

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Search by project name or code
        if project_name:
            cursor.execute("SELECT name, address, code FROM projects WHERE name = ?", (project_name,))
        elif project_code:
            cursor.execute("SELECT name, address, code FROM projects WHERE code = ?", (project_code,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {"name": result[0], "address": result[1], "project_code": result[2]}
        else:
            return {"detail": "Project not found."}
    except Exception as e:
        return {"detail": f"An error occurred: {str(e)}"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)