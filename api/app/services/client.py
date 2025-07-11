from sqlalchemy import UUID
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def creer_client(db: Session, client_data: ClientCreate):
    client = Client(**client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
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
    return client

def supprimer_client(db: Session, client_id: UUID):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client
