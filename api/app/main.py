from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.database import Base, engine
from app.models.utilisateur import Utilisateur
from app.models.commande import Commande
# from app.startup import create_default_admin
from app.routes import auth
from app.routes import commandes
from app.routes import cle_apis  
from app.routes import marchands  
from app.services.commande import ServiceCommande
from app.schemas.commande import CommandeCreate, CommandeUpdate, CommandeRead
from app.models.commande import StatutCommande
# from app.utils.security import get_current_user  # Utilitaire local
#from app.routes import utilisateurs

from fastapi.openapi.utils import get_openapi


# 🔌 Vérification de la connexion à la base de données
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Connexion à la base Supabase réussie.")
    except Exception as e:
        print("❌ Erreur de connexion à la base Supabase :", e)

# 🧱 Création automatique des tables
Base.metadata.create_all(bind=engine)

# 🚀 Création de l'administrateur par défaut
#create_default_admin()

# 🌐 Initialisation de l'application FastAPI
app = FastAPI(
    title="DELIVERY API",
    description="API pour la plateforme fournissant une api de gestion de livraison",
    version="1.0.0"
)

# 🔌 Vérification de la base au démarrage
test_db_connection()

# 🔐 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚩 Route par défaut
@app.get("/")
def root():
    return {"message": "Lancement de l'API réussi"}

# 📦 Inclusion des routes
app.include_router(auth.router, tags=["auth"])
app.include_router(cle_apis.router, tags=["Clés API"])
app.include_router(commandes.router, tags=["commandes"])

app.include_router(marchands.router, tags=["Marchands"])
#app.include_router(utilisateurs.router, tags=["utilisateurs"])


# Ajout du schéma de sécurité dans la doc Swagger
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title="Mon API de Livraison",
#         version="1.0.0",
#         description="Documentation de l'API",
#         routes=app.routes,
#     )

#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }

#     # Appliquer à toutes les routes par défaut
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             method.setdefault("security", [{"BearerAuth": []}])

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi