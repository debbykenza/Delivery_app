from typing import List, Optional
from uuid import UUID
from app.models.livraison import Livraison
from app.models.paiement import MethodePaiement, Paiement, RecuPar, StatutPaiement
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.paiement import PaiementCreate
from fastapi import Depends, HTTPException

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
        return paiement

    @staticmethod
    def supprimer_paiement(db: Session, paiement_id: UUID) -> bool:
        paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
        if not paiement:
            return False
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
        return paiement
