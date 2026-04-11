import { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Auth() {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit() {
    if (!email || !password) { setError('Please enter your email and password.'); return }
    setLoading(true); setError(''); setMessage('')

    if (mode === 'login') {
      const { error: e } = await supabase.auth.signInWithPassword({ email, password })
      if (e) setError(e.message)
    } else {
      const { error: e } = await supabase.auth.signUp({ email, password })
      if (e) setError(e.message)
      else setMessage('Check your email to confirm your account.')
    }
    setLoading(false)
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', background: 'var(--bg)' }}>

      {/* Left branding panel */}
      <div style={{
        width: '420px', flexShrink: 0,
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
        padding: '48px', background: 'var(--surface)',
        borderRight: '1px solid var(--border)'
      }}>
        <div>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '24px', color: 'var(--gold)', letterSpacing: '-0.02em', marginBottom: '6px' }}>
            PIPELINE
          </div>
          <div style={{ fontSize: '13px', color: 'var(--muted)' }}>CRE Capital Markets Deal Tracker</div>
        </div>

        <div>
          <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '20px' }}>
            What's included
          </div>
          {[
            ['Kanban board', 'Drag deals through 6 pipeline stages'],
            ['List view', 'Sortable table with all deal fields'],
            ['Team sync', 'Real-time updates across your whole team'],
            ['Commission tracking', 'Log fees per deal, track total pipeline value'],
            ['Deal history', 'Full notes and timeline per transaction'],
          ].map(([title, desc]) => (
            <div key={title} style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
              <div style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'var(--gold)', marginTop: '6px', flexShrink: 0 }} />
              <div>
                <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', fontFamily: 'Syne, sans-serif', marginBottom: '2px' }}>{title}</div>
                <div style={{ fontSize: '12px', color: 'var(--muted)' }}>{desc}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ fontFamily: 'IBM Plex Mono, monospace', fontSize: '10px', color: 'var(--border)' }}>
          MMCC PIPELINE v1.0 · CONFIDENTIAL
        </div>
      </div>

      {/* Right form panel */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px' }}>
        <div style={{ width: '100%', maxWidth: '380px' }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '22px', color: 'var(--text)', marginBottom: '6px' }}>
            {mode === 'login' ? 'Sign in' : 'Create account'}
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--muted)', marginBottom: '32px' }}>
            {mode === 'login' ? "No account? " : 'Have an account? '}
            <button onClick={() => { setMode(mode === 'login' ? 'signup' : 'login'); setError(''); setMessage('') }}
              style={{ background: 'none', border: 'none', color: 'var(--gold)', cursor: 'pointer', fontSize: '13px', fontWeight: 600 }}>
              {mode === 'login' ? 'Sign up' : 'Sign in'}
            </button>
          </p>

          <Field label="Work Email">
            <input type="email" value={email} onChange={e => setEmail(e.target.value)}
              placeholder="you@mmcc.com" style={inputStyle}
              onKeyDown={e => e.key === 'Enter' && handleSubmit()} />
          </Field>

          <Field label="Password" style={{ marginBottom: '24px' }}>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)}
              placeholder="••••••••" style={inputStyle}
              onKeyDown={e => e.key === 'Enter' && handleSubmit()} />
          </Field>

          {error && <div style={{ color: 'var(--danger)', fontSize: '13px', marginBottom: '16px', padding: '10px 12px', background: 'rgba(248,81,73,0.08)', borderRadius: '6px', border: '1px solid rgba(248,81,73,0.2)' }}>{error}</div>}
          {message && <div style={{ color: 'var(--success)', fontSize: '13px', marginBottom: '16px', padding: '10px 12px', background: 'rgba(63,185,80,0.08)', borderRadius: '6px', border: '1px solid rgba(63,185,80,0.2)' }}>{message}</div>}

          <button onClick={handleSubmit} disabled={loading} style={{
            width: '100%', background: 'var(--gold)', border: 'none', color: '#000',
            padding: '12px', borderRadius: '8px', fontFamily: 'Syne, sans-serif',
            fontWeight: 700, fontSize: '14px', cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1, transition: 'opacity 0.15s, transform 0.1s',
            letterSpacing: '0.02em'
          }}>
            {loading ? 'PLEASE WAIT...' : mode === 'login' ? 'SIGN IN' : 'CREATE ACCOUNT'}
          </button>
        </div>
      </div>
    </div>
  )
}

function Field({ label, children, style }) {
  return (
    <div style={{ marginBottom: '16px', ...style }}>
      <label style={{ display: 'block', marginBottom: '6px', fontSize: '11px', fontWeight: 600, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
        {label}
      </label>
      {children}
    </div>
  )
}

const inputStyle = {
  width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)',
  color: 'var(--text)', borderRadius: '8px', padding: '10px 14px',
  fontSize: '14px', transition: 'border-color 0.15s',
}
