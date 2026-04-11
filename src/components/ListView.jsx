import { useState } from 'react'
import { Edit2, Trash2, ChevronUp, ChevronDown } from 'lucide-react'
import { STAGES, STAGE_COLORS } from '../lib/constants'
import { formatCurrency, formatDate, formatPct, formatDscr } from '../lib/format'

const COLUMNS = [
  { key: 'stage',               label: 'Stage',        width: 160,  },
  { key: 'borrower_name',       label: 'Borrower',     width: 160,  },
  { key: 'property_type',       label: 'Type',         width: 120,  },
  { key: 'property_address',    label: 'Address',      width: 200,  },
  { key: 'loan_amount',         label: 'Loan Amount',  width: 120, numeric: true },
  { key: 'ltv',                 label: 'LTV',          width: 70,  numeric: true },
  { key: 'dscr',                label: 'DSCR',         width: 70,  numeric: true },
  { key: 'lender_name',         label: 'Lender',       width: 150,  },
  { key: 'expected_close_date', label: 'Close Date',   width: 100,  },
  { key: 'commission_fee',      label: 'Fee',          width: 110, numeric: true },
]

export default function ListView({ deals, onEdit, onDelete, onUpdateStage }) {
  const [sortKey, setSortKey] = useState('stage')
  const [sortDir, setSortDir] = useState('asc')

  function handleSort(key) {
    if (sortKey === key) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortKey(key); setSortDir('asc') }
  }

  const sorted = [...deals].sort((a, b) => {
    let va = a[sortKey], vb = b[sortKey]
    if (sortKey === 'stage') { va = STAGES.indexOf(va); vb = STAGES.indexOf(vb) }
    if (va == null || va === '') return 1
    if (vb == null || vb === '') return -1
    const cmp = va < vb ? -1 : va > vb ? 1 : 0
    return sortDir === 'asc' ? cmp : -cmp
  })

  return (
    <div style={{ height: '100%', overflowY: 'auto', overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', minWidth: '1200px' }}>
        <thead style={{ position: 'sticky', top: 0, zIndex: 10, background: 'var(--surface)' }}>
          <tr style={{ borderBottom: '1px solid var(--border)' }}>
            {COLUMNS.map(col => (
              <th key={col.key} onClick={() => handleSort(col.key)} style={{
                padding: '10px 14px', textAlign: col.numeric ? 'right' : 'left',
                color: sortKey === col.key ? 'var(--gold)' : 'var(--muted)',
                fontFamily: 'Syne, sans-serif', fontWeight: 600,
                fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.08em',
                cursor: 'pointer', whiteSpace: 'nowrap', width: col.width,
                userSelect: 'none', transition: 'color 0.15s'
              }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '3px' }}>
                  {col.label}
                  {sortKey === col.key && (sortDir === 'asc' ? <ChevronUp size={10} /> : <ChevronDown size={10} />)}
                </span>
              </th>
            ))}
            <th style={{ width: 80, padding: '10px 14px' }}></th>
          </tr>
        </thead>
        <tbody>
          {sorted.length === 0 ? (
            <tr>
              <td colSpan={COLUMNS.length + 1} style={{ padding: '60px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
                No deals in pipeline. Click <strong style={{ color: 'var(--gold)' }}>NEW DEAL</strong> to add your first.
              </td>
            </tr>
          ) : sorted.map((deal, i) => {
            const colors = STAGE_COLORS[deal.stage]
            return (
              <tr key={deal.id}
                style={{ borderBottom: '1px solid var(--border)', background: 'transparent', transition: 'background 0.1s' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                {/* Stage dropdown */}
                <td style={{ padding: '9px 14px' }}>
                  <select value={deal.stage} onChange={e => onUpdateStage(deal.id, e.target.value)}
                    style={{
                      background: colors.bg, border: `1px solid ${colors.border}`,
                      color: colors.text, borderRadius: '5px', padding: '3px 7px',
                      fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700,
                      cursor: 'pointer', letterSpacing: '0.04em', textTransform: 'uppercase'
                    }}>
                    {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </td>
                <td style={{ padding: '9px 14px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: 'var(--text)', fontSize: '13px' }}>
                  {deal.borrower_name}
                </td>
                <td style={{ padding: '9px 14px', color: 'var(--muted)' }}>{deal.property_type || '—'}</td>
                <td style={{ padding: '9px 14px', color: 'var(--muted)', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {deal.property_address || '—'}
                </td>
                <td style={{ padding: '9px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600, color: 'var(--gold)', fontSize: '13px' }}>
                  {formatCurrency(deal.loan_amount)}
                </td>
                <td style={{ padding: '9px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)', fontSize: '12px' }}>
                  {formatPct(deal.ltv)}
                </td>
                <td style={{ padding: '9px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)', fontSize: '12px' }}>
                  {formatDscr(deal.dscr)}
                </td>
                <td style={{ padding: '9px 14px', color: 'var(--muted)' }}>{deal.lender_name || '—'}</td>
                <td style={{ padding: '9px 14px', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)', fontSize: '12px' }}>
                  {formatDate(deal.expected_close_date)}
                </td>
                <td style={{ padding: '9px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)', fontSize: '12px' }}>
                  {formatCurrency(deal.commission_fee)}
                </td>
                <td style={{ padding: '9px 14px' }}>
                  <div style={{ display: 'flex', gap: '5px', justifyContent: 'flex-end' }}>
                    <ActionBtn icon={Edit2} onClick={() => onEdit(deal)} title="Edit" />
                    <ActionBtn icon={Trash2} onClick={() => onDelete(deal.id)} danger title="Delete" />
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
        {sorted.length > 0 && (
          <tfoot>
            <tr style={{ borderTop: '1px solid var(--border)', background: 'var(--surface)' }}>
              <td colSpan={4} style={{ padding: '8px 14px', fontFamily: 'Syne, sans-serif', fontSize: '10px', color: 'var(--muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                {sorted.length} deals
              </td>
              <td style={{ padding: '8px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700, color: 'var(--gold)', fontSize: '13px' }}>
                {formatCurrency(sorted.reduce((s, d) => s + (d.loan_amount || 0), 0))}
              </td>
              <td colSpan={4} />
              <td style={{ padding: '8px 14px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600, color: 'var(--muted)', fontSize: '12px' }}>
                {formatCurrency(sorted.reduce((s, d) => s + (d.commission_fee || 0), 0))}
              </td>
              <td />
            </tr>
          </tfoot>
        )}
      </table>
    </div>
  )
}

function ActionBtn({ icon: Icon, onClick, danger, title }) {
  return (
    <button onClick={onClick} title={title} style={{
      background: 'transparent', border: '1px solid var(--border)',
      borderRadius: '4px', padding: '4px 6px', cursor: 'pointer',
      color: danger ? 'var(--danger)' : 'var(--muted)',
      display: 'flex', alignItems: 'center', transition: 'border-color 0.15s, background 0.15s'
    }}
    onMouseEnter={e => { e.currentTarget.style.borderColor = danger ? 'var(--danger)' : 'var(--border-hover)'; e.currentTarget.style.background = danger ? 'rgba(248,81,73,0.08)' : 'var(--surface2)' }}
    onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'transparent' }}
    >
      <Icon size={12} />
    </button>
  )
}
