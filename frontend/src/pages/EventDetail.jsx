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
  const [sess, setSess] = useState({ title:'', speaker:'', start_time:'', end_time:'', capacity:'' })

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const ev = await apiFetch(config.endpoints.event(id))
      setEvent(ev)
    } catch (e) {
      pushToast('Error cargando evento: ' + e.message, 'error')
    } finally { setLoading(false) }

    try {
      const ss = await apiFetch(config.endpoints.sessions(id))
      setSessions(Array.isArray(ss) ? ss : (ss.items || ss.results || []))
    } catch {
      setSessions([])
    }
  }, [config, id, pushToast])

  useEffect(()=>{ loadData() }, [loadData])

  const doRegister = async () => {
    setRegLoading(true)
    try {
      await apiFetch(config.endpoints.eventRegister(id), { method:'POST', auth:true })
      pushToast('¡Registro exitoso!', 'success')
      loadData()
    } catch (e) {
      pushToast('No fue posible registrarte: ' + e.message, 'error')
    } finally { setRegLoading(false) }
  }

  const createSession = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        title: sess.title,
        speaker: sess.speaker,
        start_time: sess.start_time,
        end_time: sess.end_time,
        capacity: sess.capacity ? Number(sess.capacity) : undefined,
      }
      await apiFetch(config.endpoints.sessions(id), { method:'POST', auth:true, body: payload })
      pushToast('Sesión creada', 'success')
      setFormOpen(false)
      setSess({ title:'', speaker:'', start_time:'', end_time:'', capacity:'' })
      loadData()
    } catch (e) {
      pushToast('Error creando sesión: ' + e.message, 'error')
    }
  }

  if (loading) return <div className="max-w-4xl mx-auto px-4 py-6"><Loading/></div>
  if (!event) return <div className="max-w-4xl mx-auto px-4 py-6"><Empty>Evento no encontrado.</Empty></div>

  const remaining = (typeof event.capacity !== 'undefined' && typeof event.seats_taken !== 'undefined')
    ? Math.max(0, event.capacity - event.seats_taken) : undefined

  const loggedIn = !!getToken()

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      <div className="bg-white border rounded-xl p-5">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">{event.name || event.title}</h1>
          <span className={"text-xs px-2 py-0.5 rounded-full border " + (event.status==='ACTIVE' ? "bg-emerald-50 border-emerald-200 text-emerald-700" : "bg-slate-50 border-slate-200 text-slate-700")}>{event.status || "DRAFT"}</span>
        </div>
        <p className="text-slate-700 mt-2">{event.description || "Sin descripción"}</p>
        <div className="mt-3 flex flex-wrap items-center text-sm gap-3 text-slate-600">
          {event.date && <span>📅 {new Date(event.date).toLocaleString()}</span>}
          {(event.location || event.place) && <span>📍 {event.location || event.place}</span>}
          {(typeof event.capacity !== "undefined") && <span>👥 Capacidad: {event.capacity}</span>}
          {(typeof remaining !== "undefined") && <span>🎟️ Disponibles: {remaining}</span>}
        </div>

        {loggedIn && (
          <div className="mt-4">
            <button disabled={regLoading} onClick={doRegister} className="px-4 py-2 rounded-lg bg-slate-900 text-white disabled:opacity-50">
              {regLoading ? "Registrando..." : "Registrarme a este evento"}
            </button>
          </div>
        )}
      </div>

      <div className="bg-white border rounded-xl p-5">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Sesiones</h2>
          {loggedIn && (
            <button onClick={()=>setFormOpen(!formOpen)} className="px-3 py-1.5 rounded-lg border hover:bg-slate-50">
              {formOpen ? "Cancelar" : "Nueva sesión"}
            </button>
          )}
        </div>

        {formOpen && (
          <form onSubmit={createSession} className="grid md:grid-cols-5 gap-3 mt-4">
            <input required className="border rounded-lg px-3 py-2" placeholder="Título" value={sess.title} onChange={e=>setSess(s=>({...s, title:e.target.value}))}/>
            <input className="border rounded-lg px-3 py-2" placeholder="Ponente" value={sess.speaker} onChange={e=>setSess(s=>({...s, speaker:e.target.value}))}/>
            <input required type="datetime-local" className="border rounded-lg px-3 py-2" value={sess.start_time} onChange={e=>setSess(s=>({...s, start_time:e.target.value}))}/>
            <input required type="datetime-local" className="border rounded-lg px-3 py-2" value={sess.end_time} onChange={e=>setSess(s=>({...s, end_time:e.target.value}))}/>
            <input type="number" min="0" className="border rounded-lg px-3 py-2" placeholder="Capacidad" value={sess.capacity} onChange={e=>setSess(s=>({...s, capacity:e.target.value}))}/>
            <div className="md:col-span-5">
              <button className="px-4 py-2 rounded-lg bg-emerald-600 text-white">Crear sesión</button>
            </div>
          </form>
        )}

        <div className="mt-4 space-y-3">
          {sessions.length === 0 ? <Empty>No hay sesiones registradas.</Empty> : sessions.map((s, idx) => (
            <div key={s.id || idx} className="border rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">{s.title || s.name}</div>
                  <div className="text-sm text-slate-600">{s.speaker ? ("Ponente: " + s.speaker) : "Ponente por definir"}</div>
                </div>
                <div className="text-sm text-slate-600">
                  {s.start_time && <div>🕘 {new Date(s.start_time).toLocaleString()}</div>}
                  {s.end_time && <div>🕙 {new Date(s.end_time).toLocaleString()}</div>}
                  {(typeof s.capacity !== "undefined") && <div>👥 Capacidad: {s.capacity}</div>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="text-sm">
        <Link to={"/events/" + id + "/edit"} className="underline">Editar evento</Link>
      </div>
    </div>
  )
}
