from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    nom: str
    adresse: str
    contact: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    nom: Optional[str] = None
    adresse: Optional[str] = None
    contact: Optional[str] = None


class ClientOut(ClientBase):
    id: UUID
    date_creation: datetime

    model_config = {
        "from_attributes": True  # remplace orm_mode en Pydantic v2
    }


class ClientRead(ClientOut):
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "b5cee64b-24bd-4c26-b0d8-98205879c937",
                "nom": "NICOUE Kenza",
                "adresse": "123 Rue de Paris, 75001 Paris",
                "contact": "+33 6 12 34 56 78",
                "date_creation": "2023-10-01T12:00:00Z"
            }
        }
    }
