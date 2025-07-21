# DELIVERY API
API pour la plateforme fournissant une api de gestion de livraison

## Version: 1.0.0

### /

#### GET
##### Summary:

Root

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /auth/inscription

#### POST
##### Summary:

Inscription Utilisateur

##### Description:

Endpoint to register a new user.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /auth/connexion

#### POST
##### Summary:

Connexion Utilisateur

##### Description:

Endpoint to login a user.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/creer

#### POST
##### Summary:

Creer Cle Api

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/liste

#### GET
##### Summary:

Lister Cles Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| utilisateur_id | query |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/supprimer/{cle_id}

#### DELETE
##### Summary:

Supprimer Cle Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| cle_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/revocation/{cle_id}

#### PUT
##### Summary:

Revoquer Cle Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| cle_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/nommer/{cle_id}

#### PUT
##### Summary:

Nommer Cle Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| cle_id | path |  | Yes | string (uuid) |
| nouveau_nom | query |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/regenerer/{cle_id}

#### PUT
##### Summary:

Regenerer Cle Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| cle_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /cles-api/statistiques/{utilisateur_id}

#### GET
##### Summary:

Consulter Stats Api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| utilisateur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /stats/requetes

#### GET
##### Summary:

Lister Stats Requetes

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /stats/requetes/jour

#### GET
##### Summary:

Requetes Dernier Jour

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /stats/requetes/semaine

#### GET
##### Summary:

Requetes 7 Jours

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /stats/requetes/mois

#### GET
##### Summary:

Requetes 30 Jours

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /stats/requetes/trimestre

#### GET
##### Summary:

Requetes 90 Jours

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /stats/requetes/annee

#### GET
##### Summary:

Requetes Annee

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /commandes/

#### GET
##### Summary:

Lister Commandes

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Commande

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /commandes/{commande_id}

#### GET
##### Summary:

Obtenir Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### PUT
##### Summary:

Modifier Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### DELETE
##### Summary:

Supprimer Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /commandes/{commande_id}/statut

#### PATCH
##### Summary:

Changer Statut Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/

#### GET
##### Summary:

Lister Marchands

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Marchand

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/statistiques

#### GET
##### Summary:

Voir Statistiques Livraisons Test

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | query | UUID du marchand ?? tester | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/{marchand_id}

#### GET
##### Summary:

Obtenir Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/marchands/{marchand_id}

#### PUT
##### Summary:

Modifier Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### DELETE
##### Summary:

Supprimer Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/commandes/{commande_id}/accepter

#### PUT
##### Summary:

Accepter Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/commandes/{commande_id}/livrer

#### PUT
##### Summary:

Lancer Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/commandes/{commande_id}/annuler

#### PUT
##### Summary:

Annuler Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/commandes/{commande_id}

#### GET
##### Summary:

Voir Details Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /marchands/{marchand_id}/adresse

#### PUT
##### Summary:

Modifier Adresse

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |
| adresse | query |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /abonnements/nombre-abonnes

#### GET
##### Summary:

Obtenir Nombre Abonnes

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /abonnements/temps-restant/{marchand_id}

#### GET
##### Summary:

Obtenir Temps Restant Avant Expiration

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /abonnements/historique/{marchand_id}

#### GET
##### Summary:

Obtenir Historique Abonnements

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /abonnements/souscrire

#### POST
##### Summary:

Souscrire Abonnement

##### Description:

Permet ?? un marchand de souscrire ?? un abonnement standard de 30 jours.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | query |  | Yes | string (uuid) |
| montant | query |  | Yes | number |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /abonnements/

#### GET
##### Summary:

Lister Abonnements

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /abonnements/{abonnement_id}

#### GET
##### Summary:

Obtenir Abonnement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| abonnement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### PUT
##### Summary:

Modifier Abonnement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| abonnement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### DELETE
##### Summary:

Supprimer Abonnement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| abonnement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /abonnements/marchand/{marchand_id}

#### GET
##### Summary:

Abonnements Par Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /abonnements/statut/{statut}

#### GET
##### Summary:

Abonnements Par Statut

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| statut | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/

#### GET
##### Summary:

Lister Livreurs

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Livreur

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /livreurs/{livreur_id}/modifier

