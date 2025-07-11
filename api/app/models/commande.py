from sqlalchemy import Column, String, JSON, Enum, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from enum import Enum as PyEnum

class StatutCommande(str, PyEnum):
    EN_ATTENTE = "en_attente"
    VALIDEE = "validée"
    ANNULEE = "annulée"
    EN_COURS = "en_cours"
    LIVREE = "livrée"

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String, unique=True, index=True)
    marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"))
    # client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    articles = Column(JSON)
    statut = Column(Enum(StatutCommande), default=StatutCommande.EN_ATTENTE)
    total = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # livraison_id = Column(UUID(as_uuid=True), ForeignKey("livraisons.id"), nullable=True)

    # Relations
    livraison = relationship("Livraison", back_populates="commande")
    marchand = relationship("Marchand", back_populates="commandes")
    # client = relationship("Client", back_populates="commandes")
    # livraison = relationship(
    #     "Livraison",
    #     back_populates="commande",
    #     # foreign_keys=[livraison_id],
    #     uselist=False
    # )