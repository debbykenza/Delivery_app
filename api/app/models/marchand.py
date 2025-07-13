from datetime import datetime
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Marchand(Base):
    __tablename__ = "marchands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, nullable=False)
    adresse = Column(String, nullable=True)
    contact = Column(String, nullable=False)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    date_creation = Column(DateTime, default=datetime.utcnow)
    
    utilisateur = relationship("Utilisateur")
    commandes = relationship("Commande", back_populates="marchand")
    adresses = relationship("Adresse", back_populates="marchand")
    requetes_api = relationship("RequeteAPI", back_populates="marchand")

    # abonnement = relationship("Abonnement", back_populates="marchand", uselist=False)

    
