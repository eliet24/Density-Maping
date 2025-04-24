from enum import Enum
from typing import List

class PlaceMainType(Enum):
    FOOD = "Food"
    RETAIL = "Retail"
    HEALTH = "Health"

    def to_dict(self):
        return {
            "key": self.name,
            "label": self.value
        }


class PlaceSubType:
    _registry = {}

    def __init__(self, key: str, label: str, main_type: PlaceMainType):
        self.key = key
        self.label = label
        self.main_type = main_type
        self.__class__._registry.setdefault(main_type, []).append(self)

    def to_dict(self):
        return {
            "key": self.key,
            "label": self.label,
            "main_type": self.main_type.value
        }

    @classmethod
    def get_subtypes(cls, main_type: PlaceMainType) -> List['PlaceSubType']:
        return cls._registry.get(main_type, [])

    @classmethod
    def all_subtypes(cls) -> List['PlaceSubType']:
        all_ = []
        for lst in cls._registry.values():
            all_.extend(lst)
        return all_