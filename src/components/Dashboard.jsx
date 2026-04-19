import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Briefcase, DollarSign, Clock, AlertCircle, CheckCircle, ArrowRight, Calendar } from 'lucide-react'
import { formatCurrency, formatDate } from '../lib/format'

export default function Dashboard({ session, setView }) {
  const [deals, setDeals] = useState([])
  const [tasks, setTasks] = useState([])
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchAll() }, [])

  async function fetchAll() {
    const [d, t, c] = await Promise.all([
      supabase.from('deals').select('*').order('expected_close_date', { ascending: true, nullsFirst: false }),
      supabase.from('tasks').select('*').order('due_date', { ascending: true, nullsFirst: false }),
      supabase.from('clients').select('*').order('follow_up_date', { ascending: true, nullsFirst: false }),
    ])
    setDeals(d.data || [])
    setTasks(t.data || [])
    setClients(c.data || [])
    setLoading(false)
  }

  const today = new Date().toISOString().split('T')[0]
  const in30 = new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0]

  const activeDeals = deals.filter(d => d.stage !== 'Funded / Closed')
  const pipelineVolume = activeDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
  const pendingFees = activeDeals.reduce((s, d) => s + (d.commission_fee || 0), 0)
  const ytdStart = new Date(new Date().getFullYear(), 0, 1).toISOString().split('T')[0]
  const ytdFundedDeals = deals.filter(d => d.stage === 'Funded / Closed' && (d.updated_at || '').split('T')[0] >= ytdStart)
  const ytdClosedVolume = ytdFundedDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
  const ytdFeesEarned = ytdFundedDeals.reduce((s, d) => s + (d.commission_fee || 0), 0)
  const blendedFeeRate = ytdClosedVolume > 0 ? (ytdFeesEarned / ytdClosedVolume) * 100 : 0
  const closingThisMonth = deals.filter(d => d.expected_close_date && d.expected_close_date >= today && d.expected_close_date <= in30 && d.stage !== 'Funded / Closed')

  const tasksDueToday = tasks.filter(t => t.due_date === today && t.status !== 'Done')
  const tasksOverdue = tasks.filter(t => t.due_date && t.due_date < today && t.status !== 'Done')
  const followUpsOverdue = clients.filter(c => c.follow_up_date && c.follow_up_date < today)
  const followUpsToday = clients.filter(c => c.follow_up_date === today)

  if (loading) return <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px', letterSpacing: '0.1em' }}>LOADING DASHBOARD...</div>

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '24px', background: 'var(--bg)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ marginBottom: '20px' }}>
          <h1 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '22px', color: 'var(--text)', marginBottom: '4px' }}>Good {greet()}, {(session.user.user_metadata?.display_name || session.user.email.split('@')[0]).split('.')[0]}</h1>
          <div style={{ fontSize: '13px', color: 'var(--muted)' }}>{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}</div>
        </div>

        {/* KPI Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginBottom: '24px' }}>
          <KpiCard Icon={CheckCircle} label="YTD Closed Volume" value={formatCurrency(ytdClosedVolume)} sublabel={ytdFundedDeals.length + ' deal' + (ytdFundedDeals.length !== 1 ? 's' : '') + ' funded'} accent />
          <KpiCard Icon={DollarSign} label="YTD Fees Earned" value={formatCurrency(ytdFeesEarned)} sublabel={'blended ' + blendedFeeRate.toFixed(2) + '%'} />
          <KpiCard Icon={Briefcase} label="Active Deals" value={activeDeals.length} onClick={() => setView('active')} />
          <KpiCard Icon={DollarSign} label="Pipeline Volume" value={formatCurrency(pipelineVolume)} accent />
          <KpiCard Icon={CheckCircle} label="Pending Fees" value={formatCurrency(pendingFees)} />
          <KpiCard Icon={Clock} label="Closing in 30d" value={closingThisMonth.length} onClick={() => setView('active')} highlight={closingThisMonth.length > 0} />
        </div>

        {/* Two column layout */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '16px' }}>

          {/* Tasks needing attention */}
          <Panel title="Needs Attention" count={tasksDueToday.length + tasksOverdue.length + followUpsOverdue.length + followUpsToday.length}>
            {tasksOverdue.length === 0 && tasksDueToday.length === 0 && followUpsOverdue.length === 0 && followUpsToday.length === 0 ? (
              <EmptyState>All caught up — no overdue items.</EmptyState>
            ) : (
              <>
                {tasksOverdue.map(t => (
                  <Row key={'to-' + t.id} onClick={() => setView('tasks')}>
                    <AlertCircle size={13} color="#ef4444" style={{ flexShrink: 0 }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{t.title}</div>
                      <div style={{ fontSize: '11px', color: '#ef4444' }}>Overdue since {formatDate(t.due_date)}{t.assigned_to ? ' · ' + t.assigned_to : ''}</div>
                    </div>
                    <ArrowRight size={12} color="var(--muted)" />
                  </Row>
                ))}
                {tasksDueToday.map(t => (
                  <Row key={'td-' + t.id} onClick={() => setView('tasks')}>
                    <Clock size={13} color="#c2410c" style={{ flexShrink: 0 }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{t.title}</div>
                      <div style={{ fontSize: '11px', color: '#c2410c' }}>Due today{t.assigned_to ? ' · ' + t.assigned_to : ''}</div>
                    </div>
                    <ArrowRight size={12} color="var(--muted)" />
                  </Row>
                ))}
                {followUpsOverdue.slice(0, 4).map(c => (
                  <Row key={'fo-' + c.id} onClick={() => setView('clients')}>
                    <AlertCircle size={13} color="#ef4444" style={{ flexShrink: 0 }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 500 }}>{c.first_name} {c.last_name || ''}</div>
                      <div style={{ fontSize: '11px', color: '#ef4444' }}>Follow-up overdue since {formatDate(c.follow_up_date)}</div>
                    </div>
                    <ArrowRight size={12} color="var(--muted)" />
                  </Row>
                ))}
                {followUpsToday.map(c => (
                  <Row key={'ft-' + c.id} onClick={() => setView('clients')}>
                    <Clock size={13} color="#c2410c" style={{ flexShrink: 0 }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 500 }}>{c.first_name} {c.last_name || ''}</div>
                      <div style={{ fontSize: '11px', color: '#c2410c' }}>Follow-up due today</div>
                    </div>
                    <ArrowRight size={12} color="var(--muted)" />
                  </Row>
                ))}
              </>
            )}
          </Panel>

          {/* Closing soon */}
          <Panel title="Closing Soon (30 days)" count={closingThisMonth.length}>
            {closingThisMonth.length === 0 ? (
              <EmptyState>No deals closing in the next 30 days.</EmptyState>
            ) : (
              closingThisMonth.slice(0, 6).map(d => (
                <Row key={d.id} onClick={() => setView('active')}>
                  <Calendar size={13} color="#2563eb" style={{ flexShrink: 0 }} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{d.borrower_name}{d.property_address ? ' — ' + d.property_address : ''}</div>
                    <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{formatCurrency(d.loan_amount)} · {d.stage} · {formatDate(d.expected_close_date)}</div>
                  </div>
                  <ArrowRight size={12} color="var(--muted)" />
                </Row>
              ))
            )}
          </Panel>

          {/* Pipeline by stage */}
          <Panel title="Pipeline by Stage" full>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {['Underwriting', 'Packaging', 'Engagement', 'LOI / Term Sheet', 'Due Diligence', 'Closing'].map(stage => {
                const stageDeals = activeDeals.filter(d => d.stage === stage)
                const vol = stageDeals.reduce((s, x) => s + (x.loan_amount || 0), 0)
                const pct = pipelineVolume > 0 ? (vol / pipelineVolume * 100) : 0
                return (
                  <div key={stage} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '12px' }}>
                    <div style={{ width: '120px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', fontSize: '10px', letterSpacing: '0.04em' }}>{stage}</div>
                    <div style={{ flex: 1, height: '20px', background: 'var(--surface2)', borderRadius: '4px', position: 'relative', overflow: 'hidden' }}>
                      <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: pct + '%', background: '#2563eb', transition: 'width 0.3s' }} />
                      <div style={{ position: 'absolute', left: '8px', top: '50%', transform: 'translateY(-50%)', fontSize: '11px', color: pct > 40 ? '#fff' : 'var(--text)', fontWeight: 600, fontFamily: 'IBM Plex Mono, monospace' }}>{stageDeals.length} {stageDeals.length === 1 ? 'deal' : 'deals'}</div>
                    </div>
                    <div style={{ width: '100px', textAlign: 'right', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--text)', fontWeight: 600 }}>{formatCurrency(vol)}</div>
                  </div>
                )
              })}
            </div>
          </Panel>
        </div>
      </div>
    </div>
  )
}

