from app.core.database import get_db
from app.dependencies.auth import recuperer_utilisateur_courant
from app.schemas.marchand import MarchandCreate
from app.models.marchand import Marchand
from app.models.commande import Commande, StatutCommande
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from uuid import UUID

def creer_marchand(db: Session, marchand_data: MarchandCreate):
    # Vérifier si un marchand existe déjà pour cet utilisateur
    # marchand_existant = db.query(Marchand).filter(Marchand.utilisateur_id == marchand_data.utilisateur_id).first()
    # if marchand_existant:
    #     raise HTTPException(status_code=400, detail="Ce compte a déjà un marchand associé.")

    # Créer le marchand
    nouveau_marchand = Marchand(
        nom=marchand_data.nom,
        contact=marchand_data.contact,
        adresse=marchand_data.adresse,
        utilisateur_id=marchand_data.utilisateur_id
    )
    db.add(nouveau_marchand)
    db.commit()
    db.refresh(nouveau_marchand)
    return nouveau_marchand

def lister_marchands(db: Session):
    return db.query(Marchand).all()

def obtenir_marchand(db: Session, marchand_id: UUID):
    marchand = db.query(Marchand).filter(Marchand.id == marchand_id).first()
    if not marchand:
        raise HTTPException(status_code=404, detail="Marchand non trouvé")
    return marchand


def modifier_marchand(db: Session, marchand_id: UUID, marchand_data: MarchandCreate):
    marchand = db.query(Marchand).filter(Marchand.id == marchand_id).first()
    if not marchand:
        raise HTTPException(status_code=404, detail="Marchand non trouvé")

    marchand.nom = marchand_data.nom
    marchand.contact = marchand_data.contact
    marchand.adresse = marchand_data.adresse
    # On ne modifie pas l'utilisateur associé sauf besoin spécifique
    db.commit()
    db.refresh(marchand)
    return marchand

def supprimer_marchand(db: Session, marchand_id: UUID):
    marchand = db.query(Marchand).filter(Marchand.id == marchand_id).first()
    if not marchand:
        raise HTTPException(status_code=404, detail="Marchand non trouvé")

    db.delete(marchand)
    db.commit()
    return {"message": "Marchand supprimé avec succès"}


def obtenir_marchand_par_utilisateur(db: Session, utilisateur_id: UUID):
    return db.query(Marchand).filter(Marchand.utilisateur_id == utilisateur_id).first()

# def Lister_commandes_marchand(
#     db: Session = Depends(get_db),
#     utilisateur = Depends(recuperer_utilisateur_courant)
# ):
#     marchand = marchand_service.obtenir_marchand_par_utilisateur(db, utilisateur.id)

#     if not marchand:
#         raise HTTPException(status_code=404, detail="Aucun marchand trouvé pour cet utilisateur.")

#     return marchand_service.recevoir_commandes(db, marchand.id)

def recevoir_commandes(db: Session, marchand_id: UUID):
    return db.query(Commande).filter(Commande.marchand_id == marchand_id).all()

def accepter_commande(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if commande:
        commande.statut = "validée"
        db.commit()
        return {
            "message": "Commande validée avec succès",
            # commande
        }
    raise HTTPException(status_code=404, detail="Commande non trouvée")

def lancer_livraison(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if commande:
        commande.statut = "en_cours"  
        db.commit()
        db.refresh(commande)
        return {
            "message": "Livraison lancée avec succès",
            "commande": commande
        }
    raise HTTPException(status_code=404, detail="Commande non trouvée")

def annuler_livraison(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if commande:
        commande.statut = "annulée"
        db.commit()
        db.refresh(commande)
        return {
            "message": "Commande annulée avec succès",
            "commande": commande
        }
    raise HTTPException(status_code=404, detail="Commande non trouvée")


def voir_details_commande(db: Session, commande_id: UUID):
    return db.query(Commande).filter(Commande.id == commande_id).first()

# def voir_livraisons_par_statut(db: Session, marchand_id: UUID, statut: str):
#     return db.query(Commande).filter(Commande.marchand_id == marchand_id, Commande.statut == statut).all()

# def voir_livraisons_par_statut(db: Session, marchand_id: UUID, statut: str):
#     return db.query(Commande).filter(
#         Commande.marchand_id == marchand_id,
#         Commande.statut == statut
#     ).all()


# def rechercher_livraisons(db: Session, marchand_id: UUID, critere: str):
#     return db.query(Commande).filter(Commande.marchand_id == marchand_id, Commande.description.ilike(f"%{critere}%")).all()

def voir_statistiques_livraisons(db: Session, marchand_id: UUID):
    total = db.query(Commande).filter(Commande.marchand_id == marchand_id).count()

    en_attente = db.query(Commande).filter(
        Commande.marchand_id == marchand_id,
        Commande.statut == StatutCommande.EN_ATTENTE
    ).count()

    validee = db.query(Commande).filter(
        Commande.marchand_id == marchand_id,
        Commande.statut == StatutCommande.VALIDEE
    ).count()

    annulee = db.query(Commande).filter(
        Commande.marchand_id == marchand_id,
        Commande.statut == StatutCommande.ANNULEE
    ).count()

    en_cours = db.query(Commande).filter(
        Commande.marchand_id == marchand_id,
        Commande.statut == StatutCommande.EN_COURS
    ).count()

    livree = db.query(Commande).filter(
        Commande.marchand_id == marchand_id,
        Commande.statut == StatutCommande.LIVREE
    ).count()

    return {
        "total": total,
        "en_attente": en_attente,
        "validée": validee,
        "annulée": annulee,
        "en_cours": en_cours,
        "livrée": livree
    }
    
    
   

def ajouter_adresse(db: Session, marchand_id: UUID, nouvelle_adresse: str):
    marchand = db.query(Marchand).filter(Marchand.id == marchand_id).first()
    if not marchand:
        raise HTTPException(status_code=404, detail="Marchand non trouvé")
    marchand.adresse = nouvelle_adresse
    db.commit()
    db.refresh(marchand)
    return marchand
