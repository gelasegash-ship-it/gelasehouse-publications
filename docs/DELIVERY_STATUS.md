# HOUMBA H — État de livraison

## Livré

- Interface web responsive HOUMBA H.
- Bibliothèque de publications avec recherche et catégories.
- Formulaire de publication avec sauvegarde locale de secours.
- Connexion de l’interface à l’API `/api/publications`.
- Espace assistant Houmba H 1 connecté à `/api/ai/chat`.
- Fondations backend FastAPI, configuration et sécurité.
- Dépendances de test et configuration environnement.

## À configurer avant production

- Une base PostgreSQL managée.
- Une clé secrète forte pour les jetons.
- Un fournisseur IA et sa clé côté serveur uniquement.
- Un stockage objet pour les fichiers et couvertures.
- Un domaine HTTPS et des variables d’environnement de production.
- Une politique de modération, sauvegarde et conservation des données.
- Une authentification complète côté interface et une gestion des rôles.

## Lancement local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Puis ouvrir `index.html` ou servir le dossier avec un serveur HTTP local.

## Important

Le dépôt contient une application fonctionnelle de démonstration et une base extensible. Il ne faut pas présenter les intégrations externes comme actives tant que leurs secrets et services ne sont pas configurés.

## État du 1er octobre 2026

- Supabase injoignable au niveau DNS mondial (projet en pause ou supprimé) — voir `docs/RESTAURATION-SUPABASE.md`.
- Résilience livrée (commit 5e6b25a) : le site affiche 3 publications vedettes intégrées quand la base est injoignable, au lieu d'attendre indéfiniment.
- Déploiement GitHub Pages automatisé par GitHub Actions (`.github/workflows/pages.yml`) : chaque push sur main déploie en production.
- Pipeline de validation backend actif (`validate.yml`) : compilation Python + tests + vérification HTML.
