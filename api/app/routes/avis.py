from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.avis import AvisCreate, AvisRead
from app.services.avis import ServiceAvis

router = APIRouter(prefix="/avis", tags=["Avis"])

@router.post("/", response_model=AvisRead, status_code=status.HTTP_201_CREATED)
def donner_avis(avis: AvisCreate, db: Session = Depends(get_db)):
    try:
        nouveau = ServiceAvis.creer_avis(db=db, avis_data=avis)
        return nouveau
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement de l'avis : {str(e)}")

@router.delete("/{avis_id}", status_code=204)
def supprimer_avis(avis_id: UUID, db: Session = Depends(get_db)):
    """
    Supprime un avis existant.
    """
    success = ServiceAvis.supprimer_avis(db, avis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Avis introuvable")
    return  {"message": "L'avis a été supprimé avec succès"}
@router.get("/", response_model=list[AvisRead])
def lister_avis(db: Session = Depends(get_db)):
    """
    Liste tous les avis.
    """
    return ServiceAvis.lister_avis(db)

@router.get("/livreur/{livreur_id}", response_model=list[AvisRead])
def lister_avis_par_livreur(livreur_id: UUID, db: Session = Depends(get_db)):
    """
    Liste les avis donnés à un livreur spécifique.
    """
    return ServiceAvis.lister_avis_par_livreur(db, livreur_id)