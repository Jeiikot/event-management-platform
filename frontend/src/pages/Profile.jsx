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
        await apiFetch(config.endpoints.me, { auth:true }) // si no existe, ignoramos error
      } catch {}
      try {
        const r = await apiFetch(config.endpoints.myRegistrations, { auth:true })
        const arr = Array.isArray(r) ? r : (r.items || r.results || [])
        setRegs(arr)
      } catch (e) {
        pushToast('Error cargando perfil: ' + e.message, 'error')
      } finally { setLoading(false) }
    })()
  }, [config, pushToast])

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold mb-4">Mi perfil</h1>
      {loading ? <Loading/> : (
        <div className="space-y-4">
          <div className="bg-white border rounded-xl p-4">
            <div className="text-sm text-slate-600">Sesiones y eventos a los que estoy inscrito:</div>
            {regs.length === 0 ? <Empty>No tienes registros aún.</Empty> : (
              <div className="grid md:grid-cols-2 gap-3 mt-3">
                {regs.map((ev, idx)=>(
                  <div key={ev.id || idx} className="border rounded-lg p-3 bg-slate-50">
                    <div className="font-medium">{ev.name || ev.title || ev.event_name || 'Evento'}</div>
                    {ev.date && <div className="text-sm text-slate-600">📅 {new Date(ev.date).toLocaleString()}</div>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
