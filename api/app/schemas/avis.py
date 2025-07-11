from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class AvisCreate(BaseModel):
    livreur_id: UUID
    livraison_id: UUID
    client_id: UUID
    commentaire: Optional[str] = None
    note: int = Field(..., ge=1, le=5, description="Note sur 5")

class AvisRead(BaseModel):
    id: UUID
    livreur_id: UUID
    livraison_id: UUID
    client_id: UUID
    commentaire: Optional[str]
    note: int
    date_avis: datetime

    class Config:
        orm_mode = True

class AvisUpdate(BaseModel):
    commentaire: Optional[str] = None
    note: Optional[int] = Field(None, ge=1, le=5, description="Note sur 5")