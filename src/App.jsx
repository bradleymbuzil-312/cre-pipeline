import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import Auth from './components/Auth'
import Header from './components/Header'
import Pipeline from './components/Pipeline'
import Clients from './components/Clients'
import Tasks from './components/Tasks'

export default function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('pipeline')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })
    return () => subscription.unsubscribe()
  }, [])

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '13px', letterSpacing: '0.1em' }}>
        LOADING...
      </div>
    )
  }

  if (!session) return <Auth />

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header session={session} view={view} setView={setView} />
      {view === 'pipeline' ? <Pipeline session={session} /> : view === 'clients' ? <Clients session={session} /> : <Tasks session={session} />}
    </div>
  )
}
