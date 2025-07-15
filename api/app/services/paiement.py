from typing import List, Optional
from uuid import UUID
from app.models.livraison import Livraison
from app.models.notification import TypeNotification
from app.models.paiement import MethodePaiement, Paiement, RecuPar, StatutPaiement
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notification import NotificationCreate
from app.schemas.paiement import PaiementCreate
from fastapi import Depends, HTTPException

from app.services.notification import creer_notification

class ServicePaiement:
    @staticmethod
    def creer_paiement(db: Session, data: PaiementCreate) -> Paiement:
        statut_paiement = (
            StatutPaiement.payé if data.methode_paiement in [MethodePaiement.mixx, MethodePaiement.flooz]
            else StatutPaiement.remis_livreur
        )
        recu_par = (
            RecuPar.marchand if data.methode_paiement in [MethodePaiement.mixx, MethodePaiement.flooz]
            else RecuPar.livreur
        )

        paiement = Paiement(
            client_id=data.client_id,
            livraison_id=data.livraison_id,
            montant=data.montant,
            methode_paiement=data.methode_paiement,
            statut_paiement=statut_paiement,
            recu_par=recu_par,
        )

        db.add(paiement)
        db.commit()
        db.refresh(paiement)
        
        notif = NotificationCreate(
            user_id=paiement.client_id,
            user_type="client",
            titre="Paiement enregistré",
            message=f"Votre paiement de {paiement.montant} a bien été enregistré.",
            type=TypeNotification.success
        )
        creer_notification(db, notif)
        
        # ✅ Si le paiement est remis au livreur, notifier aussi le marchand
        if paiement.recu_par == RecuPar.livreur:
            livraison = paiement.livraison
            commande = livraison.commande
            marchand_id = commande.marchand_id if commande else None

            if marchand_id:
                notif_marchand = NotificationCreate(
                    user_id=marchand_id,
                    user_type="marchand",
                    titre="Paiement remis au livreur",
                    message=f"Le client a remis un paiement de {paiement.montant} au livreur.",
                    type=TypeNotification.info
                )
                creer_notification(db, notif_marchand)
        return paiement

    @staticmethod
    def supprimer_paiement(db: Session, paiement_id: UUID) -> bool:
        paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
        if not paiement:
            return False
        
        notif = NotificationCreate(
            user_id=paiement.client_id,
            user_type="client",
            titre="Paiement supprimé",
            message="Un de vos paiements a été supprimé par l’administration.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif)
        db.delete(paiement)
        db.commit()
        return True

    @staticmethod
    def lister_paiements(db: Session) -> List[Paiement]:
        return db.query(Paiement).all()

    @staticmethod
    def obtenir_paiement(db: Session, paiement_id: UUID) -> Optional[Paiement]:
        return db.query(Paiement).filter(Paiement.id == paiement_id).first()

    @staticmethod
    def rechercher_par_client(db: Session, client_id: UUID) -> List[Paiement]:
        return db.query(Paiement).filter(Paiement.client_id == client_id).all()

    @staticmethod
    def rechercher_par_marchand(db: Session, marchand_id: UUID) -> List[Paiement]:
         return (
            db.query(Paiement)
            .join(Paiement.livraison)
            .join(Livraison.commande)
            .filter(Livraison.commande.has(marchand_id=marchand_id))
            .all()
        )

    @staticmethod
    def rechercher_par_statut(db: Session, statut: StatutPaiement) -> List[Paiement]:
        return db.query(Paiement).filter(Paiement.statut_paiement == statut).all()
    
    @staticmethod
    def rembourser_paiement(db: Session, paiement_id: UUID) -> Paiement:
        paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
        if not paiement:
            raise HTTPException(status_code=404, detail="Paiement introuvable")
        paiement.statut_paiement = StatutPaiement.remboursé
        db.commit()
        db.refresh(paiement)
        
        # 🔔 Notification client
        notif_client = NotificationCreate(
            user_id=paiement.client_id,
            user_type="client",
            titre="Paiement remboursé",
            message=f"Votre paiement de {paiement.montant} a été remboursé.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_client)

        # 🔔 Notification marchand
        marchand_id = paiement.livraison.commande.marchand_id
        notif_marchand = NotificationCreate(
            user_id=marchand_id,
            user_type="marchand",
            titre="Remboursement effectué",
            message=f"Vous avez effectué un remboursement de {paiement.montant}.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)
        return paiement

    @staticmethod
    def transferer_au_marchand(db: Session, paiement_id: UUID) -> Paiement:
        paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
        if not paiement:
            raise HTTPException(status_code=404, detail="Paiement introuvable")
        
        if paiement.statut_paiement != StatutPaiement.remis_livreur:
            raise HTTPException(status_code=400, detail="Paiement non remis au livreur ou déjà payé")

        paiement.statut_paiement = StatutPaiement.payé
        db.commit()
        db.refresh(paiement)
        
        
        livraison = paiement.livraison
        commande = livraison.commande
        marchand_id = commande.marchand_id
        livreur_id = livraison.livreur_id

        # 🔔 Marchand
        notif_marchand = NotificationCreate(
            user_id=marchand_id,
            user_type="marchand",
            titre="Paiement reçu",
            message=f"Un paiement de {paiement.montant} vous a été transféré.",
            type=TypeNotification.success
        )
        creer_notification(db, notif_marchand)

        # 🔔 Livreur (confirmation de transfert)
        if livreur_id:
            notif_livreur = NotificationCreate(
                user_id=livreur_id,
                user_type="livreur",
                titre="Transfert effectué",
                message=f"Vous avez transféré {paiement.montant} au marchand.",
                type=TypeNotification.success
            )
            creer_notification(db, notif_livreur)
        return paiement
