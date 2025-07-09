from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.cle_api import *
from app.services.cle_api import *
from app.core.database import get_db

router = APIRouter(prefix="/cles-api", tags=["Clés API"])

@router.post("/creer", response_model=CleAPIResponse)
def creer_cle_api(payload: CleAPICreate, db: Session = Depends(get_db)):
    return creer_cle(db, payload)

@router.get("/liste", response_model=list[CleAPIResponse])
def lister_cles_api(utilisateur_id: UUID, db: Session = Depends(get_db)):
    return recuperer_cles_par_utilisateur(db, utilisateur_id)

@router.delete("/supprimer/{cle_id}", response_model=dict)
def supprimer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
    return supprimer_cle(db, cle_id)

@router.put("/revocation/{cle_id}", response_model=CleAPIResponse)
def revoquer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
    return revoquer_cle(db, cle_id)

@router.put("/nommer/{cle_id}", response_model=CleAPIResponse)
def nommer_cle_api(cle_id: UUID, nouveau_nom: str, db: Session = Depends(get_db)):
    return nommer_cle(db, cle_id, nouveau_nom)

@router.put("/regenerer/{cle_id}", response_model=CleAPIResponse)
def regenerer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
    return regenerer_cle(db, cle_id)

@router.get("/statistiques/{utilisateur_id}", response_model=StatistiquesAPIResponse)
def consulter_stats_api(utilisateur_id: UUID, db: Session = Depends(get_db)):
    return consulter_statistiques(db, utilisateur_id)
