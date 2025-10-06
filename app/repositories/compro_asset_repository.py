"""
Compro Assets Repository
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from atams.db.repository import BaseRepository
from app.models.compro_asset import ComproAsset


class ComproAssetRepository(BaseRepository[ComproAsset]):
    """Repository for ComproAsset operations"""

    def __init__(self):
        super().__init__(ComproAsset)

    def get_all(self, db: Session) -> List[ComproAsset]:
        """Get all compro assets"""
        return db.query(ComproAsset).all()

    def get_by_id(self, db: Session, ca_id: int) -> Optional[ComproAsset]:
        """Get compro asset by ID"""
        return db.query(ComproAsset).filter(ComproAsset.ca_id == ca_id).first()

    def create(self, db: Session, data: dict) -> ComproAsset:
        """Create new compro asset"""
        db_obj = ComproAsset(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, ca_id: int, data: dict) -> Optional[ComproAsset]:
        """Update compro asset"""
        db_obj = self.get_by_id(db, ca_id)
        if not db_obj:
            return None

        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, ca_id: int) -> bool:
        """Delete compro asset"""
        db_obj = self.get_by_id(db, ca_id)
        if not db_obj:
            return False

        db.delete(db_obj)
        db.commit()
        return True
