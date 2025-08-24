import { Link, useNavigate } from 'react-router-dom'
import { loadConfig, saveConfig } from '../utils/config'
import { clearToken } from '../utils/api'
import { useState } from 'react'

export default function Navbar({ user, setUser }) {
  const [cfg, setCfg] = useState(loadConfig())
  const [edit, setEdit] = useState(false)
  const [url, setUrl] = useState(cfg.BASE_URL)
  const nav = useNavigate()

  const onSave = () => {
    const newCfg = { ...cfg, BASE_URL: url }
    saveConfig(newCfg); setCfg(newCfg); setEdit(false)
  }

  const logout = () => {
    clearToken(); setUser(null); nav('/')
  }

  return (
    <header className="bg-white border-b sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
        <Link to="/" className="text-lg font-semibold">🎟️ Mis Eventos</Link>
        <nav className="ml-auto flex items-center gap-4">
          <Link to="/" className="text-slate-700 hover:text-slate-900">Eventos</Link>
          {user && <Link to="/profile" className="text-slate-700 hover:text-slate-900">Mi perfil</Link>}
          {user ? (
            <div className="flex items-center gap-2">
              <Link to="/events/new" className="px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-800">Crear evento</Link>
              <button onClick={logout} className="px-3 py-1.5 rounded-lg border hover:bg-slate-50">Salir</button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login" className="px-3 py-1.5 rounded-lg border hover:bg-slate-50">Entrar</Link>
              <Link to="/register" className="px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-800">Registrarme</Link>
            </div>
          )}
        </nav>
      </div>
      <div className="bg-slate-50 border-t">
        <div className="max-w-6xl mx-auto px-4 py-2 text-xs flex items-center gap-2">
          {!edit ? (
            <>
              <span className="text-slate-500">API:</span>
              <code className="bg-white border px-2 py-1 rounded">{cfg.BASE_URL}</code>
              <button onClick={() => setEdit(true)} className="ml-2 text-slate-600 hover:text-slate-900 underline">cambiar</button>
            </>
          ) : (
            <div className="flex items-center gap-2 w-full">
              <input className="border rounded px-2 py-1 text-sm w-full" value={url} onChange={(e)=>setUrl(e.target.value)} />
              <button onClick={onSave} className="px-2 py-1 rounded bg-emerald-600 text-white">Guardar</button>
              <button onClick={()=>setEdit(false)} className="px-2 py-1 rounded border">Cancelar</button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
