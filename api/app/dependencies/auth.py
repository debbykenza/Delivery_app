from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import verify_access_token  # tu peux renommer la fonction si tu veux
from app.core.database import SessionLocal
from app.models.utilisateur import Utilisateur, Role

# Schéma d'authentification (HTTP Bearer Token)
schema_authentification = HTTPBearer()


#  Connexion à la base de données
def recuperer_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  Récupération de l'utilisateur courant à partir du token
def recuperer_utilisateur_courant(
    identifiants: HTTPAuthorizationCredentials = Depends(schema_authentification),
    db: Session = Depends(recuperer_db)
) -> Utilisateur:
    token = identifiants.credentials
    donnees_token = verify_access_token(token)

    if not donnees_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
        )

    utilisateur_id = donnees_token.get("sub")
    if not utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant utilisateur manquant dans le token",
        )

    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()

    if not utilisateur or not utilisateur.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif ou inexistant",
        )

    return utilisateur


#  Dépendance pour vérifier le rôle de l'utilisateur

#  Accès réservé à l'administrateur
def exiger_admin(utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)):
    if utilisateur.role != Role.admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administrateur.")
    return utilisateur

#  Accès réservé au livreur
def exiger_livreur(utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)):
    if utilisateur.role != Role.livreur:
        raise HTTPException(status_code=403, detail="Accès réservé aux livreurs.")
    return utilisateur

#  Accès réservé au marchand
def exiger_marchand(utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)):
    if utilisateur.role != Role.marchand:
        raise HTTPException(status_code=403, detail="Accès réservé aux marchands.")
    return utilisateur

#  Accès réservé aux utilisateurs standards
def exiger_utilisateur(utilisateur: Utilisateur = Depends(recuperer_utilisateur_courant)):
    if utilisateur.role != Role.utilisateur:
        raise HTTPException(status_code=403, detail="Accès réservé aux utilisateurs.")
    return utilisateur
