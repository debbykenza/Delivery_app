# from pydantic import BaseModel, Field, validator
# from typing import Optional, List, Dict
# from uuid import UUID
# from datetime import datetime
# from enum import Enum

# class StatutCommande(str, Enum):
#     """Enumération des statuts possibles d'une commande"""
#     EN_ATTENTE = "en_attente"
#     VALIDEE = "validée"
#     ANNULEE = "annulée"
#     EN_COURS = "en_cours"
#     LIVREE = "livrée"

# class ArticleSchema(BaseModel):
#     """Schéma pour un article dans une commande"""
#     id: int = Field(..., description="ID unique du produit")
#     nom: str = Field(..., max_length=100, description="Nom du produit")
#     quantite: int = Field(..., gt=0, description="Quantité commandée")
#     prix: float = Field(..., gt=0, description="Prix unitaire")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "id": 1,
#                 "nom": "T-shirt en coton",
#                 "quantite": 2,
#                 "prix": 29.99
#             }
#         }

# class CommandeCreate(BaseModel):
#     """Schéma pour la création d'une commande"""
#     # marchand_id: UUID = Field(..., description="ID du marchand associé")
#     produits: List[ArticleSchema] = Field(..., min_items=1, description="Liste des articles commandés")

#     @validator('produits')
#     def valider_produits(cls, v):
#         if not v:
#             raise ValueError("La commande doit contenir au moins un article")
#         return v

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "marchand_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "produits": [
#                     {
#                         "id": 1,
#                         "nom": "T-shirt en coton",
#                         "quantite": 2,
#                         "prix": 29.99
#                     }
#                 ]
#             }
#         }

# class CommandeUpdate(BaseModel):
#     """Schéma pour la mise à jour d'une commande"""
#     produits: Optional[List[ArticleSchema]] = Field(None, description="Nouvelle liste d'articles")
#     statut: Optional[StatutCommande] = Field(None, description="Nouveau statut de la commande")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "statut": "validée",
#                 "produits": [
#                     {
#                         "id": 1,
#                         "nom": "T-shirt en coton",
#                         "quantite": 3,  # Quantité modifiée
#                         "prix": 29.99
#                     }
#                 ]
#             }
#         }

# class CommandeRead(BaseModel):
#     """Schéma pour la lecture d'une commande"""
#     id: UUID = Field(..., description="ID unique de la commande")
#     reference: str = Field(..., description="Référence unique de la commande")
#     produits: List[Dict] = Field(..., description="Articles commandés")
#     statut: StatutCommande = Field(..., description="Statut actuel")
#     total: float = Field(..., description="Montant total calculé")
#     created_at: datetime = Field(..., description="Date de création")
#     # client_id: UUID = Field(..., description="ID du client")
#     # marchand_id: UUID = Field(..., description="ID du marchand")

#     class Config:
#         from_attributes = True
#         json_schema_extra = {
#             "example": {
#                 "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "reference": "CMD-AB1234",
#                 "statut": "en_attente",
#                 "total": 59.98,
#                 "created_at": "2023-01-01T00:00:00",
#                 # "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 # "marchand_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "produits": [
#                     {
#                         "id": 1,
#                         "nom": "T-shirt en coton",
#                         "quantite": 2,
#                         "prix": 29.99
#                     }
#                 ]
#             }
#         }


from pydantic import BaseModel, Field
from uuid import UUID
from typing import Any, List, Optional
from datetime import datetime
from enum import Enum


class StatutCommande(str, Enum):
    EN_ATTENTE = "en_attente"
    VALIDEE = "validée"
    ANNULEE = "annulée"
    EN_COURS = "en_cours"
    LIVREE = "livrée"

class ChangementStatutCommande(BaseModel):
    nouveau_statut: StatutCommande

class CommandeCreate(BaseModel):
    marchand_id: UUID
    client_id: UUID
    details: dict  # contient les articles, exemple : {"produits": [...]}
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "abf4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "marchand_id": "b5cee64b-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "details": {
                    "produits": [
                        {
                            "id": 1,
                            "nom": "T-shirt en coton",
                            "quantite": 2,
                            "prix": 29.99
                        }
                    ]
                }
            }
        }
# class CommandeUpdate(BaseModel):
#     statut: Optional[StatutCommande] = None
#     details: Optional[dict] = None

class CommandeUpdate(BaseModel):
    details: Optional[dict] = None
    class Config:
        json_schema_extra = {
            "example": {
                "details": {
                    "produits": [
                        {
                            "id": 1,
                            "nom": "T-shirt en coton",
                            "quantite": 3,
                            "prix": 29.99
                        }
                    ]
                }
            }
        }

class CommandeRead(BaseModel):
    id: UUID
    reference: str
    statut: StatutCommande
    total: float
    articles: dict
    created_at: datetime
    marchand_id: Optional[UUID]
    client_id: Optional[UUID]
    class Config:
        from_attributes = True
