from os import getenv
import os
import requests
from gotrue import Session
from app.models.abonnement import Abonnement
from app.core.database import SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler  # Import manquant ajouté ici


def check_transaction_status(tx_ref: str):
    url = "https://paygateglobal.com/api/v2/status"
    payload = {
        "auth_token": os.getenv("API_PAYGATE"),
        "identifier": tx_ref
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[DEBUG] Réponse de l'API de vérification: {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERREUR] Statut HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Erreur de vérification: {e}")
    return None

def update_transaction_statuses():
    db: Session = SessionLocal()
    
    abonnements = db.query(Abonnement).filter(Abonnement.statut == "inactif").all()
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
                ab.statut = "actif"
                
                db.commit()

        finally:
            db.close()

scheduler = BackgroundScheduler()

def start_payment_checker():
    if not scheduler.running:
        scheduler.add_job(update_transaction_statuses, 'interval', minutes=5)
        scheduler.start()
