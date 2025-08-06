# services/abonnement.py

from app.models.marchand import Marchand
from app.models.utilisateur import Utilisateur
from app.schemas.notification import NotificationCreate, TypeNotification
from app.services.notification import creer_notification


from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, Depends
from app.models.abonnement import Abonnement, StatutAbonnement
from app.schemas.abonnement import AbonnementCreate, AbonnementUpdate
from app.core.database import get_db
from datetime import timezone



class ServiceAbonnement:

    @staticmethod
    def creer_abonnement(db: Session, data: AbonnementCreate) -> Abonnement:
        date_debut = datetime.utcnow()
        date_expiration = date_debut + timedelta(days=data.duree_jours)

        abonnement = Abonnement(
            marchand_id=data.marchand_id,
            montant=data.montant,
            date_debut=date_debut,
            date_expiration=date_expiration,
            statut=StatutAbonnement.actif
        )

        db.add(abonnement)
        db.commit()
        db.refresh(abonnement)
        
        notif = NotificationCreate(
            user_id=data.marchand_id,
            user_type="marchand",
            titre="Nouvel abonnement créé",
            message=f"Votre abonnement a été créé pour {data.duree_jours} jours.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        
        return abonnement
    
    @staticmethod
    def souscrire_abonnement(db: Session, marchand_id: UUID, montant: float, reference_abonnement: str, utilisateur_courant: Utilisateur) -> Abonnement:
        """
        Permet à un marchand de souscrire un nouvel abonnement
        - Vérifie qu’il n’y a pas déjà un abonnement actif
        - Crée un abonnement actif de durée définie
        - Envoie une notification automatique
        """
        

        # Vérification de l'existence d'un abonnement actif
        abonnement_actif = db.query(Abonnement).filter(
            Abonnement.marchand_id == marchand_id,
            Abonnement.statut == StatutAbonnement.actif
        ).first()

        if abonnement_actif:
            raise HTTPException(status_code=400, detail="Un abonnement actif existe déjà.")

        # Dates
        date_debut = datetime.utcnow()
        date_expiration = date_debut + timedelta(days=365)  # Durée de 365 jours

        # Création de l'abonnement
        nouvel_abonnement = Abonnement(
            marchand_id=marchand_id,
            utilisateur_id=utilisateur_courant.id,
            montant=montant,
            date_debut=date_debut,
            date_expiration=date_expiration,
            statut=StatutAbonnement.inactif,
            reference_abonnement=reference_abonnement,
        )

        db.add(nouvel_abonnement)

        # Création de la notification liée
        # notification = Notification(
        #     titre="Abonnement activé",
        #     type=TypeNotification.info,
        #     contenu=f"Votre abonnement a été activé pour {duree_jours} jours.",
        #     date_envoie=datetime.utcnow()
        # )

        # db.add(notification)

        db.commit()
        db.refresh(nouvel_abonnement)
        
        # Création de la notification
        notif = NotificationCreate(
        user_id=utilisateur_courant.id,
        user_type="utilisateur",
        titre="Abonnement activé",
        message=f"Votre abonnement pour le marchand {marchand_id} a été activé pour 365 jours.",
        type=TypeNotification.success
        )
        creer_notification(db, notif)

        return nouvel_abonnement


    @staticmethod
    def lister_abonnements(db: Session):
        return db.query(Abonnement).all()
    
    @staticmethod
    def abonnements_par_utilisateur(db: Session, utilisateur_id: UUID) -> list[Abonnement]:
        return db.query(Abonnement)\
            .filter(Abonnement.utilisateur_id == utilisateur_id)\
            .order_by(Abonnement.date_debut.desc())\
            .all()


    @staticmethod
    def get_abonnement_par_id(db: Session, abonnement_id: UUID):
        abonnement = db.query(Abonnement).filter_by(id=abonnement_id).first()
        if not abonnement:
            raise HTTPException(404, "Abonnement introuvable")
        return abonnement

    @staticmethod
    def get_abonnement_par_marchand(db: Session, marchand_id: UUID):
        return db.query(Abonnement).filter_by(marchand_id=marchand_id).all()

    @staticmethod
    def get_abonnement_par_statut(db: Session, statut: StatutAbonnement):
        return db.query(Abonnement).filter_by(statut=statut).all()

    @staticmethod
    def supprimer_abonnement(db: Session, abonnement_id: UUID) -> bool:
        abonnement = db.query(Abonnement).filter_by(id=abonnement_id).first()
        if abonnement:
            db.delete(abonnement)
            db.commit()
            
            
            notif = NotificationCreate(
                user_id=abonnement.marchand_id,
                user_type="marchand",
                titre="Abonnement supprimé",
                message=f"Votre abonnement a été supprimé.",
                type=TypeNotification.warning
            )
            creer_notification(db, notif)
            return True
        return False

    @staticmethod
    def modifier_abonnement(db: Session, abonnement_id: UUID, data: AbonnementUpdate):
        abonnement = ServiceAbonnement.get_abonnement_par_id(db, abonnement_id)

        if data.montant:
            abonnement.montant = data.montant
        if data.statut:
            abonnement.statut = data.statut
        if data.date_expiration:
            abonnement.date_expiration = data.date_expiration

        db.commit()
        db.refresh(abonnement)
        
        notif = NotificationCreate(
            user_id=abonnement.marchand_id,
            user_type="marchand",
            titre="Abonnement modifié",
            message=f"Votre abonnement a été modifié.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return abonnement

    # @staticmethod
    # def verifier_et_mettre_a_jour_abonnements(db: Session):
    #     """Met automatiquement à jour les abonnements expirés"""
    #     abonnements = db.query(Abonnement).filter(Abonnement.statut == StatutAbonnement.actif).all()
    #     for ab in abonnements:
    #         if ab.date_expiration < datetime.now(timezone.utc):
    #             ab.statut = StatutAbonnement.expiré
    #     db.commit()


    @staticmethod
    def temps_restant_avant_expiration(db: Session, marchand_id: UUID) -> dict:
        abonnement = db.query(Abonnement)\
            .filter(Abonnement.marchand_id == marchand_id)\
            .order_by(Abonnement.date_expiration.desc())\
            .first()

        if not abonnement:
            raise HTTPException(status_code=404, detail="Aucun abonnement trouvé")

        maintenant = datetime.now(timezone.utc)
        if abonnement.date_expiration < maintenant:
            return {"message": "Abonnement expiré", "jours_restants": 0}

        temps_restant = abonnement.date_expiration - maintenant
        return {
            "message": "Abonnement actif",
            "jours_restants": temps_restant.days,
            "heures_restantes": temps_restant.seconds // 3600
        }
        
    @staticmethod
    def compter_abonnes(db: Session) -> int:
        return db.query(Abonnement.marchand_id).distinct().count()
    
    
    @staticmethod
    def historique_abonnements_marchand(db: Session, marchand_id: UUID) -> list[Abonnement]:
        return db.query(Abonnement)\
            .filter(Abonnement.marchand_id == marchand_id)\
            .order_by(Abonnement.date_debut.desc())\
            .all()

