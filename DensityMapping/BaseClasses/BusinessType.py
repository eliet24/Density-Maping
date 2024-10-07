from enum import Enum
from pydantic import BaseModel


class BusinessType(Enum):
    FASHION = "FASHION"
    FOOD = "FOOD"
    HEALTH_AND_COSMETICS = "HEALTH_AND_COSMETICS"
    ELECTRONICS = "ELECTRONICS"

