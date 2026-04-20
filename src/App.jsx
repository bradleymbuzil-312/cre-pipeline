import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import Auth from './components/Auth'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import Pipeline from './components/Pipeline'
import Clients from './components/Clients'
import Tasks from './components/Tasks'
import AccessManager from './components/AccessManager'
import Properties from './components/Properties'
import Referrals from './components/Referrals'
import Lenders from './components/Lenders'
import MaturityWatch from './components/MaturityWatch'
import Resources from './components/Resources'
import Calendar from './components/Calendar'
import Dashboard from './components/Dashboard'
import GlobalSearch from './components/GlobalSearch'
import { ToastProvider } from './components/Toast'
import { PROSPECTING_STAGES, ACTIVE_STAGES } from './lib/constants'
import { X } from 'lucide-react'

export default function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('home')
  const [accessOpen, setAccessOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_e, s) => setSession(s))
    return () => subscription.unsubscribe()
  }, [])

  // Global keyboard shortcut for search
  useEffect(() => {
    if (!session) return
    function handleKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setSearchOpen(true)
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [session])

  if (loading) return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '13px', letterSpacing: '0.1em' }}>LOADING...</div>
  if (!session) return <Auth />

  return (
    <ToastProvider>
      <div style={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar view={view} setView={setView} openAccess={() => setAccessOpen(true)} />
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Topbar session={session} openSearch={() => setSearchOpen(true)} openAccess={() => setAccessOpen(true)} />
        {view === 'home' ? <Dashboard session={session} setView={setView} /> :
         view === 'prospecting' ? <Pipeline session={session} stages={PROSPECTING_STAGES} title="Prospecting" /> :
         view === 'active' ? <Pipeline session={session} stages={ACTIVE_STAGES} title="Active Deals" /> :
         view === 'properties' ? <Properties session={session} /> :
         view === 'referrals' ? <Referrals session={session} /> :
         view === 'clients' ? <Clients session={session} /> :
         view === 'lenders' ? <Lenders session={session} /> :
         view === 'borrowers' ? <Clients session={session} defaultType="Borrower" title="Borrowers" /> :
         view === 'maturity' ? <MaturityWatch session={session} setView={setView} /> :
         view === 'resources' ? <Resources /> :
         view === 'calendar' ? <Calendar session={session} setView={setView} /> :
         view === 'tasks' ? <Tasks session={session} /> :
         <Dashboard session={session} setView={setView} />}

        {accessOpen && (
          <div onClick={e => { if (e.target === e.currentTarget) setAccessOpen(false) }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.3)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
            <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '820px', maxHeight: '90vh', display: 'flex', flexDirection: 'column', boxShadow: '0 32px 80px rgba(0,0,0,0.15)', overflow: 'hidden' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 20px', borderBottom: '1px solid var(--border)' }}>
                <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '15px', color: 'var(--text)' }}>Team Access</h2>
                <button onClick={() => setAccessOpen(false)} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
              </div>
              <div style={{ flex: 1, overflow: 'hidden', display: 'flex' }}>
                <AccessManager session={session} />
              </div>
            </div>
          </div>
        )}

        {searchOpen && <GlobalSearch onClose={() => setSearchOpen(false)} setView={setView} />}
        </div>
      </div>
    </ToastProvider>
  )
}
