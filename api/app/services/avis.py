from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.avis import Avis
from app.schemas.avis import AvisCreate

class ServiceAvis:
    @staticmethod
    def creer_avis(db: Session, avis_data: AvisCreate) -> Avis:
        # nouvel_avis = Avis(
        #     livreur_id=avis_data.livreur_id,
        #     livraison_id=avis_data.livraison_id,
        #     client_id=avis_data.client_id,
        #     commentaire=avis_data.commentaire,
        #     note=avis_data.note,
        #     date_avis=datetime.utcnow()
        # )
        nouvel_avis = Avis(
            livreur_id=avis_data.livreur_id,
            livraison_id=avis_data.livraison_id,
            client_id=avis_data.client_id,
            commentaire=avis_data.commentaire,
            note=avis_data.note
        )
        db.add(nouvel_avis)
        db.commit()
        db.refresh(nouvel_avis)
        return nouvel_avis

    @staticmethod
    def supprimer_avis(db: Session, avis_id: UUID) -> bool:
        """
        Supprime un avis à partir de son identifiant.
        """
        avis = db.query(Avis).filter(Avis.id == avis_id).first()
        if avis:
            db.delete(avis)
            db.commit()
            return True
        return False

    @staticmethod
    def lister_avis(db: Session):
        """
        Récupère tous les avis présents dans la base de données.
        """
        return db.query(Avis).all()

    @staticmethod
    def lister_avis_par_livreur(db: Session, livreur_id: UUID):
        """
        Récupère les avis donnés à un livreur spécifique.
        """
        return db.query(Avis).filter(Avis.livreur_id == livreur_id).all()