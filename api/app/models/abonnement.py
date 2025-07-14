from datetime import datetime, timedelta
from sqlalchemy import Column, Float, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from app.core.database import Base


class StatutAbonnement(str, PyEnum):
    actif = "actif"
    expiré = "expiré"
    suspendu = "suspendu"


class Abonnement(Base):
    __tablename__ = "abonnements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"), nullable=False)
    montant = Column(Float, nullable=False)
    date_debut = Column(DateTime, default=datetime.utcnow)
    date_expiration = Column(DateTime)
    statut = Column(Enum(StatutAbonnement), default=StatutAbonnement.actif)

    marchand = relationship("Marchand", back_populates="abonnement")
