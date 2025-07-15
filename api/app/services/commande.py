# from sqlalchemy.orm import Session
# from app.models.commande import Commande, StatutCommande
# from app.schemas.commande import CommandeCreate, CommandeUpdate
# from typing import Optional, Dict, List
# import random
# import string
# from uuid import UUID

# class ServiceCommande:
#     """
#     Service métier pour la gestion des commandes
#     """

#     @staticmethod
#     def generer_reference() -> str:
#         """
#         Génère une référence unique pour une commande
#         Format : CMD-AB1234 (2 lettres + 4 chiffres)
#         """
#         lettres = string.ascii_uppercase
#         chiffres = ''.join(random.choices(string.digits, k=4))
#         return f"CMD-{''.join(random.choices(lettres, k=2))}{chiffres}"

#     @staticmethod
#     def calculer_total(articles: List[Dict]) -> float:
#         """
#         Calcule le montant total de la commande
#         """
#         return sum(item.get("prix", 0) * item.get("quantite", 0) for item in articles)

#     @classmethod
#     def creer_commande(
#         cls,
#         db: Session,
#         donnees_commande: CommandeCreate,
#         # id_client: UUID
#     ) -> Commande:
#         """
#         Crée une nouvelle commande dans le système
#         """
#         if not donnees_commande.details.get('produits', []):
#             raise ValueError("La commande doit contenir au moins un article")

#         reference = cls.generer_reference()
#         total = cls.calculer_total(donnees_commande.details['produits'])

#         commande = Commande(
#             reference=reference,
#             details=donnees_commande.details,
#             total=total,
#             # marchand_id=donnees_commande.marchand_id,
#             # client_id=id_client,
#             statut=StatutCommande.EN_ATTENTE
#         )

#         db.add(commande)
#         db.commit()
#         db.refresh(commande)
#         return commande

#     @staticmethod
#     def obtenir_commandes(
#         db: Session,
#         est_admin: bool,
#         id_client: Optional[UUID] = None
#     ) -> List[Commande]:
#         """
#         Récupère les commandes selon les permissions
#         """
#         requete = db.query(Commande)
#         if not est_admin and id_client:
#             requete = requete.filter(Commande.client_id == id_client)
#         return requete.all()

#     @staticmethod
#     def obtenir_commande(
#         db: Session,
#         id_commande: str
#     ) -> Optional[Commande]:
#         """
#         Récupère une commande spécifique par son ID
#         """
#         return db.query(Commande).filter(Commande.id == id_commande).first()

#     @staticmethod
#     def modifier_commande(
#         db: Session,
#         commande: Commande,
#         donnees_maj: CommandeUpdate
#     ) -> Commande:
#         """
#         Met à jour les informations d'une commande
#         """
#         for champ, valeur in donnees_maj.model_dump(exclude_unset=True).items():
#             if champ == 'details' and 'produits' in valeur:
#                 commande.total = ServiceCommande.calculer_total(valeur['produits'])
#             setattr(commande, champ, valeur)
        
#         db.commit()
#         db.refresh(commande)
#         return commande

#     @staticmethod
#     def supprimer_commande(
#         db: Session,
#         commande: Commande
#     ) -> None:
#         """
#         Supprime définitivement une commande
#         """
#         db.delete(commande)
#         db.commit()

#     @staticmethod
#     def changer_statut(
#         db: Session,
#         id_commande: str,
#         nouveau_statut: StatutCommande
#     ) -> Optional[Commande]:
#         """
#         Modifie le statut d'une commande avec validation des transitions
#         """
#         commande = db.query(Commande).get(id_commande)
#         if not commande:
#             return None

#         transitions_valides = {
#             StatutCommande.EN_ATTENTE: [StatutCommande.VALIDEE, StatutCommande.ANNULEE],
#             StatutCommande.VALIDEE: [StatutCommande.EN_COURS],
#             StatutCommande.EN_COURS: [StatutCommande.LIVREE]
#         }

#         if nouveau_statut in transitions_valides.get(commande.statut, []):
#             commande.statut = nouveau_statut
#             db.commit()
#             return commande
#         return None

