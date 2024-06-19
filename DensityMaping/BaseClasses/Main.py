from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

users_db: Dict[int, User] = {}
products_db: Dict[int, Product] = {}
orders_db: Dict[int, Order] = {}
