from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.livreur import LivreurCreate, LivreurRead, LivreurUpdate, StatutLivreurUpdate
from app.services.livreur import LivreurService
from app.core.database import get_db

router = APIRouter(prefix="/livreurs", tags=["Livreurs"])

@router.post("/", response_model=LivreurRead, status_code=status.HTTP_201_CREATED)
def creer_livreur(livreur: LivreurCreate, db: Session = Depends(get_db)):
    return LivreurService.creer_livreur(db, livreur)

@router.get("/", response_model=list[LivreurRead])
def lister_livreurs(db: Session = Depends(get_db)):
    return LivreurService.lister_livreurs(db)

@router.get("/{livreur_id}", response_model=LivreurRead)
def obtenir_livreur(livreur_id: UUID, db: Session = Depends(get_db)):
    livreur = LivreurService.obtenir_livreur(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return livreur

@router.patch("/{livreur_id}/statut", response_model=LivreurRead)
def changer_statut_livreur(livreur_id: UUID, update: StatutLivreurUpdate, db: Session = Depends(get_db)):
    livreur = LivreurService.mettre_a_jour_statut(db, livreur_id, update)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return livreur

@router.patch("/{livreur_id}/modifier", response_model=LivreurRead)
def modifier_livreur(livreur_id: UUID, update: LivreurUpdate, db: Session = Depends(get_db)):
    livreur = LivreurService.modifier_livreur(db, livreur_id, update)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return livreur


@router.delete("/{livreur_id}")
def supprimer_livreur(livreur_id: UUID, db: Session = Depends(get_db)):
    success = LivreurService.supprimer_livreur(db, livreur_id)
    if not success:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return {"detail": "Livreur supprimé avec succès"}

