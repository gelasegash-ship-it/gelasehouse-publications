/* GELASETECH — Supabase client + Houmba H 1 validation flow */
(function () {
  'use strict';
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
      const { data, error } = await client.from('publications').select('*').order('created_at', { ascending: false });
      if (error) throw error;
      return data || [];
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