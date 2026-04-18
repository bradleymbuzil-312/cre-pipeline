import { useState, useRef, useEffect } from 'react'
import { Trash2, ChevronRight, Building2, Calendar, MoreHorizontal, GripVertical } from 'lucide-react'
import { STAGES } from '../lib/constants'
import { formatCurrency, formatDate } from '../lib/format'

export default function DealCard({ deal, onEdit, onDelete, onUpdateStage, onDragStart, onDragEnd, isDragging }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)
  const currentIdx = STAGES.indexOf(deal.stage)
  const canAdvance = currentIdx < STAGES.length - 1

  useEffect(() => {
    function handleClick(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false)
    }
    if (menuOpen) document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [menuOpen])

  return (
    <div
      draggable
      onDragStart={e => { e.dataTransfer.effectAllowed = 'move'; onDragStart?.(deal) }}
      onDragEnd={() => onDragEnd?.()}
      className={isDragging ? 'deal-card-dragging' : ''}
      style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', padding: '11px 12px', transition: 'border-color 0.15s, box-shadow 0.15s, opacity 0.15s' }}
      onMouseEnter={e => { if (!isDragging) { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.06)' } }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '7px', gap: '4px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '4px', flex: 1, minWidth: 0 }}>
          <GripVertical size={12} color="var(--muted)" style={{ flexShrink: 0, marginTop: '2px', cursor: 'grab', opacity: 0.5 }} />
          <div onClick={() => onEdit(deal)} title="Click to open deal"
            style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: 'var(--text)', lineHeight: 1.3, flex: 1, cursor: 'pointer', transition: 'color 0.15s' }}
            onMouseEnter={e => e.currentTarget.style.color = '#2563eb'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--text)'}>
            {deal.borrower_name}
          </div>
        </div>
        <div ref={menuRef} style={{ position: 'relative', flexShrink: 0 }}>
          <button onClick={() => setMenuOpen(o => !o)} style={{ background: 'transparent', border: 'none', color: 'var(--muted)', cursor: 'pointer', padding: '1px 3px', display: 'flex', alignItems: 'center', borderRadius: '4px' }}
            onMouseEnter={e => e.currentTarget.style.color = 'var(--text)'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--muted)'}>
            <MoreHorizontal size={14} />
          </button>
          {menuOpen && (
            <div style={{ position: 'absolute', right: 0, top: 'calc(100% + 4px)', zIndex: 200, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '7px', overflow: 'hidden', minWidth: '130px', boxShadow: '0 8px 32px rgba(0,0,0,0.12)' }}>
              <MenuItem icon={Trash2} label="Delete deal" danger onClick={() => { onDelete(deal.id); setMenuOpen(false) }} />
            </div>
          )}
        </div>
      </div>

      {(deal.property_address || deal.property_type) && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '7px', paddingLeft: '16px' }}>
          <Building2 size={10} color="var(--muted)" style={{ flexShrink: 0 }} />
          <span style={{ fontSize: '11px', color: 'var(--muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {[deal.property_type, deal.property_address].filter(Boolean).join(' · ')}
          </span>
        </div>
      )}

      <div style={{ fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600, fontSize: '15px', color: '#2563eb', marginBottom: '7px', letterSpacing: '-0.02em', paddingLeft: '16px' }}>
        {formatCurrency(deal.loan_amount)}
      </div>

      {(deal.ltv || deal.dscr || deal.commission_fee) && (
        <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginBottom: '7px', paddingLeft: '16px' }}>
          {deal.ltv && <Chip>{deal.ltv}% LTV</Chip>}
          {deal.dscr && <Chip>{parseFloat(deal.dscr).toFixed(2)}x DSCR</Chip>}
          {deal.commission_fee && <Chip gold>Fee: {formatCurrency(deal.commission_fee)}</Chip>}
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingLeft: '16px' }}>
        <span style={{ fontSize: '11px', color: 'var(--muted)', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
          {deal.lender_name || ''}
        </span>
        {deal.expected_close_date && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '3px', flexShrink: 0 }}>
            <Calendar size={9} color="var(--muted)" />
            <span style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>
              {formatDate(deal.expected_close_date)}
            </span>
          </div>
        )}
      </div>

      {canAdvance && (
        <button onClick={() => onUpdateStage(deal.id, STAGES[currentIdx + 1])} style={{ marginTop: '9px', marginLeft: '16px', width: 'calc(100% - 16px)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '3px', background: 'transparent', border: '1px solid var(--border)', borderRadius: '5px', color: 'var(--muted)', fontSize: '10px', padding: '4px 8px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.03em', transition: 'all 0.15s' }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.color = '#2563eb'; e.currentTarget.style.background = '#eff6ff' }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.background = 'transparent' }}>
          Move to {STAGES[currentIdx + 1]} <ChevronRight size={9} />
        </button>
      )}
    </div>
  )
}

function MenuItem({ icon: Icon, label, onClick, danger }) {
  return (
    <button onClick={onClick} style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%', padding: '9px 13px', background: 'transparent', border: 'none', color: danger ? '#ef4444' : 'var(--text)', fontSize: '12px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', fontWeight: 500, textAlign: 'left' }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
      <Icon size={12} /> {label}
    </button>
  )
}

function Chip({ children, gold }) {
  return (
    <span style={{ fontSize: '10px', padding: '2px 6px', borderRadius: '3px', background: gold ? '#eff6ff' : 'var(--surface2)', border: '1px solid ' + (gold ? '#bfdbfe' : 'var(--border)'), color: gold ? '#1d4ed8' : 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>
      {children}
    </span>
  )
}
