from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.sql import func

class CleAPI(Base):
    __tablename__ = "cles_api"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cle = Column(String, unique=True, nullable=False)
    nom = Column(String)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    est_active = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())

    utilisateur = relationship("Utilisateur", back_populates="cles_api")
