# from pydantic import BaseModel, Field
# from uuid import UUID
# from datetime import datetime
# from enum import Enum
# from typing import Optional


# class StatutAbonnement(str, Enum):
#     actif = "actif"
#     expiré = "expiré"
#     suspendu = "suspendu"


# class AbonnementCreate(BaseModel):
#     marchand_id: UUID
#     montant: float
#     duree_jours: int  # Ex: 30 jours

# class AbonnementRead(BaseModel):
#     id: UUID
#     marchand_id: UUID
#     montant: float
#     date_debut: datetime
#     date_expiration: datetime
#     statut: StatutAbonnement

#     class Config:
#         orm_mode = True
