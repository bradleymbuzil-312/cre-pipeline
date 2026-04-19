import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { LogOut, Bell, Search, Settings } from 'lucide-react'

export default function Header({ session, view, setView, openAccess, openSearch }) {
  const [alertCount, setAlertCount] = useState(0)
  const [menuOpen, setMenuOpen] = useState(false)
  useEffect(() => { fetchAlerts(); const i = setInterval(fetchAlerts, 60000); return () => clearInterval(i) }, [])
  async function fetchAlerts() {
    const today = new Date().toISOString().split('T')[0]
    const { data } = await supabase.from('clients').select('id').lte('follow_up_date', today).not('follow_up_date', 'is', null)
    setAlertCount(data?.length || 0)
  }

  const NAV = [
    ['home', 'Home'],
    ['prospecting', 'Prospecting'],
    ['active', 'Active'],
    ['properties', 'Properties'],
    ['lenders', 'Lenders'],
    ['referrals', 'Referrals'],
    ['clients', 'Contacts'],
    ['tasks', 'Tasks'],
    ['maturity', 'Maturity'],
  ]

  const isMac = typeof navigator !== 'undefined' && /Mac/.test(navigator.platform)

  return (
    <div className="app-header" style={{ minHeight: '56px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px', background: 'var(--surface)', borderBottom: '1px solid var(--border)', flexShrink: 0, zIndex: 10, gap: '12px', flexWrap: 'wrap' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flexWrap: 'wrap', rowGap: '6px' }}>
        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '16px', color: '#2563eb', letterSpacing: '-0.01em' }}>PIPELINE</span>
        <div style={{ display: 'flex', gap: '2px', background: 'var(--surface2)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border)', flexWrap: 'wrap' }}>
          {NAV.map(([v, label]) => (
            <button key={v} onClick={() => setView(v)} style={{ background: view === v ? 'var(--border)' : 'transparent', border: 'none', padding: '5px 10px', borderRadius: '4px', color: view === v ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '10.5px', letterSpacing: '0.04em', textTransform: 'uppercase', whiteSpace: 'nowrap' }}>{label}</button>
          ))}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {/* Search button */}
        <button onClick={openSearch} title={'Search (' + (isMac ? '⌘K' : 'Ctrl+K') + ')'} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 10px', cursor: 'pointer', color: 'var(--muted)', fontSize: '11px', fontFamily: 'DM Sans, sans-serif' }}>
          <Search size={12} />
          <span style={{ display: 'none' }} className="search-label">Search</span>
          <kbd style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '3px', padding: '1px 4px', fontSize: '9px', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)' }}>{isMac ? '⌘K' : 'Ctrl+K'}</kbd>
        </button>

        {/* Bell */}
        <button onClick={() => setView('clients')} title={alertCount > 0 ? (alertCount + ' follow-ups due') : 'No follow-ups due'} style={{ position: 'relative', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 8px', cursor: 'pointer', display: 'flex', alignItems: 'center', color: alertCount > 0 ? '#2563eb' : 'var(--muted)' }}>
          <Bell size={14} />
          {alertCount > 0 && <span style={{ position: 'absolute', top: '-6px', right: '-6px', background: '#ef4444', color: '#fff', borderRadius: '9px', padding: '1px 5px', fontSize: '9px', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700, minWidth: '16px', textAlign: 'center', lineHeight: '14px' }}>{alertCount}</span>}
        </button>

        {/* User menu */}
        <div style={{ position: 'relative' }}>
          <button onClick={() => setMenuOpen(o => !o)} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '4px 8px', cursor: 'pointer' }}>
            <div style={{ width: '22px', height: '22px', borderRadius: '50%', background: '#2563eb', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', fontWeight: 700, fontFamily: 'Syne, sans-serif' }}>{session.user.email.charAt(0).toUpperCase()}</div>
            <Settings size={13} color="var(--muted)" />
          </button>
          {menuOpen && (
            <>
              <div onClick={() => setMenuOpen(false)} style={{ position: 'fixed', inset: 0, zIndex: 49 }} />
              <div style={{ position: 'absolute', right: 0, top: 'calc(100% + 6px)', zIndex: 50, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', boxShadow: '0 12px 32px rgba(0,0,0,0.1)', minWidth: '200px', overflow: 'hidden' }}>
                <div style={{ padding: '10px 12px', borderBottom: '1px solid var(--border)', fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>{session.user.email}</div>
                <button onClick={() => { setMenuOpen(false); openAccess() }} style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%', padding: '9px 12px', background: 'transparent', border: 'none', color: 'var(--text)', fontSize: '12px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', textAlign: 'left' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                  <Settings size={12} /> Team Access
                </button>
                <div style={{ height: '1px', background: 'var(--border)' }} />
                <button onClick={() => { setMenuOpen(false); supabase.auth.signOut() }} style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%', padding: '9px 12px', background: 'transparent', border: 'none', color: '#ef4444', fontSize: '12px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', textAlign: 'left' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                  <LogOut size={12} /> Sign out
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