function greet() {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
}

function KpiCard({ Icon, label, value, sublabel, accent, highlight, onClick }) {
  return (
    <div onClick={onClick} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '16px', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s' }}
      onMouseEnter={e => { if (onClick) { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.boxShadow = '0 4px 12px rgba(37,99,235,0.08)' } }}
      onMouseLeave={e => { if (onClick) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' } }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</span>
        <Icon size={14} color={accent || highlight ? '#2563eb' : 'var(--muted)'} />
      </div>
      <div style={{ fontSize: '22px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: accent || highlight ? '#2563eb' : 'var(--text)' }}>{value}</div>
      {sublabel && <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', marginTop: '4px', letterSpacing: '0.04em' }}>{sublabel}</div>}
    </div>
  )
}

function Panel({ title, count, children, full }) {
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden', gridColumn: full ? '1 / -1' : 'auto' }}>
      <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{title}</span>
        {count !== undefined && count > 0 && <span style={{ background: '#2563eb', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }}>{count}</span>}
      </div>
      <div style={{ padding: '10px', display: 'flex', flexDirection: 'column', gap: '4px' }}>{children}</div>
    </div>
  )
}

function Row({ children, onClick }) {
  return (
    <div onClick={onClick} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 10px', borderRadius: '6px', cursor: onClick ? 'pointer' : 'default', transition: 'background 0.12s' }}
      onMouseEnter={e => { if (onClick) e.currentTarget.style.background = 'var(--surface2)' }}
      onMouseLeave={e => { if (onClick) e.currentTarget.style.background = 'transparent' }}>
      {children}
    </div>
  )
}

function EmptyState({ children }) {
  return <div style={{ padding: '14px', color: 'var(--muted)', fontSize: '12px', textAlign: 'center' }}>{children}</div>
}
