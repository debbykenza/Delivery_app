
import enum
from sqlalchemy import Column, Enum, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from sqlalchemy.orm import relationship

class Role(str, enum.Enum):
    admin = "admin"
    utilisateur = "utilisateur"
    marchand = "marchand"
    livreur = "livreur"
    client = "client"

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String)
    email = Column(String, unique=True)
    mot_de_passe = Column(String, nullable=True)  # Nullable si utilisation de Supabase pour l'auth
    is_active = Column(Boolean, default=True)     # Pour gérer l'activation des comptes
    role = Column(Enum(Role), nullable=False)  # ✅ Utilise SQLAlchemy.Enum
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_mise_a_jour = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Utilisateur {self.email} - {self.role}>"
    
    cles_api = relationship("CleAPI", back_populates="utilisateur")
    marchands = relationship("Marchand", back_populates="utilisateur")
    adresses = relationship("Adresse", back_populates="utilisateur")