#### PATCH
##### Summary:

Modifier Livreur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/{livreur_id}

#### DELETE
##### Summary:

Supprimer Livreur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### GET
##### Summary:

Obtenir Livreur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/{livreur_id}/statut

#### PATCH
##### Summary:

Changer Statut Livreur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/accepter/{livraison_id}/{livreur_id}

#### PUT
##### Summary:

Accepter Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/livraisons/{livraison_id}/demarrer

#### PUT
##### Summary:

Demarrer Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/commandes/{commande_id}

#### GET
##### Summary:

Voir Details Commande

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| commande_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/livraisons/{livraison_id}/terminer

#### PUT
##### Summary:

Terminer Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/annuler/{livraison_id}

#### PUT
##### Summary:

Annuler Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/signaler-probleme/{livraison_id}

#### PUT
##### Summary:

Signaler Probleme

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livreurs/historique/{livreur_id}

#### GET
##### Summary:

Voir Historique Livraisons

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livraisons/creer

#### POST
##### Summary:

Creer Livraison

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livraisons/suivre/{livraison_id}

#### GET
##### Summary:

Obtenir Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livraisons/supprimer/{livraison_id}

#### DELETE
##### Summary:

Supprimer Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /livraisons/disponibles

#### GET
##### Summary:

Livraisons Disponibles

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /livraisons/statut/{livraison_id}

#### PUT
##### Summary:

Mettre A Jour Statut

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /positions/

#### POST
##### Summary:

Enregistrer Position

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /positions/livreur/{livreur_id}

#### GET
##### Summary:

Derniere Position

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /positions/livraison/{livraison_id}

#### GET
##### Summary:

Positions Par Livraison

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livraison_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /positions/{livreur_id}

#### PUT
##### Summary:

Modifier Position

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /positions/{position_id}

#### DELETE
##### Summary:

Supprimer Position

##### Description:

Supprime une position GPS (cas exceptionnel uniquement).

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| position_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /clients/

#### GET
##### Summary:

Lister Les Clients

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Clients

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /clients/{client_id}

#### GET
##### Summary:

Obtenir Client

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| client_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### PUT
##### Summary:

Modifier Clients

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| client_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### DELETE
##### Summary:

Supprimer Clients

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| client_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /clients/commande

#### POST
##### Summary:

Creer Commande

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /adresses/

#### GET
##### Summary:

Lister Adresses

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Adresse

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /adresses/{adresse_id}

#### PUT
##### Summary:

Modifier Adresse

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| adresse_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### DELETE
##### Summary:

Supprimer Adresse

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| adresse_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/client/{client_id}

#### GET
##### Summary:

Lister Adresses Client

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| client_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/livreur/{livreur_id}

#### GET
##### Summary:

Lister Adresses Livreur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/marchand/{marchand_id}

#### GET
##### Summary:

Lister Adresses Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/utilisateur/{utilisateur_id}

#### GET
##### Summary:

Lister Adresses Utilisateur

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| utilisateur_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/{adresse_id}/zone/geojson

#### GET
##### Summary:

Get Zone Geojson

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| adresse_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /adresses/{adresse_id}/point/geojson

#### GET
##### Summary:

Get Position Point Geojson

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| adresse_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /avis/

#### GET
##### Summary:

Lister Avis

##### Description:

Liste tous les avis.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Donner Avis

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /avis/{avis_id}

#### DELETE
##### Summary:

Supprimer Avis

##### Description:

Supprime un avis existant.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| avis_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /avis/livreur/{livreur_id}

#### GET
##### Summary:

Lister Avis Par Livreur

##### Description:

Liste les avis donn??s ?? un livreur sp??cifique.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| livreur_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/

#### GET
##### Summary:

Lister Paiements

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

#### POST
##### Summary:

Creer Paiement

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/{paiement_id}

#### DELETE
##### Summary:

Supprimer Paiement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| paiement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### GET
##### Summary:

Obtenir Paiement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| paiement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/client/{client_id}

#### GET
##### Summary:

Paiements Par Client

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| client_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/marchand/{marchand_id}

#### GET
##### Summary:

Paiements Par Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| marchand_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/{paiement_id}/transferer

