import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, Search, Upload } from 'lucide-react'
import ClientModal from './ClientModal'
import ClientCard from './ClientCard'
import ImportModal from './ImportModal'

const FILTERS = ['All', 'Follow-up Due', 'Overdue', 'Borrower', 'Referral Source', 'Broker', 'Lender']

export default function Clients({ session, defaultType }) {
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState(defaultType || 'All')
  const [modalOpen, setModalOpen] = useState(false)
  const [editingClient, setEditingClient] = useState(null)
  const [importOpen, setImportOpen] = useState(false)

  useEffect(() => {
    fetchClients()
    const channel = supabase.channel('clients-realtime').on('postgres_changes', { event: '*', schema: 'public', table: 'clients' }, fetchClients).subscribe()
    return () => supabase.removeChannel(channel)
  }, [])

  async function fetchClients() {
    const { data } = await supabase.from('clients').select('*').order('follow_up_date', { ascending: true, nullsFirst: false })
    setClients(data || [])
    setLoading(false)
  }

  async function deleteClient(id) {
    if (!window.confirm('Delete this client?')) return
    await supabase.from('clients').delete().eq('id', id)
    fetchClients()
  }

  const today = new Date().toISOString().split('T')[0]
  const filtered = clients.filter(c => {
    const name = (c.first_name + ' ' + (c.last_name || '') + ' ' + (c.company || '')).toLowerCase()
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
  const BLUE = '#2563eb'

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Stat label="Total Clients" value={clients.length} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Due Today" value={dueTodayCount} highlight={dueTodayCount > 0} />
          <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} />
          <Stat label="Overdue" value={overdueCount} danger={overdueCount > 0} />
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexShrink: 0 }}>
          <div style={{ position: 'relative' }}>
            <Search size={12} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted)' }} />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search clients..."
              style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px 6px 28px', fontSize: '12px', width: '180px', fontFamily: 'DM Sans, sans-serif' }} />
          </div>
          <button onClick={() => setImportOpen(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', color: 'var(--muted)', border: '1px solid var(--border)', padding: '7px 12px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = BLUE; e.currentTarget.style.color = BLUE }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
            <Upload size={12} /> IMPORT FROM OUTLOOK
          </button>
          <button onClick={() => { setEditingClient(null); setModalOpen(true) }}
            style={{ display: 'flex', alignItems: 'center', gap: '6px', background: BLUE, color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
            <Plus size={13} strokeWidth={2.5} /> NEW CLIENT
          </button>
        </div>
      </div>
      <div style={{ display: 'flex', gap: '6px', padding: '10px 24px', background: 'var(--bg)', borderBottom: '1px solid var(--border)', flexShrink: 0, overflowX: 'auto' }}>
        {FILTERS.map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{ background: filter === f ? BLUE : 'var(--surface)', color: filter === f ? '#fff' : 'var(--muted)', border: '1px solid ' + (filter === f ? BLUE : 'var(--border)'), borderRadius: '20px', padding: '4px 12px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', letterSpacing: '0.04em', whiteSpace: 'nowrap', transition: 'all 0.15s' }}>
            {f}{f === 'Overdue' && overdueCount > 0 && <span style={{ marginLeft: '5px', background: '#ef4444', color: '#fff', borderRadius: '9px', padding: '0 5px', fontSize: '9px' }}>{overdueCount}</span>}
          </button>
        ))}
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 24px' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px' }}>LOADING CLIENTS...</div>
        ) : filtered.length === 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '200px', color: 'var(--muted)', gap: '12px' }}>
            <div>No clients found</div>
            {clients.length === 0 && (
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={() => setImportOpen(true)} style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--muted)', padding: '8px 16px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Upload size={12} /> Import from Outlook
                </button>
                <button onClick={() => { setEditingClient(null); setModalOpen(true) }} style={{ background: BLUE, color: '#fff', border: 'none', padding: '8px 18px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer' }}>
                  Add first client
                </button>
              </div>
            )}
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '12px' }}>
            {filtered.map(client => (
              <ClientCard key={client.id} client={client} onEdit={() => { setEditingClient(client); setModalOpen(true) }} onDelete={() => deleteClient(client.id)} onRefresh={fetchClients} session={session} />
            ))}
          </div>
        )}
      </div>
      {modalOpen && <ClientModal client={editingClient} session={session} onClose={() => setModalOpen(false)} onSaved={fetchClients} />}
      {importOpen && <ImportModal session={session} onClose={() => setImportOpen(false)} onImported={() => { fetchClients(); setImportOpen(false) }} />}
    </div>
  )
}

function Stat({ label, value, highlight, danger }) {
  return (
    <div>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: danger ? '#ef4444' : highlight ? '#2563eb' : 'var(--text)' }}>{value}</div>
    </div>
  )
}
