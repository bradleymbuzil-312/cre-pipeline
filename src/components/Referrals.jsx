import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, ChevronDown, ChevronRight, Users, Building2, MapPin, Trash2, Edit2 } from 'lucide-react'
import PropertyModal from './PropertyModal'

export default function Referrals({ session }) {
  const [referralSources, setReferralSources] = useState([])
  const [borrowers, setBorrowers] = useState([])
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState({})
  const [expandedBorrowers, setExpandedBorrowers] = useState({})
  const [addingBorrowerTo, setAddingBorrowerTo] = useState(null)
  const [newBorrower, setNewBorrower] = useState({ first_name: '', last_name: '', company: '', email: '', phone: '' })
  const [propModalOpen, setPropModalOpen] = useState(false)
  const [propModalBorrower, setPropModalBorrower] = useState(null)
  const [editingProp, setEditingProp] = useState(null)
  const [addingSource, setAddingSource] = useState(false)
  const [newSource, setNewSource] = useState({ first_name: '', last_name: '', company: '', email: '', phone: '' })

  useEffect(() => { fetchAll() }, [])

  async function fetchAll() {
    const [s, b, p] = await Promise.all([
      supabase.from('clients').select('*').eq('client_type', 'Referral Source').order('first_name'),
      supabase.from('clients').select('*').eq('client_type', 'Borrower').order('first_name'),
      supabase.from('properties').select('*').order('address'),
    ])
    setReferralSources(s.data || [])
    setBorrowers(b.data || [])
    setProperties(p.data || [])
    setLoading(false)
  }

  async function createBorrower(sourceId) {
    if (!newBorrower.first_name.trim()) return
    await supabase.from('clients').insert({
      ...newBorrower,
      client_type: 'Borrower',
      referral_source_id: sourceId,
      created_by: session.user.id,
    })
    setNewBorrower({ first_name: '', last_name: '', company: '', email: '', phone: '' })
    setAddingBorrowerTo(null)
    fetchAll()
  }

  async function createReferralSource() {
    if (!newSource.first_name.trim()) return
    await supabase.from('clients').insert({
      ...newSource,
      client_type: 'Referral Source',
      created_by: session.user.id,
    })
    setNewSource({ first_name: '', last_name: '', company: '', email: '', phone: '' })
    setAddingSource(false)
    fetchAll()
  }

  async function removeBorrowerFromSource(borrowerId) {
    if (!window.confirm('Unlink this borrower from the referral source?')) return
    await supabase.from('clients').update({ referral_source_id: null }).eq('id', borrowerId)
    fetchAll()
  }

  function openAddProperty(borrower) {
    setPropModalBorrower(borrower)
    setEditingProp(null)
    setPropModalOpen(true)
  }

  function openEditProperty(property) {
    setEditingProp(property)
    setPropModalBorrower(null)
    setPropModalOpen(true)
  }

  const IS = { background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '5px', padding: '6px 9px', fontSize: '11px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }

  const borrowersBySource = referralSources.reduce((acc, s) => {
    acc[s.id] = borrowers.filter(b => b.referral_source_id === s.id)
    return acc
  }, {})
  const orphanBorrowers = borrowers.filter(b => !b.referral_source_id)
  const propsByBorrower = borrowers.reduce((acc, b) => {
    acc[b.id] = properties.filter(p => p.borrower_id === b.id)
    return acc
  }, {})

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0 }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Stat label="Referral Sources" value={referralSources.length} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Borrowers" value={borrowers.length} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Properties" value={properties.length} />
        </div>
        <button onClick={() => setAddingSource(true)} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#2563eb', color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em' }}>
          <Plus size={13} strokeWidth={2.5} /> NEW REFERRAL SOURCE
        </button>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '20px 24px' }}>
        <div style={{ maxWidth: '900px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>

          {addingSource && (
            <div style={{ background: 'var(--surface)', border: '1px solid #2563eb', borderRadius: '10px', padding: '14px' }}>
              <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>New Referral Source</div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px', marginBottom: '10px' }}>
                <input placeholder="First name *" value={newSource.first_name} onChange={e => setNewSource(s => ({ ...s, first_name: e.target.value }))} style={IS} />
                <input placeholder="Last name" value={newSource.last_name} onChange={e => setNewSource(s => ({ ...s, last_name: e.target.value }))} style={IS} />
                <input placeholder="Company" value={newSource.company} onChange={e => setNewSource(s => ({ ...s, company: e.target.value }))} style={IS} />
                <input placeholder="Email" value={newSource.email} onChange={e => setNewSource(s => ({ ...s, email: e.target.value }))} style={IS} />
                <input placeholder="Phone" value={newSource.phone} onChange={e => setNewSource(s => ({ ...s, phone: e.target.value }))} style={IS} />
              </div>
              <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                <button onClick={() => { setAddingSource(false); setNewSource({ first_name: '', last_name: '', company: '', email: '', phone: '' }) }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '6px 14px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600 }}>CANCEL</button>
                <button onClick={createReferralSource} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '6px 16px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }}>CREATE</button>
              </div>
            </div>
          )}

          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px' }}>LOADING...</div>
          ) : referralSources.length === 0 && orphanBorrowers.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)', fontSize: '13px' }}>
              No referral sources yet. Click NEW REFERRAL SOURCE to add one.
            </div>
          ) : (
            <>
              {referralSources.map(source => {
                const srcBorrowers = borrowersBySource[source.id] || []
                const isExpanded = expanded[source.id]
                return (
                  <div key={source.id} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden' }}>
                    <div onClick={() => setExpanded(e => ({ ...e, [source.id]: !e[source.id] }))} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '14px 16px', cursor: 'pointer', background: isExpanded ? 'var(--surface2)' : 'transparent', transition: 'background 0.15s' }}>
                      {isExpanded ? <ChevronDown size={15} color="var(--muted)" /> : <ChevronRight size={15} color="var(--muted)" />}
                      <Users size={14} color="#2563eb" />
                      <div style={{ flex: 1 }}>
                        <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)' }}>{source.first_name} {source.last_name || ''}</div>
                        {source.company && <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{source.company}</div>}
                      </div>
                      <span style={{ fontSize: '10px', padding: '2px 8px', borderRadius: '3px', background: '#eff6ff', color: '#1d4ed8', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{srcBorrowers.length} borrower{srcBorrowers.length !== 1 ? 's' : ''}</span>
                    </div>

                    {isExpanded && (
                      <div style={{ padding: '12px 16px 16px 42px', borderTop: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {srcBorrowers.map(b => {
                          const bProps = propsByBorrower[b.id] || []
                          const bExpanded = expandedBorrowers[b.id]
                          return (
                            <div key={b.id} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 12px' }}>
                                <button onClick={() => setExpandedBorrowers(e => ({ ...e, [b.id]: !e[b.id] }))} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}>
                                  {bExpanded ? <ChevronDown size={13} /> : <ChevronRight size={13} />}
                                </button>
                                <Building2 size={12} color="var(--muted)" />
                                <div style={{ flex: 1 }}>
                                  <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '13px', color: 'var(--text)' }}>{b.first_name} {b.last_name || ''}{b.company ? (' — ' + b.company) : ''}</div>
                                  {(b.email || b.phone) && <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>{[b.email, b.phone].filter(Boolean).join(' · ')}</div>}
                                </div>
                                <span style={{ fontSize: '9px', padding: '1px 6px', borderRadius: '3px', background: 'var(--surface)', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase' }}>{bProps.length} prop{bProps.length !== 1 ? 's' : ''}</span>
                                <button onClick={() => openAddProperty(b)} title="Add property" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}><Plus size={11} /></button>
                                <button onClick={() => removeBorrowerFromSource(b.id)} title="Unlink" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 6px', cursor: 'pointer', color: '#ef4444', display: 'flex', alignItems: 'center' }}><Trash2 size={10} /></button>
                              </div>

                              {bExpanded && bProps.length > 0 && (
                                <div style={{ padding: '0 12px 10px 30px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                                  {bProps.map(p => (
                                    <div key={p.id} onClick={() => openEditProperty(p)} style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 10px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '5px', cursor: 'pointer', transition: 'border-color 0.15s' }}
                                      onMouseEnter={e => e.currentTarget.style.borderColor = '#2563eb'}
                                      onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}>
                                      <MapPin size={10} color="var(--muted)" />
                                      <div style={{ flex: 1 }}>
                                        <div style={{ fontSize: '12px', color: 'var(--text)', fontWeight: 500 }}>{p.address}</div>
                                        <div style={{ fontSize: '10px', color: 'var(--muted)' }}>{[p.property_type, p.city, p.state].filter(Boolean).join(' · ')}</div>
                                      </div>
                                      <Edit2 size={10} color="var(--muted)" />
                                    </div>
                                  ))}
                                </div>
                              )}
                              {bExpanded && bProps.length === 0 && (
                                <div style={{ padding: '4px 12px 10px 30px', fontSize: '11px', color: 'var(--muted)', fontStyle: 'italic' }}>No properties yet. Click + to add one.</div>
                              )}
                            </div>
                          )
                        })}

                        {addingBorrowerTo === source.id ? (
                          <div style={{ background: 'var(--surface2)', border: '1px solid #2563eb', borderRadius: '8px', padding: '10px' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '6px', marginBottom: '8px' }}>
                              <input placeholder="First name *" value={newBorrower.first_name} onChange={e => setNewBorrower(b => ({ ...b, first_name: e.target.value }))} style={IS} />
                              <input placeholder="Last name" value={newBorrower.last_name} onChange={e => setNewBorrower(b => ({ ...b, last_name: e.target.value }))} style={IS} />
                              <input placeholder="Company" value={newBorrower.company} onChange={e => setNewBorrower(b => ({ ...b, company: e.target.value }))} style={IS} />
                              <input placeholder="Email" value={newBorrower.email} onChange={e => setNewBorrower(b => ({ ...b, email: e.target.value }))} style={IS} />
                              <input placeholder="Phone" value={newBorrower.phone} onChange={e => setNewBorrower(b => ({ ...b, phone: e.target.value }))} style={IS} />
                            </div>
                            <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                              <button onClick={() => { setAddingBorrowerTo(null); setNewBorrower({ first_name: '', last_name: '', company: '', email: '', phone: '' }) }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '5px 12px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600 }}>CANCEL</button>
                              <button onClick={() => createBorrower(source.id)} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '5px 14px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }}>ADD</button>
                            </div>
                          </div>
                        ) : (
                          <button onClick={() => setAddingBorrowerTo(source.id)} style={{ background: 'transparent', border: '1px dashed var(--border)', color: 'var(--muted)', padding: '8px', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px' }}
                            onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.color = '#2563eb' }}
                            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
                            <Plus size={11} /> ADD BORROWER UNDER {source.first_name.toUpperCase()}
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}

              {orphanBorrowers.length > 0 && (
                <div style={{ background: 'var(--surface)', border: '1px dashed var(--border)', borderRadius: '10px', padding: '14px' }}>
                  <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>Unassigned Borrowers ({orphanBorrowers.length})</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {orphanBorrowers.map(b => {
                      const bProps = propsByBorrower[b.id] || []
                      return (
                        <div key={b.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'var(--surface2)', borderRadius: '6px' }}>
                          <Building2 size={12} color="var(--muted)" />
                          <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text)' }}>{b.first_name} {b.last_name || ''}{b.company ? (' — ' + b.company) : ''}</div>
                          </div>
                          <span style={{ fontSize: '9px', padding: '1px 6px', borderRadius: '3px', background: 'var(--surface)', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase' }}>{bProps.length} prop{bProps.length !== 1 ? 's' : ''}</span>
                          <button onClick={() => openAddProperty(b)} title="Add property" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}><Plus size={11} /></button>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {propModalOpen && <PropertyModal property={editingProp || (propModalBorrower ? { borrower_id: propModalBorrower.id } : null)} session={session} onClose={() => setPropModalOpen(false)} onSaved={fetchAll} />}
    </div>
  )
}

function Stat({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: 'var(--text)' }}>{value}</div>
    </div>
  )
}
