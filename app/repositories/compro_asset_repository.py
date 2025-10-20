"""
Compro Assets Repository
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status
from atams.db.repository import BaseRepository
from app.models.compro_asset import ComproAsset
from app.models.compro_category import ComproCategory


class ComproAssetRepository(BaseRepository[ComproAsset]):
    """Repository for ComproAsset operations"""

    def __init__(self):
        super().__init__(ComproAsset)

    def get_all(self, db: Session) -> List[dict]:
        """
        Get all compro assets with category join
        Returns list of dictionaries with asset and category data
        """
        query = (
            db.query(
                ComproAsset.ca_id,
                ComproAsset.ca_title,
                ComproAsset.ca_image,
                ComproAsset.ca_subtitle,
                ComproAsset.ca_link,
                ComproAsset.ca_cc_id,
                ComproCategory.cc_id,
                ComproCategory.cc_name
            )
            .outerjoin(ComproCategory, ComproAsset.ca_cc_id == ComproCategory.cc_id)
            .all()
        )

        # Convert to dict for easier schema mapping
        results = []
        for row in query:
            results.append({
                "ca_id": row.ca_id,
                "ca_title": row.ca_title,
                "ca_image": row.ca_image,
                "ca_subtitle": row.ca_subtitle,
                "ca_link": row.ca_link,
                "ca_cc_id": row.ca_cc_id,
                "cc_id": row.cc_id,
                "cc_name": row.cc_name
            })
        return results

    def get_by_id(self, db: Session, ca_id: int) -> Optional[dict]:
        """
        Get compro asset by ID with category join
        Returns dictionary with asset and category data
        """
        query = (
            db.query(
                ComproAsset.ca_id,
                ComproAsset.ca_title,
                ComproAsset.ca_tagline,
                ComproAsset.ca_image,
                ComproAsset.ca_image_carousel,
                ComproAsset.ca_subtitle,
                ComproAsset.ca_link,
                ComproAsset.ca_cc_id,
                ComproAsset.created_at,
                ComproAsset.created_by,
                ComproAsset.updated_at,
                ComproAsset.updated_by,
                ComproCategory.cc_id,
                ComproCategory.cc_name
            )
            .outerjoin(ComproCategory, ComproAsset.ca_cc_id == ComproCategory.cc_id)
            .filter(ComproAsset.ca_id == ca_id)
            .first()
        )

        if not query:
            return None

        # Convert to dict for easier schema mapping
        return {
            "ca_id": query.ca_id,
            "ca_title": query.ca_title,
            "ca_tagline": query.ca_tagline,
            "ca_image": query.ca_image,
            "ca_image_carousel": query.ca_image_carousel,
            "ca_subtitle": query.ca_subtitle,
            "ca_link": query.ca_link,
            "ca_cc_id": query.ca_cc_id,
            "created_at": query.created_at,
            "created_by": query.created_by,
            "updated_at": query.updated_at,
            "updated_by": query.updated_by,
            "cc_id": query.cc_id,
            "cc_name": query.cc_name
        }

    def create(self, db: Session, data: dict) -> ComproAsset:
        """Create new compro asset"""
        try:
            db_obj = ComproAsset(**data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            # Check if it's a foreign key constraint error
            if "foreign key constraint" in str(e.orig).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid category ID. Category does not exist."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred: {str(e)}"
            )

    def update(self, db: Session, ca_id: int, data: dict) -> Optional[ComproAsset]:
        """Update compro asset"""
        try:
            db_obj = self.get_by_id(db, ca_id)
            if not db_obj:
                return None

            for key, value in data.items():
                setattr(db_obj, key, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            # Check if it's a foreign key constraint error
            if "foreign key constraint" in str(e.orig).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid category ID. Category does not exist."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred: {str(e)}"
            )

    def delete(self, db: Session, ca_id: int) -> bool:
        """Delete compro asset"""
        try:
            db_obj = self.get_by_id(db, ca_id)
            if not db_obj:
                return False

            db.delete(db_obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred: {str(e)}"
            )
