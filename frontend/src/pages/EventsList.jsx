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
  const pageSize = config.pageSize || 10

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      params.set('page', page)
      params.set('size', pageSize) // backend expects 'size'
      if (q) params.set('search', q)
      const data = await apiFetch(`${config.endpoints.events}?${params.toString()}`)
      if (Array.isArray(data)) {
        setItems(data); setTotal(data.length)
      } else {
        setItems(data.items || []); setTotal(data.total || 0)
      }
    } catch (e) {
      console.error(e)
    } finally { setLoading(false) }
  }, [config, page, pageSize, q])

  useEffect(()=>{ fetchData() }, [fetchData])

  const totalPages = Math.max(1, Math.ceil((total||0)/(pageSize||1)))

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="flex items-center gap-3 mb-4">
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Buscar eventos..."
               className="border rounded-lg px-3 py-2 w-full" />
        <button onClick={()=>setPage(1)} className="px-3 py-2 rounded-lg border">Buscar</button>
      </div>

      {loading ? <Loading/> : (
        items.length === 0 ? <Empty>No hay eventos.</Empty> : (
          <div className="grid md:grid-cols-2 gap-4">
            {items.map(ev => (
              <div key={ev.id} className="border rounded-xl p-4 bg-white">
                <div className="font-semibold text-lg">{ev.name}</div>
                <p className="text-sm text-slate-600 line-clamp-3">{ev.description || "Sin descripción"}</p>
                <div className="mt-3 flex items-center text-sm gap-3 text-slate-600">
                  {ev.start_at && <span>📅 {new Date(ev.start_at).toLocaleString()}</span>}
                  {(ev.venue || ev.location || ev.place) && <span>📍 {ev.venue || ev.location || ev.place}</span>}
                  {(typeof ev.capacity_available !== "undefined") && <span>👥 {ev.capacity_available} cupos</span>}
                </div>
                <div className="mt-4">
                  <Link to={"/events/" + (ev.id)} className="px-3 py-1.5 rounded-lg border hover:bg-slate-50">Ver detalle</Link>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      <div className="mt-6 flex items-center justify-center gap-2">
        <button disabled={page<=1} onClick={()=>setPage(p=>Math.max(1, p-1))}
                className="px-3 py-1.5 rounded-lg border disabled:opacity-50">Anterior</button>
        <span className="text-sm text-slate-600">Página {page} de {totalPages}</span>
        <button disabled={page>=totalPages} onClick={()=>setPage(p=>Math.min(totalPages, p+1))}
                className="px-3 py-1.5 rounded-lg border disabled:opacity-50">Siguiente</button>
      </div>
    </div>
  )
}