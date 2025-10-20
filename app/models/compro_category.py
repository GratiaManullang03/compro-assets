"""
Compro Category Model
"""
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text
from atams.db.base import Base


class ComproCategory(Base):
    __tablename__ = "compro_category"
    __table_args__ = {"schema": "compro"}

    # Primary key
    cc_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Content columns
    cc_name = Column(String, nullable=False)

    # Audit columns
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))
    created_by = Column(String, nullable=False, server_default=text("'SYSTEM'"))
