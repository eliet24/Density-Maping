from pydantic import BaseModel
from typing import List, Dict, Optional

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
# TODO: create ENUM for area_type and add select option in the web_page, create ENUM or class for shape_type
# TODO: use the Point class for the cordinates represntation, the missing_business should hold a list of BusinessType
# TODO: Enum class, maybe create Sub BusinessTypes,

class AreaBase(BaseModel):
    area_type: str
    shape_type: str
    coordinates: List[Dict[str, float]]     # TODO: check how to change to Point class presentation
    radius: Optional[float] = None
    missing_businesses: List[str]
    business_data: str


class Area(AreaBase):
    area_id: int
    user_id: str
