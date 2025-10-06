"""
Compro Assets Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ComproAssetBase(BaseModel):
    """Base schema for ComproAsset"""
    ca_title: Optional[str] = None
    ca_tagline: Optional[str] = None
    ca_image: Optional[str] = None
    ca_image_carousel: Optional[List[str]] = Field(default_factory=list)
    ca_subtitle: Optional[str] = None
    ca_link: Optional[str] = None


class ComproAssetCreate(ComproAssetBase):
    """Schema for creating ComproAsset"""
    pass


class ComproAssetUpdate(ComproAssetBase):
    """Schema for updating ComproAsset"""
    pass


class ComproAsset(ComproAssetBase):
    """Schema for ComproAsset with all fields (detail)"""
    ca_id: int
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


class ComproAssetList(BaseModel):
    """Schema for ComproAsset list (simplified)"""
    ca_id: int
    ca_title: Optional[str] = None
    ca_image: Optional[str] = None
    ca_link: Optional[str] = None
    ca_subtitle: Optional[str] = None

    class Config:
        from_attributes = True
