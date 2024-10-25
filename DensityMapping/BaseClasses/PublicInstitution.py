from enum import Enum
from typing import Optional, Dict
from .Square import Square
from .Circle import Circle
from .Point import Point


class InstitutionType(Enum):
    GOVERNMENTAL = "GOVERNMENTAL"
    HEALTHCARE = "HEALTHCARE"
    PUBLIC_SAFETY_AND_EMERGENCY_SERVICES = "PUBLIC_SAFETY_AND_EMERGENCY_SERVICES"
    JUDICIAL_AND_LEGAL = "JUDICIAL_AND_LEGAL"
    TRANSPORTATION_AND_INFRASTRUCTURE = "TRANSPORTATION_AND_INFRASTRUCTURE"
    ECONOMIC_AND_FINANCIAL = "ECONOMIC_AND_FINANCIAL"
    CULTURE_AND_SPORTS = "CULTURE_AND_SPORTS"
    SOCIAL_AND_WELFARE_SERVICES = "SOCIAL_AND_WELFARE_SERVICES"
    LABOR_AND_WORKFORCE = "LABOR_AND_WORKFORCE"
    RELIGIOUS_INSTITUTIONS = "RELIGIOUS_INSTITUTIONS"
    EDUCATIONAL_INSTITUTION = "EDUCATIONAL_INSTITUTION"


class PublicInstitution(Circle):
    institution_id: int
    institution_type: InstitutionType
    institution_var: float
    institutions_squares_value_dist: Optional[Dict[Square, float]] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, radius: float, circle_center: Point, institution_id: int,
                 institution_type: InstitutionType, institution_var: float,
                 institution_squares_value_dist: Optional[Dict[Square, float]] = None):
        super().__init__(
            radius=radius,
            circle_center=circle_center,
            institution_id=institution_id,
            institution_type=institution_type,
            institution_var=institution_var,
            institution_squares_value_dist=institution_squares_value_dist
        )

    # getters and Setters
    def get_institution_id(self):
        return self.business_id

    def get_institution_type(self):
        return self.institution_type

    def get_varience(self):
        return self.institution_var

    # setters
    def set_institution_id(self, inst_id: int):
        self.institution_id = inst_id

    def set_business_type(self, institution_type: InstitutionType):
        self.institution_type = institution_type

    def set_varience(self, var: float):
        self.institution_var = var

    # function for finding the initialized business center on the MapGrid
    def find_init_center(self, size_ratio: int):
        return Point(x=size_ratio / 2 * self.circle_to_square(), y=size_ratio / 2 * self.circle_to_square())
