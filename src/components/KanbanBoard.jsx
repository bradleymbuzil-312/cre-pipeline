import { STAGES as DEFAULT_STAGES, STAGE_COLORS } from '../lib/constants'
import { formatCurrency } from '../lib/format'
import DealCard from './DealCard'

export default function KanbanBoard({ deals, onEdit, onDelete, onUpdateStage, stages }) {
  const stageList = stages || DEFAULT_STAGES
  return (
    <div style={{ display: 'flex', gap: '12px', padding: '16px 20px', overflowX: 'auto', overflowY: 'hidden', height: '100%', alignItems: 'flex-start' }}>
      {stageList.map(stage => {
        const stageDeals = deals.filter(d => d.stage === stage)
        const volume = stageDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
        const colors = STAGE_COLORS[stage] || { bg: '#f1f5f9', border: '#cbd5e1', text: '#64748b' }
        return (
          <div key={stage} style={{ minWidth: '268px', maxWidth: '268px', display: 'flex', flexDirection: 'column', height: 'calc(100vh - 168px)' }}>
            <div style={{ padding: '9px 12px', marginBottom: '8px', background: colors.bg, border: '1px solid ' + colors.border, borderRadius: '7px', flexShrink: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', color: colors.text, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{stage}</span>
                <span style={{ background: colors.border, color: colors.text, borderRadius: '9px', padding: '1px 7px', fontSize: '11px', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600 }}>{stageDeals.length}</span>
              </div>
              {volume > 0 && <div style={{ fontSize: '11px', color: colors.text, opacity: 0.7, fontFamily: 'IBM Plex Mono, monospace', marginTop: '3px' }}>{formatCurrency(volume)}</div>}
            </div>
            <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '7px', paddingBottom: '8px' }}>
              {stageDeals.length === 0 ? (
                <div style={{ border: '1px dashed var(--border)', borderRadius: '7px', padding: '24px 12px', textAlign: 'center', color: 'var(--muted)', fontSize: '12px', opacity: 0.5 }}>No deals</div>
              ) : (
                stageDeals.map(deal => <DealCard key={deal.id} deal={deal} onEdit={onEdit} onDelete={onDelete} onUpdateStage={onUpdateStage} />)
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
