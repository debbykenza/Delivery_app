from pydantic import BaseModel, HttpUrl
from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Optional


class StatutLivraison(str, Enum):
    en_attente = "en_attente"
    acceptee = "acceptee"
    en_cours = "en_cours"
    terminee = "terminee"
    annulee = "annulee"
    # livree = "livree"


class TypeLivraison(str, Enum):
    express = "express"
    standard = "standard"


class LivraisonBase(BaseModel):
    commande_id: UUID
    livreur_id: Optional[UUID] = None
    statut: StatutLivraison = StatutLivraison.en_attente
    # url_suivi: Optional[HttpUrl] = None
    # type_livraison: TypeLivraison
    #probleme: Optional[str] = None


class LivraisonCreate(LivraisonBase):
    pass


class LivraisonRead(LivraisonBase):
    id: UUID
    date_creation: datetime

    class Config:
        from_attributes = True


class LivraisonStatutUpdate(BaseModel):
    nouveau_statut: StatutLivraison


class ProblemeSignalement(BaseModel):
    description: str
    class Config:
        schema_extra = {
            "example": {
                "description": "Le livreur a rencontré un problème avec la livraison."
            }
        }

class CommandeInfo(BaseModel):
    id: UUID
    reference: Optional[str] = None
    client_id: Optional[UUID] = None
    total: Optional[float] = None
    
    class Config:
        from_attributes = True

class LivreurInfo(BaseModel):
    id: UUID
    nom: str
    # prenom: str
    contact: Optional[str] = None
    
    class Config:
        from_attributes = True

class LivraisonRead(BaseModel):
    id: UUID
    commande_id: UUID
    livreur_id: Optional[UUID] = None
    # client_id: Optional[UUID] = None
    statut: StatutLivraison
    date_livraison: datetime
    probleme: Optional[str] = None
    
    # Relations
    commande: Optional[CommandeInfo] = None
    livreur: Optional[LivreurInfo] = None
    
    class Config:
        from_attributes = True