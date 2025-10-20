"""
Compro Assets Endpoints

GET endpoints: No authentication required (public)
POST/PUT/DELETE endpoints: Requires authentication with role_level >= 10
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.compro_asset_service import ComproAssetService
from app.schemas.compro_asset import ComproAsset, ComproAssetCreate, ComproAssetUpdate, ComproAssetList
from app.schemas.common import DataResponse
from app.api.deps import require_auth, require_min_role_level

router = APIRouter()
service = ComproAssetService()


@router.get(
    "/",
    response_model=DataResponse[List[ComproAssetList]],
    status_code=status.HTTP_200_OK
)
async def get_assets(db: Session = Depends(get_db)):
    """
    Get all assets (public endpoint)

    **Authorization:** None (public)

    **Response:**
    - Returns list of assets with simplified fields
    - Status code 200
    """
    assets = service.get_all_assets(db)
    return DataResponse(
        success=True,
        message="Assets retrieved successfully",
        data=assets
    )


@router.get(
    "/{ca_id}",
    response_model=DataResponse[ComproAsset],
    status_code=status.HTTP_200_OK
)
async def get_asset(ca_id: int, db: Session = Depends(get_db)):
    """
    Get asset by ID (public endpoint)

    **Authorization:** None (public)

    **Response:**
    - Returns full asset details
    - Status code 200
    - Raises 404 if not found
    """
    asset = service.get_asset_by_id(db, ca_id)
    return DataResponse(
        success=True,
        message="Asset retrieved successfully",
        data=asset
    )


@router.post(
    "/",
    response_model=DataResponse[ComproAsset],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_min_role_level(10))]
)
async def create_asset(
    asset: ComproAssetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Create new asset

    **Authorization:** Required (role_level >= 10)

    **Response:**
    - Returns created asset
    - Status code 201
    - Raises 403 if insufficient permission
    """
    new_asset = service.create_asset(db, asset, current_user)
    return DataResponse(
        success=True,
        message="Asset created successfully",
        data=new_asset
    )


@router.put(
    "/{ca_id}",
    response_model=DataResponse[ComproAsset],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_min_role_level(10))]
)
async def update_asset(
    ca_id: int,
    asset: ComproAssetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Update existing asset

    **Authorization:** Required (role_level >= 10)

    **Response:**
    - Returns updated asset
    - Status code 200
    - Raises 404 if not found
    - Raises 403 if insufficient permission
    """
    updated_asset = service.update_asset(db, ca_id, asset, current_user)
    return DataResponse(
        success=True,
        message="Asset updated successfully",
        data=updated_asset
    )


@router.delete(
    "/{ca_id}",
    response_model=DataResponse[None],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_min_role_level(10))]
)
async def delete_asset(
    ca_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Delete asset

    **Authorization:** Required (role_level >= 10)

    **Response:**
    - Returns success message
    - Status code 200
    - Raises 404 if not found
    - Raises 403 if insufficient permission
    """
    service.delete_asset(db, ca_id)
    return DataResponse(
        success=True,
        message="Asset deleted successfully",
        data=None
    )
