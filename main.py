from fastapi import FastAPI
from api.endpoints import property_routes

app = FastAPI()
app.include_router(property_routes)