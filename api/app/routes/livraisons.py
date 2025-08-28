from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies.auth import recuperer_utilisateur_courant
from app.models.livraison import Livraison
from app.schemas.livraison import LivraisonCreate, LivraisonRead, LivraisonStatutUpdate, ProblemeSignalement
from app.services.livraison import LivraisonService
from app.core.database import get_db

router = APIRouter(prefix="/livraisons", tags=["Livraisons"])


@router.post("/creer", response_model=None)
def creer_livraison(livraison: LivraisonCreate, db: Session = Depends(get_db)):
    return LivraisonService.creer_livraison(db, livraison)

@router.get("/", response_model=List[LivraisonRead])
def lister_livraisons(db: Session = Depends(get_db)):
    return LivraisonService.obtenir_livraisons(db)

@router.get("/suivre/{livraison_id}")
def obtenir_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    livraison = LivraisonService.obtenir_livraison(db, livraison_id)
    if not livraison:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    return livraison

@router.delete("/supprimer/{livraison_id}")
def supprimer_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    return LivraisonService.supprimer_livraison(db, livraison_id)


# @router.put("/accepter/{livraison_id}/{livreur_id}")
# def accepter_livraison(livraison_id: UUID, livreur_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.accepter_livraison(db, livraison_id, livreur_id)


# @router.put("/valider/{livraison_id}")
# def valider_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.valider_livraison(db, livraison_id)


# @router.put("/annuler/{livraison_id}")
# def annuler_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.annuler_livraison(db, livraison_id)


# @router.get("/historique/{livreur_id}")
# def voir_historique_livraisons(livreur_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.voir_historique_livraisons(db, livreur_id)


# @router.get("/rechercher/")
# def rechercher_livraisons(mot_cle: str, db: Session = Depends(get_db)):
#     return LivraisonService.rechercher_livraisons(db, mot_cle)


# @router.get("/commande/{commande_id}")
# def voir_details_commande(commande_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.voir_details_commande(db, commande_id)


@router.get("/disponibles")
def livraisons_disponibles(db: Session = Depends(get_db)):
    return LivraisonService.livraisons_disponibles(db)



@router.put("/statut/{livraison_id}")
def mettre_a_jour_statut(livraison_id: UUID, update: LivraisonStatutUpdate, db: Session = Depends(get_db)):
    return LivraisonService.mettre_a_jour_statut(db, livraison_id, update)


# @router.put("/demarrer/{livraison_id}")
# def demarrer_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
#     return LivraisonService.demarrer_livraison(db, livraison_id)


# @router.put("/signaler-probleme/{livraison_id}")
# def signaler_probleme(livraison_id: UUID, data: ProblemeSignalement, db: Session = Depends(get_db)):
#     return LivraisonService.signaler_probleme(db, livraison_id, data)


@router.get("/mes-livraisons", response_model=List[LivraisonRead])
def mes_livraisons(
    statut: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return LivraisonService.get_livraisons_par_utilisateur(db, current_user.id, statut)
    
# @router.get("/mes-livraisons/{marchand_id}")
# def Lister_commandes_marchand(marchand_id: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
#     return ServiceCommande.obtenir_commandes_par_marchand(db, marchand_id)

@router.get("/marchand/{marchand_id}", response_model=List[LivraisonRead])
def livraisons_marchand(
    marchand_id: UUID, 
    statut: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupère les livraisons d'un marchand spécifique"""
    return LivraisonService.get_livraisons_marchand(db, marchand_id, statut)

@router.get("/livreur/{livreur_id}", response_model=List[LivraisonRead])
def livraisons_livreur(
    livreur_id: UUID, 
    statut: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupère les livraisons d'un livreur spécifique"""
    return LivraisonService.get_livraisons_livreur(db, livreur_id, statut)

@router.get("/client/{client_id}", response_model=List[LivraisonRead])
def livraisons_client(
    client_id: UUID, 
    statut: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupère les livraisons d'un client spécifique"""
    return LivraisonService.get_livraisons_client(db, client_id, statut)

@router.get("/livraisons/{livraison_id}/infos-client", response_model=dict)
def obtenir_infos_client_livraison(
    livraison_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère les informations complètes du client associé à une livraison
    """
    livraison = LivraisonService.obtenir_livraison(db, livraison_id)
    if not livraison:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    
    infos_client = LivraisonService.obtenir_infos_client_par_livraison(db, livraison_id)
    
    if not infos_client:
        raise HTTPException(status_code=404, detail="Informations client non trouvées")
    
    return {
        "livraison_id": livraison_id,
        "client": infos_client
    }