from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from sqlalchemy import select, func
from geoalchemy2.functions import ST_AsGeoJSON
from shapely import wkt
import json

from fastapi import HTTPException
from app.models.adresse import Adresse
from app.schemas.adresse import AdresseCreate, AdresseRead

# ✅ Fonction utilitaire : conversion WKT → GeoJSON
def wkt_to_geojson(wkt_string):
    shape = wkt.loads(wkt_string)
    return {
        "type": "Feature",
        "geometry": shape.__geo_interface__,
        "properties": {}
    }

class ServiceAdresse:
    @staticmethod
    def creer_adresse(db: Session, adresse_data: AdresseCreate) -> Adresse:
        # 🛑 Vérification : un seul ID doit être fourni
        liens = [
            adresse_data.utilisateur_id,
            adresse_data.marchand_id,
            adresse_data.livreur_id,
            adresse_data.client_id
        ]
        ids_remplis = [id for id in liens if id is not None]
        if len(ids_remplis) != 1:
            raise HTTPException(
                status_code=400,
                detail="Une seule des relations (utilisateur, marchand, livreur ou client) doit être renseignée."
            )

        # 🧭 Conversion des géométries WKT
        point_geom = from_shape(wkt.loads(adresse_data.position_point_wkt), srid=4326)
        poly_geom = None
        if adresse_data.zone_polygone_wkt:
            poly_geom = from_shape(wkt.loads(adresse_data.zone_polygone_wkt), srid=4326)

        # ✅ Création de l'adresse
        adresse = Adresse(
            pays=adresse_data.pays,
            ville=adresse_data.ville,
            position_point=point_geom,
            zone_polygone=poly_geom,
            utilisateur_id=adresse_data.utilisateur_id,
            marchand_id=adresse_data.marchand_id,
            livreur_id=adresse_data.livreur_id,
            client_id=adresse_data.client_id,
        )
        db.add(adresse)
        db.commit()
        db.refresh(adresse)
        return adresse

    @staticmethod
    def modifier_adresse(db: Session, adresse_id: str, adresse_data: AdresseCreate) -> Adresse:
        adresse = db.query(Adresse).filter(Adresse.id == adresse_id).first()
        if not adresse:
            return None

        adresse.pays = adresse_data.pays
        adresse.ville = adresse_data.ville
        adresse.position_point = from_shape(wkt.loads(adresse_data.position_point_wkt), srid=4326)

        if adresse_data.zone_polygone_wkt:
            adresse.zone_polygone = from_shape(wkt.loads(adresse_data.zone_polygone_wkt), srid=4326)
        else:
            adresse.zone_polygone = None

        adresse.utilisateur_id = adresse_data.utilisateur_id
        adresse.marchand_id = adresse_data.marchand_id
        adresse.livreur_id = adresse_data.livreur_id
        adresse.client_id = adresse_data.client_id

        db.commit()
        db.refresh(adresse)
        return adresse

    @staticmethod
    def supprimer_adresse(db: Session, adresse_id: str) -> bool:
        adresse = db.query(Adresse).filter(Adresse.id == adresse_id).first()
        if not adresse:
            return False
        db.delete(adresse)
        db.commit()
        return True

    @staticmethod
    def get_zone_polygone_geojson(db: Session, adresse_id: str):
        result = db.execute(
            select(func.ST_AsText(Adresse.zone_polygone)).where(Adresse.id == adresse_id)
        ).scalar_one_or_none()

        if result:
            return wkt_to_geojson(result)
        return None

    @staticmethod
    def get_position_point_geojson(db: Session, adresse_id: str):
        result = db.execute(
            select(func.ST_AsText(Adresse.position_point)).where(Adresse.id == adresse_id)
        ).scalar_one_or_none()

        if result:
            return wkt_to_geojson(result)
        return None

    @staticmethod
    def lister_toutes_adresses(db: Session):
        adresses = db.query(Adresse).all()
        return [AdresseRead.from_orm(adresse) for adresse in adresses]

    @staticmethod
    def lister_adresses_par_client(db: Session, client_id: str):
        adresses = db.query(Adresse).filter(Adresse.client_id == client_id).all()
        return [AdresseRead.from_orm(adresse) for adresse in adresses]

    @staticmethod
    def lister_adresses_par_livreur(db: Session, livreur_id: str):
        adresses = db.query(Adresse).filter(Adresse.livreur_id == livreur_id).all()
        return [AdresseRead.from_orm(adresse) for adresse in adresses]

    @staticmethod
    def lister_adresses_par_marchand(db: Session, marchand_id: str):
        adresses = db.query(Adresse).filter(Adresse.marchand_id == marchand_id).all()
        return [AdresseRead.from_orm(adresse) for adresse in adresses]

    @staticmethod
    def lister_adresses_par_utilisateur(db: Session, utilisateur_id: str):
        adresses = db.query(Adresse).filter(Adresse.utilisateur_id == utilisateur_id).all()
        return [AdresseRead.from_orm(adresse) for adresse in adresses]

    