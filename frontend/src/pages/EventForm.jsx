import { useEffect, useState } from 'react'
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
  const [ev, setEv] = useState({ name:'', description:'', date:'', location:'', capacity:0, status:'DRAFT' })

  useEffect(()=>{
    (async()=>{
      if (!id) return
      try {
        const data = await apiFetch(config.endpoints.event(id))
        setEv({
          name: data.name || data.title || '',
          description: data.description || '',
          ate: data.start_at ? data.start_at.slice(0,16) : '',
          location: data.venue || '',
          capacity: typeof data.capacity_total !== 'undefined' ? data.capacity_total : 0,
          status: data.status || 'DRAFT',
        })
      } catch (e) {
        pushToast('Error cargando evento: ' + e.message, 'error')
      } finally { setLoading(false) }
    })()
  }, [id, config, pushToast])

  const onSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const payload = {
        name: ev.name.trim(),
        description: ev.description?.trim() || null,
        status: ev.status,
        venue: ev.location?.trim() || null,
        start_at: start ? start.toISOString() : null,
        end_at: end ? end.toISOString() : null,
        capacity_total: capacityTotal,
        capacity_available: capacityTotal,
      };
      if (isEdit) {
        await apiFetch(config.endpoints.event(id), { method:'PUT', auth:true, body: payload })
        pushToast('Evento actualizado', 'success')
        nav('/events/' + id)
      } else {
        const created = await apiFetch(config.endpoints.events, { method:'POST', auth:true, body: payload })
        pushToast('Evento creado', 'success')
        const newId = created?.id || created?._id || created?.uuid
        nav(newId ? '/events/' + newId : '/')
      }
    } catch (e) {
      pushToast('Error guardando: ' + e.message, 'error')
    } finally { setSaving(false) }
  }

  if (loading) return <div className="max-w-3xl mx-auto px-4 py-6"><Loading/></div>

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold mb-4">{isEdit ? 'Editar evento' : 'Crear evento'}</h1>
      <form onSubmit={onSubmit} className="bg-white border rounded-xl p-5 grid gap-4">
        <div>
          <label className="text-sm text-slate-600">Nombre</label>
          <input required className="border rounded-lg px-3 py-2 w-full" value={ev.name} onChange={e=>setEv(s=>({...s, name:e.target.value}))} />
        </div>
        <div>
          <label className="text-sm text-slate-600">Descripción</label>
          <textarea rows="4" className="border rounded-lg px-3 py-2 w-full" value={ev.description} onChange={e=>setEv(s=>({...s, description:e.target.value}))}></textarea>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="text-sm text-slate-600">Fecha y hora</label>
            <input type="datetime-local" className="border rounded-lg px-3 py-2 w-full" value={ev.date} onChange={e=>setEv(s=>({...s, date:e.target.value}))} />
          </div>
          <div>
            <label className="text-sm text-slate-600">Lugar</label>
            <input className="border rounded-lg px-3 py-2 w-full" value={ev.location} onChange={e=>setEv(s=>({...s, location:e.target.value}))} />
          </div>
          <div>
            <label className="text-sm text-slate-600">Capacidad</label>
            <input type="number" min="1" className="border rounded-lg px-3 py-2 w-full" value={ev.capacity} onChange={e=>setEv(s=>({...s, capacity:e.target.value}))} />
          </div>
        </div>
        <div>
          <label className="text-sm text-slate-600">Estado</label>
          <select className="border rounded-lg px-3 py-2 w-full" value={ev.status} onChange={e=>setEv(s=>({...s, status:e.target.value}))}>
            <option value="DRAFT">Borrador</option>
            <option value="ACTIVE">Activo</option>
            <option value="ARCHIVED">Archivado</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <button disabled={saving} className="px-4 py-2 rounded-lg bg-slate-900 text-white disabled:opacity-50">{saving ? 'Guardando...' : 'Guardar'}</button>
        </div>
      </form>
    </div>
  )
}
