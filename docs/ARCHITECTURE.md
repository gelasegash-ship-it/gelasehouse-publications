# Architecture de Houmba H

## Identité

- **Produit :** Houmba H
- **IA intégrée :** Houmba H 1, aussi appelée Houmba Omega
- **Dépôt de livraison :** gelasehouse-publications
- **Gelasehouse Publications :** base historique de publication, pas le nom du produit final.

## Couches

1. Interface web responsive (`index.html`, puis migration possible vers React/Next.js).
2. API (`backend/app/main.py`, FastAPI).
3. Persistance : SQLite en développement, PostgreSQL en production.
4. Authentification : comptes, sessions/JWT, récupération de compte et rôles.
5. Domaine social : profils, publications, commentaires, réactions, abonnements, communautés et messagerie.
6. Médias : stockage objet privé/public avec contrôle de type, taille et antivirus.
7. Modération : signalements, journal d’audit, rôles modérateur et administrateur.
8. IA Houmba H 1 : orchestration des conversations, recherche, outils, mémoire contrôlée, limites d’usage et journalisation minimisée.
9. Déploiement : frontend statique/CDN, API séparée, base managée et secrets dans le gestionnaire de l’hébergeur.

## Règles de sécurité

- Aucun secret dans Git.
- Validation serveur de toutes les entrées.
- Limitation de débit sur authentification, publication et IA.
- CORS explicite en production.
- Mots de passe hachés avec un algorithme moderne.
- Permissions vérifiées côté serveur.
- Suppression et export des données prévus dès la conception.
