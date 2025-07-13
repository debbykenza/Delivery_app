# journal_requete.py

from datetime import datetime
import time
from sqlalchemy import UUID
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.database import SessionLocal
from app.models.requete_api import RequeteAPI

# 🚫 Endpoints techniques à ignorer dans les statistiques
ROUTES_IGNOREE = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
    "/stats/requetes",
    "/"
]

# Middleware pour journaliser les requêtes API
class JournalRequeteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        debut = time.time()
        response = await call_next(request)
        duree = time.time() - debut

        db = SessionLocal()
        try:
            # Récupère le marchand_id depuis l'en-tête ou autre
            marchand_id = request.headers.get("X-MARCHAND-ID")  # ou extrais depuis le token
            if marchand_id:
                marchand_id = UUID(marchand_id)

            requete = RequeteAPI(
                endpoint=str(request.url.path),
                méthode=request.method,
                statut=response.status_code,
                temps_réponse=round(duree, 4),
                marchand_id=marchand_id  # ✅ Enregistrement ici
            )
            db.add(requete)
            db.commit()
        finally:
            db.close()

        return response

    
   