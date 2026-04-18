import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, Search, Upload, LayoutGrid, Network, ChevronDown, ChevronRight, Users, Building2, MapPin, Trash2, Edit2 } from 'lucide-react'
import ClientModal from './ClientModal'
import ClientCard from './ClientCard'
import ImportModal from './ImportModal'
import PropertyModal from './PropertyModal'
import { toastOk, toastErr } from '../lib/toast'

const FILTERS = ['All', 'Follow-up Due', 'Overdue', 'Borrower', 'Referral Source', 'Broker', 'Lender']

export default function Contacts({ session }) {
  const [mode, setMode] = useState('flat')
  const [clients, setClients] = useState([])
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('All')
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [importOpen, setImportOpen] = useState(false)
  // Hierarchy state
  const [expanded, setExpanded] = useState({})
  const [expandedBorrowers, setExpandedBorrowers] = useState({})
  const [addingBorrowerTo, setAddingBorrowerTo] = useState(null)
  const [newBorrower, setNewBorrower] = useState({ first_name: '', last_name: '', company: '', email: '', phone: '' })
  const [propModalOpen, setPropModalOpen] = useState(false)
  const [propModalBorrower, setPropModalBorrower] = useState(null)
  const [editingProp, setEditingProp] = useState(null)

  useEffect(() => {
    fetchAll()
    const ch = supabase.channel('contacts-rt').on('postgres_changes', { event: '*', schema: 'public', table: 'clients' }, fetchAll).subscribe()
    return () => supabase.removeChannel(ch)
  }, [])

  async function fetchAll() {
    const [c, p] = await Promise.all([
      supabase.from('clients').select('*').order('follow_up_date', { ascending: true, nullsFirst: false }),
      supabase.from('properties').select('*').order('address'),
    ])
    setClients(c.data || [])
    setProperties(p.data || [])
    setLoading(false)
  }

  async function deleteClient(id) {
    if (!window.confirm('Delete this contact?')) return
    const { error } = await supabase.from('clients').delete().eq('id', id)
    if (error) toastErr('Failed to delete: ' + error.message)
    else { toastOk('Contact deleted'); fetchAll() }
  }

  async function createBorrowerUnder(sourceId) {
    if (!newBorrower.first_name.trim()) return
    const { error } = await supabase.from('clients').insert({ ...newBorrower, client_type: 'Borrower', referral_source_id: sourceId, created_by: session.user.id })
    if (error) toastErr(error.message)
    else {
      toastOk('Borrower added')
      setNewBorrower({ first_name: '', last_name: '', company: '', email: '', phone: '' })
      setAddingBorrowerTo(null)
      fetchAll()
    }
  }

  async function removeBorrowerFromSource(borrowerId) {
    if (!window.confirm('Unlink this borrower from the referral source?')) return
    await supabase.from('clients').update({ referral_source_id: null }).eq('id', borrowerId)
    toastOk('Unlinked from source')
    fetchAll()
  }

  function openAddProperty(borrower) { setPropModalBorrower(borrower); setEditingProp(null); setPropModalOpen(true) }
  function openEditProperty(property) { setEditingProp(property); setPropModalBorrower(null); setPropModalOpen(true) }

  const today = new Date().toISOString().split('T')[0]
  const filtered = clients.filter(c => {
    const name = ((c.first_name || '') + ' ' + (c.last_name || '') + ' ' + (c.company || '')).toLowerCase()
    if (search && !name.includes(search.toLowerCase())) return false
    if (filter === 'Follow-up Due') return c.follow_up_date === today
    if (filter === 'Overdue') return c.follow_up_date && c.follow_up_date < today
    if (filter === 'Borrower') return c.client_type === 'Borrower'
    if (filter === 'Referral Source') return c.client_type === 'Referral Source'
    if (filter === 'Broker') return c.client_type === 'Broker'
    if (filter === 'Lender') return c.client_type === 'Lender'
    return true
  })
  const overdueCount = clients.filter(c => c.follow_up_date && c.follow_up_date < today).length
  const dueTodayCount = clients.filter(c => c.follow_up_date === today).length

  // Hierarchy data
  const referralSources = clients.filter(c => c.client_type === 'Referral Source')
  const borrowers = clients.filter(c => c.client_type === 'Borrower')
  const borrowersBySource = Object.fromEntries(referralSources.map(s => [s.id, borrowers.filter(b => b.referral_source_id === s.id)]))
  const orphanBorrowers = borrowers.filter(b => !b.referral_source_id)
  const propsByBorrower = Object.fromEntries(borrowers.map(b => [b.id, properties.filter(p => p.borrower_id === b.id)]))

  const IS = { background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '5px', padding: '6px 9px', fontSize: '11px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* Toolbar */}
      <div className="toolbar stats-row" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Stat label="Total" value={clients.length} onClick={() => setFilter('All')} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Due Today" value={dueTodayCount} highlight={dueTodayCount > 0} onClick={() => setFilter('Follow-up Due')} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Overdue" value={overdueCount} danger={overdueCount > 0} onClick={() => setFilter('Overdue')} />
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          {/* View mode toggle */}
          <div style={{ display: 'flex', background: 'var(--surface2)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border)' }}>
            {[['flat', 'Grid', LayoutGrid], ['tree', 'Hierarchy', Network]].map(([m, label, Icon]) => (
              <button key={m} onClick={() => setMode(m)} title={label} style={{ background: mode === m ? 'var(--surface)' : 'transparent', boxShadow: mode === m ? '0 1px 2px rgba(0,0,0,0.05)' : 'none', border: 'none', padding: '5px 9px', borderRadius: '4px', color: mode === m ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '10px', textTransform: 'uppercase' }}>
                <Icon size={11} /> {label}
              </button>
            ))}
          </div>
          {mode === 'flat' && (
            <div style={{ position: 'relative' }}>
              <Search size={12} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted)' }} />
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search contacts..." style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px 6px 28px', fontSize: '12px', width: '180px' }} />
            </div>
          )}
          <button onClick={() => setImportOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', color: 'var(--muted)', border: '1px solid var(--border)', padding: '7px 12px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.color = '#2563eb' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
            <Upload size={12} /> IMPORT
          </button>
          <button onClick={() => { setEditing(null); setModalOpen(true) }} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#2563eb', color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
            <Plus size={13} strokeWidth={2.5} /> NEW CONTACT
          </button>
        </div>
      </div>

      {/* Filter pills (flat mode only) */}
      {mode === 'flat' && (
        <div style={{ display: 'flex', gap: '6px', padding: '10px 24px', background: 'var(--bg)', borderBottom: '1px solid var(--border)', flexShrink: 0, overflowX: 'auto' }}>
          {FILTERS.map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{ background: filter === f ? '#2563eb' : 'var(--surface)', color: filter === f ? '#fff' : 'var(--muted)', border: '1px solid ' + (filter === f ? '#2563eb' : 'var(--border)'), borderRadius: '20px', padding: '4px 12px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
              {f}
              {f === 'Overdue' && overdueCount > 0 && <span style={{ marginLeft: '5px', background: '#ef4444', color: '#fff', borderRadius: '9px', padding: '0 5px', fontSize: '9px' }}>{overdueCount}</span>}
            </button>
          ))}
        </div>
      )}

      {/* Content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 24px' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px' }}>LOADING...</div>
        ) : mode === 'flat' ? (
          filtered.length === 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '200px', color: 'var(--muted)', gap: '12px' }}>
              <div>No contacts found</div>
              {clients.length === 0 && (
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button onClick={() => setImportOpen(true)} style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--muted)', padding: '8px 16px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', cursor: 'pointer' }}>Import from Outlook</button>
                  <button onClick={() => { setEditing(null); setModalOpen(true) }} style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '8px 18px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer' }}>Add first contact</button>
                </div>
              )}
            </div>
          ) : (
            <div className="client-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '12px' }}>
              {filtered.map(client => (
                <ClientCard key={client.id} client={client} onEdit={() => { setEditing(client); setModalOpen(true) }} onDelete={() => deleteClient(client.id)} onRefresh={fetchAll} session={session} />
              ))}
            </div>
          )
        ) : (
          /* Hierarchy mode */
          <div style={{ maxWidth: '900px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {referralSources.length === 0 && orphanBorrowers.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)', fontSize: '13px' }}>
                No referral sources or borrowers yet. Add one using NEW CONTACT, set their type to "Referral Source" or "Borrower".
              </div>
            ) : (
              <>
                {referralSources.map(source => {
                  const srcBorrowers = borrowersBySource[source.id] || []
                  const isExpanded = expanded[source.id]
                  return (
                    <div key={source.id} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden' }}>
                      <div onClick={() => setExpanded(e => ({ ...e, [source.id]: !e[source.id] }))} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '14px 16px', cursor: 'pointer' }}>
                        {isExpanded ? <ChevronDown size={15} color="var(--muted)" /> : <ChevronRight size={15} color="var(--muted)" />}
                        <Users size={14} color="#2563eb" />
                        <div style={{ flex: 1 }}>
                          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)' }}>{source.first_name} {source.last_name || ''}</div>
                          {source.company && <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{source.company}</div>}
                        </div>
                        <span style={{ fontSize: '10px', padding: '2px 8px', borderRadius: '3px', background: '#eff6ff', color: '#1d4ed8', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase' }}>{srcBorrowers.length} borrower{srcBorrowers.length !== 1 ? 's' : ''}</span>
                      </div>
                      {isExpanded && (
                        <div style={{ padding: '12px 16px 16px 42px', borderTop: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {srcBorrowers.map(b => {
                            const bProps = propsByBorrower[b.id] || []
                            const bExpanded = expandedBorrowers[b.id]
                            return (
                              <div key={b.id} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 12px' }}>
                                  <button onClick={() => setExpandedBorrowers(e => ({ ...e, [b.id]: !e[b.id] }))} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}>{bExpanded ? <ChevronDown size={13} /> : <ChevronRight size={13} />}</button>
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
                                      <div key={p.id} onClick={() => openEditProperty(p)} style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 10px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '5px', cursor: 'pointer' }}>
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
                                {bExpanded && bProps.length === 0 && <div style={{ padding: '4px 12px 10px 30px', fontSize: '11px', color: 'var(--muted)', fontStyle: 'italic' }}>No properties yet. Click + to add.</div>}
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
                                <button onClick={() => createBorrowerUnder(source.id)} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '5px 14px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }}>ADD</button>
                              </div>
                            </div>
                          ) : (
                            <button onClick={() => setAddingBorrowerTo(source.id)} style={{ background: 'transparent', border: '1px dashed var(--border)', color: 'var(--muted)', padding: '8px', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px' }}>
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
        )}
      </div>

      {modalOpen && <ClientModal client={editing} session={session} onClose={() => setModalOpen(false)} onSaved={() => { toastOk(editing ? 'Contact updated' : 'Contact added'); fetchAll() }} />}
      {importOpen && <ImportModal session={session} onClose={() => setImportOpen(false)} onImported={() => { toastOk('Contacts imported'); fetchAll(); setImportOpen(false) }} />}
      {propModalOpen && <PropertyModal property={editingProp || (propModalBorrower ? { borrower_id: propModalBorrower.id } : null)} session={session} onClose={() => setPropModalOpen(false)} onSaved={() => { toastOk('Property saved'); fetchAll() }} />}
    </div>
  )
}

function Stat({ label, value, highlight, danger, onClick }) {
  return (
    <div onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }}>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: danger ? '#ef4444' : highlight ? '#2563eb' : 'var(--text)' }}>{value}</div>
    </div>
  )
}
