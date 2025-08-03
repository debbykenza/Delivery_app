# from app.dependencies.auth import recuperer_utilisateur_courant
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from uuid import UUID

# from app.core.database import get_db
# from app.models.utilisateur import Utilisateur
# from app.schemas.commande import CommandeCreate, CommandeUpdate, CommandeRead
# from app.services.commande import ServiceCommande
# from app.models.commande import StatutCommande


# # Création du routeur pour les commandes
# router = APIRouter(prefix="/commandes", tags=["commandes"])


# @router.post("/", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
# def creer_commande(
#     commande_data: CommandeCreate,
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Crée une nouvelle commande pour l'utilisateur courant, si autorisé.
#     """
#     print("BODY REÇU:", commande_data)

#     # Vérification simple : est-ce que l'utilisateur est actif ?
#     if not utilisateur_courant.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Utilisateur inactif. Création de commande refusée."
#         )

#     try:
#         commande = ServiceCommande.creer_commande(
#             db=db,
#             donnees_commande=commande_data,
#             #id_client=utilisateur_courant.id  # <-- Ajouté ici
#         )
#         return commande

#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Erreur lors de la création de la commande"
#         )



# @router.get("/{commande_id}", response_model=CommandeRead)
# def obtenir_commande(
#     commande_id: str,
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Récupère une commande spécifique avec vérification des permissions
#     """
#     commande = ServiceCommande.obtenir_commande(db, commande_id)
    
#     if not commande:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Commande non trouvée"
#         )
        
#     # if not bool(getattr(utilisateur_courant, 'is_admin', False)) and str(commande.client_id) != str(utilisateur_courant.id):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN,
#     #         detail="Accès non autorisé à cette commande"
#     #     )
        
#     return commande

# @router.put("/{commande_id}", response_model=CommandeRead)
# def modifier_commande(
#     commande_id: str,
#     commande_update: CommandeUpdate,
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Met à jour une commande existante
#     """
#     commande = ServiceCommande.obtenir_commande(db, commande_id)
    
#     # Vérification des permissions
#     # if not commande:
#     #     raise HTTPException(status_code=404, detail="Commande non trouvée")
#     # if not bool(getattr(utilisateur_courant, 'is_admin', False)) and str(commande.client_id) != str(utilisateur_courant.id):
#     #     raise HTTPException(status_code=403, detail="Accès interdit")
    
#     return ServiceCommande.modifier_commande(
#         db=db,
#         commande=commande,
#         donnees_maj=commande_update
#     )

# @router.patch("/{commande_id}/statut", response_model=CommandeRead)
# def changer_statut_commande(
#     commande_id: str,
#     nouveau_statut: StatutCommande,
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Modifie le statut d'une commande (réservé aux administrateurs)
#     """
#     # if not bool(getattr(utilisateur_courant, 'is_admin', False)):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN,
#     #         detail="Action réservée aux administrateurs"
#     #     )
    
#     commande = ServiceCommande.changer_statut(
#         db=db,
#         id_commande=commande_id,
#         nouveau_statut=nouveau_statut
#     )
    
#     if not commande:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Transition de statut non autorisée"
#         )
        
#     return commande

# @router.delete("/{commande_id}", status_code=status.HTTP_204_NO_CONTENT)
# def supprimer_commande(
#     commande_id: str,
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Supprime une commande (réservé aux administrateurs)
#     """
#     # if not bool(getattr(utilisateur_courant, 'is_admin', False)):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN,
#     #         detail="Action réservée aux administrateurs"
#     #     )
    
#     commande = ServiceCommande.obtenir_commande(db, commande_id)
#     if not commande:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Commande non trouvée"
#         )
    
#     ServiceCommande.supprimer_commande(db, commande)
#     return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.commande import ChangementStatutCommande, CommandeCreate, CommandeUpdate, CommandeRead
from app.services.commande import ServiceCommande
from app.models.commande import StatutCommande
from app.dependencies.auth import recuperer_utilisateur_courant
from app.models.utilisateur import Utilisateur
from app.core.database import get_db
from app.services.marchand import obtenir_marchand_par_utilisateur

router = APIRouter(prefix="/commandes", tags=["commandes"])


# @router.get("/par-utilisateur", response_model=List[CommandeRead])
# def lister_commandes_par_utilisateur_courant(
#     db: Session = Depends(get_db),
#     utilisateur_courant: Utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     """
#     Liste toutes les commandes visibles par l'utilisateur
#     (Toutes si admin, seulement les siennes sinon)
#     """
#     return ServiceCommande.obtenir_commandes(
#         db=db,
#         # est_admin=bool(getattr(utilisateur_courant, 'is_admin', False)),
#         # id_client=utilisateur_courant.id
#     )
    
@router.get("/par-utilisateur/mes-marchands", response_model=List[CommandeRead])
def lister_commandes_mes_marchands(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)
):
    """
    Récupère toutes les commandes des marchands gérés par l'utilisateur connecté.
    """
    # 1. Récupérer tous les marchands de l'utilisateur
    marchands = obtenir_marchand_par_utilisateur(db, utilisateur.id)
    
    if not marchands:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun marchand associé à cet utilisateur"
        )

    # 2. Récupérer les commandes de tous ces marchands
    commandes = []
    for marchand in marchands:
        commandes.extend(ServiceCommande.obtenir_commandes_par_marchand(db, marchand.id))
    
    return commandes


@router.post("/", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
def creer_commande(
    commande_data: CommandeCreate,
    db: Session = Depends(get_db),
):
    try:
        commande = ServiceCommande.creer_commande(db=db, donnees_commande=commande_data)
        return commande
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("ERREUR:", str(e))
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la commande")


@router.get("/", response_model=List[CommandeRead])
def lister_commandes(db: Session = Depends(get_db)):
    return ServiceCommande.obtenir_commandes(db)


@router.get("/{commande_id}", response_model=CommandeRead)
def obtenir_commande(commande_id: str, db: Session = Depends(get_db)):
    commande = ServiceCommande.obtenir_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.put("/{commande_id}", response_model=CommandeRead)
def modifier_commande(
    commande_id: str,
    commande_update: CommandeUpdate,
    db: Session = Depends(get_db)
):
    commande = ServiceCommande.obtenir_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    return ServiceCommande.modifier_commande(db=db, commande=commande, donnees_maj=commande_update)


@router.patch("/{commande_id}/statut", response_model=CommandeRead)
def changer_statut_commande(
    commande_id: str,
    payload: ChangementStatutCommande,
    db: Session = Depends(get_db)
):
    commande = ServiceCommande.changer_statut(
        db=db,
        id_commande=commande_id,
        nouveau_statut=payload.nouveau_statut
    )
    if not commande:
        raise HTTPException(status_code=400, detail="Transition de statut non autorisée")
    return commande


@router.delete("/{commande_id}", status_code=status.HTTP_200_OK)
def supprimer_commande(commande_id: str, db: Session = Depends(get_db)):
    commande = ServiceCommande.obtenir_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    ServiceCommande.supprimer_commande(db, commande)
    return {"message": "Commande supprimée avec succès"}
