from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.position import Position

class PositionCreate(BaseModel):
    livreur_id: UUID
    livraison_id: UUID
    latitude: float
    longitude: float

class PositionOut(BaseModel):
    id: UUID
    livreur_id: UUID
    livraison_id: UUID
    latitude: float
    longitude: float
    timestamp: datetime

    class Config:
        orm_mode = True

class PositionUpdate(BaseModel):
    latitude: float
    longitude: float
