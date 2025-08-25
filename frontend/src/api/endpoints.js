const API = '/api/v1';

export const endpoints = {
  register: `${API}/auth/register`,
  login:    `${API}/auth/login`,
  me:       `${API}/users/me`,

  events:   `${API}/events`,
  event:           (id) => `${API}/events/${id}`,

  eventRegister:   (id) => `${API}/registrations/events/${id}`,
  myRegistrations: `${API}/registrations/events`,

  sessions:        (eventId)  => `${API}/sessions/events/${eventId}`,
  session:         (sessionId) => `${API}/sessions/${sessionId}`,

  speakers:        `${API}/speakers/`,
  speaker:         (speakerId) => `${API}/speakers/${speakerId}`,
};
