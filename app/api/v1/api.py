from fastapi import APIRouter
from app.api.v1.endpoints import compro_assets, compro_category

api_router = APIRouter()

# Register routes
api_router.include_router(compro_assets.router, prefix="/assets", tags=["Compro Assets"])
api_router.include_router(compro_category.router, prefix="/categories", tags=["Compro Categories"])
