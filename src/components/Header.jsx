import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabase'
import { LogOut, Bell, Settings, UserCog, Search, Home, Briefcase, Target, Building2, Users, ClipboardList, X } from 'lucide-react'

export default function Header({ session, view, setView }) {
  const [alertCount, setAlertCount] = useState(0)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState({ deals: [], clients: [], properties: [], tasks: [] })
  const [searching, setSearching] = useState(false)
  const settingsRef = useRef(null)
  const searchRef = useRef(null)

  useEffect(() => { fetchAlerts(); const i = setInterval(fetchAlerts, 60000); return () => clearInterval(i) }, [])
  useEffect(() => {
    function onDoc(e) {
      if (settingsRef.current && !settingsRef.current.contains(e.target)) setSettingsOpen(false)
      if (searchRef.current && !searchRef.current.contains(e.target)) setSearchOpen(false)
    }
    document.addEventListener('mousedown', onDoc)
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); setSearchOpen(true) }
      if (e.key === 'Escape') { setSearchOpen(false); setSettingsOpen(false) }
    }
    document.addEventListener('keydown', onKey)
    return () => { document.removeEventListener('mousedown', onDoc); document.removeEventListener('keydown', onKey) }
  }, [])

  async function fetchAlerts() {
    const today = new Date().toISOString().split('T')[0]
    const [follows, tasks] = await Promise.all([
      supabase.from('clients').select('id').lte('follow_up_date', today).not('follow_up_date', 'is', null),
      supabase.from('tasks').select('id').lte('due_date', today).not('due_date', 'is', null).neq('status', 'Done'),
    ])
    setAlertCount((follows.data?.length || 0) + (tasks.data?.length || 0))
  }

  async function runSearch(q) {
    if (!q || q.length < 2) { setSearchResults({ deals: [], clients: [], properties: [], tasks: [] }); return }
    setSearching(true)
    const [d, c, p, t] = await Promise.all([
      supabase.from('deals').select('id, borrower_name, property_address, stage, loan_amount').or('borrower_name.ilike.%' + q + '%,property_address.ilike.%' + q + '%,lender_name.ilike.%' + q + '%').limit(6),
      supabase.from('clients').select('id, first_name, last_name, company, email, client_type').or('first_name.ilike.%' + q + '%,last_name.ilike.%' + q + '%,company.ilike.%' + q + '%,email.ilike.%' + q + '%').limit(6),
      supabase.from('properties').select('id, address, city, state, property_type').or('address.ilike.%' + q + '%,city.ilike.%' + q + '%').limit(6),
      supabase.from('tasks').select('id, title, assigned_to, status').ilike('title', '%' + q + '%').limit(6),
    ])
    setSearchResults({ deals: d.data || [], clients: c.data || [], properties: p.data || [], tasks: t.data || [] })
    setSearching(false)
  }

  useEffect(() => {
    const t = setTimeout(() => runSearch(searchQuery), 180)
    return () => clearTimeout(t)
  }, [searchQuery])

  const NAV = [
    ['dashboard', 'Home', Home],
    ['prospecting', 'Prospecting', Target],
    ['active', 'Active Deals', Briefcase],
    ['properties', 'Properties', Building2],
    ['contacts', 'Contacts', Users],
    ['tasks', 'Tasks', ClipboardList],
  ]

  const totalResults = searchResults.deals.length + searchResults.clients.length + searchResults.properties.length + searchResults.tasks.length

  return (
    <>
    <div className="nav-wrap" style={{ height: '56px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px', background: 'var(--surface)', borderBottom: '1px solid var(--border)', flexShrink: 0, zIndex: 10, gap: '10px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', minWidth: 0 }}>
        <span onClick={() => setView('dashboard')} style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '16px', color: '#2563eb', letterSpacing: '-0.01em', cursor: 'pointer', whiteSpace: 'nowrap' }}>PIPELINE</span>
        <div className="nav-pills" style={{ display: 'flex', gap: '2px', background: 'var(--surface2)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border)' }}>
          {NAV.map(([v, label, Icon]) => (
            <button key={v} onClick={() => setView(v)} title={label} style={{ background: view === v ? 'var(--surface)' : 'transparent', boxShadow: view === v ? '0 1px 2px rgba(0,0,0,0.05)' : 'none', border: 'none', padding: '5px 10px', borderRadius: '4px', color: view === v ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '10.5px', letterSpacing: '0.04em', textTransform: 'uppercase', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '5px' }}>
              <Icon size={11} /> {label}
            </button>
          ))}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {/* Global search trigger */}
        <button onClick={() => setSearchOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--muted)', padding: '5px 10px', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontFamily: 'DM Sans, sans-serif' }}>
          <Search size={12} />
          <span>Search...</span>
          <span style={{ fontSize: '9px', padding: '1px 4px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '3px', fontFamily: 'IBM Plex Mono, monospace', marginLeft: '6px' }}>⌘ K</span>
        </button>
        <button onClick={() => { setView('contacts') }} title={alertCount > 0 ? (alertCount + ' items need attention') : 'No alerts'} style={{ position: 'relative', background: 'transparent', border: '1px solid var(--border)', borderRadius: '6px', padding: '5px 8px', cursor: 'pointer', display: 'flex', alignItems: 'center', color: alertCount > 0 ? '#2563eb' : 'var(--muted)' }}>
          <Bell size={14} />
          {alertCount > 0 && <span style={{ position: 'absolute', top: '-6px', right: '-6px', background: '#ef4444', color: '#fff', borderRadius: '9px', padding: '1px 5px', fontSize: '9px', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700, minWidth: '16px', textAlign: 'center', lineHeight: '14px' }}>{alertCount}</span>}
        </button>
        <span className="header-email" style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>{session.user.email}</span>
        <div ref={settingsRef} style={{ position: 'relative' }}>
          <button onClick={() => setSettingsOpen(o => !o)} title="Settings" style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '5px 8px', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
            <Settings size={14} />
          </button>
          {settingsOpen && (
            <div style={{ position: 'absolute', top: 'calc(100% + 4px)', right: 0, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden', minWidth: '180px', boxShadow: '0 8px 24px rgba(0,0,0,0.1)', zIndex: 200 }}>
              <SettingsItem icon={UserCog} label="Team Access" onClick={() => { setView('access'); setSettingsOpen(false) }} />
              <div style={{ height: '1px', background: 'var(--border)' }} />
              <SettingsItem icon={LogOut} label="Sign Out" onClick={() => supabase.auth.signOut()} />
            </div>
          )}
        </div>
      </div>
    </div>

    {/* Global search modal */}
    {searchOpen && (
      <div onClick={e => { if (e.target === e.currentTarget) setSearchOpen(false) }} style={{ position: 'fixed', inset: 0, zIndex: 10000, background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'flex-start', justifyContent: 'center', paddingTop: '80px' }}>
        <div ref={searchRef} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '580px', maxHeight: '70vh', display: 'flex', flexDirection: 'column', boxShadow: '0 24px 60px rgba(0,0,0,0.15)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '14px 18px', borderBottom: '1px solid var(--border)' }}>
            <Search size={16} color="var(--muted)" />
            <input autoFocus value={searchQuery} onChange={e => setSearchQuery(e.target.value)} placeholder="Search deals, contacts, properties, tasks..." style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--text)', fontSize: '14px', fontFamily: 'DM Sans, sans-serif', outline: 'none' }} />
            <button onClick={() => setSearchOpen(false)} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '5px', padding: '3px 5px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}><X size={13} /></button>
          </div>
          <div style={{ overflowY: 'auto', flex: 1, padding: '10px' }}>
            {!searchQuery && <div style={{ padding: '30px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>Type to search across all data...</div>}
            {searching && searchQuery && <div style={{ padding: '20px', textAlign: 'center', color: 'var(--muted)', fontSize: '12px' }}>Searching...</div>}
            {!searching && searchQuery && totalResults === 0 && <div style={{ padding: '20px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>No results for "{searchQuery}"</div>}
            {searchResults.deals.length > 0 && (
              <SearchSection label="Deals">
                {searchResults.deals.map(d => (
                  <SearchResult key={d.id} onClick={() => { setView(d.stage === 'Funded / Closed' || ['LOI / Term Sheet','Due Diligence','Closing'].includes(d.stage) ? 'active' : 'prospecting'); setSearchOpen(false); setSearchQuery('') }}
                    primary={d.borrower_name} secondary={d.property_address || d.stage} badge={d.stage} />
                ))}
              </SearchSection>
            )}
            {searchResults.clients.length > 0 && (
              <SearchSection label="Contacts">
                {searchResults.clients.map(c => (
                  <SearchResult key={c.id} onClick={() => { setView('contacts'); setSearchOpen(false); setSearchQuery('') }}
                    primary={(c.first_name || '') + ' ' + (c.last_name || '')} secondary={[c.company, c.email].filter(Boolean).join(' · ')} badge={c.client_type} />
                ))}
              </SearchSection>
            )}
            {searchResults.properties.length > 0 && (
              <SearchSection label="Properties">
                {searchResults.properties.map(p => (
                  <SearchResult key={p.id} onClick={() => { setView('properties'); setSearchOpen(false); setSearchQuery('') }}
                    primary={p.address} secondary={[p.city, p.state, p.property_type].filter(Boolean).join(' · ')} />
                ))}
              </SearchSection>
            )}
            {searchResults.tasks.length > 0 && (
              <SearchSection label="Tasks">
                {searchResults.tasks.map(t => (
                  <SearchResult key={t.id} onClick={() => { setView('tasks'); setSearchOpen(false); setSearchQuery('') }}
                    primary={t.title} secondary={t.assigned_to || 'Unassigned'} badge={t.status} />
                ))}
              </SearchSection>
            )}
          </div>
        </div>
      </div>
    )}
    </>
  )
}

function SettingsItem({ icon: Icon, label, onClick }) {
  return (
    <button onClick={onClick} style={{ display: 'flex', alignItems: 'center', gap: '10px', width: '100%', padding: '10px 14px', background: 'transparent', border: 'none', color: 'var(--text)', fontSize: '13px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', fontWeight: 500, textAlign: 'left' }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
      <Icon size={13} color="var(--muted)" /> {label}
    </button>
  )
}

function SearchSection({ label, children }) {
  return (
    <div style={{ marginBottom: '8px' }}>
      <div style={{ fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em', padding: '6px 10px' }}>{label}</div>
      <div>{children}</div>
    </div>
  )
}

function SearchResult({ primary, secondary, badge, onClick }) {
  return (
    <button onClick={onClick} style={{ display: 'flex', alignItems: 'center', gap: '10px', width: '100%', padding: '10px 12px', background: 'transparent', border: 'none', borderRadius: '6px', cursor: 'pointer', textAlign: 'left', transition: 'background 0.1s' }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', fontFamily: 'Syne, sans-serif', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{primary || 'Untitled'}</div>
        {secondary && <div style={{ fontSize: '11px', color: 'var(--muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{secondary}</div>}
      </div>
      {badge && <span style={{ fontSize: '9px', padding: '2px 7px', borderRadius: '3px', background: 'var(--blue-light)', color: 'var(--blue-dim)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', whiteSpace: 'nowrap' }}>{badge}</span>}
    </button>
  )
}
