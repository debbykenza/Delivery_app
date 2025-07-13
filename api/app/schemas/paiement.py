
from uuid import UUID
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.paiement import MethodePaiement, StatutPaiement


class MethodePaiement(str, Enum):
    mixx = "mixx"
    flooz = "flooz"
    presentiel = "presentiel"

class StatutPaiement(str, Enum):
    en_attente = "en_attente"
    remis_livreur = "remis_livreur"
    paye = "paye"
    echoue = "echoue"
    rembourse = "rembourse"


class RecuPar(str, Enum):
    marchand = "marchand"
    livreur = "livreur"

class PaiementCreate(BaseModel):
    montant: float
    livraison_id: UUID
    client_id: UUID
    # statut_paiement: StatutPaiement = StatutPaiement.en_attente
    methode_paiement: MethodePaiement #= MethodePaiement.presentiel
    # recu_par: RecuPar #= RecuPar.livreur
    
    class Config:
        schema_extra = {
            "example": {
                "montant": 1500.0,
                "livraison_id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "123e4567-e89b-12d3-a456-426614174001",
                "statut_paiement": "en_attente",
                "methode_paiement": "mixx",
                "recu_par": "livreur"
            }
        }
        orm_mode = True



class PaiementRead(BaseModel):
    id: UUID
    client_id: UUID
    livraison_id: UUID
    montant: float
    methode_paiement: MethodePaiement
    statut_paiement: StatutPaiement
    recu_par: RecuPar
    date_paiement: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "123e4567-e89b-12d3-a456-426614174001",
                "livraison_id": "123e4567-e89b-12d3-a456-426614174002",
                "montant": 1500.0,
                "methode": "mixx",
                "statut": "en_attente",
                "recu_par": "livreur",
                "date_paiement": "2023-10-01T12:00:00Z"
            }
        }