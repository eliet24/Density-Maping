from fastapi import FastAPI, Query
from typing import Optional
from place_types import PlaceMainType, PlaceSubType, Place
from place_types import data  # registers subtypes

app = FastAPI(title="Place Type API")


@app.get("/")
def root():
    return {"message": "Place Type API is running."}


@app.get("/main-types")
def get_main_types():
    return [t.to_dict() for t in PlaceMainType]


@app.get("/subtypes")
def get_all_subtypes(main_type: Optional[str] = Query(None)):
    if main_type:
        try:
            mt_enum = PlaceMainType[main_type.upper()]
        except KeyError:
            return {"error": f"Invalid main type: {main_type}"}
        return [s.to_dict() for s in PlaceSubType.get_subtypes(mt_enum)]
    return [s.to_dict() for s in PlaceSubType.all_subtypes()]


@app.get("/subtypes/search")
def search_subtypes(q: str = Query(..., description="Keyword to search subtype labels")):
    result = [s.to_dict() for s in PlaceSubType.all_subtypes() if q.lower() in s.label.lower()]
    return result


@app.get("/subtypes/by-main")
def get_subtypes_grouped():
    return {
        mt.value: [s.to_dict() for s in PlaceSubType.get_subtypes(mt)]
        for mt in PlaceMainType
    }

