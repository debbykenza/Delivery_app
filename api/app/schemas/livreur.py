from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field

class TypeVehicule(str, Enum):
    moto = "moto"
    voiture = "voiture"
    camion = "camion"
    tricycle = "tricycle"


class StatutLivreur(str, Enum):
    disponible = "disponible"
    indisponible = "indisponible"


class LivreurBase(BaseModel):
    nom: str
    vehicule: TypeVehicule
    contact: str
    immatriculation: str
    mot_de_passe: str
    est_actif: bool = False
    statut: StatutLivreur = StatutLivreur.disponible
    # est_disponible: bool = True


class LivreurCreate(LivreurBase):
    pass


class LivreurRead(LivreurBase):
    id: UUID
    date_creation: datetime

    class Config:
        orm_mode = True


class LivreurUpdate(BaseModel):
    nom: str
    vehicule: TypeVehicule
    contact: str
    immatriculation: str
    # statut: StatutLivreur | None = None
    # est_disponible: bool | None = None

class StatutLivreurUpdate(BaseModel):
    nouveau_statut: StatutLivreur

    class Config:
        schema_extra = {
            "example": {
                "nouveau_statut": "disponible"
            }
        }