"""
Compro Assets Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, HttpUrl


class ComproAssetBase(BaseModel):
    """Base schema for ComproAsset"""
    ca_title: Optional[str] = Field(None, min_length=1, max_length=500, description="Asset title")
    ca_tagline: Optional[str] = Field(None, max_length=1000, description="Asset tagline")
    ca_image: Optional[str] = Field(None, max_length=2000, description="Main image path or URL")
    ca_image_carousel: Optional[List[str]] = Field(
        default_factory=list,
        max_length=20,
        description="Carousel image paths (max 20 images)"
    )
    ca_subtitle: Optional[str] = Field(None, max_length=1000, description="Asset subtitle")
    ca_link: Optional[str] = Field(None, max_length=2000, description="External link URL")
    ca_cc_id: Optional[int] = Field(None, gt=0, description="Category ID (must be greater than 0)")

    @field_validator('ca_title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty string"""
        if v is not None and v.strip() == "":
            raise ValueError("Title cannot be empty string")
        return v

    @field_validator('ca_image_carousel')
    @classmethod
    def validate_carousel(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate carousel images"""
        if v is not None:
            # Remove empty strings
            v = [img for img in v if img.strip()]
            if len(v) > 20:
                raise ValueError("Maximum 20 images allowed in carousel")
        return v if v else []


class ComproAssetCreate(ComproAssetBase):
    """Schema for creating ComproAsset"""
    pass


class ComproAssetUpdate(ComproAssetBase):
    """Schema for updating ComproAsset"""
    pass


class ComproAsset(ComproAssetBase):
    """Schema for ComproAsset with all fields (detail)"""
    ca_id: int
    cc_id: Optional[int] = None
    cc_name: Optional[str] = None
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
    cc_id: Optional[int] = None
    cc_name: Optional[str] = None

    class Config:
        from_attributes = True
