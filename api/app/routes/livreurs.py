from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.livraison import ProblemeSignalement
from app.schemas.livreur import LivreurCreate, LivreurRead, LivreurUpdate, StatutLivreurUpdate
from app.services.livraison import LivraisonService
from app.services.livreur import LivreurService
from app.core.database import get_db

router = APIRouter(prefix="/livreurs", tags=["Livreurs"])

@router.post("/", response_model=LivreurRead, status_code=status.HTTP_201_CREATED)
def creer_livreur(livreur: LivreurCreate, db: Session = Depends(get_db)):
    return LivreurService.creer_livreur(db, livreur)


# Connexion du livreur
@router.post("/connexion")
def connexion_livreur(
    contact: str = Body(..., embed=True),  # Ajoutez embed=True pour les corps simples
    mot_de_passe: str = Body(..., embed=True), 
    db: Session = Depends(get_db)
):
    livreur = LivreurService.authentifier_livreur(db, contact, mot_de_passe)
    if not livreur:
        raise HTTPException(status_code=401, detail="Échec d'authentification")
    return {"message": "Connexion réussie", "livreur": livreur}


# Activer un livreur (par l’admin)
@router.put("/{livreur_id}/activer")
def activer_livreur(livreur_id: UUID, db: Session = Depends(get_db)):
    livreur = LivreurService.activer_livreur(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return {"message": "Livreur activé avec succès", "livreur": livreur}


# Désactiver un livreur (par l’admin)
@router.put("/{livreur_id}/desactiver")
def desactiver_livreur(livreur_id: UUID, db: Session = Depends(get_db)):
    livreur = LivreurService.desactiver_livreur(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur non trouvé")
    return {"message": "Livreur désactivé avec succès", "livreur": livreur}

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


@router.put("/accepter/{livraison_id}/{livreur_id}")
def accepter_livraison(livraison_id: UUID, livreur_id: UUID, db: Session = Depends(get_db)):
    return LivraisonService.accepter_livraison(db, livraison_id, livreur_id)

@router.put("/livraisons/{livraison_id}/demarrer")
def demarrer_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    livraison = LivraisonService.demarrer_livraison(db, livraison_id)
    if not livraison:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    return {"message": "Livraison démarrée avec succès", "livraison": livraison}


@router.get("/commandes/{commande_id}")
def voir_details_commande(commande_id: UUID, db: Session = Depends(get_db)):
    commande = LivreurService.voir_details_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

@router.put("/livraisons/{livraison_id}/terminer")
def terminer_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    livraison = LivraisonService.terminer_livraison(db, livraison_id)
    if not livraison:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    return {"message": "Livraison validée avec succès", "livraison": livraison}


@router.put("/annuler/{livraison_id}")
def annuler_livraison(livraison_id: UUID, db: Session = Depends(get_db)):
    return LivraisonService.annuler_livraison(db, livraison_id)

@router.put("/signaler-probleme/{livraison_id}")
def signaler_probleme(livraison_id: UUID, data: ProblemeSignalement, db: Session = Depends(get_db)):
    return LivraisonService.signaler_probleme(db, livraison_id, data)


@router.get("/historique/{livreur_id}")
def voir_historique_livraisons(livreur_id: UUID, db: Session = Depends(get_db)):
    return LivraisonService.voir_historique_livraisons(db, livreur_id)


# @router.get("/rechercher/")
# def rechercher_livraisons(mot_cle: str, db: Session = Depends(get_db)):
#     return LivraisonService.rechercher_livraisons(db, mot_cle)


@router.get("/contact/{contact}/existe")
def verifier_contact_existe(contact: str, db: Session = Depends(get_db)):
    existe = LivreurService.verifier_contact_existe(db, contact)
    return {"existe": existe}