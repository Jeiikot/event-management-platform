import { Routes, Route, Link } from 'react-router-dom'
import Navbar from './components/Navbar'
import Toasts, { useToasts } from './components/Toasts'
import EventsList from './pages/EventsList'
import EventDetail from './pages/EventDetail'
import EventForm from './pages/EventForm'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import { useState } from 'react'

export default function App() {
  const [user, setUser] = useState(null)
  const { toasts, push, dismiss } = useToasts()

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar user={user} setUser={setUser} />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<EventsList />} />
          <Route path="/events/new" element={<EventForm pushToast={push} />} />
          <Route path="/events/:id" element={<EventDetail pushToast={push} />} />
          <Route path="/events/:id/edit" element={<EventForm pushToast={push} />} />
          <Route path="/login" element={<Login setUser={setUser} pushToast={push} />} />
          <Route path="/register" element={<Register pushToast={push} />} />
          <Route path="/profile" element={<Profile pushToast={push} />} />
          <Route path="*" element={<div className="max-w-3xl mx-auto px-4 py-10">Ruta no encontrada.</div>} />
        </Routes>
      </main>
      <footer className="border-t bg-white">
        <div className="max-w-6xl mx-auto px-4 py-6 text-xs text-slate-500 flex items-center justify-between">
          <div>Vite + React + Tailwind • Ajusta la URL del backend en .env o en la cabecera (API → cambiar).</div>
          <Link to="/" className="underline">Inicio</Link>
        </div>
      </footer>
      <Toasts toasts={toasts} dismiss={dismiss} />
    </div>
  )
}
