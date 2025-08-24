const API_VERSION = '/api/v1'

const DEFAULT_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
  endpoints: {
    register: `${API_VERSION}/auth/register`,
    login: `${API_VERSION}/auth/login`,
    me: `${API_VERSION}/users/me`,
    events: `${API_VERSION}/events`,
    event: (eventId) => `${API_VERSION}/events/${eventId}`,
    eventRegister: (eventId) => `${API_VERSION}/registrations/events/${eventId}`,
    myRegistrations: `${API_VERSION}/registrations/events`,
    sessions: (eventId) => `${API_VERSION}/sessions/events/${eventId}`,
    session: (sessionId) => `${API_VERSION}/sessions/${sessionId}`,
    speakers: `${API_VERSION}/speakers/`,
    speaker: (speakerId) => `${API_VERSION}/speakers/${speakerId}`,
  },
  pageSize: 10,
}

export function loadConfig() {
  const raw = localStorage.getItem('mis_eventos_config')
  if (!raw) return DEFAULT_CONFIG
  try {
    const parsed = JSON.parse(raw)
    return {
      ...DEFAULT_CONFIG,
      ...parsed,
      endpoints: { ...DEFAULT_CONFIG.endpoints, ...(parsed.endpoints || {}) }
    }
  } catch {
    return DEFAULT_CONFIG
  }
}

export function saveConfig(cfg) {
  localStorage.setItem('mis_eventos_config', JSON.stringify(cfg))
}
