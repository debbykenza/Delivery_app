from datetime import datetime, timedelta
from sqlalchemy import Column, Float, Enum, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from app.core.database import Base


class StatutAbonnement(str, PyEnum):
    actif = "actif"
    expiré = "expiré"
    suspendu = "suspendu"
    inactif = "inactif"


class Abonnement(Base):
    __tablename__ = "abonnements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"), nullable=False)
    montant = Column(Float, nullable=False)
    date_debut = Column(DateTime, default=datetime.utcnow)
    date_expiration = Column(DateTime)
    statut = Column(Enum(StatutAbonnement), default=StatutAbonnement.inactif)
    reference_abonnement = Column(String(50), unique=True, nullable=True)
    # numero = Column(String(155), unique=True, nullable=False)
    # pays= Column(String(5), nullable=False) 
    # lien_de_paiement = Column(String(255), nullable=False)
    # transaction_id= Column(String(255), nullable=False, unique=True)

    marchand = relationship("Marchand", back_populates="abonnement")
