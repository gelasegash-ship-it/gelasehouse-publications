/* GELASETECH — optional Supabase bridge
 * This file never contains secrets. Configure supabase-config.js locally or in deployment.
 */
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
      const { data, error } = await client.auth.signUp({
        email, password,
        options: { data: { display_name: displayName || '' } }
      });
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
      const { data, error } = await client
        .from('publications')
        .select('*')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data || [];
    },
    async createPublication(payload) {
      const { data: sessionData } = await client.auth.getSession();
      if (!sessionData.session) throw new Error('Connexion requise');
      const row = {
        title: payload.title || 'Publication sans titre',
        content: payload.content || '',
        author_id: sessionData.session.user.id
      };
      const { data, error } = await client.from('publications').insert(row).select().single();
      if (error) throw error;
      return data;
    }
  };
})();
