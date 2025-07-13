from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.position import PositionCreate, PositionOut, PositionUpdate
from app.services.position import ServicePosition

router = APIRouter(prefix="/positions", tags=["Positions"])

@router.post("/", response_model=PositionOut)
def enregistrer_position(position_data: PositionCreate, db: Session = Depends(get_db)):
    return ServicePosition.enregistrer_position(db, position_data)

@router.get("/livreur/{livreur_id}", response_model=PositionOut)
def derniere_position(livreur_id: UUID, db: Session = Depends(get_db)):
    position = ServicePosition.get_derniere_position_livreur(db, livreur_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position non trouvée")
    return position

@router.get("/livraison/{livraison_id}", response_model=list[PositionOut])
def positions_par_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    return ServicePosition.get_positions_par_livraison(db, livraison_id)

@router.put("/{livreur_id}", response_model=PositionOut)
def modifier_position(livreur_id: UUID, data: PositionUpdate, db: Session = Depends(get_db)):
    try:
        return ServicePosition.maj_derniere_position(db, livreur_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Position non trouvée")

@router.delete("/{position_id}", status_code=status.HTTP_200_OK)
def supprimer_position(position_id: UUID, db: Session = Depends(get_db)):
    """
    Supprime une position GPS (cas exceptionnel uniquement).
    """
    success = ServicePosition.supprimer_position(db, position_id)
    if not success:
        raise HTTPException(status_code=404, detail="Position non trouvée")
    
    return {"message": "Position supprimée avec succès"}