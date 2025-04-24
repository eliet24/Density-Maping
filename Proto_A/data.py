from .PlaceType import PlaceSubType, PlaceMainType

ASIAN_RESTAURANT = PlaceSubType("asian_restaurant", "Asian Restaurant", PlaceMainType.FOOD)
PIZZA_PLACE = PlaceSubType("pizza_place", "Pizza Place", PlaceMainType.FOOD)
BURGER_JOINT = PlaceSubType("burger_joint", "Burger Joint", PlaceMainType.FOOD)

GROCERY_STORE = PlaceSubType("grocery_store", "Grocery Store", PlaceMainType.RETAIL)
CLOTHING_STORE = PlaceSubType("clothing_store", "Clothing Store", PlaceMainType.RETAIL)

HOSPITAL = PlaceSubType("hospital", "Hospital", PlaceMainType.HEALTH)
PHARMACY = PlaceSubType("pharmacy", "Pharmacy", PlaceMainType.HEALTH)
