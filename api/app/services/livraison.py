from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from uuid import UUID
from fastapi import HTTPException 

from app.models.livraison import Livraison
from app.models.commande import Commande
from app.models.client import Client
# from app.models.avis import Avis
from app.models.marchand import Marchand
from app.models.notification import TypeNotification
from app.schemas.livraison import LivraisonCreate, LivraisonStatutUpdate, ProblemeSignalement
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification


class LivraisonService:

    @staticmethod
    def creer_livraison(db: Session, livraison_data: LivraisonCreate):
        livraison = Livraison(**livraison_data.dict())
        db.add(livraison)
        db.commit()
        db.refresh(livraison)
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        # Notification au marchand
        notif = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Nouvelle livraison créée",
            message="Une nouvelle demande de livraison a été enregistrée.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return livraison

    @staticmethod
    def obtenir_livraison(db: Session, livraison_id: UUID):
        return db.query(Livraison).filter(Livraison.id == livraison_id).first()
    
    @staticmethod
    def obtenir_livraisons(db: Session):
        return db.query(Livraison).all()

    @staticmethod
    def accepter_livraison(db: Session, livraison_id: UUID, livreur_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.livreur_id = livreur_id
        livraison.statut = "acceptee"
        db.commit()
        db.refresh(livraison)
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        
        
        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Livraison acceptée",
            message="Un livreur a accepté la livraison.",
            type=TypeNotification.success
        )
        creer_notification(db, notif_marchand)

        # 🔔 Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Livreur assigné",
            message="Un livreur a accepté la livraison.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_client)

        # 🔔 Livreur
        notif_livreur = NotificationCreate(
            user_id=livreur_id,
            user_type="livreur",
            titre="Nouvelle livraison",
            message="Vous avez accepté une nouvelle livraison.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_livreur)

        # ✅ Retour avec message personnalisé
        return {
            "message": "Livraison acceptée avec succès.",
            "livraison": livraison
        }

    @staticmethod
    def terminer_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = "terminee"
        db.commit()
        db.refresh(livraison)
        
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        # 🔔 Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Livraison terminée",
            message="Votre livraison a été finalisée avec succès.",
            type=TypeNotification.success
        )
        creer_notification(db, notif_client)

        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Livraison terminée",
            message="Une de vos livraisons vient d'être terminée.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)

        # 🔔 Livreur
        notif_livreur = NotificationCreate(
            user_id=livraison.livreur_id,
            user_type="livreur",
            titre="Livraison finalisée",
            message="Vous avez terminé une livraison.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_livreur)
        return livraison

    @staticmethod
    def annuler_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = "annulee"
        db.commit()
        db.refresh(livraison)
        
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        # 🔔 Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Livraison annulée",
            message="Votre livraison a été annulée.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif_client)

        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Livraison annulée",
            message="Une de vos livraisons a été annulée.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif_marchand)

        # 🔔 Livreur
        if livraison.livreur_id:
            notif_livreur = NotificationCreate(
                user_id=livraison.livreur_id,
                user_type="livreur",
                titre="Livraison annulée",
                message="Une livraison à laquelle vous étiez affecté a été annulée.",
                type=TypeNotification.warning
            )
            creer_notification(db, notif_livreur)
        return {
            "message": "Livraison a été annulée avec succès.",
            "livraison": livraison
        }

    @staticmethod
    def voir_historique_livraisons(db: Session, livreur_id: UUID):
        return db.query(Livraison).filter(Livraison.livreur_id == livreur_id).all()

    @staticmethod
    def rechercher_livraisons(db: Session, mot_cle: str):
        return db.query(Livraison).filter(
            or_(
                Livraison.statut.ilike(f"%{mot_cle}%"),
                # Livraison.url_suivi.ilike(f"%{mot_cle}%"),
                Livraison.type_livraison.ilike(f"%{mot_cle}%")
            )
        ).all()

    # @staticmethod
    # def voir_avis_client(db: Session, livraison_id: UUID):
    #     return db.query(Avis).filter(Avis.livraison_id == livraison_id).all()

    @staticmethod
    def voir_details_commande(db: Session, commande_id: UUID):
        return db.query(Commande).filter(Commande.id == commande_id).first()

    # @staticmethod
    # def livraisons_disponibles_par_localisation(db: Session, ville: str):
    #     return db.query(Livraison).filter(and_(
    #         Livraison.ville == ville,
    #         Livraison.statut == "en_attente",
    #         Livraison.livreur_id == None
    #     )).all()
        
    @staticmethod
    def livraisons_disponibles(db: Session):
        return db.query(Livraison).filter(and_(
            Livraison.statut == "en_attente",
            # Livraison.livreur_id == None
        )).all()

    @staticmethod
    def mettre_a_jour_statut(db: Session, livraison_id: UUID, update_data: LivraisonStatutUpdate):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = update_data.nouveau_statut
        db.commit()
        db.refresh(livraison)
        return livraison

    @staticmethod
    def demarrer_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = "en_cours"
        db.commit()
        db.refresh(livraison)
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
         # 🔔 Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Livraison en cours",
            message="Votre livraison est actuellement en cours.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_client)

        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Livraison démarrée",
            message="Une livraison a été démarrée.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)

        # 🔔 Livreur
        notif_livreur = NotificationCreate(
            user_id=livraison.livreur_id,
            user_type="livreur",
            titre="Livraison en cours",
            message="Vous avez démarré une livraison.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_livreur)
        return livraison

    @staticmethod
    def signaler_probleme(db: Session, livraison_id: UUID, data: ProblemeSignalement):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.probleme = data.description
        # livraison.statut = "probleme"
        db.commit()
        db.refresh(livraison)
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        # 🔔 Client
        notif_client = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Problème signalé",
            message="Un problème a été détecté durant votre livraison.",
            type=TypeNotification.error
        )
        creer_notification(db, notif_client)

        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Problème signalé",
            message="Un problème a été signalé lors de la livraison.",
            type=TypeNotification.error
        )
        creer_notification(db, notif_marchand)

        # 🔔 Livreur
        if livraison.livreur_id:
            notif_livreur = NotificationCreate(
                user_id=livraison.livreur_id,
                user_type="livreur",
                titre="Problème signalé",
                message="Un problème a été signalé sur une livraison que vous effectuez.",
                type=TypeNotification.error
            )
            creer_notification(db, notif_livreur)
            return {"message": "votre signalement a été pris en compte."}

    @staticmethod
    def supprimer_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        
        # ✅ Récupération du marchand via la commande
        commande = db.query(Commande).filter(Commande.id == livraison.commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        
        notif = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Livraison supprimée",
            message="Une livraison a été supprimée.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif)
    
        db.delete(livraison)
        db.commit()
        return {"message": "Livraison supprimée avec succès"}
    
    
    @staticmethod
    def get_livraisons_par_utilisateur(db: Session, utilisateur_id: UUID, statut: Optional[str] = None):
        """Récupère toutes les livraisons des marchands d'un utilisateur"""
        # Récupère les marchands de l'utilisateur
        marchands = db.query(Marchand).filter(Marchand.utilisateur_id == utilisateur_id).all()
        
        if not marchands:
            return []
        
        marchand_ids = [m.id for m in marchands]
        
        query = db.query(Livraison).join(Commande).filter(
            Commande.marchand_id.in_(marchand_ids)
        ).options(
            joinedload(Livraison.commande),
            joinedload(Livraison.livreur)
        )
        
        if statut:
            query = query.filter(Livraison.statut == statut)
            
        return query.order_by(Livraison.date_livraison.desc()).all()
    
    @staticmethod
    def get_livraisons_marchand(db: Session, marchand_id: UUID, statut: Optional[str] = None):
        """Récupère les livraisons d'un marchand avec les données jointes"""
        query = db.query(Livraison).join(Commande).filter(
            Commande.marchand_id == marchand_id
        ).options(
            joinedload(Livraison.commande),
            joinedload(Livraison.livreur)
            # joinedload(Livraison.client)
        )
        
        if statut:
            query = query.filter(Livraison.statut == statut)
            
        return query.order_by(Livraison.date_livraison.desc()).all()

    @staticmethod
    def get_livraisons_livreur(db: Session, livreur_id: UUID, statut: Optional[str] = None):
        """Récupère les livraisons d'un livreur avec les données jointes"""
        query = db.query(Livraison).filter(
            Livraison.livreur_id == livreur_id
        ).options(
            joinedload(Livraison.commande),
            joinedload(Livraison.livreur)
        )
        
        if statut:
            query = query.filter(Livraison.statut == statut)
            
        return query.order_by(Livraison.date_livraison.desc()).all()

    @staticmethod
    def get_livraisons_client(db: Session, client_id: UUID, statut: Optional[str] = None):
        """Récupère les livraisons d'un client avec les données jointes"""
        query = db.query(Livraison).join(Commande).filter(
            Commande.client_id == client_id
        ).options(
            joinedload(Livraison.commande),
            joinedload(Livraison.livreur)
        )
        
        if statut:
            query = query.filter(Livraison.statut == statut)
            
        return query.order_by(Livraison.date_livraison.desc()).all()

    @staticmethod
    def get_livraison_with_details(db: Session, livraison_id: UUID):
        """Récupère une livraison avec tous les détails"""
        return db.query(Livraison).filter(
            Livraison.id == livraison_id
        ).options(
            joinedload(Livraison.commande),
            joinedload(Livraison.livreur)
        ).first()