from app.models.commande import Commande, StatutCommande
from sqlalchemy.orm import Session
import uuid

from app.models.notification import TypeNotification
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification


class ServiceCommande:

    @classmethod
    def generer_reference(cls) -> str:
        return f"C-{uuid.uuid4().hex[:8].upper()}"

    @classmethod
    def calculer_total(cls, produits: list) -> float:
        total = 0
        for produit in produits:
            total += produit.get("prix", 0) * produit.get("quantite", 1)
        return total

    @classmethod
    def creer_commande(cls, db: Session, donnees_commande) -> Commande:
        produits = donnees_commande.details.get("produits", [])
        if not produits:
            raise ValueError("La commande doit contenir au moins un article")

        reference = cls.generer_reference()
        total = cls.calculer_total(produits)

        commande = Commande(
            reference=reference,
            articles=donnees_commande.details,
            total=total,
            statut=StatutCommande.EN_ATTENTE,
            marchand_id=donnees_commande.marchand_id,
            client_id=donnees_commande.client_id
        )


        db.add(commande)
        db.commit()
        db.refresh(commande)
        
        notif = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Commande créée",
            message=f"Votre commande {commande.reference} a été enregistrée.",
            type=TypeNotification.success
        )
        creer_notification(db, notif)
        
        notif_marchand = NotificationCreate(
            user_id=commande.marchand_id,
            user_type="marchand",
            titre="Nouvelle commande reçue",
            message=f"Vous avez reçu une nouvelle commande.",
            type=TypeNotification.info
        )
        creer_notification(db, notif_marchand)
        return commande

    @classmethod
    def obtenir_commandes(cls, db: Session):
        return db.query(Commande).all()

    @classmethod
    def obtenir_commande(cls, db: Session, commande_id: str):
        return db.query(Commande).filter_by(id=commande_id).first()

    @classmethod
    def modifier_commande(cls, db: Session, commande: Commande, donnees_maj) -> Commande:
        if donnees_maj.details:
            commande.articles = donnees_maj.details
            commande.total = cls.calculer_total(donnees_maj.details.get("produits", []))
        # if donnees_maj.statut:
        #     commande.statut = donnees_maj.statut

        db.commit()
        db.refresh(commande)
        
        notif = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Commande modifiée",
            message=f"Les détails de votre commande {commande.reference} ont été mis à jour.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return commande

    # @classmethod
    # def changer_statut(cls, db: Session, id_commande: str, nouveau_statut: StatutCommande):
    #     commande = cls.obtenir_commande(db, id_commande)
    #     if commande:
    #         commande.statut = nouveau_statut
    #         db.commit()
    #         db.refresh(commande)
    #         return commande
    #     return None
    
    @classmethod
    def changer_statut(cls, db: Session, id_commande: str, nouveau_statut: StatutCommande):
        commande = cls.obtenir_commande(db, id_commande)
        if not commande:
            return None

        transitions_valides = {
            StatutCommande.EN_ATTENTE: [StatutCommande.VALIDEE, StatutCommande.ANNULEE],
            StatutCommande.VALIDEE: [StatutCommande.EN_COURS, StatutCommande.ANNULEE],
            StatutCommande.EN_COURS: [StatutCommande.LIVREE, StatutCommande.ANNULEE],
            StatutCommande.LIVREE: [],  # Fin de cycle
            StatutCommande.ANNULEE: []  # Fin de cycle
        }

        if nouveau_statut not in transitions_valides.get(commande.statut, []):
            # Transition non autorisée, on retourne None pour la gestion dans la route
            return None

        commande.statut = nouveau_statut
        db.commit()
        db.refresh(commande)
        
        notif = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Statut de commande mis à jour",
            message=f"Votre commande {commande.reference} est maintenant : {commande.statut.value}.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return commande


    @classmethod
    def supprimer_commande(cls, db: Session, commande: Commande):
        
        notif = NotificationCreate(
            user_id=commande.client_id,
            user_type="client",
            titre="Commande supprimée",
            message=f"Votre commande {commande.reference} a été supprimée.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif)
        db.delete(commande)
        db.commit()
