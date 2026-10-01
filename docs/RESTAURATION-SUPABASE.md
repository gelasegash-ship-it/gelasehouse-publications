# RESTAURATION SUPABASE — Guide express (5 minutes)

**Symptôme (1er oct 2026) :** le sous-domaine `ryueclnqtzqcswebxwwl.supabase.co` ne répond plus au DNS mondial (NXDOMAIN). Le site affiche le mode vedettes (publications intégrées) au lieu d'attendre indéfiniment.

## Cas A — Le projet est EN PAUSE (le plus fréquent en plan gratuit)
1. Va sur **https://supabase.com/dashboard** et connecte-toi.
2. Ouvre le projet (s'il apparaît avec la mention *Paused*).
3. Clique **Restore project**. Attends 2-3 minutes.
4. Rien d'autre à faire : `supabase-config.js` contient déjà la bonne URL et la bonne clé. Le site se reconnecte tout seul dès que le DNS revient.

## Cas B — Le projet a été SUPPRIMÉ
1. Sur le dashboard, crée un **nouveau projet** (plan gratuit suffit).
2. Ouvre le **SQL Editor** et colle l'intégralité du fichier :
   `supabase/migrations/202609130001_houmba_h.sql` → **Run**.
3. Va dans **Settings → API** et copie :
   - Project URL (`https://xxxxx.supabase.co`)
   - Publishable key (`sb_publishable_...`)
4. Remplace ces deux valeurs dans `supabase-config.js` (à la racine du site) et pousse le changement (ou envoie-les à l'agent Gelasehouse qui le fait).

## Après restauration
- Les publications réelles, les comptes utilisateurs, les commentaires et les likes fonctionnent à nouveau.
- La validation Houmba H 1 (`validation_requests`) redevient opérationnelle.
- Le mode vedettes disparaît automatiquement (il ne s'affiche QUE quand Supabase est injoignable).
