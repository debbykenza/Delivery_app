from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from geoalchemy2.shape import to_shape

class AdresseCreate(BaseModel):
    pays: str
    ville: str
    position_point_wkt: str  # Point au format WKT, ex: "POINT(-1.2345 48.1234)"
    zone_polygone_wkt: Optional[str] = None  # Polygone WKT optionnel

    utilisateur_id: Optional[UUID] = None
    marchand_id: Optional[UUID] = None
    livreur_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    class Config:
        json_schema_extra = {
            "example": {
                "pays": "France",
                "ville": "Paris",
                "position_point_wkt": "POINT(2.3522 48.8566)",
                # "zone_polygone_wkt": "POLYGON((2.3522 48.8566, 2.3622 48.8666, 2.3722 48.8566, 2.3522 48.8566))",
                "utilisateur_id": None,
                "marchand_id": None,
                "livreur_id": None,
                "client_id": "abf4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            }
        }
        
class AdresseRead(BaseModel):
    id: UUID
    pays: str
    ville: str
    position_point_wkt: str
    zone_polygone_wkt: Optional[str] = None
    utilisateur_id: Optional[UUID]
    marchand_id: Optional[UUID]
    livreur_id: Optional[UUID]
    client_id: Optional[UUID]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, adresse):
        return cls(
            id=adresse.id,
            pays=adresse.pays,
            ville=adresse.ville,
            position_point_wkt=to_shape(adresse.position_point).wkt if adresse.position_point else None,
            zone_polygone_wkt=to_shape(adresse.zone_polygone).wkt if adresse.zone_polygone else None,
            utilisateur_id=adresse.utilisateur_id,
            marchand_id=adresse.marchand_id,
            livreur_id=adresse.livreur_id,
            client_id=adresse.client_id,
        )