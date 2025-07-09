from http.client import HTTPException
from app.models.marchand import Marchand
from app.schemas.marchand import MarchandCreate, MarchandOut
from app.core.database import get_db
from app.dependencies.auth import recuperer_utilisateur_courant
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import marchand as marchand_service
from uuid import UUID

router = APIRouter(prefix="/marchands", tags=["Marchands"])

@router.post("/", response_model=MarchandOut)
def creer_marchand(marchand_data: MarchandCreate, db: Session = Depends(get_db)):
    return marchand_service.creer_marchand(db, marchand_data)


@router.get("/commandes")
def Lister_commandes_marchand(db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
    marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
    return marchand_service.recevoir_commandes(db, marchand.id)

@router.put("/commandes/{commande_id}/accepter")
def accepter_commande(commande_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.accepter_commande(db, commande_id)

@router.put("/commandes/{commande_id}/livrer")
def lancer_livraison(commande_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.lancer_livraison(db, commande_id)

@router.put("/commandes/{commande_id}/annuler")
def annuler_livraison(commande_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.annuler_livraison(db, commande_id)

@router.get("/commandes/{commande_id}")
def voir_details_commande(commande_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.voir_details_commande(db, commande_id)

@router.get("/livraisons")
def voir_livraisons(statut: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
    marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
    return marchand_service.voir_livraisons_par_statut(db, marchand.id, statut)

@router.get("/livraisons/recherche")
def rechercher_livraisons(critere: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
    marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
    return marchand_service.rechercher_livraisons(db, marchand.id, critere)

@router.get("/statistiques")
def voir_statistiques(db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
    marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
    return marchand_service.voir_statistiques_livraisons(db, marchand.id)

@router.put("/{marchand_id}/adresse")
def modifier_adresse(marchand_id: UUID, adresse: str, db: Session = Depends(get_db)):
    return marchand_service.ajouter_adresse(db, marchand_id, adresse)
