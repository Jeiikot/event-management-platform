import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import { loadConfig } from '../utils/config'
import { Loading } from './bits'

export default function EventForm({ pushToast }) {
  const nav = useNavigate()
  const { id } = useParams()
  const isEdit = !!id
  const config = loadConfig()
  const [loading, setLoading] = useState(!!id)
  const [saving, setSaving] = useState(false)
  // capacidad mínima 1 (backend ge=1)
  const [ev, setEv] = useState({ name:'', description:'', startDate:'', endDate:'', location:'', capacity:1, status:'DRAFT' })

  useEffect(()=>{
    (async()=>{
      if (!id) return
      try {
        const data = await apiFetch(config.endpoints.event(id))
        setEv({
          name: data.name || '',
          description: data.description || '',
          startDate: data.start_at ? data.start_at.slice(0,16) : '',
          endDate: data.end_at ? data.end_at.slice(0,16) : '',
          location: data.venue || '',
          capacity: data.capacity_total ?? data.capacity_available ?? 1,
          status: data.status || 'DRAFT',
        })
      } catch (e) {
        pushToast && pushToast('Error cargando evento: ' + e.message, 'error')
      } finally { setLoading(false) }
    })()
  }, [id, config, pushToast])

  const valid = useMemo(()=>{
    if (!ev.name?.trim()) return false
    if (!ev.startDate || !ev.endDate) return false
    const start = new Date(ev.startDate)
    const end = new Date(ev.endDate)
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return false
    if (end <= start) return false
    if (!Number.isFinite(Number(ev.capacity)) || Number(ev.capacity) < 1) return false
    return true
  }, [ev])

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!valid) return
    setSaving(true)
    try {
      const start = new Date(ev.startDate)
      const end = new Date(ev.endDate)
      const capacityTotal = Math.max(1, Number(ev.capacity) || 1)

      const payload = {
        name: ev.name.trim(),
        description: ev.description?.trim() || null,
        status: ev.status, // DRAFT | PUBLISHED | CANCELLED | FINISHED
        venue: ev.location?.trim() || null,
        start_at: start.toISOString(),
        end_at: end.toISOString(),
        capacity_total: capacityTotal,
        capacity_available: capacityTotal,
      }
      if (isEdit) {
        await apiFetch(config.endpoints.event(id), { method:'PATCH', auth:true, body: payload })
        pushToast && pushToast('Evento actualizado', 'success')
        nav('/events/' + id)
      } else {
        const created = await apiFetch(config.endpoints.events, { method:'POST', auth:true, body: payload })
        pushToast && pushToast('Evento creado', 'success')
        const newId = created?.id
        nav(newId ? '/events/' + newId : '/')
      }
    } catch (e) {
      pushToast && pushToast('Error guardando: ' + e.message, 'error')
    } finally { setSaving(false) }
  }

  if (loading) return <Loading/>

  const endBeforeStart = ev.startDate && ev.endDate && new Date(ev.endDate) <= new Date(ev.startDate)

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <h1 className="text-xl font-semibold mb-2">{isEdit ? 'Editar' : 'Crear'} evento</h1>

      {/* PREVIEW estilo EventDetail */}
      <div className="bg-white border rounded-xl p-4 mb-5 text-slate-700">
        {ev.name ? <div className="text-lg font-medium">{ev.name}</div> : <div className="text-slate-400">Nombre del evento…</div>}
        {ev.description && <p className="mt-1">{ev.description}</p>}
        <div className="mt-2 flex items-center flex-wrap gap-3 text-slate-600 text-sm">
          {ev.startDate && <div>📅 {new Date(ev.startDate).toLocaleString()}</div>}
          {ev.endDate &&   <div>🕙 {new Date(ev.endDate).toLocaleString()}</div>}
          {ev.location &&  <div>📍 {ev.location}</div>}
          {ev.capacity &&  <div>👥 Capacidad: {ev.capacity}</div>}
        </div>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="text-sm text-slate-600">Nombre *</label>
          <input required className="border rounded-lg px-3 py-2 w-full"
                 value={ev.name} onChange={e=>setEv(s=>({...s, name:e.target.value}))}/>
        </div>

        <div>
          <label className="text-sm text-slate-600">Descripción</label>
          <textarea className="border rounded-lg px-3 py-2 w-full"
                    value={ev.description} onChange={e=>setEv(s=>({...s, description:e.target.value}))}/>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm text-slate-600">📅 Fecha y hora (inicio) *</label>
            <input required type="datetime-local" className="border rounded-lg px-3 py-2 w-full"
                   value={ev.startDate} onChange={e=>setEv(s=>({...s, startDate:e.target.value}))}/>
          </div>
          <div>
            <label className="text-sm text-slate-600">🕙 Fecha y hora (fin) *</label>
            <input required type="datetime-local" className="border rounded-lg px-3 py-2 w-full"
                   value={ev.endDate} onChange={e=>setEv(s=>({...s, endDate:e.target.value}))}/>
            {endBeforeStart && <div className="text-xs text-red-600 mt-1">La fecha de fin debe ser posterior a la de inicio.</div>}
          </div>
        </div>

        <div>
          <label className="text-sm text-slate-600">📍 Lugar</label>
          <input className="border rounded-lg px-3 py-2 w-full"
                 value={ev.location} onChange={e=>setEv(s=>({...s, location:e.target.value}))}/>
        </div>

        <div>
          <label className="text-sm text-slate-600">👥 Capacidad total *</label>
          <input required type="number" min="1" step="1" className="border rounded-lg px-3 py-2 w-full"
                 value={ev.capacity} onChange={e=>setEv(s=>({...s, capacity:e.target.value}))}/>
          {Number(ev.capacity) < 1 && <div className="text-xs text-red-600 mt-1">La capacidad debe ser mínimo 1.</div>}
        </div>

        <div>
          <label className="text-sm text-slate-600">Estado</label>
          <select className="border rounded-lg px-3 py-2 w-full"
                  value={ev.status} onChange={e=>setEv(s=>({...s, status:e.target.value}))}>
            <option value="DRAFT">Borrador</option>
            <option value="PUBLISHED">Publicado</option>
            <option value="CANCELLED">Cancelado</option>
            <option value="FINISHED">Finalizado</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <button disabled={saving || !valid}
                  className="px-4 py-2 rounded-lg border bg-black text-white disabled:opacity-50">
            {saving ? 'Guardando...' : 'Guardar'}
          </button>
          {!valid && <span className="text-xs text-slate-500">Completa los campos obligatorios.</span>}
        </div>
      </form>
    </div>
  )
}
