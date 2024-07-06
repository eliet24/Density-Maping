import os
import sys
import numpy as np
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from BaseClasses.Point import Point
from models import Business, Customer, MapGrid, BusinessType
from schemas import BusinessCreate, CustomerCreate, MapGridCreate
from database import db_businesses, db_customers, db_map_grids
from auth import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure the templates directory
templates = Jinja2Templates(directory="templates")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Root endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Token endpoint
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD operations for Business
@app.post("/businesses/", response_model=Business)
def create_business(business: BusinessCreate, token: str = Depends(oauth2_scheme)):
    db_businesses[business.business_id] = business
    return business

@app.get("/businesses/{business_id}", response_model=Business)
def read_business(business_id: int, token: str = Depends(oauth2_scheme)):
    if business_id in db_businesses:
        return db_businesses[business_id]
    raise HTTPException(status_code=404, detail="Business not found")

@app.put("/businesses/{business_id}", response_model=Business)
def update_business(business_id: int, business: BusinessCreate, token: str = Depends(oauth2_scheme)):
    if business_id in db_businesses:
        db_businesses[business_id] = business
        return business
    raise HTTPException(status_code=404, detail="Business not found")

@app.delete("/businesses/{business_id}")
def delete_business(business_id: int, token: str = Depends(oauth2_scheme)):
    if business_id in db_businesses:
        del db_businesses[business_id]
        return {"detail": "Business deleted"}
    raise HTTPException(status_code=404, detail="Business not found")

# CRUD operations for Customer
@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, token: str = Depends(oauth2_scheme)):
    db_customers[customer.cust_id] = customer
    return customer

@app.get("/customers/{cust_id}", response_model=Customer)
def read_customer(cust_id: str, token: str = Depends(oauth2_scheme)):
    if cust_id in db_customers:
        return db_customers[cust_id]
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{cust_id}", response_model=Customer)
def update_customer(cust_id: str, customer: CustomerCreate, token: str = Depends(oauth2_scheme)):
    if cust_id in db_customers:
        db_customers[cust_id] = customer
        return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{cust_id}")
def delete_customer(cust_id: str, token: str = Depends(oauth2_scheme)):
    if cust_id in db_customers:
        del db_customers[cust_id]
        return {"detail": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")

# CRUD operations for MapGrid
@app.post("/mapgrids/", response_model=MapGrid)
def create_mapgrid(mapgrid: MapGridCreate, token: str = Depends(oauth2_scheme)):
    grid_id = len(db_map_grids) + 1
    db_map_grids[grid_id] = mapgrid
    return mapgrid

@app.get("/mapgrids/{grid_id}", response_model=MapGrid)
def read_mapgrid(grid_id: int, token: str = Depends(oauth2_scheme)):
    if grid_id in db_map_grids:
        return db_map_grids[grid_id]
    raise HTTPException(status_code=404, detail="MapGrid not found")

@app.put("/mapgrids/{grid_id}", response_model=MapGrid)
def update_mapgrid(grid_id: int, mapgrid: MapGridCreate, token: str = Depends(oauth2_scheme)):
    if grid_id in db_map_grids:
        db_map_grids[grid_id] = mapgrid
        return mapgrid
    raise HTTPException(status_code=404, detail="MapGrid not found")

@app.delete("/mapgrids/{grid_id}")
def delete_mapgrid(grid_id: int, token: str = Depends(oauth2_scheme)):
    if grid_id in db_map_grids:
        del db_map_grids[grid_id]
        return {"detail": "MapGrid deleted"}
    raise HTTPException(status_code=404, detail="MapGrid not found")

# Endpoint to get grid data
@app.get("/grid", response_model=List[Dict[str, float]])
def get_grid():
    x_axis_len = 20
    y_axis_len = 20
    grid_square_len = 1

    grid_squares_values = np.random.randint(0, 101, size=(x_axis_len, y_axis_len)).tolist()
    map_grid = MapGrid(x_axis_len=x_axis_len, y_axis_len=y_axis_len, grid_square_len=grid_square_len,
                       grid_squares_values=grid_squares_values)

    return map_grid


# Buttons
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/create_business", response_class=HTMLResponse)
async def create_business(request: Request,
                          radius: float = Form(...),
                          circle_center_x: float = Form(...),
                          circle_center_y: float = Form(...),
                          business_id: int = Form(...),
                          req_income: float = Form(...),
                          business_type: BusinessType = Form(...),
                          business_var: float = Form(...)):
    circle_center = Point(x=circle_center_x, y=circle_center_y)
    new_business = Business(
        radius=radius,
        circle_center=circle_center,
        business_id=business_id,
        req_income=req_income,
        business_type=business_type,
        business_var=business_var
    )

    db_businesses[business_id] = new_business
    return templates.TemplateResponse("index.html", {"request": request, "message": "Business created successfully!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

