import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, Search } from 'lucide-react'
import LenderCard from './LenderCard'
import LenderModal from './LenderModal'
import { useToast } from './Toast'

const LENDER_TYPES = ['Bank', 'Credit Union', 'Life Company', 'Agency', 'CMBS', 'Debt Fund', 'SBA', 'Bridge Lender', 'Private', 'Other']

export default function Lenders({ session }) {
  const [lenders, setLenders] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const { toast } = useToast()

  useEffect(() => { fetchLenders() }, [])

  async function fetchLenders() {
    const { data } = await supabase.from('lenders').select('*').order('name')
    setLenders(data || [])
    setLoading(false)
  }

  async function handleDelete(lender) {
    if (!window.confirm(`Delete lender "${lender.name}"? This cannot be undone.`)) return
    const { error } = await supabase.from('lenders').delete().eq('id', lender.id)
    if (error) { toast('Error deleting: ' + error.message, 'error'); return }
    toast('Lender deleted', 'success')
    fetchLenders()
  }

  const filtered = lenders.filter(l => {
    if (typeFilter && l.type !== typeFilter) return false
    if (search) {
      const q = search.toLowerCase()
      const fields = [l.name, l.type, l.contact_name, l.email, (l.geographies || []).join(' '), (l.asset_types || []).join(' ')].filter(Boolean).join(' ').toLowerCase()
      if (!fields.includes(q)) return false
    }
    return true
  })

  const IS = { background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '7px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif' }

  return (
    <div style={{ padding: '20px 24px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '22px', color: 'var(--text)', marginBottom: '2px' }}>Lenders</h1>
          <div style={{ fontSize: '12px', color: 'var(--muted)' }}>{lenders.length} total \u00b7 matching database for deal placement</div>
        </div>
        <button onClick={() => { setEditing(null); setModalOpen(true) }} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#2563eb', border: 'none', color: '#fff', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>
          <Plus size={13} /> NEW LENDER
        </button>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '16px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flex: 1, minWidth: '240px', maxWidth: '400px' }}>
          <Search size={13} color="var(--muted)" style={{ position: 'absolute', marginLeft: '10px', pointerEvents: 'none' }} />
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search lenders..." style={{ ...IS, paddingLeft: '30px', width: '100%' }} />
        </div>
        <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} style={{ ...IS, minWidth: '160px' }}>
          <option value="">All types</option>
          {LENDER_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      {loading ? (
        <div style={{ fontSize: '12px', color: 'var(--muted)', padding: '40px', textAlign: 'center', fontFamily: 'IBM Plex Mono, monospace' }}>LOADING LENDERS...</div>
      ) : filtered.length === 0 ? (
        <div style={{ fontSize: '13px', color: 'var(--muted)', padding: '40px', textAlign: 'center', background: 'var(--surface2)', borderRadius: '8px', border: '1px dashed var(--border)' }}>
          {lenders.length === 0 ? 'No lenders yet. Add your first lender to start building your matching database.' : 'No lenders match your filters.'}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '14px' }}>
          {filtered.map(l => <LenderCard key={l.id} lender={l} onEdit={() => { setEditing(l); setModalOpen(true) }} onDelete={() => handleDelete(l)} />)}
        </div>
      )}

      {modalOpen && <LenderModal lender={editing} session={session} onClose={() => setModalOpen(false)} onSaved={fetchLenders} />}
    </div>
  )
}