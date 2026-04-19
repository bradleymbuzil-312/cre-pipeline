import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabase'
import { Search, Bell, LogOut, Settings } from 'lucide-react'

export default function Topbar({ session, openSearch, openAccess }) {
  const [alertCount, setAlertCount] = useState(0)
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    async function fetchAlerts() {
      const today = new Date().toISOString().split('T')[0]
      const { data } = await supabase.from('clients').select('id').lte('follow_up_date', today).not('follow_up_date', 'is', null)
      setAlertCount(data?.length || 0)
    }
    fetchAlerts()
  }, [])

  useEffect(() => {
    function onDoc(e) { if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false) }
    document.addEventListener('mousedown', onDoc)
    return () => document.removeEventListener('mousedown', onDoc)
  }, [])

  const isMac = typeof navigator !== 'undefined' && /Mac/i.test(navigator.platform)
  const email = session?.user?.email || ''
  const initial = (email[0] || 'U').toUpperCase()
  const name = email.split('@')[0] || 'user'

  async function signOut() {
    await supabase.auth.signOut()
    window.location.reload()
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '12px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', position: 'sticky', top: 0, zIndex: 10 }}>
      <div style={{ flex: 1, maxWidth: '500px', position: 'relative' }}>
        <button onClick={openSearch} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '8px', padding: '7px 10px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '6px', color: 'var(--muted)', cursor: 'pointer', fontSize: '13px', textAlign: 'left' }}>
          <Search size={14} />
          <span style={{ flex: 1 }}>Search deals, borrowers, lenders...</span>
          <span style={{ background: 'var(--border)', padding: '2px 6px', borderRadius: '4px', fontSize: '11px', color: 'var(--dim)', fontFamily: 'IBM Plex Mono, monospace' }}>{isMac ? '\u2318K' : 'Ctrl+K'}</span>
        </button>
      </div>

      <button title={alertCount + ' follow-ups'} style={{ position: 'relative', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '7px 9px', cursor: 'pointer', color: 'var(--muted)', display: 'flex' }}>
        <Bell size={14} />
        {alertCount > 0 && <span style={{ position: 'absolute', top: '-4px', right: '-4px', background: 'var(--amber)', color: '#000', fontSize: '9px', fontWeight: 700, padding: '1px 5px', borderRadius: '9px' }}>{alertCount}</span>}
      </button>

      <div ref={menuRef} style={{ position: 'relative' }}>
        <button onClick={() => setMenuOpen(o => !o)} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 10px 5px 6px', cursor: 'pointer', color: 'var(--muted)' }}>
          <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: 'var(--brand)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '11px' }}>{initial}</div>
          <span style={{ fontSize: '12px' }}>{name}</span>
        </button>
        {menuOpen && (
          <div style={{ position: 'absolute', top: 'calc(100% + 6px)', right: 0, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', minWidth: '200px', boxShadow: '0 12px 32px rgba(0,0,0,0.4)', overflow: 'hidden', zIndex: 100 }}>
            <div style={{ padding: '10px 12px', borderBottom: '1px solid var(--border)' }}>
              <div style={{ fontSize: '12px', color: 'var(--text)', fontWeight: 600 }}>{name}</div>
              <div style={{ fontSize: '11px', color: 'var(--muted)', marginTop: '2px' }}>{email}</div>
            </div>
            <button onClick={() => { setMenuOpen(false); openAccess?.() }} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'transparent', border: 'none', color: 'var(--text)', cursor: 'pointer', fontSize: '12px', textAlign: 'left' }} onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'} onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
              <Settings size={13} /> Team Access
            </button>
            <button onClick={signOut} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'transparent', border: 'none', color: 'var(--danger)', cursor: 'pointer', fontSize: '12px', textAlign: 'left' }} onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'} onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
              <LogOut size={13} /> Sign out
            </button>
          </div>
        )}
      </div>
    </div>
  )
}