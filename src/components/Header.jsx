import { supabase } from '../lib/supabase'
import { LogOut } from 'lucide-react'

export default function Header({ session }) {
  return (
    <div style={{
      height: '56px', display: 'flex', alignItems: 'center',
      justifyContent: 'space-between', padding: '0 24px',
      background: 'var(--surface)', borderBottom: '1px solid var(--border)',
      flexShrink: 0, zIndex: 10
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '17px', color: 'var(--gold)', letterSpacing: '-0.01em' }}>
          PIPELINE
        </span>
        <span style={{ color: 'var(--border)', fontSize: '14px' }}>|</span>
        <span style={{ fontFamily: 'Syne, sans-serif', fontSize: '11px', color: 'var(--muted)', fontWeight: 500, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          CRE Capital Markets
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <span style={{ fontSize: '12px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>
          {session.user.email}
        </span>
        <button
          onClick={() => supabase.auth.signOut()}
          style={{
            display: 'flex', alignItems: 'center', gap: '5px',
            background: 'transparent', border: '1px solid var(--border)',
            color: 'var(--muted)', padding: '5px 10px', borderRadius: '5px',
            cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600,
            letterSpacing: '0.05em', transition: 'color 0.15s, border-color 0.15s'
          }}
          onMouseEnter={e => { e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.borderColor = 'var(--border-hover)' }}
          onMouseLeave={e => { e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.borderColor = 'var(--border)' }}
        >
          <LogOut size={11} /> SIGN OUT
        </button>
      </div>
    </div>
  )
}
