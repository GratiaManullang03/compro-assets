"""
Compro Category Service
"""
from typing import List
from sqlalchemy.orm import Session

from app.repositories.compro_category_repository import ComproCategoryRepository
from app.schemas.compro_category import ComproCategory


class ComproCategoryService:
    """Service for ComproCategory business logic"""

    def __init__(self):
        self.repository = ComproCategoryRepository()

    def get_all_categories(self, db: Session) -> List[ComproCategory]:
        """
        Get all categories (public endpoint)
        Returns list of categories ordered by name
        """
        categories = self.repository.get_all(db)
        return [ComproCategory.model_validate(cat) for cat in categories]
