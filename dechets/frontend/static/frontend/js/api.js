/* ============================================================
   api.js — Petit client JS pour consommer l'API DRF avec JWT
   ============================================================ */

const API_BASE = '/api';

const TokenStore = {
  getAccess() { return localStorage.getItem('access_token'); },
  getRefresh() { return localStorage.getItem('refresh_token'); },
  set(access, refresh) {
    localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
  },
  clear() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
  },
  isLoggedIn() { return !!this.getAccess(); },
};

/**
 * Redirige vers la page de connexion si l'utilisateur n'est pas authentifié.
 * À appeler en haut de chaque page protégée.
 */
function requireAuth() {
  if (!TokenStore.isLoggedIn()) {
    window.location.href = '/app/login/';
  }
}

/**
 * Tente de rafraîchir le token d'accès via le refresh token.
 * Retourne true si succès, false sinon.
 */
async function tryRefreshToken() {
  const refresh = TokenStore.getRefresh();
  if (!refresh) return false;
  try {
    const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    TokenStore.set(data.access, null);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Wrapper fetch() qui ajoute automatiquement le header Authorization,
 * et tente un refresh silencieux si le token a expiré (401).
 *
 * @param {string} path - chemin relatif à API_BASE, ex: '/signalements/'
 * @param {object} options - options fetch standard (method, body, headers...)
 * @param {boolean} isFormData - true si body est un FormData (ne pas fixer Content-Type)
 */
async function apiFetch(path, options = {}, isFormData = false) {
  const doFetch = () => {
    const headers = Object.assign({}, options.headers);
    const token = TokenStore.getAccess();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (!isFormData && options.body && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }
    return fetch(`${API_BASE}${path}`, Object.assign({}, options, { headers }));
  };

  let res = await doFetch();

  if (res.status === 401) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      res = await doFetch();
    } else {
      TokenStore.clear();
      window.location.href = '/app/login/';
      return Promise.reject(new Error('Session expirée'));
    }
  }

  return res;
}

/**
 * Récupère TOUTES les pages d'un endpoint paginé DRF et retourne
 * la liste complète des résultats (utile pour remplir des <select>, la carte, etc.)
 */
async function apiFetchAll(path) {
  let results = [];
  let url = path;
  while (url) {
    const res = await apiFetch(url.startsWith('http') ? url.replace(API_BASE, '') : url);
    if (!res.ok) break;
    const data = await res.json();
    if (Array.isArray(data)) {
      results = results.concat(data);
      url = null;
    } else {
      results = results.concat(data.results || []);
      url = data.next ? data.next.replace(window.location.origin + API_BASE, '') : null;
    }
  }
  return results;
}

async function logout() {
  TokenStore.clear();
  window.location.href = '/app/login/';
}

/* Petite fonction utilitaire d'affichage de messages d'erreur/succès */
function showAlert(containerId, message, type = 'danger') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>`;
}
