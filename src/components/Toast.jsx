import { createContext, useContext, useState, useCallback } from 'react'
import { CheckCircle, XCircle, Info, X } from 'lucide-react'

const ToastContext = createContext(null)

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) return { toast: () => {} }
  return ctx
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const toast = useCallback((message, type = 'success', duration = 3000) => {
    const id = Math.random().toString(36).slice(2)
    setToasts(prev => [...prev, { id, message, type }])
    if (duration > 0) {
      setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), duration)
    }
  }, [])

  const dismiss = id => setToasts(prev => prev.filter(t => t.id !== id))

  const COLORS = {
    success: { bg: '#f0fdf4', border: '#86efac', text: '#15803d', Icon: CheckCircle },
    error:   { bg: '#fef2f2', border: '#fecaca', text: '#b91c1c', Icon: XCircle },
    info:    { bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8', Icon: Info },
  }

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div style={{ position: 'fixed', top: '16px', right: '16px', zIndex: 10000, display: 'flex', flexDirection: 'column', gap: '8px', pointerEvents: 'none' }}>
        {toasts.map(t => {
          const c = COLORS[t.type] || COLORS.info
          const { Icon } = c
          return (
            <div key={t.id} style={{ pointerEvents: 'auto', display: 'flex', alignItems: 'center', gap: '10px', background: c.bg, border: '1px solid ' + c.border, color: c.text, padding: '10px 14px', borderRadius: '8px', fontSize: '13px', fontFamily: 'DM Sans, sans-serif', fontWeight: 500, minWidth: '240px', maxWidth: '400px', boxShadow: '0 8px 24px rgba(0,0,0,0.08)', animation: 'slideIn 0.2s ease-out' }}>
              <Icon size={16} />
              <span style={{ flex: 1 }}>{t.message}</span>
              <button onClick={() => dismiss(t.id)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: c.text, opacity: 0.6, display: 'flex', alignItems: 'center', padding: 0 }}><X size={14} /></button>
            </div>
          )
        })}
      </div>
      <style>{'@keyframes slideIn { from { opacity: 0; transform: translateX(10px) } to { opacity: 1; transform: translateX(0) } }'}</style>
    </ToastContext.Provider>
  )
}
