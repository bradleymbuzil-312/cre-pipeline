import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabase'
import { Search, X, Briefcase, Users, Building2 } from 'lucide-react'

export default function GlobalSearch({ onClose, setView }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState({ deals: [], clients: [], properties: [] })
  const [loading, setLoading] = useState(false)
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
    function handleEsc(e) { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [])

  useEffect(() => {
    if (!query.trim()) { setResults({ deals: [], clients: [], properties: [] }); return }
    const t = setTimeout(async () => {
      setLoading(true)
      const q = query.trim()
      const like = '%' + q + '%'
      const [d, c, p] = await Promise.all([
        supabase.from('deals').select('id, borrower_name, property_address, loan_amount, stage, city').or('borrower_name.ilike.' + like + ',property_address.ilike.' + like + ',lender_name.ilike.' + like + ',city.ilike.' + like).limit(8),
        supabase.from('clients').select('id, first_name, last_name, company, email, client_type').or('first_name.ilike.' + like + ',last_name.ilike.' + like + ',company.ilike.' + like + ',email.ilike.' + like).limit(8),
        supabase.from('properties').select('id, address, city, state, property_type').or('address.ilike.' + like + ',city.ilike.' + like).limit(8),
      ])
      setResults({ deals: d.data || [], clients: c.data || [], properties: p.data || [] })
      setLoading(false)
    }, 200)
    return () => clearTimeout(t)
  }, [query])

  function navigate(view) { setView(view); onClose() }

  const totalResults = results.deals.length + results.clients.length + results.properties.length

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 2000, background: 'rgba(0,0,0,0.3)', backdropFilter: 'blur(4px)', display: 'flex', justifyContent: 'center', paddingTop: '80px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '560px', maxHeight: '60vh', display: 'flex', flexDirection: 'column', boxShadow: '0 32px 80px rgba(0,0,0,0.12)', overflow: 'hidden', marginLeft: '16px', marginRight: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '14px 16px', borderBottom: '1px solid var(--border)' }}>
          <Search size={16} color="var(--muted)" />
          <input ref={inputRef} value={query} onChange={e => setQuery(e.target.value)} placeholder="Search deals, contacts, properties..." style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--text)', fontSize: '15px', fontFamily: 'DM Sans, sans-serif', outline: 'none' }} />
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', borderRadius: '4px', padding: '3px 6px', cursor: 'pointer', fontSize: '10px', fontFamily: 'IBM Plex Mono, monospace' }}>ESC</button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '6px' }}>
          {!query.trim() ? (
            <div style={{ padding: '24px', color: 'var(--muted)', fontSize: '13px', textAlign: 'center' }}>
              Start typing to search. Press <kbd style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '3px', padding: '1px 6px', fontSize: '10px', fontFamily: 'IBM Plex Mono, monospace' }}>ESC</kbd> to close.
            </div>
          ) : loading ? (
            <div style={{ padding: '20px', color: 'var(--muted)', fontSize: '12px', textAlign: 'center', fontFamily: 'IBM Plex Mono, monospace' }}>SEARCHING...</div>
          ) : totalResults === 0 ? (
            <div style={{ padding: '20px', color: 'var(--muted)', fontSize: '13px', textAlign: 'center' }}>No results for "{query}"</div>
          ) : (
            <>
              {results.deals.length > 0 && (
                <Section icon={Briefcase} title="Deals">
                  {results.deals.map(d => (
                    <SearchResult key={d.id} onClick={() => navigate(['Funded / Closed', 'Closing', 'Due Diligence', 'LOI / Term Sheet'].includes(d.stage) ? 'active' : 'prospecting')}>
                      <div style={{ fontWeight: 600, color: 'var(--text)' }}>{d.borrower_name}</div>
                      <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{[d.property_address, d.city, d.stage].filter(Boolean).join(' · ')}</div>
                    </SearchResult>
                  ))}
                </Section>
              )}
              {results.clients.length > 0 && (
                <Section icon={Users} title="Contacts">
                  {results.clients.map(c => (
                    <SearchResult key={c.id} onClick={() => navigate('clients')}>
                      <div style={{ fontWeight: 600, color: 'var(--text)' }}>{c.first_name} {c.last_name || ''}</div>
                      <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{[c.company, c.email, c.client_type].filter(Boolean).join(' · ')}</div>
                    </SearchResult>
                  ))}
                </Section>
              )}
              {results.properties.length > 0 && (
                <Section icon={Building2} title="Properties">
                  {results.properties.map(p => (
                    <SearchResult key={p.id} onClick={() => navigate('properties')}>
                      <div style={{ fontWeight: 600, color: 'var(--text)' }}>{p.address}</div>
                      <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{[p.property_type, p.city, p.state].filter(Boolean).join(' · ')}</div>
                    </SearchResult>
                  ))}
                </Section>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function Section({ icon: Icon, title, children }) {
  return (
    <div style={{ marginBottom: '4px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 10px', fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
        <Icon size={11} /> {title}
      </div>
      {children}
    </div>
  )
}

function SearchResult({ children, onClick }) {
  return (
    <button onClick={onClick} style={{ width: '100%', textAlign: 'left', display: 'block', padding: '8px 10px', background: 'transparent', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '13px', fontFamily: 'DM Sans, sans-serif', transition: 'background 0.12s' }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
      {children}
    </button>
  )
}
