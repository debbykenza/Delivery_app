from sqlalchemy import UUID
from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.notification import TypeNotification
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification

def creer_client(db: Session, client_data: ClientCreate):
    client = Client(**client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    
    notif = NotificationCreate(
        user_id=client.id,
        user_type="client",
        titre="Compte créé",
        message=f"Bienvenue {client.nom}, votre compte client a été créé avec succès.",
        type=TypeNotification.success
    )
    creer_notification(db, notif)
    return client

def obtenir_client_par_id(db: Session, client_id: UUID):
    return db.query(Client).filter(Client.id == client_id).first()

def lister_clients(db: Session):
    return db.query(Client).all()

def modifier_client(db: Session, client_id: UUID, update_data: ClientUpdate):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(client, field, value)
        db.commit()
        db.refresh(client)
        
        notif = NotificationCreate(
            user_id=client_id,
            user_type="client",
            titre="Profil mis à jour",
            message="Vos informations ont été mises à jour avec succès.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
    return client

def supprimer_client(db: Session, client_id: UUID):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
        
        notif = NotificationCreate(
            user_id=client_id,
            user_type="client",
            titre="Compte supprimé",
            message="Votre compte a été supprimé du système.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif)
    return client

from sqlalchemy import UUID
from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.notification import TypeNotification
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification


def mettre_a_jour_adresse_client(db: Session, client_id: UUID, nouvelle_adresse: str):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None
    
    # Mise à jour de l'adresse
    client.adresse = nouvelle_adresse
    db.commit()
    db.refresh(client)
    
    # Création de la notification
    notif = NotificationCreate(
        user_id=client_id,
        user_type="client",
        titre="Adresse mise à jour",
        message=f"Votre adresse a été modifiée avec succès en : {nouvelle_adresse}.",
        type=TypeNotification.info
    )
    creer_notification(db, notif)
    
    return client

