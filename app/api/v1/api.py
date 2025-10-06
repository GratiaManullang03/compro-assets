from fastapi import APIRouter
from app.api.v1.endpoints import compro_assets

api_router = APIRouter()

# Register routes
api_router.include_router(compro_assets.router, prefix="/assets", tags=["Compro Assets"])
