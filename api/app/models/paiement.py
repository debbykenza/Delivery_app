from datetime import datetime
from sqlalchemy import Column, Float, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum


class StatutPaiement(str, PyEnum):
    en_attente = "en_attente" # le client n'a pas encore payé
    remis_livreur = "remis_livreur" # le client a remis l'argent au livreur
    payé = "paye" # le client a payé
    échoué = "échoue" # le paiement a échoué
    remboursé = "rembourse" # le paiement a été remboursé
    
class MethodePaiement(str, PyEnum):
    mixx = "mixx"
    flooz = "flooz"
    presentiel = "presentiel"
    
class RecuPar(str, PyEnum):
    livreur = "livreur"
    marchand = "marchand"


class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    livraison_id = Column(UUID(as_uuid=True), ForeignKey("livraisons.id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    montant = Column(Float)
    statut_paiement = Column(Enum(StatutPaiement), default=StatutPaiement.en_attente)
    methode_paiement = Column(Enum(MethodePaiement), default=MethodePaiement.mixx)
    recu_par = Column(Enum(RecuPar), default=RecuPar.livreur)
    date_paiement = Column(DateTime, default=datetime.utcnow)
    
    livraison = relationship("Livraison", back_populates="paiement")
    client = relationship("Client", back_populates="paiements")