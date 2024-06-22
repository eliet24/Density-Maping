from fastapi import FastAPI, HTTPException
from models import Business, Customer, MapGrid
from schemas import BusinessCreate, CustomerCreate, MapGridCreate
from database import db_businesses, db_customers, db_map_grids

app = FastAPI()


# CRUD operations for Business
@app.post("/businesses/", response_model=Business)
def create_business(business: BusinessCreate):
    db_businesses[business.business_id] = business
    return business


@app.get("/businesses/{business_id}", response_model=Business)
def read_business(business_id: int):
    if business_id in db_businesses:
        return db_businesses[business_id]
    raise HTTPException(status_code=404, detail="Business not found")


@app.put("/businesses/{business_id}", response_model=Business)
def update_business(business_id: int, business: BusinessCreate):
    if business_id in db_businesses:
        db_businesses[business_id] = business
        return business
    raise HTTPException(status_code=404, detail="Business not found")


@app.delete("/businesses/{business_id}")
def delete_business(business_id: int):
    if business_id in db_businesses:
        del db_businesses[business_id]
        return {"detail": "Business deleted"}
    raise HTTPException(status_code=404, detail="Business not found")


# CRUD operations for Customer
@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate):
    db_customers[customer.cust_id] = customer
    return customer


@app.get("/customers/{cust_id}", response_model=Customer)
def read_customer(cust_id: str):
    if cust_id in db_customers:
        return db_customers[cust_id]
    raise HTTPException(status_code=404, detail="Customer not found")


@app.put("/customers/{cust_id}", response_model=Customer)
def update_customer(cust_id: str, customer: CustomerCreate):
    if cust_id in db_customers:
        db_customers[cust_id] = customer
        return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@app.delete("/customers/{cust_id}")
def delete_customer(cust_id: str):
    if cust_id in db_customers:
        del db_customers[cust_id]
        return {"detail": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")


# CRUD operations for MapGrid
@app.post("/mapgrids/", response_model=MapGrid)
def create_mapgrid(mapgrid: MapGridCreate):
    grid_id = len(db_map_grids) + 1
    db_map_grids[grid_id] = mapgrid
    return mapgrid


@app.get("/mapgrids/{grid_id}", response_model=MapGrid)
def read_mapgrid(grid_id: int):
    if grid_id in db_map_grids:
        return db_map_grids[grid_id]
    raise HTTPException(status_code=404, detail="MapGrid not found")


@app.put("/mapgrids/{grid_id}", response_model=MapGrid)
def update_mapgrid(grid_id: int, mapgrid: MapGridCreate):
    if grid_id in db_map_grids:
        db_map_grids[grid_id] = mapgrid
        return mapgrid
    raise HTTPException(status_code=404, detail="MapGrid not found")


@app.delete("/mapgrids/{grid_id}")
def delete_mapgrid(grid_id: int):
    if grid_id in db_map_grids:
        del db_map_grids[grid_id]
        return {"detail": "MapGrid deleted"}
    raise HTTPException(status_code=404, detail="MapGrid not found")
