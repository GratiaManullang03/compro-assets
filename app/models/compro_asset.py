"""
Compro Assets Model
"""
from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ARRAY, text
from atams.db.base import Base


class ComproAsset(Base):
    __tablename__ = "compro_assets"
    __table_args__ = {"schema": "compro"}

    # Primary key
    ca_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Content columns
    ca_title = Column(Text, nullable=True)
    ca_tagline = Column(Text, nullable=True)
    ca_image = Column(Text, nullable=True)
    ca_image_carousel = Column(ARRAY(Text), nullable=True, default=[], server_default=text("'{}'"))
    ca_subtitle = Column(Text, nullable=True)
    ca_link = Column(Text, nullable=True)

    # Audit columns
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))
    created_by = Column(Text, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Text, nullable=True)
