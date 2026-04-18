import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { formatCurrency } from '../lib/format'
import { STAGES, ACTIVE_STAGES, PROSPECTING_STAGES, STAGE_COLORS } from '../lib/constants'
import { Briefcase, Users, Building2, ClipboardList, AlertCircle, Calendar, Clock, ArrowRight, DollarSign } from 'lucide-react'

export default function Dashboard({ session, setView }) {
  const [deals, setDeals] = useState([])
  const [clients, setClients] = useState([])
  const [tasks, setTasks] = useState([])
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchAll() }, [])

  async function fetchAll() {
    const [d, c, t, p] = await Promise.all([
      supabase.from('deals').select('*'),
      supabase.from('clients').select('*'),
      supabase.from('tasks').select('*').neq('status', 'Done'),
      supabase.from('properties').select('id, address'),
    ])
    setDeals(d.data || [])
    setClients(c.data || [])
    setTasks(t.data || [])
    setProperties(p.data || [])
    setLoading(false)
  }

  const today = new Date().toISOString().split('T')[0]
  const in7Days = new Date(Date.now() + 7*24*60*60*1000).toISOString().split('T')[0]
  const in30Days = new Date(Date.now() + 30*24*60*60*1000).toISOString().split('T')[0]

  const activeDeals = deals.filter(d => d.stage !== 'Funded / Closed')
  const pipelineVolume = activeDeals.reduce((s, d) => s + (d.loan_amount || 0), 0)
  const pendingFees = activeDeals.reduce((s, d) => s + (d.commission_fee || 0), 0)
  const fundedThisYear = deals.filter(d => d.stage === 'Funded / Closed' && d.updated_at && d.updated_at.startsWith(new Date().getFullYear().toString()))
  const ytdFees = fundedThisYear.reduce((s, d) => s + (d.commission_fee || 0), 0)
  const ytdVolume = fundedThisYear.reduce((s, d) => s + (d.loan_amount || 0), 0)

  const closingThisWeek = activeDeals.filter(d => d.expected_close_date && d.expected_close_date >= today && d.expected_close_date <= in7Days).sort((a,b) => (a.expected_close_date||'').localeCompare(b.expected_close_date||''))
  const closingThisMonth = activeDeals.filter(d => d.expected_close_date && d.expected_close_date >= today && d.expected_close_date <= in30Days)

  const overdueFollowUps = clients.filter(c => c.follow_up_date && c.follow_up_date < today)
  const dueTodayFollowUps = clients.filter(c => c.follow_up_date === today)
  const overdueTasks = tasks.filter(t => t.due_date && t.due_date < today)
  const dueTodayTasks = tasks.filter(t => t.due_date === today)

  const prospectingDeals = deals.filter(d => PROSPECTING_STAGES.includes(d.stage))
  const activeContractDeals = deals.filter(d => ACTIVE_STAGES.includes(d.stage))

  const byStage = STAGES.map(stage => ({
    stage,
    count: deals.filter(d => d.stage === stage).length,
    volume: deals.filter(d => d.stage === stage).reduce((s, d) => s + (d.loan_amount || 0), 0),
  }))

  if (loading) {
    return <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontSize: '12px', letterSpacing: '0.1em' }}>LOADING DASHBOARD...</div>
  }

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '24px', background: 'var(--bg)' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
        {/* Greeting */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '22px', color: 'var(--text)', letterSpacing: '-0.01em' }}>
            {greeting()}, Bradley
          </div>
          <div style={{ fontSize: '13px', color: 'var(--muted)', marginTop: '2px' }}>Here is what needs attention today.</div>
        </div>

        {/* Top metrics */}
        <div className="dashboard-stats" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '20px' }}>
          <MetricCard label="Pipeline Volume" value={formatCurrency(pipelineVolume)} sub={activeDeals.length + ' active'} icon={Briefcase} blue onClick={() => setView('active')} />
          <MetricCard label="Pending Fees" value={formatCurrency(pendingFees)} sub="not yet funded" icon={DollarSign} onClick={() => setView('active')} />
          <MetricCard label="YTD Volume Closed" value={formatCurrency(ytdVolume)} sub={fundedThisYear.length + ' funded'} icon={Building2} success />
          <MetricCard label="YTD Fees Earned" value={formatCurrency(ytdFees)} sub={new Date().getFullYear().toString()} icon={DollarSign} success />
        </div>

        {/* Alerts row */}
        {(overdueTasks.length > 0 || overdueFollowUps.length > 0 || dueTodayFollowUps.length > 0 || dueTodayTasks.length > 0) && (
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '14px 18px', marginBottom: '20px', display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            {overdueTasks.length > 0 && <AlertChip icon={AlertCircle} count={overdueTasks.length} label="Overdue Tasks" danger onClick={() => setView('tasks')} />}
            {dueTodayTasks.length > 0 && <AlertChip icon={Clock} count={dueTodayTasks.length} label="Tasks Due Today" warn onClick={() => setView('tasks')} />}
            {overdueFollowUps.length > 0 && <AlertChip icon={AlertCircle} count={overdueFollowUps.length} label="Overdue Follow-ups" danger onClick={() => setView('contacts')} />}
            {dueTodayFollowUps.length > 0 && <AlertChip icon={Clock} count={dueTodayFollowUps.length} label="Follow-ups Today" warn onClick={() => setView('contacts')} />}
          </div>
        )}

        {/* Two-column layout */}
        <div className="dashboard-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          {/* Closing this week */}
          <Card title="Closing This Week" count={closingThisWeek.length} linkLabel="See all active" onLinkClick={() => setView('active')}>
            {closingThisWeek.length === 0 ? (
              <Empty>No deals closing in the next 7 days.</Empty>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {closingThisWeek.slice(0, 6).map(d => {
                  const c = STAGE_COLORS[d.stage] || { bg: '#f1f5f9', text: '#64748b', border: '#cbd5e1' }
                  return (
                    <div key={d.id} onClick={() => setView('active')} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 10px', background: 'var(--surface2)', borderRadius: '6px', cursor: 'pointer' }}>
                      <Calendar size={12} color="var(--muted)" />
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', fontFamily: 'Syne, sans-serif', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{d.borrower_name}</div>
                        <div style={{ fontSize: '10px', color: 'var(--muted)' }}>{d.property_address || d.property_type || ''}</div>
                      </div>
                      <span style={{ fontSize: '9px', padding: '1px 6px', borderRadius: '3px', background: c.bg, color: c.text, border: '1px solid ' + c.border, fontFamily: 'Syne, sans-serif', fontWeight: 700, whiteSpace: 'nowrap' }}>{d.stage}</span>
                      <span style={{ fontSize: '11px', color: 'var(--blue)', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600, whiteSpace: 'nowrap' }}>{formatCurrency(d.loan_amount)}</span>
                      <span style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', whiteSpace: 'nowrap' }}>{new Date(d.expected_close_date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                    </div>
                  )
                })}
              </div>
            )}
          </Card>

          {/* Today's tasks */}
          <Card title="Today's Tasks" count={dueTodayTasks.length + overdueTasks.length} linkLabel="See all tasks" onLinkClick={() => setView('tasks')}>
            {(dueTodayTasks.length + overdueTasks.length) === 0 ? (
              <Empty>No tasks due today or overdue. All clear.</Empty>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {[...overdueTasks, ...dueTodayTasks].slice(0, 6).map(t => {
                  const od = t.due_date < today
                  return (
                    <div key={t.id} onClick={() => setView('tasks')} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 10px', background: 'var(--surface2)', borderRadius: '6px', cursor: 'pointer' }}>
                      {od ? <AlertCircle size={12} color="var(--danger)" /> : <Clock size={12} color="var(--warn)" />}
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', fontFamily: 'Syne, sans-serif', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.title}</div>
                        <div style={{ fontSize: '10px', color: 'var(--muted)' }}>{t.assigned_to || 'Unassigned'} · {t.priority || 'Medium'}</div>
                      </div>
                      <span style={{ fontSize: '10px', color: od ? 'var(--danger)' : 'var(--warn)', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 600 }}>{od ? 'OVERDUE' : 'TODAY'}</span>
                    </div>
                  )
                })}
              </div>
            )}
          </Card>
        </div>

        {/* Pipeline by stage */}
        <Card title="Pipeline by Stage">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(' + STAGES.length + ', 1fr)', gap: '8px' }}>
            {byStage.map(({ stage, count, volume }) => {
              const c = STAGE_COLORS[stage] || { bg: '#f1f5f9', text: '#64748b', border: '#cbd5e1' }
              const isProspecting = PROSPECTING_STAGES.includes(stage)
              return (
                <button key={stage} onClick={() => setView(isProspecting ? 'prospecting' : 'active')} style={{ background: c.bg, border: '1px solid ' + c.border, borderRadius: '8px', padding: '10px 8px', cursor: 'pointer', textAlign: 'left' }}>
                  <div style={{ fontSize: '9px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: c.text, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{stage}</div>
                  <div style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: c.text }}>{count}</div>
                  {volume > 0 && <div style={{ fontSize: '10px', color: c.text, opacity: 0.7, fontFamily: 'IBM Plex Mono, monospace', marginTop: '2px' }}>{formatCurrency(volume)}</div>}
                </button>
              )
            })}
          </div>
          <div style={{ display: 'flex', gap: '12px', marginTop: '12px', fontSize: '11px', color: 'var(--muted)' }}>
            <span>Prospecting: {prospectingDeals.length}</span>
            <span>·</span>
            <span>Active: {activeContractDeals.length}</span>
            <span>·</span>
            <span>Properties: {properties.length}</span>
            <span>·</span>
            <span>Contacts: {clients.length}</span>
          </div>
        </Card>
      </div>
    </div>
  )
}

