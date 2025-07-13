from datetime import datetime
import enum
from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class StatutLivraisonEnum(str, enum.Enum):
    en_attente = "en_attente"
    acceptee = "acceptee"
    en_cours = "en_cours"
    terminee = "terminee"
    annulee = "annulee"
    # livree = "livree"

class TypeLivraisonEnum(str, enum.Enum):
    express = "express"
    standard = "standard"

class Livraison(Base):
    __tablename__ = "livraisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commande_id = Column(UUID(as_uuid=True), ForeignKey("commandes.id"), unique=True)
    livreur_id = Column(UUID(as_uuid=True), ForeignKey("livreurs.id"))
    statut = Column(Enum("en_attente", "acceptee", "annulee", "en_cours", "terminee", name="statut_livraison"))
    #url_suivi = Column(String)
    # marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"))
    date_livraison = Column(DateTime, default=datetime.utcnow) 
    probleme = Column(String, nullable=True)
    commande = relationship(
        "Commande",
        back_populates="livraison",

    )

    livreur = relationship("Livreur", back_populates="livraisons")
    avis = relationship("Avis", back_populates="livraison")
    paiement = relationship("Paiement", back_populates="livraison")

