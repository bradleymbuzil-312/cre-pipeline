import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import Auth from './components/Auth'
import Header from './components/Header'
import Pipeline from './components/Pipeline'
import Contacts from './components/Contacts'
import Tasks from './components/Tasks'
import AccessManager from './components/AccessManager'
import Properties from './components/Properties'
import Dashboard from './components/Dashboard'
import Toast from './components/Toast'
import { PROSPECTING_STAGES, ACTIVE_STAGES } from './lib/constants'

export default function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('dashboard')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_e, s) => setSession(s))
    return () => subscription.unsubscribe()
  }, [])

  if (loading) return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '13px', letterSpacing: '0.1em' }}>LOADING...</div>
  if (!session) return <Auth />

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header session={session} view={view} setView={setView} />
      {view === 'dashboard' ? <Dashboard session={session} setView={setView} /> :
       view === 'prospecting' ? <Pipeline session={session} stages={PROSPECTING_STAGES} title="Prospecting" /> :
       view === 'active' ? <Pipeline session={session} stages={ACTIVE_STAGES} title="Active Deals" /> :
       view === 'properties' ? <Properties session={session} /> :
       view === 'contacts' ? <Contacts session={session} /> :
       view === 'tasks' ? <Tasks session={session} /> :
       view === 'access' ? <AccessManager session={session} /> :
       <Dashboard session={session} setView={setView} />}
      <Toast />
    </div>
  )
}
