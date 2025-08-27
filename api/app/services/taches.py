from os import getenv
import os
import requests
from gotrue import Session
from app.models.abonnement import Abonnement, StatutAbonnement
from app.core.database import SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler

from app.models.marchand import Marchand
from app.services.abonnement import ServiceAbonnement


def check_transaction_status(tx_ref: str):
    url = "https://paygateglobal.com/api/v1/status"
    payload = {
        "auth_token": os.getenv("API_PAYGATE"),
        "tx_reference": tx_ref
    }
    try:
        response = requests.post(url, json=payload)
        # print(f"[DEBUG1] Réponse de l'API de vérification: {response}")
        print(f"[DEBUG] Réponse de l'API de vérification: {response.text}")
        if response.status_code == 200:
            # print(f"[DEBUG3] Réponse de l'API de vérification: {response.json()}")
            return response.json()
        else:
            print(f"[ERREUR] Statut HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Erreur de vérification: {e}")
    return None

def update_transaction_statuses():
    db: Session = SessionLocal()
    
    marchands = db.query(Marchand).filter(Marchand.status == "inactif").all()
    
    abonnements = db.query(Abonnement).filter(Abonnement.statut == StatutAbonnement.inactif).all()
    print(f"Vérification des transactions pour {len(abonnements)} abonnements inactifs...")
    
    for ab in abonnements:
        try:
            status_data = check_transaction_status(ab.reference_abonnement)
            if not status_data:
                print(f"Aucune donnée de statut pour la référence {ab.reference_abonnement}")
                continue

            status = status_data.get("status")
            print(f"Statut reçu pour l'abonnement {ab.id}: {status}")

            if status == 0:  # Paiement réussi
                print(f"Paiement confirmé pour l'abonnement {ab.id}")
                # ab.statut = "actif"
                # print(f"Statut de l'abonnement 1 : {ab.statut}")
                try:
                    # Appel correct de la méthode du service
                    ServiceAbonnement.activer_abonnement(db, ab.id)
                    print(f"Abonnement {ab.id} activé avec succès")
                    
                except Exception as e:
                    print(f"Erreur lors de l'activation de l'abonnement {ab.id}: {e}")
                # ab.statut = StatutAbonnement.actif
                
                # print(f"Statut de l'abonnement 2 : {ab.statut}")
                
                db.commit()

        finally:
            db.close()

scheduler = BackgroundScheduler()

def start_payment_checker():
    if not scheduler.running:
        scheduler.add_job(update_transaction_statuses, 'interval', seconds=15)
        scheduler.start()


# from os import getenv
# import os
# import requests
# from app.models.abonnement import Abonnement, StatutAbonnement
# from app.core.database import SessionLocal
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.abonnement import ServiceAbonnement
# from sqlalchemy.orm import Session
# import logging

# # Configuration du logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def check_transaction_status(tx_ref: str):
#     """Vérifie le statut d'une transaction auprès de PayGate"""
#     url = "https://paygateglobal.com/api/v1/status"
#     payload = {
#         "auth_token": os.getenv("API_PAYGATE"),
#         "tx_reference": tx_ref
#     }
    
#     try:
#         response = requests.post(url, json=payload, timeout=10)
#         logger.info(f"Réponse API PayGate pour {tx_ref}: {response.text}")
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             logger.error(f"Statut HTTP {response.status_code} pour {tx_ref}")
#             return None
            
#     except requests.exceptions.Timeout:
#         logger.error(f"Timeout lors de la vérification de {tx_ref}")
#     except requests.exceptions.ConnectionError:
#         logger.error(f"Erreur de connexion pour {tx_ref}")
#     except Exception as e:
#         logger.error(f"Exception lors de la vérification de {tx_ref}: {e}")
    
#     return None

# def update_transaction_statuses():
#     """Met à jour le statut des transactions et active les abonnements payés"""
#     db: Session = SessionLocal()
    
#     try:
#         # Récupérer tous les abonnements inactifs avec une référence de transaction
#         abonnements = db.query(Abonnement).filter(
#             Abonnement.statut == StatutAbonnement.inactif,
#             Abonnement.reference_abonnement.isnot(None)
#         ).all()
        
#         logger.info(f"Vérification de {len(abonnements)} abonnements inactifs")
        
#         for abonnement in abonnements:
#             try:
#                 logger.info(f"Vérification de l'abonnement {abonnement.id}, référence: {abonnement.reference_abonnement}")
                
#                 status_data = check_transaction_status(abonnement.reference_abonnement)
                
#                 if not status_data:
#                     continue

#                 status = status_data.get("status")
#                 logger.info(f"Statut {status} pour l'abonnement {abonnement.id}")

#                 if status == 0:  # Paiement réussi
#                     logger.info(f"Paiement confirmé - Activation de l'abonnement {abonnement.id}")
                    
#                     try:
#                         # Activer l'abonnement via le service
#                         ServiceAbonnement.activer_abonnement(db, abonnement.id)
#                         logger.info(f"Abonnement {abonnement.id} activé avec succès")
                        
#                     except Exception as e:
#                         logger.error(f"Erreur lors de l'activation de l'abonnement {abonnement.id}: {e}")
#                         # Rollback en cas d'erreur
#                         db.rollback()
#                         continue
                        
#                 elif status == 1:  # Paiement échoué
#                     logger.warning(f"Paiement échoué pour l'abonnement {abonnement.id}")
#                     # Logique pour les échecs de paiement peut être ajoutée ici
                    
#             except Exception as e:
#                 logger.error(f"Erreur lors du traitement de l'abonnement {abonnement.id}: {e}")
#                 continue
                
#         # Commit final après tous les traitements
#         db.commit()
        
#     except Exception as e:
#         logger.error(f"Erreur générale dans update_transaction_statuses: {e}")
#         db.rollback()
#     finally:
#         db.close()

# # Configuration du scheduler
# scheduler = BackgroundScheduler()

# def start_payment_checker():
#     """Démarre le scheduler pour vérifier les paiements périodiquement"""
#     if not scheduler.running:
#         scheduler.add_job(
#             update_transaction_statuses, 
#             'interval', 
#             seconds=15,
#             id='payment_checker',
#             max_instances=1
#         )
#         scheduler.start()
#         logger.info("Scheduler démarré - Vérification des paiements toutes les 15 secondes")

# def stop_payment_checker():
#     """Arrête le scheduler"""
#     if scheduler.running:
#         scheduler.shutdown()
#         logger.info("Scheduler arrêté")