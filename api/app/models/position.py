from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    livreur_id = Column(UUID(as_uuid=True), ForeignKey("livreurs.id"), nullable=False)
    livraison_id = Column(UUID(as_uuid=True), ForeignKey("livraisons.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # relations (facultatives mais utiles)
    livreur = relationship("Livreur", back_populates="positions", lazy="joined")
    livraison = relationship("Livraison", back_populates="positions", lazy="joined")