import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, Search, Building2, MapPin, Edit2, Trash2 } from 'lucide-react'
import PropertyModal from './PropertyModal'
import { formatCurrency } from '../lib/format'

export default function Properties({ session }) {
  const [properties, setProperties] = useState([])
  const [borrowers, setBorrowers] = useState([])
  const [deals, setDeals] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filterBorrower, setFilterBorrower] = useState('all')
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)

  useEffect(() => { fetchAll() }, [])

  async function fetchAll() {
    const [p, b, d] = await Promise.all([
      supabase.from('properties').select('*').order('created_at', { ascending: false }),
      supabase.from('clients').select('id, first_name, last_name, company').eq('client_type', 'Borrower').order('first_name'),
      supabase.from('deals').select('id, property_id, borrower_name, loan_amount, stage'),
    ])
    setProperties(p.data || [])
    setBorrowers(b.data || [])
    setDeals(d.data || [])
    setLoading(false)
  }

  async function deleteProperty(id) {
    if (!window.confirm('Delete this property?')) return
    await supabase.from('properties').delete().eq('id', id)
    fetchAll()
  }

  const borrowerMap = Object.fromEntries(borrowers.map(b => [b.id, (b.first_name + ' ' + (b.last_name || '')).trim() + (b.company ? ' / ' + b.company : '')]))
  const dealsByProperty = deals.reduce((acc, d) => { if (d.property_id) { acc[d.property_id] = acc[d.property_id] || []; acc[d.property_id].push(d) } return acc }, {})

  const filtered = properties.filter(p => {
    if (filterBorrower !== 'all' && p.borrower_id !== filterBorrower) return false
    if (!search) return true
    const hay = (p.address + ' ' + (p.city || '') + ' ' + (p.state || '') + ' ' + (borrowerMap[p.borrower_id] || '')).toLowerCase()
    return hay.includes(search.toLowerCase())
  })

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, gap: '16px' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Stat label="Total Properties" value={properties.length} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Linked to Deals" value={Object.keys(dealsByProperty).length} highlight />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Without Borrower" value={properties.filter(p => !p.borrower_id).length} />
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <div style={{ position: 'relative' }}>
            <Search size={12} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted)' }} />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search properties..." style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px 6px 28px', fontSize: '12px', width: '180px' }} />
          </div>
          <select value={filterBorrower} onChange={e => setFilterBorrower(e.target.value)} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif' }}>
            <option value="all">All borrowers</option>
            {borrowers.map(b => <option key={b.id} value={b.id}>{b.first_name} {b.last_name || ''}</option>)}
          </select>
          <button onClick={() => { setEditing(null); setModalOpen(true) }} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#2563eb', color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
            <Plus size={13} strokeWidth={2.5} /> NEW PROPERTY
          </button>
        </div>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 24px' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px' }}>LOADING PROPERTIES...</div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)' }}>
            {properties.length === 0 ? 'No properties yet. Click NEW PROPERTY to add your first one.' : 'No properties match your filters.'}
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '12px' }}>
            {filtered.map(p => {
              const linkedDeals = dealsByProperty[p.id] || []
              const totalVolume = linkedDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
              return (
                <div key={p.id} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '14px', transition: 'all 0.15s' }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.06)' }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                    <div style={{ flex: 1 }}>
                      <div onClick={() => { setEditing(p); setModalOpen(true) }} style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)', cursor: 'pointer', lineHeight: 1.3, marginBottom: '4px', transition: 'color 0.15s' }}
                        onMouseEnter={e => e.currentTarget.style.color = '#2563eb'}
                        onMouseLeave={e => e.currentTarget.style.color = 'var(--text)'}>
                        {p.address}
                      </div>
                      {(p.city || p.state) && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--muted)' }}>
                          <MapPin size={10} />
                          {[p.city, p.state].filter(Boolean).join(', ')}{p.zip ? ' ' + p.zip : ''}
                        </div>
                      )}
                    </div>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      <button onClick={() => { setEditing(p); setModalOpen(true) }} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}><Edit2 size={11} /></button>
                      <button onClick={() => deleteProperty(p.id)} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: '#ef4444', display: 'flex', alignItems: 'center' }}><Trash2 size={11} /></button>
                    </div>
                  </div>

                  {p.property_type && (
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '10px', padding: '2px 7px', borderRadius: '3px', background: '#eff6ff', color: '#1d4ed8', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
                      <Building2 size={9} /> {p.property_type}
                    </div>
                  )}

                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', fontSize: '11px', color: 'var(--muted)', marginBottom: '8px' }}>
                    {p.total_units && <span>{p.total_units} units</span>}
                    {p.sq_ft && <span>{Number(p.sq_ft).toLocaleString()} sq ft</span>}
                    {p.year_built && <span>Built {p.year_built}</span>}
                  </div>

                  {p.borrower_id && borrowerMap[p.borrower_id] && (
                    <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '8px', padding: '6px 9px', background: 'var(--surface2)', borderRadius: '5px', fontFamily: 'IBM Plex Mono, monospace' }}>
                      Borrower: {borrowerMap[p.borrower_id]}
                    </div>
                  )}

                  {linkedDeals.length > 0 && (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '8px', borderTop: '1px solid var(--border)' }}>
                      <span style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase' }}>{linkedDeals.length} deal{linkedDeals.length > 1 ? 's' : ''}</span>
                      <span style={{ fontSize: '12px', color: '#2563eb', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600 }}>{formatCurrency(totalVolume)}</span>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>

      {modalOpen && <PropertyModal property={editing} session={session} onClose={() => setModalOpen(false)} onSaved={fetchAll} />}
    </div>
  )
}

function Stat({ label, value, highlight }) {
  return (
    <div>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: highlight ? '#2563eb' : 'var(--text)' }}>{value}</div>
    </div>
  )
}
