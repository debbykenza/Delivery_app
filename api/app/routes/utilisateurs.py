from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.utilisateur import UtilisateurResponse, UtilisateurUpdate
from app.services.utilisateur import mettre_a_jour_utilisateur, recuperer_tous_les_utilisateurs
from app.core.database import get_db

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.get("/", response_model=List[UtilisateurResponse])
def lister_utilisateurs(db: Session = Depends(get_db)):
    """
    Récupère la liste de tous les utilisateurs.
    """
    utilisateurs = recuperer_tous_les_utilisateurs(db)
    return utilisateurs

@router.put("/{utilisateur_id}", response_model=UtilisateurResponse)
def modifier_utilisateur(utilisateur_id: UUID, utilisateur_data: UtilisateurUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un utilisateur.
    """
    utilisateur = mettre_a_jour_utilisateur(db, utilisateur_id, utilisateur_data)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur