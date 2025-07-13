from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.paiement import Paiement, MethodePaiement
from app.models.paiement import RecuPar, StatutPaiement
from app.models.paiement import StatutPaiement
from app.schemas.paiement import PaiementCreate, PaiementRead
from app.services.paiement import ServicePaiement
from app.core.database import get_db


router = APIRouter(prefix="/paiements", tags=["Paiements"])

@router.post("/", response_model=PaiementRead)
def creer_paiement(data: PaiementCreate, db: Session = Depends(get_db)):
    return ServicePaiement.creer_paiement(db, data)

@router.delete("/{paiement_id}")
def supprimer_paiement(paiement_id: UUID, db: Session = Depends(get_db)):
    if not ServicePaiement.supprimer_paiement(db, paiement_id):
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    return {"message": "Paiement supprimé avec succès"}

@router.get("/", response_model=List[PaiementRead])
def lister_paiements(db: Session = Depends(get_db)):
    return ServicePaiement.lister_paiements(db)

@router.get("/{paiement_id}", response_model=PaiementRead)
def obtenir_paiement(paiement_id: UUID, db: Session = Depends(get_db)):
    paiement = ServicePaiement.obtenir_paiement(db, paiement_id)
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    return paiement

@router.get("/client/{client_id}", response_model=List[PaiementRead])
def paiements_par_client(client_id: UUID, db: Session = Depends(get_db)):
    return ServicePaiement.rechercher_par_client(db, client_id)

@router.get("/marchand/{marchand_id}", response_model=List[PaiementRead])
def paiements_par_marchand(marchand_id: UUID, db: Session = Depends(get_db)):
    return ServicePaiement.rechercher_par_marchand(db, marchand_id)

@router.put("/{paiement_id}/transferer", response_model=PaiementRead)
def transferer_au_marchand(paiement_id: UUID, db: Session = Depends(get_db)):
    return ServicePaiement.transferer_au_marchand(db, paiement_id)


@router.get("/statut/{statut}", response_model=List[PaiementRead])
def paiements_par_statut(statut: StatutPaiement, db: Session = Depends(get_db)):
    return ServicePaiement.rechercher_par_statut(db, statut)

@router.put("/{paiement_id}/rembourser", response_model=PaiementRead)
def rembourser_paiement(paiement_id: UUID, db: Session = Depends(get_db)):
    return ServicePaiement.rembourser_paiement(db, paiement_id)
