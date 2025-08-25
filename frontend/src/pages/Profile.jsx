import { useEffect, useState } from 'react'
import { apiFetch } from '../utils/api'
import { loadConfig } from '../utils/config'
import { Loading, Empty } from './bits'

export default function Profile({ pushToast }) {
  const config = loadConfig()
  const [loading, setLoading] = useState(true)
  const [regs, setRegs] = useState([])

  useEffect(()=>{
    (async()=>{
      setLoading(true)
      try {
        await apiFetch(config.endpoints.me, { auth:true }) // valida token
      } catch {}
      try {
        const r = await apiFetch(config.endpoints.myRegistrations, { auth:true })
        const arr = Array.isArray(r) ? r : (r.items || r.results || [])
        // expandir datos del evento
        const detailed = await Promise.all(arr.map(async reg => {
          const ev = await apiFetch(config.endpoints.event(reg.event_id), { auth:true })
          return { ...reg, name: ev.name, date: ev.start_at, venue: ev.venue }
        }))
        setRegs(detailed)
      } catch (e) {
        pushToast && pushToast('Error cargando perfil: ' + e.message, 'error')
      } finally { setLoading(false) }
    })()
  }, [config, pushToast])

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <h1 className="text-xl font-semibold mb-4">Mis inscripciones</h1>
      {loading ? <Loading/> : (
        <div className="bg-white border rounded-xl p-5">
          {regs.length === 0 ? <Empty>No tienes inscripciones.</Empty> : (
            <div className="grid md:grid-cols-2 gap-3 mt-3">
              {regs.map((ev, idx)=>(
                <div key={ev.id || idx} className="border rounded-lg p-3 bg-slate-50">
                  <div className="font-medium">{ev.name || 'Evento'}</div>
                  {ev.date && <div className="text-sm text-slate-600">📅 {new Date(ev.date).toLocaleString()}</div>}
                  {ev.venue && <div className="text-sm text-slate-600">📍 {ev.venue}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}