from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.adresse import AdresseCreate, AdresseRead
from app.core.database import get_db
from app.services.adresse import ServiceAdresse

router = APIRouter(prefix="/adresses", tags=["Adresses"])

# ✅ Créer une adresse
@router.post("/", status_code=201)
def creer_adresse(adresse_data: AdresseCreate, db: Session = Depends(get_db)):
    adresse = ServiceAdresse.creer_adresse(db, adresse_data)
    return {
        "message": "Adresse créée avec succès",
        "adresse": AdresseRead.from_orm(adresse)
    }

# ✅ Modifier une adresse
@router.put("/{adresse_id}", status_code=200)
def modifier_adresse(
    adresse_id: str,
    adresse_data: AdresseCreate,
    db: Session = Depends(get_db)
):
    adresse = ServiceAdresse.modifier_adresse(db, adresse_id, adresse_data)
    if not adresse:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")
    return {
        "message": "Adresse modifiée avec succès",
        "adresse": AdresseRead.from_orm(adresse)
    }
# ✅ Supprimer une adresse
@router.delete("/{adresse_id}", status_code=200)
def supprimer_adresse(adresse_id: str, db: Session = Depends(get_db)):
    success = ServiceAdresse.supprimer_adresse(db, adresse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")
    return {"message": "Adresse supprimée avec succès"}

# ✅ Lister toutes les adresses
@router.get("/", response_model=List[AdresseRead])
def lister_adresses(db: Session = Depends(get_db)):
    return ServiceAdresse.lister_toutes_adresses(db)

# ✅ Lister par client
@router.get("/client/{client_id}", response_model=List[AdresseRead])
def lister_adresses_client(client_id: str, db: Session = Depends(get_db)):
    return ServiceAdresse.lister_adresses_par_client(db, client_id)

# ✅ Lister par livreur
@router.get("/livreur/{livreur_id}", response_model=List[AdresseRead])
def lister_adresses_livreur(livreur_id: str, db: Session = Depends(get_db)):
    return ServiceAdresse.lister_adresses_par_livreur(db, livreur_id)

# ✅ Lister par marchand
@router.get("/marchand/{marchand_id}", response_model=List[AdresseRead])
def lister_adresses_marchand(marchand_id: str, db: Session = Depends(get_db)):
    return ServiceAdresse.lister_adresses_par_marchand(db, marchand_id)

# ✅ Lister par utilisateur
@router.get("/utilisateur/{utilisateur_id}", response_model=List[AdresseRead])
def lister_adresses_utilisateur(utilisateur_id: str, db: Session = Depends(get_db)):
    return ServiceAdresse.lister_adresses_par_utilisateur(db, utilisateur_id)

# ✅ Récupérer le polygone au format GeoJSON
@router.get("/{adresse_id}/zone/geojson")
def get_zone_geojson(adresse_id: str, db: Session = Depends(get_db)):
    geojson = ServiceAdresse.get_zone_polygone_geojson(db, adresse_id)
    if not geojson:
        raise HTTPException(status_code=404, detail="Zone non trouvée")
    return geojson

# ✅ Récupérer le point au format GeoJSON
@router.get("/{adresse_id}/point/geojson")
def get_position_point_geojson(adresse_id: str, db: Session = Depends(get_db)):
    geojson = ServiceAdresse.get_position_point_geojson(db, adresse_id)
    if not geojson:
        raise HTTPException(status_code=404, detail="Point non trouvé")
    return geojson
