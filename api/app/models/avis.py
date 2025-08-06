from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Avis(Base):
    __tablename__ = "avis"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    livreur_id = Column(UUID(as_uuid=True), ForeignKey("livreurs.id"))
    livraison_id = Column(UUID(as_uuid=True), ForeignKey("livraisons.id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    commentaire = Column(String)
    note = Column(Integer)
    # date_avis = Column(DateTime(timezone=True), server_default=func.now())
    date_avis = Column(DateTime, default=datetime.utcnow)
    livreur = relationship("Livreur", back_populates="avis")
    livraison = relationship("Livraison", back_populates="avis")
    client = relationship("Client", back_populates="avis")
    

    
    