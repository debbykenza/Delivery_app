from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.requete_api import RequeteAPI

# Service pour récupérer les statistiques des requêtes API
def obtenir_stats_requetes(db: Session):
    resultats = (
        db.query(
            RequeteAPI.endpoint,
            RequeteAPI.méthode,
            func.count().label("nombre_requetes"),
            func.avg(RequeteAPI.temps_réponse).label("temps_moyen"),
            func.min(RequeteAPI.date).label("date_min"),
            func.max(RequeteAPI.date).label("date_max"),
        )
        .group_by(RequeteAPI.endpoint, RequeteAPI.méthode)
        .all()
    )

    return [
        {
            "endpoint": endpoint,
            "methode": methode,
            "nombre_requetes": nombre_requetes,
            "temps_reponse_moyen": round(temps_moyen, 4) if temps_moyen else 0,
            "date_min": date_min.isoformat() if date_min else None,
            "date_max": date_max.isoformat() if date_max else None,
        }
        for endpoint, methode, nombre_requetes, temps_moyen, date_min, date_max in resultats
    ]

    
# Suppression automatique des requêtes API anciennes après 360 jours
def supprimer_requetes_anciennes(db):
    seuil = datetime.utcnow() - timedelta(days=360)
    db.query(RequeteAPI).filter(RequeteAPI.date < seuil).delete()
    db.commit()
    
# 🔸 Requêtes d'un marchand spécifique
def lister_requetes_par_marchand(marchand_id: str, db: Session):
    requetes = (
        db.query(RequeteAPI)
        .filter(RequeteAPI.marchand_id == marchand_id)
        .order_by(RequeteAPI.date.desc())
        .all()
    )

    return [
        {
            "endpoint": r.endpoint,
            "methode": r.méthode,
            "statut": r.statut,
            "temps_reponse": r.temps_réponse,
            "date": r.date.isoformat() if r.date else None,
        }
        for r in requetes
    ]



# 🔸 Requêtes totales par période (globales)
def requetes_par_periode(nb_jours: int, db: Session):
    date_limite = datetime.utcnow() - timedelta(days=nb_jours)

    resultats = (
        db.query(
            RequeteAPI.endpoint,
            RequeteAPI.méthode,
            func.count().label("nombre_requetes"),
            func.avg(RequeteAPI.temps_réponse).label("temps_moyen"),
            func.min(RequeteAPI.date).label("date_min"),
            func.max(RequeteAPI.date).label("date_max"),
        )
        .filter(RequeteAPI.date >= date_limite)
        .group_by(RequeteAPI.endpoint, RequeteAPI.méthode)
        .all()
    )

    return [
        {
            "endpoint": endpoint,
            "methode": methode,
            "nombre_requetes": nombre_requetes,
            "temps_reponse_moyen": round(temps_moyen, 4),
            "date_min": date_min.isoformat() if date_min else None,
            "date_max": date_max.isoformat() if date_max else None,
        }
        for endpoint, methode, nombre_requetes, temps_moyen, date_min, date_max in resultats
    ]


# 🔸 Requêtes par période pour un marchand
def requetes_par_periode_et_marchand(marchand_id: str, nb_jours: int, db: Session):
    date_limite = datetime.utcnow() - timedelta(days=nb_jours)

    resultats = (
        db.query(
            RequeteAPI.endpoint,
            RequeteAPI.méthode,
            func.count().label("nombre_requetes"),
            func.avg(RequeteAPI.temps_réponse).label("temps_moyen"),
            func.min(RequeteAPI.date).label("date_min"),
            func.max(RequeteAPI.date).label("date_max"),
        )
        .filter(RequeteAPI.date >= date_limite)
        .filter(RequeteAPI.marchand_id == marchand_id)
        .group_by(RequeteAPI.endpoint, RequeteAPI.méthode)
        .all()
    )

    return [
        {
            "endpoint": endpoint,
            "methode": methode,
            "nombre_requetes": nombre_requetes,
            "temps_reponse_moyen": round(temps_moyen, 4),
            "date_min": date_min.isoformat() if date_min else None,
            "date_max": date_max.isoformat() if date_max else None,
        }
        for endpoint, methode, nombre_requetes, temps_moyen, date_min, date_max in resultats
    ]

