from datetime import datetime
from sqlalchemy import Column, DateTime, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Livreur(Base):
    __tablename__ = "livreurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String)
    vehicule = Column(Enum("moto", "voiture", "camion", name="type_vehicule"))
    contact = Column(String)
    immatriculation = Column(String)
    statut = Column(Enum("disponible", "indisponible", name="statut_livreur"))
    # est_disponible = Column(Boolean, default=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    livraisons = relationship("Livraison", back_populates="livreur")
    avis = relationship("Avis", back_populates="livreur")