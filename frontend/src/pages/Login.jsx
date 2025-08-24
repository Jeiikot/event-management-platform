import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch, setToken } from '../utils/api'
import { loadConfig } from '../utils/config'

export default function Login({ setUser, pushToast }) {
  const nav = useNavigate()
  const config = loadConfig()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const data = await apiFetch(config.endpoints.login, { method:'POST', body: { email, password } })
      const token = data?.access_token || data?.token
      if (!token) throw new Error('Token no recibido')
      setToken(token); setUser({ email })
      pushToast('Bienvenido', 'success')
      nav('/')
    } catch (e) {
      pushToast('No se pudo iniciar sesión: ' + e.message, 'error')
    } finally { setLoading(false) }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold mb-4">Iniciar sesión</h1>
      <form onSubmit={onSubmit} className="bg-white border rounded-xl p-5 grid gap-3">
        <input type="email" className="border rounded-lg px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="border rounded-lg px-3 py-2" placeholder="Contraseña" value={password} onChange={e=>setPassword(e.target.value)} />
        <button disabled={loading} className="px-4 py-2 rounded-lg bg-slate-900 text-white disabled:opacity-50">{loading ? 'Entrando...' : 'Entrar'}</button>
    </form>
  </div>
  )
}
