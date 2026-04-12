import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { LogOut, Bell } from 'lucide-react'

export default function Header({ session, view, setView }) {
  const [alertCount, setAlertCount] = useState(0)

  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 60000)
    return () => clearInterval(interval)
  }, [])

  async function fetchAlerts() {
    const today = new Date().toISOString().split('T')[0]
    const { data } = await supabase.from('clients').select('id').lte('follow_up_date', today).not('follow_up_date', 'is', null)
    setAlertCount(data?.length || 0)
  }

  const NAV = [['pipeline','Deals'],['clients','Clients'],['tasks','Tasks'],['access','Access']]

  return (
    <div style={{ height: '56px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', background: 'var(--surface)', borderBottom: '1px solid var(--border)', flexShrink: 0, zIndex: 10 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '17px', color: 'var(--gold)', letterSpacing: '-0.01em' }}>PIPELINE</span>
        <div style={{ display: 'flex', gap: '2px', background: 'var(--surface2)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border)' }}>
          {NAV.map(([v, label]) => (
            <button key={v} onClick={() => setView(v)} style={{ background: view === v ? 'var(--border)' : 'transparent', border: 'none', padding: '5px 14px', borderRadius: '4px', color: view === v ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', letterSpacing: '0.05em', textTransform: 'uppercase', transition: 'all 0.15s' }}>
              {label}
            </button>
          ))}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <button onClick={() => setView('clients')} title={alertCount > 0 ? `${alertCount} follow-up${alertCount > 1 ? 's' : ''} due` : 'No follow-ups due'} style={{ position: 'relative', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 8px', cursor: 'pointer', display: 'flex', alignItems: 'center', color: alertCount > 0 ? 'var(--gold)' : 'var(--muted)', transition: 'all 0.15s' }}>
          <Bell size={14} />
          {alertCount > 0 && <span style={{ position: 'absolute', top: '-6px', right: '-6px', background: 'var(--danger)', color: '#fff', borderRadius: '9px', padding: '1px 5px', fontSize: '9px', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700, minWidth: '16px', textAlign: 'center', lineHeight: '14px' }}>{alertCount}</span>}
        </button>
        <span style={{ fontSize: '12px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>{session.user.email}</span>
        <button onClick={() => supabase.auth.signOut()} style={{ display: 'flex', alignItems: 'center', gap: '5px', background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.05em', transition: 'color 0.15s, border-color 0.15s' }} onMouseEnter={e => { e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.borderColor = 'var(--border-hover)' }} onMouseLeave={e => { e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.borderColor = 'var(--border)' }}>
          <LogOut size={11} /> SIGN OUT
        </button>
      </div>
    </div>
  )
}
