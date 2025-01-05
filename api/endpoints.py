from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.property_manager import PropertyManager
from services.property_search import PropertySearch

property_routes = APIRouter()

property_manager = PropertyManager()
property_search = PropertySearch(property_manager)

class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]

@property_routes.post("/api/v1/properties")
async def create_property(property_data: PropertyCreate, user_id: str):
    try:
        property_id = property_manager.add_property(user_id, property_data.dict())
        return {"property_id": property_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@property_routes.get("/api/v1/properties/search")
async def search_properties(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    page: int = 1,
    limit: int = 10):
    criteria = {"min_price": min_price, "max_price": max_price, "location": location}
    results = property_search.search_properties(criteria)
    start = (page - 1) * limit
    end = start + limit
    return [result.__dict__ for result in results[start:end]]
