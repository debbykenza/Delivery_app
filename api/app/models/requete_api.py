from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app.core.database import Base

# Modèle SQLAlchemy pour la table des requêtes API
class RequeteAPI(Base):
    __tablename__ = "requete_api"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"))
    endpoint = Column(String, nullable=False)        # Ex: "/commandes/creer"
    méthode = Column(String, nullable=False)         # Ex: "POST", "GET"
    statut = Column(Integer, nullable=False)         # Code HTTP: 200, 400, etc.
    temps_réponse = Column(Float, nullable=False)    # Temps de réponse en secondes
    date = Column(DateTime, default=datetime.utcnow)
    marchand = relationship("Marchand", back_populates="requetes_api")