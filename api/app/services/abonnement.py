# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from app.models.abonnement import Abonnement, StatutAbonnement
# from app.schemas.abonnement import AbonnementCreate


# class ServiceAbonnement:
#     @staticmethod
#     def creer_abonnement(db: Session, data: AbonnementCreate) -> Abonnement:
#         date_debut = datetime.utcnow()
#         date_expiration = date_debut + timedelta(days=data.duree_jours)

#         nouvel_abonnement = Abonnement(
#             marchand_id=data.marchand_id,
#             montant=data.montant,
#             date_debut=date_debut,
#             date_expiration=date_expiration,
#             statut=StatutAbonnement.actif
#         )

#         db.add(nouvel_abonnement)
#         db.commit()
#         db.refresh(nouvel_abonnement)
#         return nouvel_abonnement

#     @staticmethod
#     def supprimer_abonnement(db: Session, abonnement_id: UUID) -> bool:
#         abonnement = db.query(Abonnement).filter(Abonnement.id == abonnement_id).first()
#         if not abonnement:
#             return False
#         db.delete(abonnement)
#         db.commit()
#         return True

#     @staticmethod
#     def lister_abonnements(db: Session):
#         return db.query(Abonnement).all()

#     @staticmethod
#     def get_abonnement_par_marchand(db: Session, marchand_id: UUID):
#         return db.query(Abonnement).filter(Abonnement.marchand_id == marchand_id).all()

#     @staticmethod
#     def get_abonnement_par_statut(db: Session, statut: StatutAbonnement):
#         return db.query(Abonnement).filter(Abonnement.statut == statut).all()
