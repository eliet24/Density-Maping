from enum import Enum
from pydantic import BaseModel


class BusinessType(Enum):
    FASHION = 1
    FOOD = 2
    HEALTH_AND_COSMETICS = 3
    ELECTRONICS = 4

