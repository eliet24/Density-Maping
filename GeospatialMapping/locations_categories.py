categories_dict = {
    "public_services": {
        "education": {
            "formal": [
                "kindergarten", "daycare", "elementary_school",
                "high_school", "college", "university",
                "yeshiva", "beit_midrash"
            ],
            "informal": ["hobbies", "courses", "private_lessons"]
        },
        "community": {
            "community_center": [],
            "teen_club": [],
            "youth_movement": []
        },
        "health": {
            "clinic": [],
            "hospital": [],
            "family_health_station": [],
            "maternity_clinic": []
        },
        "religion": {
            "synagogue": []
        }
    },
    "consumption": {
        "food": [],
        "dining": [],
        "culture_and_leisure": [],
        "clothing": [],
        "home": []
    },
    "work": {},
    "home": {}
}


translation_dict = {
    "public_services": "שירותים ציבוריים",
    "education": "חינוך",
    "formal": "פורמלי",
    "informal": "לא פורמלי",
    "community": "קהילה",
    "health": "בריאות",
    "religion": "דת",
    "consumption": "צריכה",
    "work": "עבודה",
    "home": "בית",
    "kindergarten": "גן ילדים",
    "daycare": "מעון",
    "elementary_school": "בית ספר יסודי",
    "high_school": "בית ספר על יסודי",
    "college": "מכללה",
    "university": "אוניברסיטה",
    "yeshiva": "ישיבה",
    "beit_midrash": "בית מדרש",
    "hobbies": "חוגים",
    "courses": "קורסים",
    "private_lessons": "שיעור פרטי",
    "community_center": "מתנס",
    "teen_club": "מועדון נער",
    "youth_movement": "תנועת נוער",
    "clinic": "קופת חולים",
    "hospital": "בית חולים",
    "family_health_station": "תחנת בריאות המשפחה",
    "maternity_clinic": "טיפת חלב",
    "food": "מזון",
    "dining": "הסעדה",
    "culture_and_leisure": "תרבות ופנאי",
    "clothing": "ביגוד",
    "home": "לבית"
}

def translate_categories(categories, translation_dict):
    if isinstance(categories, dict):
        return {
            translation_dict.get(key, key): translate_categories(value, translation_dict)
            for key, value in categories.items()
        }
    elif isinstance(categories, list):
        return [translation_dict.get(item, item) for item in categories]
    else:
        return translation_dict.get(categories, categories)

