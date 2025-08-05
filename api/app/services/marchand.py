from app.core.database import get_db
from app.dependencies.auth import recuperer_utilisateur_courant
from app.models.livraison import Livraison
from app.models.livreur import Livreur
from app.models.notification import TypeNotification
from app.schemas.marchand import MarchandCreate
from app.schemas.commande import CommandeRead
from app.models.marchand import Marchand
from app.models.commande import Commande, StatutCommande
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from uuid import UUID

from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification

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
        utilisateur_id=marchand_data.utilisateur_id,
        status="inactif"  # Par défaut, le statut est inactif
    )
    db.add(nouveau_marchand)
    db.commit()
    db.refresh(nouveau_marchand)
    
    notif = NotificationCreate(
        user_id=marchand_data.utilisateur_id,
        user_type="utilisateur",
        titre="Nouveau magasin créé",
        message="Votre nouveau magasin a été créé avec succès.",
        type=TypeNotification.success
    )
    creer_notification(db, notif)
    return nouveau_marchand

def lister_marchands(db: Session):
    return db.query(Marchand).all()

def lister_marchands_par_utilisateur(db: Session, utilisateur_id: UUID):
    return db.query(Marchand).filter(Marchand.utilisateur_id == utilisateur_id).all()


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
    
    notif = NotificationCreate(
        user_id=marchand_data.utilisateur_id,
        user_type="utilisateur",
        titre="Informations du magasin modifiées",
        message="les informations de votre magasin ont été mises à jour avec succès.",
        type=TypeNotification.info
    )
    creer_notification(db, notif)
    return marchand

def supprimer_marchand(db: Session, marchand_id: UUID):
    marchand = db.query(Marchand).filter(Marchand.id == marchand_id).first()
    if not marchand:
        raise HTTPException(status_code=404, detail="Marchand non trouvé")

    
    notif = NotificationCreate(
        user_id=marchand.utilisateur_id,
        user_type="utilisateur",
        titre="Magasin supprimé",
        message="Votre magasin a été supprimé.",
        type=TypeNotification.warning
    )
    creer_notification(db, notif)
    db.delete(marchand)
    db.commit()
    return {"message": "Magasin supprimé avec succès"}


def obtenir_marchand_par_utilisateur(db: Session, utilisateur_id: UUID):
    return db.query(Marchand).filter(Marchand.utilisateur_id == utilisateur_id).all()



def recevoir_commandes(db: Session, marchand_id: UUID):
    return db.query(Commande).filter(Commande.marchand_id == marchand_id).all()

def accepter_commande(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if commande:
        commande.statut = "validée"
        db.commit()
        
        #  Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Commande acceptée",
            message="Votre commande a été validée par le marchand.",
            type=TypeNotification.success
        )
        creer_notification(db, notif_client)

        #  Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand.utilisateur_id,
            user_type="marchand",
            titre="Commande validée",
            message="Vous avez validé une commande.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)
        return {
            "message": "Commande validée avec succès",
            # commande
        }
    raise HTTPException(status_code=404, detail="Commande non trouvée")

# def lancer_livraison(db: Session, commande_id: UUID):
#     commande = db.query(Commande).filter(Commande.id == commande_id).first()
#     if commande:
#         commande.statut = "en_cours"  
#         db.commit()
#         db.refresh(commande)
#         return {
#             "message": "Livraison lancée avec succès",
#             "commande": commande
#         }
#     raise HTTPException(status_code=404, detail="Commande non trouvée")
def lancer_livraison(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    # 1. Mettre à jour le statut de la commande
    commande.statut = "en_cours"
    db.commit()
    db.refresh(commande)

    # 2. Créer une livraison liée, sans livreur_id
    nouvelle_livraison = Livraison(
        commande_id=commande_id,
        statut="en_attente",
        livreur_id=None  # pas encore affecté
    )
    db.add(nouvelle_livraison)
    db.commit()
    db.refresh(nouvelle_livraison)
    
    #  Client
    notif_client = NotificationCreate(
        user_id=commande.client_id,
        user_type="client",
        titre="Livraison en cours",
        message="La livraison de votre commande a été lancée.",
        type=TypeNotification.info
    )
    creer_notification(db, notif_client)

    #  Marchand
    notif_marchand = NotificationCreate(
        user_id=commande.marchand.utilisateur_id,
        user_type="marchand",
        titre="Livraison lancée",
        message="Une nouvelle livraison a été lancée avec succès.",
        type=TypeNotification.success
    )
    creer_notification(db, notif_marchand)

    # Tous les livreurs → notification de disponibilité
    livreurs = db.query(Livreur).all()
    for livreur in livreurs:
        notif_livreur = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Nouvelle livraison disponible",
            message="Une nouvelle livraison est en attente d’acceptation.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_livreur)

    return {
        "message": "Livraison lancée avec succès",
        "commande": CommandeRead.from_orm(commande),
        "livraison": nouvelle_livraison
    }

def annuler_livraison(db: Session, commande_id: UUID):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if commande:
        commande.statut = "annulée"
        db.commit()
        db.refresh(commande)
        
        #  Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Commande annulée",
            message="Votre commande a été annulée par le marchand.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif_client)

        #  Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand.utilisateur_id,
            user_type="marchand",
            titre="Annulation confirmée",
            message="L’annulation de la commande a bien été prise en compte.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)
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
