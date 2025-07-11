from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from uuid import UUID
from fastapi import HTTPException 

from app.models.livraison import Livraison
from app.models.commande import Commande
# from app.models.avis import Avis
from app.schemas.livraison import LivraisonCreate, LivraisonStatutUpdate, ProblemeSignalement


class LivraisonService:

    @staticmethod
    def creer_livraison(db: Session, livraison_data: LivraisonCreate):
        livraison = Livraison(**livraison_data.dict())
        db.add(livraison)
        db.commit()
        db.refresh(livraison)
        return livraison

    @staticmethod
    def obtenir_livraison(db: Session, livraison_id: UUID):
        return db.query(Livraison).filter(Livraison.id == livraison_id).first()

    @staticmethod
    def accepter_livraison(db: Session, livraison_id: UUID, livreur_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.livreur_id = livreur_id
        livraison.statut = "acceptee"
        db.commit()
        db.refresh(livraison)
        return livraison

    @staticmethod
    def terminer_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = "terminee"
        db.commit()
        db.refresh(livraison)
        return livraison

    @staticmethod
    def annuler_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        livraison.statut = "annulee"
        db.commit()
        db.refresh(livraison)
        return livraison

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
        return livraison

    @staticmethod
    def supprimer_livraison(db: Session, livraison_id: UUID):
        livraison = db.query(Livraison).filter(Livraison.id == livraison_id).first()
        if not livraison:
            raise HTTPException(status_code=404, detail="Livraison introuvable")
        db.delete(livraison)
        db.commit()
        return {"message": "Livraison supprimée avec succès"}
