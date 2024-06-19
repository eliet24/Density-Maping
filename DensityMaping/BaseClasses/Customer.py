from enum import Enum
from datetime import date

from DensityMaping.BaseClasses import Business, Point


class RelationshipStatus(Enum):
    MARRIED = 1
    BACHELOR = 2
    DIVORCE = 3
    IN_RELATIONSHIP = 4


class Customer:
    def __init__(self, cust_id: str, cust_name: str, cust_birth_date: str, cust_income: float
                 , cust_relationship_status: RelationshipStatus, cust_businesses: list = [Business],
                 cust_saved_locations: list = [Point]):
        self.cust_id = cust_id
        self.cust_name = cust_name
        self.cust_birth_date = cust_birth_date
        self.cust_income = cust_income
        self.cust_relationship_status = cust_relationship_status
        self.cust_businesses = cust_businesses
        self.cust_saved_locations = cust_saved_locations


    # Getter method for cust_id
    def get_cust_id(self):
        return self.cust_id

    # Setter method for cust_id
    def set_cust_id(self, new_id):
        self.cust_id = new_id

    # Getter method for cust_saved_locations
    def get_user_saved_locations(self):
        return self.cust_saved_locations

    # Setter method for cust_saved_locations
    def add_user_saved_location(self, new_location: Point):
        self.cust_saved_locations.append(new_location)

    def delete_cust_saved_location(self, location_for_delete: Point):
        self.cust_saved_locations.remove(location_for_delete)

def calculate_cust_age(self) -> int:
    """
    :param self:
    :return: age of the customer
    """
    day, month, year = map(int, self.cust_birth_date.split("/"))
    born = date(year, month, day)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
