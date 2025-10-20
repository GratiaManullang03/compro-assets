"""
Compro Category Endpoints

GET endpoints: No authentication required (public)
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.compro_category_service import ComproCategoryService
from app.schemas.compro_category import ComproCategory
from app.schemas.common import DataResponse

router = APIRouter()
service = ComproCategoryService()


@router.get(
    "/",
    response_model=DataResponse[List[ComproCategory]],
    status_code=status.HTTP_200_OK
)
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories (public endpoint)

    **Authorization:** None (public)

    **Response:**
    - Returns list of categories with cc_id and cc_name
    - Ordered by category name
    - Status code 200
    """
    categories = service.get_all_categories(db)
    return DataResponse(
        success=True,
        message="Categories retrieved successfully",
        data=categories
    )
