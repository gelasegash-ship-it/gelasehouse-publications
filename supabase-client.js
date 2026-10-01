/* GELASETECH — Supabase client + Houmba H 1 validation flow */
(function () {
  'use strict';

// Publications vedettes affichees quand le service distant est injoignable (ex: projet Supabase en pause).
window.GELASETECH_FEATURED = [
  { id: 'featured-1', title: 'ALPHA TECH : LA GENÈSE — le premier film IA congolais', description: 'Une conscience artificielle nommée GENESIS naît à Brazzaville 2088. Deux chapitres de 3 et 5 minutes déjà publiés, un nouvel épisode chaque samedi automatiquement. Regardez sur Instagram @gelasehouse.', category: 'Création', moderation_status: 'featured', created_at: '2026-09-05' },
  { id: 'featured-2', title: '5 services IA qui rapportent dès maintenant au Congo', description: 'Chatbot IA pour PME (75K FCFA/mois), community management (150K/mois), création de sites (250K), formation IA bootcamp (50K/session), audit cybersécurité (200K). Contact Gelasehouse : +242 05 334 37 19.', category: 'Économie', moderation_status: 'featured', created_at: '2026-10-01' },
  { id: 'featured-3', title: 'Le manifeste de l innovation congolaise', description: 'Nous ne consommons pas la technologie : nous la redéfinissons. GELASETECH réunit création, IA, communauté et publication pour faire de Brazzaville un centre technologique mondial.', category: 'Philosophie', moderation_status: 'featured', created_at: '2026-10-01' }
];

  const cfg = window.GELASETECH_SUPABASE;
  if (!cfg || !cfg.url || !cfg.publishableKey || !window.supabase) {
    window.GELASETECH_DB = { enabled: false, reason: 'Supabase non configuré' };
    return;
  }
  const client = window.supabase.createClient(cfg.url, cfg.publishableKey);
  window.GELASETECH_DB = {
    enabled: true,
    client,
    async getSession() {
      const { data, error } = await client.auth.getSession();
      if (error) throw error;
      return data.session;
    },
    async signUp(email, password, displayName) {
      const { data, error } = await client.auth.signUp({ email, password, options: { data: { display_name: displayName || '' } } });
      if (error) throw error;
      return data;
    },
    async signIn(email, password) {
      const { data, error } = await client.auth.signInWithPassword({ email, password });
      if (error) throw error;
      return data;
    },
    async signOut() {
      const { error } = await client.auth.signOut();
      if (error) throw error;
    },
    async listPublications() {
      try {
        const { data, error } = await client.from('publications').select('*').order('created_at', { ascending: false });
        if (error) throw error;
        return data || [];
      } catch (e) {
        // Supabase injoignable (projet en pause ou reseau): publications vedettes integrees
        window.GELASETECH_DB.offline = true;
        return window.GELASETECH_FEATURED || [];
      }
    },
    async createPublication(payload) {
      const session = await this.getSession();
      if (!session) throw new Error('Connexion requise');
      const row = {
        title: payload.title || 'Publication sans titre',
        description: payload.description || '',
        category: payload.category || 'Général',
        author_id: session.user.id,
        moderation_status: 'pending'
      };
      const { data, error } = await client.from('publications').insert(row).select().single();
      if (error) throw error;
      return data;
    },
    async requestHoumbaValidation(publicationId, snapshot) {
      const session = await this.getSession();
      if (!session) throw new Error('Connexion requise pour demander la validation Houmba H 1');
      const { data, error } = await client.from('validation_requests').insert({
        publication_id: publicationId,
        requester_id: session.user.id,
        engine: 'houmba_h1',
        status: 'pending',
        input_snapshot: snapshot || {}
      }).select().single();
      if (error) throw error;
      return data;
    },
    async getValidationRequests() {
      const session = await this.getSession();
      if (!session) return [];
      const { data, error } = await client.from('validation_requests')
        .select('*').eq('requester_id', session.user.id).order('created_at', { ascending: false });
      if (error) throw error;
      return data || [];
    },
    async watchValidationRequests(callback) {
      const session = await this.getSession();
      if (!session) return null;
      return client.channel('gelasetech-houmba-validation')
        .on('postgres_changes', { event: '*', schema: 'public', table: 'validation_requests', filter: 'requester_id=eq.' + session.user.id }, payload => callback(payload))
        .subscribe();
    }
  };
})();