"""
Compro Category Schemas
"""
from datetime import datetime
from pydantic import BaseModel


class ComproCategory(BaseModel):
    """Schema for ComproCategory (list response)"""
    cc_id: int
    cc_name: str

    class Config:
        from_attributes = True
