import { useEffect, useState, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import { loadConfig } from '../utils/config'
import { Loading, Empty } from './bits'
import { getToken } from '../utils/api'

export default function EventDetail({ pushToast }) {
  const { id } = useParams()
  const config = loadConfig()
  const [loading, setLoading] = useState(true)
  const [event, setEvent] = useState(null)
  const [sessions, setSessions] = useState([])
  const [regLoading, setRegLoading] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [sess, setSess] = useState({ title:'', description:'', start_time:'', end_time:'', room:'', capacity:'1', speaker:'' })

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const ev = await apiFetch(config.endpoints.event(id))
      setEvent(ev)
    } catch (e) {
      pushToast && pushToast('Error cargando evento: ' + e.message, 'error')
    } finally { setLoading(false) }

    try {
      const ss = await apiFetch(config.endpoints.sessions(id))
      const arr = Array.isArray(ss) ? ss : (ss.items || ss.results || [])
      setSessions(arr)
    } catch (e) {
      pushToast && pushToast('Error cargando sesiones: ' + e.message, 'error')
    }
  }, [config, id, pushToast])

  useEffect(()=>{ loadData() }, [loadData])

  const handleRegister = async () => {
    try {
      setRegLoading(true)
      await apiFetch(config.endpoints.eventRegister(id), { method:'POST', auth:true })
      pushToast && pushToast('Inscripción realizada', 'success')
    } catch(e) {
      pushToast && pushToast('Error al inscribirte: ' + e.message, 'error')
    } finally { setRegLoading(false) }
  }

  const saveSession = async (e) => {
    e.preventDefault()
    try {
      const cap = Math.max(1, Number(sess.capacity) || 1)
      const payload = {
        title: sess.title,
        description: sess.description || null,
        start_at: sess.start_time ? new Date(sess.start_time).toISOString() : null,
        end_at: sess.end_time ? new Date(sess.end_time).toISOString() : null,
        room: sess.room || null,
        capacity_total: cap,
        capacity_available: cap,
        speaker_ids: (sess.speaker || '').split(',').map(s=>parseInt(s,10)).filter(n=>!Number.isNaN(n)),
      }
      await apiFetch(config.endpoints.sessions(id), { method:'POST', auth:true, body: payload })
      pushToast && pushToast('Sesión creada', 'success')
      setFormOpen(false)
      setSess({ title:'', description:'', start_time:'', end_time:'', room:'', capacity:'1', speaker:'' })
      loadData()
    } catch (e) {
      pushToast && pushToast('Error creando sesión: ' + e.message, 'error')
    }
  }

  if (loading) return <Loading/>
  if (!event) return <div className="max-w-4xl mx-auto px-4 py-6"><Empty>Evento no encontrado.</Empty></div>

  const remaining = typeof event.capacity_available !== 'undefined' ? event.capacity_available : undefined
  const loggedIn = !!getToken()

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      <div className="bg-white border rounded-xl p-5">
        <div className="text-2xl font-semibold">{event.name}</div>
        {event.description && <p className="text-slate-700 mt-1">{event.description}</p>}
        <div className="mt-2 flex items-center flex-wrap gap-3 text-slate-600">
          {event.start_at && <div>📅 {new Date(event.start_at).toLocaleString()}</div>}
          {event.end_at && <div>🕙 {new Date(event.end_at).toLocaleString()}</div>}
          {event.venue && <div>📍 {event.venue}</div>}
          {(typeof remaining !== 'undefined') && <div>👥 Cupos: {remaining}</div>}
        </div>

        <div className="mt-4 flex items-center gap-2">
          {loggedIn && <button disabled={regLoading} onClick={handleRegister} className="px-4 py-2 rounded-lg border">{regLoading ? 'Inscribiendo...' : 'Inscribirme'}</button>}
          <Link to={"/events/" + id + "/edit"} className="underline text-sm">Editar evento</Link>
        </div>
      </div>

      <div className="bg-white border rounded-xl p-5">
        <div className="flex items-center justify-between">
          <div className="font-semibold">Sesiones</div>
          <button className="px-3 py-1.5 rounded-lg border" onClick={()=>setFormOpen(v=>!v)}>{formOpen ? 'Cerrar' : 'Nueva sesión'}</button>
        </div>

        {formOpen && (
          <form onSubmit={saveSession} className="grid md:grid-cols-2 gap-4 mt-4">
            <div>
              <label htmlFor="sess-title" className="text-sm text-slate-600">Título *</label>
              <input id="sess-title" className="border rounded-lg px-3 py-2 w-full" placeholder="Título"
                     value={sess.title} onChange={e=>setSess(s=>({...s, title:e.target.value}))} required/>
            </div>

            <div>
              <label htmlFor="sess-room" className="text-sm text-slate-600">Sala (opcional)</label>
              <input id="sess-room" className="border rounded-lg px-3 py-2 w-full" placeholder="Sala"
                     value={sess.room} onChange={e=>setSess(s=>({...s, room:e.target.value}))}/>
            </div>

            <div>
              <label htmlFor="sess-start" className="text-sm text-slate-600">📅 Fecha y hora (inicio) *</label>
              <input id="sess-start" className="border rounded-lg px-3 py-2 w-full" type="datetime-local"
                     value={sess.start_time} onChange={e=>setSess(s=>({...s, start_time:e.target.value}))} required/>
            </div>

            <div>
              <label htmlFor="sess-end" className="text-sm text-slate-600">🕙 Fecha y hora (fin) *</label>
              <input id="sess-end" className="border rounded-lg px-3 py-2 w-full" type="datetime-local"
                     value={sess.end_time} onChange={e=>setSess(s=>({...s, end_time:e.target.value}))} required/>
            </div>

            <div>
              <label htmlFor="sess-cap" className="text-sm text-slate-600">👥 Capacidad *</label>
              <input id="sess-cap" className="border rounded-lg px-3 py-2 w-full" type="number" min="1"
                     value={sess.capacity} onChange={e=>setSess(s=>({...s, capacity:e.target.value}))} required/>
            </div>

            <div>
              <label htmlFor="sess-speakers" className="text-sm text-slate-600">IDs de speakers (ej: 1,2)</label>
              <input id="sess-speakers" className="border rounded-lg px-3 py-2 w-full" placeholder="1,2"
                     value={sess.speaker} onChange={e=>setSess(s=>({...s, speaker:e.target.value}))}/>
            </div>

            <div className="md:col-span-2">
              <label htmlFor="sess-desc" className="text-sm text-slate-600">Descripción (opcional)</label>
              <textarea id="sess-desc" className="border rounded-lg px-3 py-2 w-full" rows={3}
                        placeholder="Descripción"
                        value={sess.description} onChange={e=>setSess(s=>({...s, description:e.target.value}))}/>
            </div>

            <div className="md:col-span-2">
              <button className="px-4 py-2 rounded-lg border bg-black text-white">Guardar sesión</button>
            </div>
          </form>
        )}

        <div className="mt-4">
          {sessions.length === 0 ? <Empty>No hay sesiones.</Empty> : (
            <div className="space-y-3">
              {sessions.map(s => (
                <div key={s.id} className="border rounded-lg p-3">
                  <div className="font-medium">{s.title}</div>
                  <div className="text-sm text-slate-600 flex flex-wrap gap-3">
                    {s.start_at && <div>📅 {new Date(s.start_at).toLocaleString()}</div>}
                    {s.end_at && <div>🕙 {new Date(s.end_at).toLocaleString()}</div>}
                    {(typeof s.capacity_total !== "undefined") && <div>👥 Capacidad: {s.capacity_total}</div>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
