"""
Compro Assets Service
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.compro_asset_repository import ComproAssetRepository
from app.schemas.compro_asset import ComproAsset, ComproAssetCreate, ComproAssetUpdate, ComproAssetList


class ComproAssetService:
    """Service for ComproAsset business logic"""

    def __init__(self):
        self.repository = ComproAssetRepository()

    def get_all_assets(self, db: Session) -> List[ComproAssetList]:
        """
        Get all assets (public endpoint)
        Returns simplified list view with category info
        """
        assets = self.repository.get_all(db)
        return [ComproAssetList(**asset) for asset in assets]

    def get_asset_by_id(self, db: Session, ca_id: int) -> ComproAsset:
        """
        Get asset by ID (public endpoint)
        Returns full detail with category info
        """
        asset = self.repository.get_by_id(db, ca_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with ID {ca_id} not found"
            )
        return ComproAsset(**asset)

    def create_asset(
        self,
        db: Session,
        asset_data: ComproAssetCreate,
        current_user: dict
    ) -> ComproAsset:
        """
        Create new asset
        Authorization already validated by endpoint dependency
        """
        # Prepare data with audit fields (only created_by, created_at handled by DB default)
        data = asset_data.model_dump()
        data["created_by"] = current_user.get("username", "system")
        # Don't set created_at, let DB handle with NOW()
        # Don't set updated_at and updated_by on create

        # Create asset
        new_asset = self.repository.create(db, data)
        return ComproAsset.model_validate(new_asset)

    def update_asset(
        self,
        db: Session,
        ca_id: int,
        asset_data: ComproAssetUpdate,
        current_user: dict
    ) -> ComproAsset:
        """
        Update existing asset
        Authorization already validated by endpoint dependency
        """
        # Check if asset exists
        existing = self.repository.get_by_id(db, ca_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with ID {ca_id} not found"
            )

        # Prepare data with audit fields (only update fields, don't touch created_*)
        data = asset_data.model_dump()
        data["updated_by"] = current_user.get("username", "system")
        data["updated_at"] = datetime.now()
        # Don't modify created_at and created_by

        # Update asset
        updated_asset = self.repository.update(db, ca_id, data)
        return ComproAsset.model_validate(updated_asset)

    def delete_asset(
        self,
        db: Session,
        ca_id: int
    ) -> None:
        """
        Delete asset
        Authorization already validated by endpoint dependency
        """
        # Check if asset exists
        existing = self.repository.get_by_id(db, ca_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with ID {ca_id} not found"
            )

        # Delete asset
        self.repository.delete(db, ca_id)
