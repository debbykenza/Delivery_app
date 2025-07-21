# schemas/abonnement.py

from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class StatutAbonnement(str, Enum):
    actif = "actif"
    expiré = "expiré"
    suspendu = "suspendu"


class AbonnementCreate(BaseModel):
    marchand_id: UUID
    montant: float
    duree_jours: int = 30  # Par défaut 30 jours


class AbonnementRead(BaseModel):
    id: UUID
    marchand_id: UUID
    montant: float
    date_debut: datetime
    date_expiration: datetime
    statut: StatutAbonnement

    class Config:
        orm_mode = True


class AbonnementUpdate(BaseModel):
    montant: float | None = None
    statut: StatutAbonnement | None = None
    date_expiration: datetime | None = None


