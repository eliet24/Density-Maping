import json
from .PlaceType import PlaceSubType, PlaceMainType

class Place:
    def __init__(self, name: str, subtype: PlaceSubType, lat: float, lng: float):
        self.name = name
        self.subtype = subtype
        self.main_type = subtype.main_type
        self.lat = lat
        self.lng = lng

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.main_type.value,
            "subtype": self.subtype.label,
            "location": {
                "lat": self.lat,
                "lng": self.lng
            }
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
