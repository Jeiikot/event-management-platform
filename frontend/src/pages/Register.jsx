import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import { loadConfig } from '../utils/config'

export default function Register({ pushToast }) {
  const nav = useNavigate()
  const config = loadConfig()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await apiFetch(config.endpoints.register, { method:'POST', body: { email, password } })
      pushToast('Registro exitoso, ahora inicia sesión', 'success')
      nav('/login')
    } catch (e) {
      pushToast('No se pudo registrar: ' + e.message, 'error')
    } finally { setLoading(false) }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold mb-4">Crear cuenta</h1>
      <form onSubmit={onSubmit} className="bg-white border rounded-xl p-5 grid gap-3">
        <input type="email" className="border rounded-lg px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="border rounded-lg px-3 py-2" placeholder="Contraseña" value={password} onChange={e=>setPassword(e.target.value)} />
        <button disabled={loading} className="px-4 py-2 rounded-lg bg-slate-900 text-white disabled:opacity-50">{loading ? 'Creando...' : 'Crear cuenta'}</button>
      </form>
    </div>
  )
}
