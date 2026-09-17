# GELASETECH — Production Roadmap

## Delivered

- Responsive GELASETECH interface
- GitHub Pages deployment workflow
- PWA manifest and service worker
- Supabase security baseline and feed indexes
- Public Supabase configuration template

## Execution order

1. Configure browser publishable key through deployment secrets or generated config.
2. Add Supabase Auth and session handling.
3. Replace local feed storage with `public.publications`.
4. Add comments and likes with realtime subscriptions.
5. Add Storage buckets and upload policies.
6. Deploy OMEGA Edge Function with server-side provider secrets.
7. Add moderation queue and audit logs.
8. Integrate payment providers only through verified server webhooks.
9. Add automated tests, backups and monitoring.

## Security rules

- Never expose `service_role` keys.
- Never trust client-provided author IDs or payment statuses.
- Never mark a payment completed without provider verification.
- Require explicit confirmation for withdrawals and transfers.
