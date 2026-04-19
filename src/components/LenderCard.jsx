import { Edit2, Trash2, Phone, Mail, Building2 } from 'lucide-react'

export default function LenderCard({ lender, onEdit, onDelete }) {
  const boxParts = []
  if (lender.asset_types?.length) boxParts.push(lender.asset_types.slice(0, 3).join(', ') + (lender.asset_types.length > 3 ? ' +' + (lender.asset_types.length - 3) : ''))
  if (lender.geographies?.length) boxParts.push(lender.geographies.join(', '))

  const fmt = (n) => n ? '$' + (n >= 1e6 ? (n/1e6).toFixed(1) + 'M' : (n/1e3).toFixed(0) + 'K') : '\u2014'
  const loanRange = lender.min_loan || lender.max_loan ? fmt(lender.min_loan) + ' \u2013 ' + fmt(lender.max_loan) : null

  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '14px', transition: 'border-color 0.15s, box-shadow 0.15s' }}
         onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(37,99,235,0.08)' }}
         onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' }}>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)', marginBottom: '2px' }}>{lender.name}</div>
          {lender.type && <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>{lender.type}</div>}
        </div>
        <div style={{ display: 'flex', gap: '4px' }}>
          <button onClick={onEdit} title="Edit" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex' }}><Edit2 size={11} /></button>
          <button onClick={onDelete} title="Delete" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: '#ef4444', display: 'flex' }}><Trash2 size={11} /></button>
        </div>
      </div>

      {lender.contact_name && <div style={{ fontSize: '11px', color: 'var(--text)', marginBottom: '6px', fontWeight: 500 }}>{lender.contact_name}</div>}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '3px', marginBottom: '10px' }}>
        {lender.email && <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Mail size={10} color="var(--muted)" /><a href={`mailto:${lender.email}`} style={{ fontSize: '11px', color: 'var(--muted)', textDecoration: 'none' }}>{lender.email}</a></div>}
        {lender.phone && <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Phone size={10} color="var(--muted)" /><a href={`tel:${lender.phone}`} style={{ fontSize: '11px', color: 'var(--muted)', textDecoration: 'none' }}>{lender.phone}</a></div>}
      </div>

      {boxParts.length > 0 && (
        <div style={{ padding: '8px 10px', background: 'var(--surface2)', borderRadius: '5px', marginBottom: '8px' }}>
          {boxParts.map((p, i) => <div key={i} style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', lineHeight: 1.4 }}>{p}</div>)}
          <div style={{ display: 'flex', gap: '10px', marginTop: '5px', flexWrap: 'wrap' }}>
            {loanRange && <span style={{ fontSize: '10px', color: 'var(--text)', fontWeight: 600 }}>{loanRange}</span>}
            {lender.max_ltv && <span style={{ fontSize: '10px', color: 'var(--muted)' }}>LTV {lender.max_ltv}%</span>}
            {lender.min_dscr && <span style={{ fontSize: '10px', color: 'var(--muted)' }}>DSCR {lender.min_dscr}</span>}
            {lender.rate_spread && <span style={{ fontSize: '10px', color: 'var(--muted)' }}>{lender.rate_spread}</span>}
          </div>
        </div>
      )}

      {lender.notes && <div style={{ fontSize: '11px', color: 'var(--muted)', padding: '7px 9px', background: 'var(--surface2)', borderRadius: '5px', borderLeft: '2px solid var(--border)', lineHeight: 1.5 }}>{lender.notes}</div>}
    </div>
  )
}