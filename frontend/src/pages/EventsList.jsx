import { useEffect, useState, useCallback } from 'react'
import { apiFetch } from '../utils/api'
import { loadConfig } from '../utils/config'
import { Link } from 'react-router-dom'
import { Loading, Empty } from './bits'

export default function EventsList() {
  const config = loadConfig()
  const [q, setQ] = useState('')
  const [page, setPage] = useState(1)
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const pageSize = config.pageSize

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      params.set('page', page); params.set('page_size', pageSize)
      if (q) params.set('search', q)
      const data = await apiFetch(`${config.endpoints.events}?${params.toString()}`)
      if (Array.isArray(data)) {
        setItems(data.slice(0, pageSize)); setTotal(data.length)
      } else if (data && (data.items || data.results)) {
        setItems(data.items || data.results || []); setTotal(data.total || data.count || 0)
      } else { setItems([]); setTotal(0) }
    } finally { setLoading(false) }
  }, [config, page, pageSize, q])

  useEffect(()=>{ fetchData() }, [fetchData])
  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold mb-4">Eventos</h1>
      <div className="bg-white border rounded-xl p-4 mb-4 flex items-center gap-2">
        <input value={q} onChange={(e)=>setQ(e.target.value)} placeholder="Buscar por nombre..." className="border rounded-lg px-3 py-2 w-full" />
        <button onClick={()=>{ setPage(1); fetchData() }} className="px-4 py-2 rounded-lg bg-slate-900 text-white">Buscar</button>
      </div>

      {loading ? <Loading/> : (
        items.length === 0 ? <Empty>No hay eventos.</Empty> : (
          <div className="grid md:grid-cols-2 gap-4">
            {items.map(ev => (
              <div key={ev.id || ev._id || ev.uuid} className="bg-white border rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-semibold">{ev.name || ev.title}</h3>
                  <span className={"text-xs px-2 py-0.5 rounded-full border " + (ev.status==='ACTIVE' ? "bg-emerald-50 border-emerald-200 text-emerald-700" : "bg-slate-50 border-slate-200 text-slate-700")}>{ev.status || "DRAFT"}</span>
                </div>
                <p className="text-sm text-slate-600 line-clamp-3">{ev.description || "Sin descripción"}</p>
                <div className="mt-3 flex items-center text-sm gap-3 text-slate-600">
                  {ev.date && <span>📅 {new Date(ev.date).toLocaleString()}</span>}
                  {(ev.location || ev.place) && <span>📍 {ev.location || ev.place}</span>}
                  {(typeof ev.capacity !== "undefined") && <span>👥 {ev.capacity} cupos</span>}
                </div>
                <div className="mt-4">
                  <Link to={"/events/" + (ev.id || ev._id || ev.uuid)} className="px-3 py-1.5 rounded-lg border hover:bg-slate-50">Ver detalle</Link>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      <div className="mt-6 flex items-center justify-center gap-2">
        <button disabled={page<=1} onClick={()=>setPage(p=>Math.max(1,p-1))} className="px-3 py-1.5 rounded-lg border disabled:opacity-50">Anterior</button>
        <span className="text-sm text-slate-600">Página {page} de {totalPages}</span>
        <button disabled={page>=totalPages} onClick={()=>setPage(p=>p+1)} className="px-3 py-1.5 rounded-lg border disabled:opacity-50">Siguiente</button>
      </div>
    </div>
  )
}
