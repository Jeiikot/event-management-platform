const API = '/api/v1';

export const endpoints = {
  register: `${API}/auth/register`,
  login:    `${API}/auth/login`,
  me:       `${API}/users/me`,
  events:   `${API}/events`,
  event:           (id) => `${API}/events/${id}`,
  eventRegister:   (id) => `${API}/events/${id}/register`,
  myRegistrations: `${API}/users/me/registrations`,
  sessions:  (eventId) => `${API}/events/${eventId}/sessions`,
};
