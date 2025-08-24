export function Loading({ label = 'Cargando...' }) {
  return (
    <div className="flex items-center gap-3 text-slate-600">
      <div className="w-4 h-4 border-2 border-slate-300 border-l-slate-900 rounded-full animate-spin"></div>
      <span>{label}</span>
    </div>
  )
}

export function Empty({ children }) {
  return (
    <div className="p-8 text-center border rounded-xl bg-white text-slate-500">{children}</div>
  )
}
