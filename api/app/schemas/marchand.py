from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class MarchandBase(BaseModel):
    nom: str
    contact: str
    adresse: Optional[str] = None

class MarchandCreate(MarchandBase):
    utilisateur_id: UUID
    nom: str

class MarchandOut(MarchandBase):
    id: UUID
    date_creation: datetime

    class Config:
        orm_mode = True

class MarchandUpdate(BaseModel):
    nom: Optional[str] = None
    contact: Optional[str] = None
    adresse: Optional[str] = None
    

