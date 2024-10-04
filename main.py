from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import databases
import sqlalchemy
from sqlalchemy import create_engine


from DensityMaping.BaseClasses.Business import Business, BusinessType
from DensityMaping.BaseClasses.Point import Point


# Database setup
DATABASE_URL = "sqlite:///./business_areas.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Updated database model with shape_type and business_data
areas = sqlalchemy.Table(
    "areas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("area_type", sqlalchemy.String),
    sqlalchemy.Column("shape_type", sqlalchemy.String),  # 'polygon' or 'circle'
    sqlalchemy.Column("coordinates", sqlalchemy.JSON),
    sqlalchemy.Column("radius", sqlalchemy.Float, nullable=True),  # for circles
    sqlalchemy.Column("missing_businesses", sqlalchemy.JSON),
    sqlalchemy.Column("business_data", sqlalchemy.String),  # new column for additional business info
)

# Create database engine
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Updated Pydantic models
class AreaBase(BaseModel):
    area_type: str
    shape_type: str
    coordinates: List[Dict[str, float]]
    radius: Optional[float] = None
    missing_businesses: List[str]
    business_data: str

class AreaCreate(AreaBase):
    user_id: str

class Area(AreaBase):
    id: int
    user_id: str

# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/areas/", response_model=Area)
async def create_area(area: AreaCreate):
    query = areas.insert().values(
        user_id=area.user_id,
        area_type=area.area_type,
        shape_type=area.shape_type,
        coordinates=area.coordinates,
        radius=area.radius,
        missing_businesses=area.missing_businesses,
        business_data=area.business_data
    )
    last_record_id = await database.execute(query)
    return {**area.dict(), "id": last_record_id}

@app.get("/areas/{user_id}", response_model=List[Area])
async def get_user_areas(user_id: str):
    query = areas.select().where(areas.c.user_id == user_id)
    return await database.fetch_all(query)

@app.get("/area/{area_id}")
async def get_area(area_id: int):
    query = areas.select().where(areas.c.id == area_id)
    area = await database.fetch_one(query)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)