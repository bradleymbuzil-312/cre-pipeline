import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import Auth from './components/Auth'
import Header from './components/Header'
import Pipeline from './components/Pipeline'
import Clients from './components/Clients'
import Tasks from './components/Tasks'
import AccessManager from './components/AccessManager'
import Properties from './components/Properties'
import Referrals from './components/Referrals'
import { PROSPECTING_STAGES, ACTIVE_STAGES } from './lib/constants'

export default function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('prospecting')

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
      {view === 'prospecting' ? <Pipeline session={session} stages={PROSPECTING_STAGES} title="Prospecting" /> :
       view === 'active' ? <Pipeline session={session} stages={ACTIVE_STAGES} title="Active Deals" /> :
       view === 'properties' ? <Properties session={session} /> :
       view === 'referrals' ? <Referrals session={session} /> :
       view === 'clients' ? <Clients session={session} /> :
       view === 'tasks' ? <Tasks session={session} /> :
       <AccessManager session={session} />}
    </div>
  )
}
