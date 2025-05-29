from pydantic import BaseModel
from typing import List, Dict, Optional
from .PublicInstitution import PublicInstitution, InstitutionType
from .BusinessType import BusinessType

"""
------------------------------------------------- AreaBase and Area -------------------------------------------------
Area Class: represents a Area on the map api, The Area shape the user draw on the map
parameters:
area_type: holds a string that define the area type: Home, Work, shopping, sport and health 
shape_type: holds a string that defines the shape of the area drawn: Circle, Polygon created from Points
coordinates: List of pairs of [str, float] holds the Points coordinates paired to latitude and longitude
radius: if Circle Shape chose this is the radius of it
missing_businesses: holds a List of all the Business Types the user chose as missing in the area
business_data:  a free string with input data of the user about the missing businesses in the area
functions:
-------------------------------------------------------------------------------------------------------------
"""


class AreaBase(BaseModel):
    area_type: str
    shape_type: str
    coordinates: List[Dict[str, float]]
    radius: Optional[float]
    missing_businesses: Optional[List[BusinessType]]
    missing_institutions: Optional[List[InstitutionType]]
    business_data: Optional[str]
    institution_data: Optional[str]


class Area(AreaBase):
    area_id: int
    user_id: str