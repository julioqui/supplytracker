from sqlalchemy import Column, String, Numeric, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base

class Supply(Base):
    __tablename__ = "supplies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit = Column(String, nullable=False)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Numeric(10, 3), default=0)
    min_stock = Column(Numeric(10, 3), default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()")
    )
