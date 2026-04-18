import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import KanbanBoard from './KanbanBoard'
import ListView from './ListView'
import DealModal from './DealModal'
import { LayoutGrid, List, Plus } from 'lucide-react'
import { formatCurrency } from '../lib/format'
import { STAGES } from '../lib/constants'

export default function Pipeline({ session, stages, title }) {
  const stageList = stages || STAGES
  const [deals, setDeals] = useState([])
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('kanban')
  const [modalOpen, setModalOpen] = useState(false)
  const [editingDeal, setEditingDeal] = useState(null)

  useEffect(() => {
    fetchDeals()
    const channel = supabase.channel('deals-realtime-' + (title || 'all'))
      .on('postgres_changes', { event: '*', schema: 'public', table: 'deals' }, () => fetchDeals())
      .subscribe()
    return () => supabase.removeChannel(channel)
  }, [])

  async function fetchDeals() {
    const { data, error } = await supabase.from('deals').select('*').order('created_at', { ascending: false })
    if (!error) setDeals(data || [])
    setLoading(false)
  }

  async function updateDeal(id, updates) {
    await supabase.from('deals').update({ ...updates, updated_at: new Date().toISOString() }).eq('id', id)
    fetchDeals()
  }

  async function deleteDeal(id) {
    if (!window.confirm('Delete this deal? This cannot be undone.')) return
    await supabase.from('deals').delete().eq('id', id)
    fetchDeals()
  }

  function openAdd() { setEditingDeal(null); setModalOpen(true) }
  function openEdit(deal) { setEditingDeal(deal); setModalOpen(true) }

  const filteredDeals = deals.filter(d => stageList.includes(d.stage))
  const totalVolume = filteredDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
  const totalFees = filteredDeals.filter(d => d.stage !== 'Funded / Closed').reduce((s, d) => s + (d.commission_fee || 0), 0)
  const activeDeals = filteredDeals.filter(d => d.stage !== 'Funded / Closed').length
  const closingDeals = filteredDeals.filter(d => d.stage === 'Closing').length

  const sharedProps = {
    deals: filteredDeals,
    onEdit: openEdit,
    onDelete: deleteDeal,
    onUpdateStage: (id, stage) => updateDeal(id, { stage }),
    stages: stageList,
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, gap: '16px' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          {title && <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)', paddingRight: '12px', borderRight: '1px solid var(--border)' }}>{title}</div>}
          <StatBadge label="Active" value={activeDeals} />
          <Divider />
          <StatBadge label="Volume" value={formatCurrency(totalVolume)} gold />
          <Divider />
          <StatBadge label="Pending Fees" value={formatCurrency(totalFees)} />
          <Divider />
          <StatBadge label="In Closing" value={closingDeals} highlight={closingDeals > 0} />
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexShrink: 0 }}>
          <ViewToggle view={view} setView={setView} />
          <button onClick={openAdd} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#2563eb', color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
            <Plus size={13} strokeWidth={2.5} /> NEW DEAL
          </button>
        </div>
      </div>
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px', letterSpacing: '0.1em' }}>LOADING PIPELINE...</div>
        ) : view === 'kanban' ? (
          <KanbanBoard {...sharedProps} />
        ) : (
          <ListView {...sharedProps} />
        )}
      </div>
      {modalOpen && <DealModal deal={editingDeal} session={session} onClose={() => setModalOpen(false)} onSaved={fetchDeals} />}
    </div>
  )
}

function StatBadge({ label, value, gold, highlight }) {
  return (
    <div>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: gold ? '#2563eb' : highlight ? '#0e7490' : 'var(--text)' }}>{value}</div>
    </div>
  )
}

function Divider() { return <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} /> }

function ViewToggle({ view, setView }) {
  return (
    <div style={{ display: 'flex', background: 'var(--surface2)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border)' }}>
      {[['kanban', LayoutGrid], ['list', List]].map(([v, Icon]) => (
        <button key={v} onClick={() => setView(v)} style={{ background: view === v ? 'var(--border)' : 'transparent', border: 'none', padding: '5px 9px', borderRadius: '4px', color: view === v ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
          <Icon size={14} />
        </button>
      ))}
    </div>
  )
}
