# routes/abonnement.py

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.dependencies.auth import recuperer_utilisateur_courant
from app.services.abonnement import ServiceAbonnement
from app.schemas.abonnement import AbonnementCreate, AbonnementRead, AbonnementUpdate
from app.core.database import get_db

router = APIRouter(prefix="/abonnements", tags=["Abonnements"])


# @router.post("/", response_model=AbonnementRead, status_code=201)
# def creer_abonnement(data: AbonnementCreate, db: Session = Depends(get_db)):
#     return ServiceAbonnement.creer_abonnement(db, data)

@router.get("/nombre-abonnes")
def obtenir_nombre_abonnes(db: Session = Depends(get_db)):
    nombre = ServiceAbonnement.compter_abonnes(db)
    return {"nombre_abonnes": nombre}


@router.get("/temps-restant/{marchand_id}")
def obtenir_temps_restant_avant_expiration(marchand_id: UUID, db: Session = Depends(get_db)):
    return ServiceAbonnement.temps_restant_avant_expiration(db, marchand_id)



@router.get("/historique/{marchand_id}", response_model=list[AbonnementRead])
def obtenir_historique_abonnements(marchand_id: UUID, db: Session = Depends(get_db)):
    return ServiceAbonnement.historique_abonnements_marchand(db, marchand_id)


@router.post("/souscrire", status_code=201)
def souscrire_abonnement(
    marchand_id: UUID,
    montant: float,
    reference_abonnement: Optional[str] = None,
    db: Session = Depends(get_db),
    utilisateur_courant = Depends(recuperer_utilisateur_courant)
):
    """
    Permet à un marchand de souscrire à un abonnement standard de 30 jours.
    """
    abonnement = ServiceAbonnement.souscrire_abonnement(db, marchand_id, montant, reference_abonnement, utilisateur_courant=utilisateur_courant)

    return {
        "message": "Abonnement souscrit avec succès",
        "montant": abonnement.montant,
        "date_debut": abonnement.date_debut.strftime("%d-%m-%Y %H:%M:%S"),
        "date_expiration": abonnement.date_expiration.strftime("%d-%m-%Y %H:%M:%S"),
        "reference_abonnement": abonnement.reference_abonnement,
        "marchand_id": abonnement.marchand_id,
        "utilisateur_id": abonnement.utilisateur_id,
        
    }
    



@router.get("/", response_model=list[AbonnementRead])
def lister_abonnements(db: Session = Depends(get_db)):
    return ServiceAbonnement.lister_abonnements(db)

@router.get("/mes-abonnements", response_model=list[AbonnementRead])
def lister_mes_abonnements(
    db: Session = Depends(get_db),
    utilisateur_courant = Depends(recuperer_utilisateur_courant)
):
    return ServiceAbonnement.abonnements_par_utilisateur(db, utilisateur_courant.id)


@router.get("/{abonnement_id}", response_model=AbonnementRead)
def obtenir_abonnement(abonnement_id: UUID, db: Session = Depends(get_db)):
    return ServiceAbonnement.get_abonnement_par_id(db, abonnement_id)


@router.get("/marchand/{marchand_id}", response_model=list[AbonnementRead])
def abonnements_par_marchand(marchand_id: UUID, db: Session = Depends(get_db)):
    return ServiceAbonnement.get_abonnement_par_marchand(db, marchand_id)


@router.get("/statut/{statut}", response_model=list[AbonnementRead])
def abonnements_par_statut(statut: str, db: Session = Depends(get_db)):
    return ServiceAbonnement.get_abonnement_par_statut(db, statut)


@router.put("/{abonnement_id}", response_model=AbonnementRead)
def modifier_abonnement(abonnement_id: UUID, data: AbonnementUpdate, db: Session = Depends(get_db)):
    return ServiceAbonnement.modifier_abonnement(db, abonnement_id, data)


@router.delete("/{abonnement_id}")
def supprimer_abonnement(abonnement_id: UUID, db: Session = Depends(get_db)):
    success = ServiceAbonnement.supprimer_abonnement(db, abonnement_id)
    if not success:
        raise HTTPException(404, "Abonnement introuvable")
    return {"message": "Abonnement supprimé avec succès."}


# @router.post("/verifier-expirations")
# def verifier_expirations(db: Session = Depends(get_db)):
#     ServiceAbonnement.verifier_et_mettre_a_jour_abonnements(db)
#     return {"message": "Vérification des abonnements terminée"}


@router.post(
    "/abonnements/{abonnement_id}/activer",
    response_model=AbonnementRead,
    summary="Activer un abonnement inactif",
    description="Permet d'activer un abonnement qui est actuellement inactif"
)
async def activer_abonnement(
    abonnement_id: UUID,
    db: Session = Depends(get_db),
    # utilisateur_courant = Depends(recuperer_utilisateur_courant)
):
    """
    Active un abonnement inactif.
    
    - **abonnement_id**: UUID de l'abonnement à activer
    """
    try:
        abonnement = ServiceAbonnement.activer_abonnement(
            db=db, 
            abonnement_id=abonnement_id
        )
        return abonnement
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'activation de l'abonnement: {str(e)}"
        )



