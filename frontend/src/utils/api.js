import { loadConfig } from './config'

export function getToken() {
  return localStorage.getItem('mis_eventos_token') || ''
}
export function setToken(t) {
  localStorage.setItem('mis_eventos_token', t || '')
}
export function clearToken() {
  localStorage.removeItem('mis_eventos_token')
}

export function apiUrl(path) {
  const cfg = loadConfig()
  const base = (cfg.BASE_URL || '').replace(/\/+$/, '')
  const p = (path || '').replace(/^\/+/, '')
  return `${base}/${p}`
}

export async function apiFetch(path, { method='GET', auth=false, headers={}, body } = {}) {
  const h = { 'Content-Type': 'application/json', ...headers }
  if (auth) {
    const token = getToken()
    if (token) h['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(apiUrl(path), {
    method, headers: h,
    body: body ? JSON.stringify(body) : undefined
  })
  if (!res.ok) {
    let msg = `HTTP ${res.status}`
    try { const j = await res.json(); msg = j.detail || JSON.stringify(j) } catch {}
    const err = new Error(msg); err.status = res.status; throw err
  }
  const text = await res.text()
  try { return text ? JSON.parse(text) : null } catch { return text }
}