#### PUT
##### Summary:

Transferer Au Marchand

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| paiement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/statut/{statut}

#### GET
##### Summary:

Paiements Par Statut

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| statut | path |  | Yes | [StatutPaiement-Input](#statutpaiement-input) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /paiements/{paiement_id}/rembourser

#### PUT
##### Summary:

Rembourser Paiement

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| paiement_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /notifications/

#### GET
##### Summary:

Lire Notifications

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| user_id | query |  | Yes | string (uuid) |
| user_type | query |  | Yes | string |
| non_lues | query |  | No | boolean |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

#### POST
##### Summary:

Ajouter Notification

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

### /notifications/{notif_id}/lue

#### PATCH
##### Summary:

Marquer Notification Comme Lue

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| notif_id | path |  | Yes | string (uuid) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### Models


#### AbonnementRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| marchand_id | string (uuid) |  | Yes |
| montant | number |  | Yes |
| date_debut | dateTime |  | Yes |
| date_expiration | dateTime |  | Yes |
| statut | [StatutAbonnement](#statutabonnement) |  | Yes |

#### AbonnementUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| montant |  |  | No |
| statut |  |  | No |
| date_expiration |  |  | No |

#### AdresseCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| pays | string |  | Yes |
| ville | string |  | Yes |
| position_point_wkt | string |  | Yes |
| zone_polygone_wkt |  |  | No |
| utilisateur_id |  |  | No |
| marchand_id |  |  | No |
| livreur_id |  |  | No |
| client_id |  |  | No |

#### AdresseRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| pays | string |  | Yes |
| ville | string |  | Yes |
| position_point_wkt | string |  | Yes |
| zone_polygone_wkt |  |  | No |
| utilisateur_id |  |  | Yes |
| marchand_id |  |  | Yes |
| livreur_id |  |  | Yes |
| client_id |  |  | Yes |

#### AvisCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| livreur_id | string (uuid) |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| client_id | string (uuid) |  | Yes |
| commentaire |  |  | No |
| note | integer | Note sur 5 | Yes |

#### AvisRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| livreur_id | string (uuid) |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| client_id | string (uuid) |  | Yes |
| commentaire |  |  | Yes |
| note | integer |  | Yes |
| date_avis | dateTime |  | Yes |

#### ChangementStatutCommande

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nouveau_statut | [StatutCommande](#statutcommande) |  | Yes |

#### CleAPICreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom |  |  | No |
| utilisateur_id | string (uuid) |  | Yes |

#### CleAPIResponse

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| nom |  |  | Yes |
| cle | string |  | Yes |
| utilisateur_id | string (uuid) |  | Yes |
| est_active | boolean |  | Yes |
| date_creation | dateTime |  | Yes |

#### ClientCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| adresse | string |  | Yes |
| contact | string |  | Yes |

#### ClientOut

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| adresse | string |  | Yes |
| contact | string |  | Yes |
| id | string (uuid) |  | Yes |
| date_creation | dateTime |  | Yes |

#### ClientUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom |  |  | No |
| adresse |  |  | No |
| contact |  |  | No |

#### CommandeCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| marchand_id | string (uuid) |  | Yes |
| client_id | string (uuid) |  | Yes |
| details | object |  | Yes |

#### CommandeRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| reference | string |  | Yes |
| statut | [StatutCommande](#statutcommande) |  | Yes |
| total | number |  | Yes |
| articles | object |  | Yes |
| created_at | dateTime |  | Yes |
| marchand_id |  |  | Yes |
| client_id |  |  | Yes |

#### CommandeUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| details |  |  | No |

#### HTTPValidationError

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| detail | [ [ValidationError](#validationerror) ] |  | No |

#### LivraisonCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| commande_id | string (uuid) |  | Yes |
| livreur_id |  |  | No |
| statut | [StatutLivraison](#statutlivraison) |  | No |

#### LivraisonStatutUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nouveau_statut | [StatutLivraison](#statutlivraison) |  | Yes |

#### LivreurCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| vehicule | [TypeVehicule](#typevehicule) |  | Yes |
| contact | string |  | Yes |
| immatriculation | string |  | Yes |
| statut | [StatutLivreur](#statutlivreur) |  | No |

#### LivreurRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| vehicule | [TypeVehicule](#typevehicule) |  | Yes |
| contact | string |  | Yes |
| immatriculation | string |  | Yes |
| statut | [StatutLivreur](#statutlivreur) |  | No |
| id | string (uuid) |  | Yes |
| date_creation | dateTime |  | Yes |

#### LivreurUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| vehicule | [TypeVehicule](#typevehicule) |  | Yes |
| contact | string |  | Yes |
| immatriculation | string |  | Yes |

#### LoginRequest

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string (email) |  | Yes |
| mot_de_passe | string |  | Yes |

#### LoginResponse

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| access_token | string |  | Yes |
| token_type | string |  | Yes |

#### MarchandCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| contact | string |  | Yes |
| adresse |  |  | No |
| utilisateur_id | string (uuid) |  | Yes |

#### MarchandOut

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| contact | string |  | Yes |
| adresse |  |  | No |
| id | string (uuid) |  | Yes |
| date_creation | dateTime |  | Yes |

#### MethodePaiement

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| MethodePaiement | string |  |  |

#### NotificationCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| user_id | string (uuid) |  | Yes |
| user_type | string |  | Yes |
| titre | string |  | Yes |
| message | string |  | Yes |
| type | [TypeNotification](#typenotification) |  | No |

#### NotificationRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| user_id | string (uuid) |  | Yes |
| user_type | string |  | Yes |
| titre | string |  | Yes |
| message | string |  | Yes |
| type | [TypeNotification](#typenotification) |  | No |
| id | string (uuid) |  | Yes |
| lu | boolean |  | Yes |
| date_envoi | dateTime |  | Yes |

#### PaiementCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| montant | number |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| client_id | string (uuid) |  | Yes |
| methode_paiement | [MethodePaiement](#methodepaiement) |  | Yes |

#### PaiementRead

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| client_id | string (uuid) |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| montant | number |  | Yes |
| methode_paiement | [MethodePaiement](#methodepaiement) |  | Yes |
| statut_paiement | [StatutPaiement-Output](#statutpaiement-output) |  | Yes |
| recu_par | [RecuPar](#recupar) |  | Yes |
| date_paiement | dateTime |  | Yes |

#### PositionCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| livreur_id | string (uuid) |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| latitude | number |  | Yes |
| longitude | number |  | Yes |

#### PositionOut

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string (uuid) |  | Yes |
| livreur_id | string (uuid) |  | Yes |
| livraison_id | string (uuid) |  | Yes |
| latitude | number |  | Yes |
| longitude | number |  | Yes |
| timestamp | dateTime |  | Yes |

#### PositionUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| latitude | number |  | Yes |
| longitude | number |  | Yes |

#### ProblemeSignalement

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| description | string |  | Yes |

#### RecuPar

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| RecuPar | string |  |  |

#### RegisterRequest

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nom | string |  | Yes |
| email | string (email) |  | Yes |
| mot_de_passe | string |  | Yes |
| role | string |  | Yes |
| is_active | boolean |  | No |

#### RegisterResponse

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | string |  | Yes |
| nom | string |  | Yes |
| email | string (email) |  | Yes |

#### StatistiquesAPIResponse

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| total_cles | integer |  | Yes |
| cles_actives | integer |  | Yes |
| cles_revoquees | integer |  | Yes |

#### StatutAbonnement

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutAbonnement | string |  |  |

#### StatutCommande

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutCommande | string |  |  |

#### StatutLivraison

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutLivraison | string |  |  |

#### StatutLivreur

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutLivreur | string |  |  |

#### StatutLivreurUpdate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nouveau_statut | [StatutLivreur](#statutlivreur) |  | Yes |

#### StatutPaiement-Input

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutPaiement-Input | string |  |  |

#### StatutPaiement-Output

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| StatutPaiement-Output | string |  |  |

#### TypeNotification

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| TypeNotification | string |  |  |

#### TypeVehicule

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| TypeVehicule | string |  |  |

#### ValidationError

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| loc | [  ] |  | Yes |
| msg | string |  | Yes |
| type | string |  | Yes |