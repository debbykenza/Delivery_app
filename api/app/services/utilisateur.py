from datetime import datetime, timedelta
from http.client import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.utilisateur import Utilisateur, Role
from app.core.security import hash_password
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate

import bcrypt

def creer_utilisateur(db: Session, utilisateur_data: UtilisateurCreate) -> Utilisateur:
    """
    Crée un nouvel utilisateur dans la base de données.
    """
    utilisateur = Utilisateur(
        nom=utilisateur_data.nom,
        email=utilisateur_data.email,
        mot_de_passe=hash_password(utilisateur_data.mot_de_passe),
        role=utilisateur_data.role,
        is_active=utilisateur_data.is_active
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def authentifier_utilisateur(db: Session, email: str, mot_de_passe: str) -> Utilisateur | None:
    """
    Authentifie un utilisateur en vérifiant ses identifiants.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()

    if not utilisateur or not utilisateur.mot_de_passe:
        return None

    if not bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur.mot_de_passe.encode('utf-8')):
        return None

    return utilisateur


def mettre_a_jour_utilisateur(db: Session, utilisateur_id: UUID, utilisateur_data: UtilisateurUpdate) -> Utilisateur:
    """
    Met à jour les informations d'un utilisateur existant.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        return None

    if utilisateur_data.nom is not None:
        utilisateur.nom = utilisateur_data.nom
    if utilisateur_data.email is not None:
        utilisateur.email = utilisateur_data.email
    if utilisateur_data.mot_de_passe is not None:
        utilisateur.mot_de_passe = hash_password(utilisateur_data.mot_de_passe)
    if utilisateur_data.is_active is not None:
        utilisateur.is_active = utilisateur_data.is_active
    if utilisateur_data.role is not None:
        utilisateur.role = Role(utilisateur_data.role)

    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def recuperer_utilisateur_par_id(db: Session, utilisateur_id: UUID) -> Utilisateur:
    """
    Récupère un utilisateur par son ID.
    """
    return db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()

def recuperer_utilisateur_par_email(db: Session, email: str) -> Utilisateur:
    """
    Récupère un utilisateur par son adresse email.
    """
    return db.query(Utilisateur).filter(Utilisateur.email == email).first()

def supprimer_utilisateur(db: Session, utilisateur_id: UUID) -> bool:
    """
    Supprime un utilisateur de la base de données.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        return False

    db.delete(utilisateur)
    db.commit()
    return True

def recuperer_tous_les_utilisateurs(db: Session) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs de la base de données.
    """
    return db.query(Utilisateur).all()

def activer_utilisateur(db: Session, utilisateur_id: UUID) -> Utilisateur:
    """
    Active un utilisateur en mettant à jour son statut is_active.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        return None

    utilisateur.is_active = True
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def desactiver_utilisateur(db: Session, utilisateur_id: UUID) -> Utilisateur:
    """
    Désactive un utilisateur en mettant à jour son statut is_active.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        return None

    utilisateur.is_active = False
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def recuperer_utilisateur_par_role(db: Session, role: Role) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs ayant un rôle spécifique.
    """
    return db.query(Utilisateur).filter(Utilisateur.role == role).all()

def recuperer_utilisateur_par_nom(db: Session, nom: str) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs dont le nom correspond à la chaîne de caractères donnée.
    """
    return db.query(Utilisateur).filter(Utilisateur.nom.ilike(f"%{nom}%")).all()

def recuperer_utilisateur_par_date_creation(db: Session, date_debut: datetime, date_fin: datetime) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs créés entre deux dates.
    """
    return db.query(Utilisateur).filter(Utilisateur.date_creation.between(date_debut, date_fin)).all()

def recuperer_utilisateur_par_date_mise_a_jour(db: Session, date_debut: datetime, date_fin: datetime) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs mis à jour entre deux dates.
    """
    return db.query(Utilisateur).filter(Utilisateur.date_mise_a_jour.between(date_debut, date_fin)).all()   

def recuperer_utilisateur_par_statut(db: Session, is_active: bool) -> list[Utilisateur]:
    """
    Récupère tous les utilisateurs ayant un statut actif ou inactif.
    """
    return db.query(Utilisateur).filter(Utilisateur.is_active == is_active).all()

def recuperer_utilisateur_courant(db: Session, utilisateur_id: UUID) -> Utilisateur:
    """
    Récupère l'utilisateur actuellement connecté.
    """
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

