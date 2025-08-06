from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    utilisateur = "utilisateur"
    marchand = "marchand"
    livreur = "livreur"

class UtilisateurBase(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[Role] = Role.utilisateur  # Valeur par défaut pour le rôle
    

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str
    role: Role 

class UtilisateurRead(UtilisateurBase):
    id: UUID
    is_active: bool
    role: str
    date_creation: datetime

    class Config:
        from_attributes = True

class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    
class UtilisateurResponse(BaseModel):
    id: UUID
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool
    role: Role
    date_creation: datetime

    class Config:
        from_attributes = True
        orm_mode = True  # Permet de lire les données à partir des modèles SQLAlchemy
        
class UtilisateurDelete(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
        orm_mode = True  # Permet de lire les données à partir des modèles SQLAlchemy


