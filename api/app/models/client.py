from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base



class Client(Base):
    __tablename__ = "clients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nom = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    # commandes = relationship("Commande", back_populates="client")
    # adresses = relationship("AdresseClient", back_populates="client")
    commandes = relationship("Commande", back_populates="client")
    avis = relationship("Avis", back_populates="client")



    
