# HOUMBA H — checklist de mise en production

## Supabase

- Projet cible : `gelase-pro`
- Migration : `supabase/migrations/202609130001_houmba_h.sql`
- Tables : `profiles`, `publications`, `comments`, `likes`
- RLS activé sur toutes les tables
- Ne jamais exposer la clé `service_role`

## Vercel

Configurer les variables suivantes dans Production :

- `APP_NAME`
- `APP_ENV=production`
- `CORS_ORIGINS`
- `AI_PROVIDER=openai_compatible`
- `AI_BASE_URL=https://api.openai.com/v1`
- `AI_API_KEY`
- `AI_MODEL`
- `AI_TIMEOUT_SECONDS=45`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` (backend uniquement, si nécessaire)

## Vérification

- `GET /health` retourne `status=ok`
- inscription et connexion fonctionnent
- création de publication authentifiée
- lecture publique des publications
- commentaires et likes protégés par RLS
- appel IA refusé proprement si la clé est absente
