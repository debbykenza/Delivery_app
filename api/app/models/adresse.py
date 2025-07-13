from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.database import Base
import uuid

class Adresse(Base):
    __tablename__ = "adresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pays = Column(String(100), nullable=False)
    ville = Column(String(100), nullable=False)

    # Point géographique (latitude + longitude)
    position_point = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    # Polygone optionnel (zone)
    zone_polygone = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=True)

    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=True)
    marchand_id = Column(UUID(as_uuid=True), ForeignKey("marchands.id"), nullable=True)
    livreur_id = Column(UUID(as_uuid=True), ForeignKey("livreurs.id"), nullable=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="adresses")
    marchand = relationship("Marchand", back_populates="adresses")
    livreur = relationship("Livreur", back_populates="adresses")
    client = relationship("Client", back_populates="adresses")
