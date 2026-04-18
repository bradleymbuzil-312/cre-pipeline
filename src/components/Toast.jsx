import { useState, useEffect } from 'react'

export default function Toast() {
  const [toasts, setToasts] = useState([])

  useEffect(() => {
    function onToast(e) {
      const t = { id: Date.now() + Math.random(), ...e.detail }
      setToasts(prev => [...prev, t])
      setTimeout(() => setToasts(prev => prev.filter(x => x.id !== t.id)), t.duration || 3200)
    }
    window.addEventListener('app-toast', onToast)
    return () => window.removeEventListener('app-toast', onToast)
  }, [])

  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={'toast ' + (t.type || 'info')}>{t.message}</div>
      ))}
    </div>
  )
}
