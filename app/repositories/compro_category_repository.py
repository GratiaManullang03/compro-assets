"""
Compro Category Repository
"""
from typing import List
from sqlalchemy.orm import Session
from atams.db.repository import BaseRepository
from app.models.compro_category import ComproCategory


class ComproCategoryRepository(BaseRepository[ComproCategory]):
    """Repository for ComproCategory operations"""

    def __init__(self):
        super().__init__(ComproCategory)

    def get_all(self, db: Session) -> List[ComproCategory]:
        """Get all compro categories"""
        return db.query(ComproCategory).order_by(ComproCategory.cc_name).all()
