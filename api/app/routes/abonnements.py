# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from uuid import UUID
# from app.services.abonnement import ServiceAbonnement
# from app.schemas.abonnement import AbonnementCreate, AbonnementRead
# from app.core.database import get_db

# router = APIRouter(prefix="/abonnements", tags=["Abonnements"])

# @router.post("/", response_model=AbonnementRead, status_code=status.HTTP_201_CREATED)
# def creer_abonnement(data: AbonnementCreate, db: Session = Depends(get_db)):
#     return ServiceAbonnement.creer_abonnement(db, data)

# @router.delete("/{abonnement_id}")
# def supprimer_abonnement(abonnement_id: UUID, db: Session = Depends(get_db)):
#     success = ServiceAbonnement.supprimer_abonnement(db, abonnement_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Abonnement introuvable")
#     return {"message": "Abonnement supprimé avec succès."}

# @router.get("/", response_model=list[AbonnementRead])
# def lister_abonnements(db: Session = Depends(get_db)):
#     return ServiceAbonnement.lister_abonnements(db)

# @router.get("/marchand/{marchand_id}", response_model=list[AbonnementRead])
# def abonnements_par_marchand(marchand_id: UUID, db: Session = Depends(get_db)):
#     return ServiceAbonnement.get_abonnement_par_marchand(db, marchand_id)

# @router.get("/statut/{statut}", response_model=list[AbonnementRead])
# def abonnements_par_statut(statut: str, db: Session = Depends(get_db)):
#     return ServiceAbonnement.get_abonnement_par_statut(db, statut)
