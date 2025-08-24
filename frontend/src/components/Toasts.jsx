import { useState } from 'react'

export function useToasts() {
  const [toasts, setToasts] = useState([])
  const push = (message, type='info', timeout=3000) => {
    const id = Math.random().toString(36).slice(2)
    setToasts(t => [...t, { id, message, type }])
    if (timeout > 0) setTimeout(() => dismiss(id), timeout)
  }
  const dismiss = (id) => setToasts(t => t.filter(x => x.id !== id))
  return { toasts, push, dismiss }
}

export default function Toasts({ toasts, dismiss }) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {toasts.map(t => (
        <div key={t.id} className={"px-4 py-3 rounded-xl shadow-lg text-sm bg-white border " + (t.type === "error" ? "border-red-300" : t.type === "success" ? "border-emerald-300" : "border-slate-200")}>
          <div className="flex items-center gap-2">
            <span className={"inline-block w-2 h-2 rounded-full " + (t.type==="error" ? "bg-red-500" : t.type==="success" ? "bg-emerald-500" : "bg-slate-400")}></span>
            <span className="flex-1">{t.message}</span>
            <button onClick={() => dismiss(t.id)} className="text-slate-500 hover:text-slate-700">✕</button>
          </div>
        </div>
      ))}
    </div>
  )
}
