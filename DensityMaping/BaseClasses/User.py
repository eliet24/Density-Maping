from enum import Enum
from datetime import date
from typing import Optional, List

from pydantic import BaseModel
from DensityMaping.BaseClasses import Business, Point
from DensityMaping.BaseClasses.Circle import Circle


class RelationshipStatus(str, Enum):
    MARRIED = "married"
    BACHELOR = "bachelor"
    DIVORCED = "divorced"
    IN_RELATIONSHIP = "in_relationship"


class User(BaseModel):
    user_id: str
    user_name: str
    user_birth_date: date
    user_income: float
    user_relationship_status: RelationshipStatus
    user_businesses: Optional[List[Business]] = []
    user_saved_locations: Optional[List[Circle]] = []

    # Getters and Setters
    def get_user_id(self):
        return self.user_id

    def set_user_id(self, new_id):
        self.user_id = new_id

    def get_user_saved_locations(self):
        return self.user_saved_locations

    def add_user_saved_location(self, new_location: Circle):
        self.user_saved_locations.append(new_location)

    def delete_user_saved_location(self, location_for_delete: Circle):
        self.user_saved_locations.remove(location_for_delete)

    def calculate_user_age(self) -> int:
        """
        :param self:
        :return: age of the customer
        """
        day, month, year = map(int, self.user_birth_date.split("/"))
        born = date(year, month, day)
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
