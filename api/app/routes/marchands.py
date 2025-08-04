from http.client import HTTPException
from app.models.marchand import Marchand
from app.models.utilisateur import Utilisateur
from app.schemas.marchand import MarchandCreate, MarchandOut, MarchandRead
from app.core.database import get_db
from app.dependencies.auth import recuperer_utilisateur_courant
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services import marchand as marchand_service
from uuid import UUID

from app.services.commande import ServiceCommande

router = APIRouter(prefix="/marchands", tags=["Marchands"])

@router.post("/", response_model=MarchandOut)
def creer_marchand(marchand_data: MarchandCreate, db: Session = Depends(get_db)):
    return marchand_service.creer_marchand(db, marchand_data)

@router.get("/", response_model=list[MarchandOut])
def lister_marchands(db: Session = Depends(get_db)):
    return marchand_service.lister_marchands(db)

@router.get("/par-utilisateur", response_model=list[MarchandRead])
def lister_marchands_par_utilisateur_courant(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant),
):
    return marchand_service.lister_marchands_par_utilisateur(db, utilisateur.id)

@router.get("/statistiques")
# def voir_statistiques_livraisons(
#     db: Session = Depends(get_db),
#     utilisateur=Depends(recuperer_utilisateur_courant)
# ):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
#     return marchand_service.voir_statistiques_livraisons(db, marchand.id)
def voir_statistiques_livraisons_test(
    marchand_id: UUID = Query(..., description="UUID du marchand à tester"),
    db: Session = Depends(get_db)
):
    return marchand_service.voir_statistiques_livraisons(db, marchand_id)

@router.get("/{marchand_id}", response_model=MarchandOut)
def obtenir_marchand(marchand_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.obtenir_marchand(db, marchand_id)


@router.put("/marchands/{marchand_id}")
def modifier_marchand(marchand_id: UUID, marchand_data: MarchandCreate, db: Session = Depends(get_db)):
    return marchand_service.modifier_marchand(db, marchand_id, marchand_data)

@router.delete("/marchands/{marchand_id}")
def supprimer_marchand(marchand_id: UUID, db: Session = Depends(get_db)):
    return marchand_service.supprimer_marchand(db, marchand_id)



@router.get("/commandes/{marchand_id}")
def Lister_commandes_marchand(marchand_id: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
    marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
    return ServiceCommande.obtenir_commandes_par_marchand(db, marchand_id)



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

# @router.get("/livraisons/par-statut")
# def voir_livraisons_par_statut(statut: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
#     return marchand_service.voir_livraisons_par_statut(db, marchand.id, statut)

# @router.get("/livraisons/par-statut")
# def voir_livraisons_par_statut(
#     statut: str,
#     db: Session = Depends(get_db),
#     utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
#     return marchand_service.voir_livraisons_par_statut(db, marchand.id, statut)

# def voir_livraisons_par_statut(
#     marchand_id: UUID = Query(..., description="ID du marchand"),
#     statut: str = Query(..., description="Statut des livraisons à filtrer"),
#     db: Session = Depends(get_db)
# ):
#     try:
#         livraisons = voir_livraisons_par_statut(db, marchand_id, statut)
#         return livraisons
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/livraisons/recherche")
# def rechercher_livraisons(critere: str, db: Session = Depends(get_db), utilisateur = Depends(recuperer_utilisateur_courant)):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)
#     return marchand_service.rechercher_livraisons(db, marchand.id, critere)



@router.put("/{marchand_id}/adresse")
def modifier_adresse(marchand_id: UUID, adresse: str, db: Session = Depends(get_db)):
    return marchand_service.ajouter_adresse(db, marchand_id, adresse)
