# Houmba H — Backend

Base backend prévue pour Houmba H. Cette version documente le contrat de service et prépare l’API, la base de données, l’authentification, les publications, la modération et l’intégration de Houmba H 1.

## Contrat initial

- `GET /health` — état du service
- `GET /api/publications` — catalogue public
- `POST /api/publications` — création authentifiée à implémenter avec stockage persistant
- `POST /api/ai/chat` — point d’intégration Houmba H 1

Les secrets, clés IA et paramètres de production doivent être fournis par variables d’environnement, jamais commités.
