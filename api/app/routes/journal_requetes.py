from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.journal_requete import (
    lister_requetes_par_marchand,
    obtenir_stats_requetes,
    requetes_par_periode,
    requetes_par_periode_et_marchand,
)
from app.core.database import get_db

router = APIRouter(prefix="/stats", tags=["Journal des Requêtes"])

# Stats globales, regroupées par endpoint et méthode
@router.get("/requetes")
def lister_stats_requetes(db: Session = Depends(get_db)):
    return obtenir_stats_requetes(db)

# Stats globales par périodes définies
@router.get("/requetes/jour")
def requetes_dernier_jour(db: Session = Depends(get_db)):
    return requetes_par_periode(1, db)

@router.get("/requetes/semaine")
def requetes_7_jours(db: Session = Depends(get_db)):
    return requetes_par_periode(7, db)

@router.get("/requetes/mois")
def requetes_30_jours(db: Session = Depends(get_db)):
    return requetes_par_periode(30, db)

@router.get("/requetes/trimestre")
def requetes_90_jours(db: Session = Depends(get_db)):
    return requetes_par_periode(90, db)

@router.get("/requetes/annee")
def requetes_annee(db: Session = Depends(get_db)):
    return requetes_par_periode(365, db)

# # Stats par marchand avec filtre par périodes
# @router.get("/requetes/marchand/{marchand_id}/jour")
# def requetes_marchand_dernier_jour(marchand_id: str, db: Session = Depends(get_db)):
#     return requetes_par_periode_et_marchand(marchand_id, 1, db)

# @router.get("/requetes/marchand/{marchand_id}/semaine")
# def requetes_marchand_7_jours(marchand_id: str, db: Session = Depends(get_db)):
#     return requetes_par_periode_et_marchand(marchand_id, 7, db)

# @router.get("/requetes/marchand/{marchand_id}/mois")
# def requetes_marchand_30_jours(marchand_id: str, db: Session = Depends(get_db)):
#     return requetes_par_periode_et_marchand(marchand_id, 30, db)

# @router.get("/requetes/marchand/{marchand_id}/trimestre")
# def requetes_marchand_90_jours(marchand_id: str, db: Session = Depends(get_db)):
#     return requetes_par_periode_et_marchand(marchand_id, 90, db)

# @router.get("/requetes/marchand/{marchand_id}/annee")
# def requetes_marchand_annee(marchand_id: str, db: Session = Depends(get_db)):
#     return requetes_par_periode_et_marchand(marchand_id, 365, db)


# # Liste brute de toutes les requêtes pour un marchand, sans agrégation
# @router.get("/requetes/marchand/{marchand_id}")
# def toutes_requetes_marchand(marchand_id: str, db: Session = Depends(get_db)):
#     return lister_requetes_par_marchand(marchand_id, db)
