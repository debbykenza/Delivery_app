from sqlalchemy.orm import Session
from app.models.livreur import Livreur as LivreurModel
from app.schemas.livreur import LivreurCreate, LivreurUpdate, StatutLivreurUpdate
from uuid import UUID


class LivreurService:
    @staticmethod
    def creer_livreur(db: Session, livreur_data: LivreurCreate) -> LivreurModel:
        livreur = LivreurModel(**livreur_data.dict())
        db.add(livreur)
        db.commit()
        db.refresh(livreur)
        return livreur

    @staticmethod
    def obtenir_livreur(db: Session, livreur_id: UUID):
        return db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()

    @staticmethod
    def mettre_a_jour_statut(db: Session, livreur_id: UUID, update_data: StatutLivreurUpdate):
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None

        livreur.statut = update_data.nouveau_statut
        db.commit()
        db.refresh(livreur)
        return livreur

    @staticmethod
    def lister_livreurs(db: Session):
        return db.query(LivreurModel).all()


    @staticmethod
    def modifier_livreur(db: Session, livreur_id: UUID, update_data: LivreurUpdate) -> LivreurModel:
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(livreur, key, value)
        db.commit()
        db.refresh(livreur)
        return livreur

    
    @staticmethod
    def supprimer_livreur(db: Session, livreur_id: UUID):
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return False
        db.delete(livreur)
        db.commit()
        return True
