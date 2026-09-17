/* GELASETECH loader: include Supabase only when configured. */
(function () {
  const s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
  s.onload = function () {
    const bridge = document.createElement('script');
    bridge.src = './supabase-client.js';
    document.head.appendChild(bridge);
  };
  s.onerror = function () {
    window.GELASETECH_DB = { enabled: false, reason: 'Bibliothèque Supabase indisponible' };
  };
  document.head.appendChild(s);
})();
