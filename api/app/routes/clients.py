from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.client import ClientCreate, ClientOut, ClientUpdate

from app.schemas.commande import CommandeCreate, CommandeRead
from app.services.client import (
    creer_client, mettre_a_jour_adresse_client, obtenir_client_par_id, lister_clients,
    modifier_client, supprimer_client
)
from app.core.database import get_db
from app.services.commande import ServiceCommande  # Assure-toi d’avoir ce fichier avec la session

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientOut)
def creer_clients(client: ClientCreate, db: Session = Depends(get_db)):
    return creer_client(db, client)

@router.get("/", response_model=List[ClientOut])
def lister_les_clients(db: Session = Depends(get_db)):
    return lister_clients(db)

@router.get("/{client_id}", response_model=ClientOut)
def obtenir_client(client_id: UUID, db: Session = Depends(get_db)):
    client = obtenir_client_par_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.put("/{client_id}", response_model=ClientOut)
def modifier_clients(client_id: UUID, update_data: ClientUpdate, db: Session = Depends(get_db)):
    client = modifier_client(db, client_id, update_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.delete("/{client_id}")
def supprimer_clients(client_id: UUID, db: Session = Depends(get_db)):
    client = supprimer_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return {"message": "Client supprimé"}

@router.post("/commande", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
def creer_commande(
    commande_data: CommandeCreate,
    db: Session = Depends(get_db),
):
    try:
        commande = ServiceCommande.creer_commande(db=db, donnees_commande=commande_data)
        return commande
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("ERREUR:", str(e))
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la commande")
    

@router.patch("/{client_id}/adresse", response_model=ClientOut)
def mettre_a_jour_adresse(
    client_id: UUID,
    nouvelle_adresse: str, # on attend {"nouvelle_adresse": "..."}
    db: Session = Depends(get_db)
):
    client = mettre_a_jour_adresse_client(db, client_id, nouvelle_adresse)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client