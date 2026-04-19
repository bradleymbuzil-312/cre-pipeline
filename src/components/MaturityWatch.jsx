import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Clock, AlertCircle, ExternalLink } from 'lucide-react'

function fmtMoney(n) {
  if (!n) return '\u2014'
  if (n >= 1e9) return '$' + (n/1e9).toFixed(2) + 'B'
  if (n >= 1e6) return '$' + (n/1e6).toFixed(2) + 'M'
  if (n >= 1e3) return '$' + (n/1e3).toFixed(0) + 'K'
  return '$' + n
}

function daysUntil(dateStr) {
  const t = new Date(dateStr + 'T00:00:00').getTime() - Date.now()
  return Math.ceil(t / 86400000)
}

export default function MaturityWatch({ session, setView }) {
  const [deals, setDeals] = useState([])
  const [loading, setLoading] = useState(true)
  const [monthWindow, setMonthWindow] = useState(12)

  useEffect(() => { fetchDeals() }, [monthWindow])

  async function fetchDeals() {
    setLoading(true)
    const cutoff = new Date()
    cutoff.setMonth(cutoff.getMonth() + monthWindow)
    const cutoffStr = cutoff.toISOString().split('T')[0]
    const { data } = await supabase.from('deals').select('id, borrower_name, property_address, city, state_province, loan_amount, maturity_date, lender_name, stage, capital_type, interest_rate').lte('maturity_date', cutoffStr).not('maturity_date', 'is', null).order('maturity_date')
    setDeals(data || [])
    setLoading(false)
  }

  const now = new Date()
  const overdue = deals.filter(d => new Date(d.maturity_date + 'T00:00:00') < now)
  const soon = deals.filter(d => { const dy = daysUntil(d.maturity_date); return dy >= 0 && dy <= 90 })
  const later = deals.filter(d => { const dy = daysUntil(d.maturity_date); return dy > 90 })

  const totalVolume = deals.reduce((s, d) => s + (d.loan_amount || 0), 0)

  return (
    <div style={{ padding: '20px 24px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '22px', color: 'var(--text)', marginBottom: '2px' }}>Maturity Watch</h1>
          <div style={{ fontSize: '12px', color: 'var(--muted)' }}>{deals.length} loan{deals.length !== 1 ? 's' : ''} maturing in the next {monthWindow} months \u00b7 {fmtMoney(totalVolume)} total volume</div>
        </div>
        <select value={monthWindow} onChange={e => setMonthWindow(parseInt(e.target.value))} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '7px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif' }}>
          <option value={3}>Next 3 months</option>
          <option value={6}>Next 6 months</option>
          <option value={12}>Next 12 months</option>
          <option value={24}>Next 24 months</option>
        </select>
      </div>

      {loading ? (
        <div style={{ fontSize: '12px', color: 'var(--muted)', padding: '40px', textAlign: 'center', fontFamily: 'IBM Plex Mono, monospace' }}>LOADING...</div>
      ) : deals.length === 0 ? (
        <div style={{ fontSize: '13px', color: 'var(--muted)', padding: '40px', textAlign: 'center', background: 'var(--surface2)', borderRadius: '8px', border: '1px dashed var(--border)' }}>No loans maturing in the next {monthWindow} months.</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {overdue.length > 0 && <Section title="Overdue" count={overdue.length} deals={overdue} color="#ef4444" icon={AlertCircle} />}
          {soon.length > 0 && <Section title="Maturing in 90 days" count={soon.length} deals={soon} color="#c2410c" icon={Clock} />}
          {later.length > 0 && <Section title="Later this year" count={later.length} deals={later} color="#2563eb" icon={Clock} />}
        </div>
      )}
    </div>
  )
}

function Section({ title, count, deals, color, icon: Icon }) {
  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
        <Icon size={15} color={color} />
        <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: color, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{title}</h2>
        <span style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>({count})</span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '10px' }}>
        {deals.map(d => <DealRow key={d.id} deal={d} color={color} />)}
      </div>
    </div>
  )
}

function DealRow({ deal, color }) {
  const days = daysUntil(deal.maturity_date)
  const dateStr = new Date(deal.maturity_date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  const timeLabel = days < 0 ? Math.abs(days) + ' days overdue' : days === 0 ? 'Due today' : 'in ' + days + ' days'

  return (
    <div style={{ padding: '12px 14px', background: 'var(--surface)', border: '1px solid var(--border)', borderLeft: '3px solid ' + color, borderRadius: '6px', transition: 'border-color 0.15s' }}
         onMouseEnter={e => { e.currentTarget.style.background = 'var(--surface2)' }}
         onMouseLeave={e => { e.currentTarget.style.background = 'var(--surface)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '4px' }}>
        <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: 'var(--text)' }}>{deal.borrower_name}</div>
        <div style={{ fontSize: '12px', color: 'var(--text)', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600 }}>{fmtMoney(deal.loan_amount)}</div>
      </div>
      {deal.property_address && <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '4px' }}>{deal.property_address}{deal.city ? ', ' + deal.city : ''}{deal.state_province ? ', ' + deal.state_province : ''}</div>}
      <div style={{ display: 'flex', gap: '12px', fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', flexWrap: 'wrap' }}>
        <span>{dateStr}</span>
        <span style={{ color }}>{timeLabel}</span>
        {deal.lender_name && <span>{deal.lender_name}</span>}
        {deal.interest_rate && <span>{deal.interest_rate}%</span>}
      </div>
    </div>
  )
}