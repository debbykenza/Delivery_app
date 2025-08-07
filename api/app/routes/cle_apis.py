# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from uuid import UUID
# from app.schemas.cle_api import *
# from app.services.cle_api import *
# from app.core.database import get_db

# router = APIRouter(prefix="/cles-api", tags=["Clés API"])

# @router.post("/creer", response_model=CleAPIResponse)
# def creer_cle_api(payload: CleAPICreate, db: Session = Depends(get_db)):
#     return creer_cle(db, payload)

# @router.get("/liste", response_model=list[CleAPIResponse])
# def lister_cles_api(utilisateur_id: UUID, db: Session = Depends(get_db)):
#     return recuperer_cles_par_utilisateur(db, utilisateur_id)

# @router.delete("/supprimer/{cle_id}", response_model=dict)
# def supprimer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
#     return supprimer_cle(db, cle_id)

# @router.put("/revocation/{cle_id}", response_model=CleAPIResponse)
# def revoquer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
#     return revoquer_cle(db, cle_id)

# @router.put("/nommer/{cle_id}", response_model=CleAPIResponse)
# def nommer_cle_api(cle_id: UUID, nouveau_nom: str, db: Session = Depends(get_db)):
#     return nommer_cle(db, cle_id, nouveau_nom)

# @router.put("/regenerer/{cle_id}", response_model=CleAPIResponse)
# def regenerer_cle_api(cle_id: UUID, db: Session = Depends(get_db)):
#     return regenerer_cle(db, cle_id)

# @router.get("/statistiques/{utilisateur_id}", response_model=StatistiquesAPIResponse)
# def consulter_stats_api(utilisateur_id: UUID, db: Session = Depends(get_db)):
#     return consulter_statistiques(db, utilisateur_id)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.dependencies.auth import recuperer_utilisateur_courant
from app.schemas.cle_api import *
from app.services.cle_api import *
from app.core.database import get_db

router = APIRouter(prefix="/cles-api", tags=["Clés API"])

@router.post("/creer", response_model=CleAPIResponse)
def creer_cle_api(
    payload: CleAPICreate, 
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)  # Authentification
):
    # Utiliser l'utilisateur authentifié
    payload.utilisateur_id = current_user.id
    return creer_cle(db, payload)

@router.get("/toutes", response_model=list[CleAPIResponse])
def get_toutes_cles_api(
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    # Vérification simple : seules certaines personnes peuvent voir toutes les clés (ex: admin)
    if not current_user.role == "admin" :
        raise HTTPException(status_code=403, detail="Accès refusé")

    return recuperer_toutes_les_cles(db)



@router.put("/modifier/{cle_id}", response_model=CleAPIResponse)
def modifier_cle_api(
    cle_id: UUID,
    modifications: CleAPIModification,
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    """
    Modifie une clé API existante.
    Permet de changer:
    - Le nom de la clé
    - Le marchand associé
    Les deux modifications peuvent être faites simultanément.
    """
    return modifier_cle(
        db=db,
        cle_id=cle_id,
        utilisateur_id=current_user.id,
        nouveau_nom=modifications.nouveau_nom,
        nouveau_marchand_id=modifications.nouveau_marchand_id
    )

@router.get("/liste", response_model=list[CleAPIResponse])
def lister_cles_api(
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)  # Authentification
):
    # Utiliser l'utilisateur authentifié automatiquement
    return recuperer_cles_par_utilisateur(db, current_user.id)

@router.delete("/supprimer/{cle_id}", response_model=dict)
def supprimer_cle_api(
    cle_id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return supprimer_cle(db, cle_id, current_user.id)  # Vérifier propriété

@router.put("/revocation/{cle_id}", response_model=CleAPIResponse)
def revoquer_cle_api(
    cle_id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return revoquer_cle(db, cle_id, current_user.id)

@router.put("/nommer/{cle_id}", response_model=CleAPIResponse)
def nommer_cle_api(
    cle_id: UUID, 
    payload: CleAPINomUpdate,  # Utiliser le schema
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return nommer_cle(db, cle_id, payload.nouveau_nom, current_user.id)

@router.put("/regenerer/{cle_id}", response_model=CleAPIResponse)
def regenerer_cle_api(
    cle_id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return regenerer_cle(db, cle_id, current_user.id)

@router.get("/statistiques", response_model=StatistiquesAPIResponse)
def consulter_stats_api(
    db: Session = Depends(get_db),
    current_user = Depends(recuperer_utilisateur_courant)
):
    return consulter_statistiques(db, current_user.id)

@router.get("/par-marchand/{marchand_id}", response_model=CleAPIParMarchand)
def get_cle_par_marchand(
    marchand_id: UUID,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)
):
    """
    Récupère la clé API active associée à un marchand spécifique
    Nécessite que l'utilisateur soit propriétaire du marchand
    """
    return obtenir_cle_par_marchand(db, marchand_id, utilisateur.id)