from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CleAPICreate(BaseModel):
    nom: Optional[str] = None
    utilisateur_id: UUID

class CleAPIResponse(BaseModel):
    id: UUID
    nom: Optional[str]
    cle: str
    utilisateur_id: UUID
    est_active: bool
    date_creation: datetime

    class Config:
        from_attributes = True

class StatistiquesAPIResponse(BaseModel):
    total_cles: int
    cles_actives: int
    cles_revoquees: int
    

class CleAPINomUpdate(BaseModel):
    nouveau_nom: str    
    
class CleAPIRegenerationResponse(BaseModel):
    id: UUID
    cle: str
    est_active: bool
    date_creation: datetime

    class Config:
        from_attributes = True

class CleAPIRevokeResponse(BaseModel):
    id: UUID
    est_active: bool
    date_creation: datetime

    class Config:
        from_attributes = True
        
class CleAPIListResponse(BaseModel):
    id: UUID
    nom: Optional[str]
    cle: str
    utilisateur_id: UUID
    est_active: bool
    date_creation: datetime

    class Config:
        from_attributes = True

class CleAPIList(BaseModel):
    cle_apis: list[CleAPIListResponse]

    class Config:
        from_attributes = True
        orm_mode = True
        
class CleAPIUpdate(BaseModel):
    nom: Optional[str] = None
    utilisateur_id: Optional[UUID] = None
    est_active: Optional[bool] = None

    class Config:
        from_attributes = True
        orm_mode = True
        
class CleAPIUpdateResponse(BaseModel):
    id: UUID
    nom: Optional[str]
    utilisateur_id: UUID
    est_active: bool
    date_creation: datetime

    class Config:
        from_attributes = True
        orm_mode = True
        