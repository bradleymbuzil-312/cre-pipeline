import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Home, TrendingUp, Zap, CheckSquare, Users, Building2, Landmark, Contact, Link as LinkIcon, BarChart3, Clock, Calendar, BookOpen, Settings, HelpCircle } from 'lucide-react'

const SECTIONS = [
  { group: null, items: [
    { view: 'home', label: 'Home', icon: Home }
  ]},
  { group: 'Pipeline', items: [
    { view: 'prospecting', label: 'Prospecting', icon: TrendingUp, countKey: 'prospecting' },
    { view: 'active',      label: 'Active',      icon: Zap, countKey: 'active' },
    { view: 'tasks',       label: 'Tasks',       icon: CheckSquare, countKey: 'tasks' },
  ]},
  { group: 'Records', items: [
    { view: 'borrowers',  label: 'Borrowers',  icon: Users },
    { view: 'lenders',    label: 'Lenders',    icon: Landmark, countKey: 'lenders' },
    { view: 'properties', label: 'Properties', icon: Building2, countKey: 'properties' },
    { view: 'clients',    label: 'Contacts',   icon: Contact },
    { view: 'referrals',  label: 'Referrals',  icon: LinkIcon },
  ]},
  { group: 'Insights', items: [
    { view: 'maturity', label: 'Maturity Watch', icon: Clock, countKey: 'maturity' },
    { view: 'calendar', label: 'Calendar', icon: Calendar },
  ]},
  { group: 'System', items: [
    { view: 'resources', label: 'Resources', icon: BookOpen },
    { view: 'settings', label: 'Team Access', icon: Settings, isAction: 'openAccess' },
  ]},
]

export default function Sidebar({ view, setView, openAccess }) {
  const [counts, setCounts] = useState({ prospecting: 0, active: 0, tasks: 0, lenders: 0, properties: 0, maturity: 0 })

  useEffect(() => {
    let alive = true
    async function fetchCounts() {
      const today = new Date().toISOString().split('T')[0]
      const nextYear = new Date(); nextYear.setFullYear(nextYear.getFullYear() + 1)
      const nextYearStr = nextYear.toISOString().split('T')[0]
      const [deals, tasks, lenders, props] = await Promise.all([
        supabase.from('deals').select('id, stage, maturity_date'),
        supabase.from('tasks').select('id, status'),
        supabase.from('lenders').select('id'),
        supabase.from('properties').select('id'),
      ])
      if (!alive) return
      const d = deals.data || []
      const PROSP = new Set(['Underwriting', 'Packaging'])
      const ACTIVE = new Set(['Engagement', 'LOI / Term Sheet', 'Due Diligence', 'Closing'])
      const openTasks = (tasks.data || []).filter(t => t.status !== 'Done').length
      const matCount = d.filter(x => x.maturity_date && x.maturity_date <= nextYearStr).length
      setCounts({
        prospecting: d.filter(x => PROSP.has(x.stage)).length,
        active: d.filter(x => ACTIVE.has(x.stage)).length,
        tasks: openTasks,
        lenders: (lenders.data || []).length,
        properties: (props.data || []).length,
        maturity: matCount,
      })
    }
    fetchCounts()
    return () => { alive = false }
  }, [view])

  function handleClick(item) {
    if (item.isAction === 'openAccess') { openAccess?.(); return }
    setView(item.view)
  }

  return (
    <aside style={{
      background: 'var(--surface)',
      borderRight: '1px solid var(--border)',
      padding: '16px 0',
      position: 'sticky',
      top: 0,
      height: '100vh',
      overflowY: 'auto',
      width: '240px',
      flexShrink: 0,
    }}>
      <div style={{ padding: '0 16px 16px', borderBottom: '1px solid var(--border)', marginBottom: '12px' }}>
        <h1 style={{ margin: 0, fontSize: '16px', color: '#fff', fontWeight: 700, letterSpacing: '-0.01em' }}>CRE Pipeline</h1>
        <div style={{ fontSize: '10px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '1px', marginTop: '2px' }}>MMCC — Internal Team</div>
      </div>

      <nav>
        {SECTIONS.map((section, si) => (
          <div key={si}>
            {section.group && (
              <div style={{ fontSize: '10px', color: 'var(--dim)', textTransform: 'uppercase', padding: '14px 16px 6px', letterSpacing: '1px', fontWeight: 600 }}>{section.group}</div>
            )}
            {section.items.map(item => {
              const Icon = item.icon
              const isActive = view === item.view
              const count = item.countKey ? counts[item.countKey] : null
              return (
                <a key={item.view}
                   onClick={() => handleClick(item)}
                   style={{
                     display: 'flex',
                     alignItems: 'center',
                     gap: '10px',
                     padding: '9px 16px',
                     fontSize: '13px',
                     color: isActive ? '#fff' : 'var(--muted)',
                     background: isActive ? 'var(--blue-light)' : 'transparent',
                     borderLeft: '3px solid ' + (isActive ? 'var(--brand)' : 'transparent'),
                     cursor: 'pointer',
                     textDecoration: 'none',
                     userSelect: 'none',
                     transition: 'background 0.1s, color 0.1s',
                   }}
                   onMouseEnter={e => { if (!isActive) { e.currentTarget.style.background = '#14233f'; e.currentTarget.style.color = 'var(--text)' } }}
                   onMouseLeave={e => { if (!isActive) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--muted)' } }}>
                  <Icon size={15} strokeWidth={1.8} />
                  <span style={{ flex: 1 }}>{item.label}</span>
                  {count != null && count > 0 && (
                    <span style={{ background: 'var(--border)', color: 'var(--text)', fontSize: '10px', padding: '1px 6px', borderRadius: '10px', fontWeight: 600 }}>{count}</span>
                  )}
                </a>
              )
            })}
          </div>
        ))}
      </nav>
    </aside>
  )
}