function greeting() {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 18) return 'Good afternoon'
  return 'Good evening'
}

function MetricCard({ label, value, sub, icon: Icon, blue, success, onClick }) {
  const color = blue ? 'var(--blue)' : success ? 'var(--success)' : 'var(--text)'
  return (
    <div onClick={onClick} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '14px 16px', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s' }}
      onMouseEnter={e => { if (onClick) { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.06)' } }}
      onMouseLeave={e => { if (onClick) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' } }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</span>
        <Icon size={14} color={color} />
      </div>
      <div style={{ fontSize: '20px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color, letterSpacing: '-0.01em' }}>{value}</div>
      {sub && <div style={{ fontSize: '10px', color: 'var(--muted)', marginTop: '2px' }}>{sub}</div>}
    </div>
  )
}

function AlertChip({ icon: Icon, count, label, danger, warn, onClick }) {
  const color = danger ? 'var(--danger)' : warn ? 'var(--warn)' : 'var(--blue)'
  const bg = danger ? '#fef2f2' : warn ? '#fffbeb' : '#eff6ff'
  const border = danger ? '#fecaca' : warn ? '#fde68a' : '#bfdbfe'
  return (
    <button onClick={onClick} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: bg, border: '1px solid ' + border, borderRadius: '8px', padding: '6px 12px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', color }}>
      <Icon size={12} />
      <span style={{ fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700 }}>{count}</span>
      <span>{label}</span>
      <ArrowRight size={11} />
    </button>
  )
}

function Card({ title, count, linkLabel, onLinkClick, children }) {
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '16px', marginBottom: '12px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px' }}>
          <h3 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{title}</h3>
          {count !== undefined && count > 0 && <span style={{ fontSize: '11px', fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)' }}>{count}</span>}
        </div>
        {onLinkClick && <button onClick={onLinkClick} style={{ background: 'transparent', border: 'none', color: 'var(--blue)', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '3px' }}>{linkLabel} <ArrowRight size={11} /></button>}
      </div>
      {children}
    </div>
  )
}

function Empty({ children }) {
  return <div style={{ padding: '20px', textAlign: 'center', color: 'var(--muted)', fontSize: '12px', fontStyle: 'italic' }}>{children}</div>
}
