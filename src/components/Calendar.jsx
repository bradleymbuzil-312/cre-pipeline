import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { ChevronLeft, ChevronRight, Calendar as CalIcon, AlertCircle, CheckSquare } from 'lucide-react'

const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
const WEEKDAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

function ymd(date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return y + '-' + m + '-' + d
}

function fmtMoney(n) {
  if (!n) return ''
  if (n >= 1e6) return '$' + (n/1e6).toFixed(1) + 'M'
  if (n >= 1e3) return '$' + Math.round(n/1e3) + 'K'
  return '$' + n
}

export default function Calendar({ session, setView }) {
  const today = new Date()
  const [cursor, setCursor] = useState(new Date(today.getFullYear(), today.getMonth(), 1))
  const [deals, setDeals] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedDate, setSelectedDate] = useState(ymd(today))

  useEffect(() => { fetchMonth() }, [cursor])

  async function fetchMonth() {
    setLoading(true)
    const year = cursor.getFullYear()
    const month = cursor.getMonth()
    const firstDay = new Date(year, month - 1, 15).toISOString().split('T')[0]
    const lastDay = new Date(year, month + 2, 15).toISOString().split('T')[0]
    const [d, t] = await Promise.all([
      supabase.from('deals').select('id, borrower_name, property_address, city, state_province, loan_amount, maturity_date, stage').not('maturity_date', 'is', null).gte('maturity_date', firstDay).lte('maturity_date', lastDay),
      supabase.from('tasks').select('id, title, due_date, status, priority').not('due_date', 'is', null).gte('due_date', firstDay).lte('due_date', lastDay),
    ])
    setDeals(d.data || [])
    setTasks(t.data || [])
    setLoading(false)
  }

  // Build calendar cells
  const year = cursor.getFullYear()
  const month = cursor.getMonth()
  const firstOfMonth = new Date(year, month, 1)
  const startOffset = firstOfMonth.getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const cells = []
  for (let i = 0; i < startOffset; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(new Date(year, month, d))
  while (cells.length % 7 !== 0) cells.push(null)

  // Group items by date
  const dealsByDate = {}
  for (const deal of deals) {
    const key = deal.maturity_date
    if (!dealsByDate[key]) dealsByDate[key] = []
    dealsByDate[key].push(deal)
  }
  const tasksByDate = {}
  for (const task of tasks) {
    const key = task.due_date
    if (!tasksByDate[key]) tasksByDate[key] = []
    tasksByDate[key].push(task)
  }

  function prevMonth() { setCursor(new Date(year, month - 1, 1)) }
  function nextMonth() { setCursor(new Date(year, month + 1, 1)) }
  function goToday() { const t = new Date(); setCursor(new Date(t.getFullYear(), t.getMonth(), 1)); setSelectedDate(ymd(t)) }

  const todayStr = ymd(today)
  const selectedDeals = dealsByDate[selectedDate] || []
  const selectedTasks = tasksByDate[selectedDate] || []
  const selectedHasAnything = selectedDeals.length > 0 || selectedTasks.length > 0

  return (
    <div style={{ padding: '20px 24px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '22px', color: 'var(--text)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '10px' }}>
            <CalIcon size={18} color="var(--brand)" /> Calendar
          </h1>
          <div style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '4px' }}>
            {deals.length} maturit{deals.length === 1 ? 'y' : 'ies'} \u00b7 {tasks.length} task{tasks.length !== 1 ? 's' : ''} this month
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button onClick={prevMonth} style={btnStyle}><ChevronLeft size={14} /></button>
          <div style={{ fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '14px', color: 'var(--text)', minWidth: '160px', textAlign: 'center' }}>
            {MONTHS[month]} {year}
          </div>
          <button onClick={nextMonth} style={btnStyle}><ChevronRight size={14} /></button>
          <button onClick={goToday} style={{ ...btnStyle, padding: '6px 12px', fontSize: '11px', fontWeight: 600, letterSpacing: '0.04em' }}>TODAY</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '16px', alignItems: 'start' }}>
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', background: 'var(--surface2)', borderBottom: '1px solid var(--border)' }}>
            {WEEKDAYS.map(d => (
              <div key={d} style={{ padding: '8px', textAlign: 'center', fontSize: '10px', color: 'var(--muted)', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.06em' }}>{d}</div>
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)' }}>
            {cells.map((cell, i) => {
              if (!cell) return <div key={i} style={{ minHeight: '84px', background: 'var(--bg)', borderRight: '1px solid var(--border)', borderBottom: '1px solid var(--border)' }} />
              const dayStr = ymd(cell)
              const isToday = dayStr === todayStr
              const isSelected = dayStr === selectedDate
              const dealsHere = dealsByDate[dayStr] || []
              const tasksHere = tasksByDate[dayStr] || []
              const hasAny = dealsHere.length + tasksHere.length > 0
              return (
                <div key={i} onClick={() => setSelectedDate(dayStr)}
                     style={{
                       minHeight: '84px', padding: '6px 8px', borderRight: '1px solid var(--border)', borderBottom: '1px solid var(--border)',
                       background: isSelected ? 'var(--blue-light)' : (isToday ? 'var(--surface2)' : 'transparent'),
                       cursor: 'pointer', position: 'relative',
                     }}
                     onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = 'var(--surface2)' }}
                     onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = isToday ? 'var(--surface2)' : 'transparent' }}>
                  <div style={{ fontSize: '12px', fontWeight: isToday ? 700 : 500, color: isToday ? 'var(--brand)' : 'var(--text)', marginBottom: '4px' }}>
                    {cell.getDate()}
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                    {dealsHere.slice(0, 2).map(d => (
                      <div key={d.id} style={{ fontSize: '10px', padding: '2px 4px', borderRadius: '3px', background: 'rgba(239, 68, 68, 0.15)', color: '#fca5a5', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={d.borrower_name + ' \u00b7 ' + fmtMoney(d.loan_amount)}>
                        \u25cf {fmtMoney(d.loan_amount) || d.borrower_name}
                      </div>
                    ))}
                    {tasksHere.slice(0, 2).map(t => (
                      <div key={t.id} style={{ fontSize: '10px', padding: '2px 4px', borderRadius: '3px', background: 'rgba(59, 130, 246, 0.15)', color: '#93c5fd', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={t.title}>
                        \u2713 {t.title}
                      </div>
                    ))}
                    {(dealsHere.length + tasksHere.length) > 4 && (
                      <div style={{ fontSize: '9px', color: 'var(--dim)' }}>+{(dealsHere.length + tasksHere.length) - 4} more</div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '16px', position: 'sticky', top: '80px' }}>
          <div style={{ fontSize: '11px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '4px', fontWeight: 600 }}>
            Selected Day
          </div>
          <div style={{ fontSize: '16px', color: 'var(--text)', fontWeight: 700, marginBottom: '14px' }}>
            {new Date(selectedDate + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </div>

          {!selectedHasAnything && (
            <div style={{ fontSize: '13px', color: 'var(--muted)', padding: '20px 0', textAlign: 'center' }}>
              Nothing scheduled.
            </div>
          )}

          {selectedDeals.length > 0 && (
            <div style={{ marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                <AlertCircle size={12} color="#ef4444" />
                <div style={{ fontSize: '11px', color: '#fca5a5', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.06em' }}>
                  {selectedDeals.length} Maturit{selectedDeals.length === 1 ? 'y' : 'ies'}
                </div>
              </div>
              {selectedDeals.map(d => (
                <div key={d.id} style={{ padding: '10px 12px', background: 'var(--surface2)', borderLeft: '3px solid #ef4444', borderRadius: '4px', marginBottom: '6px' }}>
                  <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 600 }}>{d.borrower_name}</div>
                  {d.property_address && <div style={{ fontSize: '11px', color: 'var(--muted)', marginTop: '2px' }}>{d.property_address}{d.city ? ', ' + d.city : ''}{d.state_province ? ', ' + d.state_province : ''}</div>}
                  <div style={{ fontSize: '11px', color: 'var(--muted)', marginTop: '4px', fontFamily: 'IBM Plex Mono, monospace' }}>
                    {fmtMoney(d.loan_amount)} \u00b7 {d.stage}
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedTasks.length > 0 && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                <CheckSquare size={12} color="#3b82f6" />
                <div style={{ fontSize: '11px', color: '#93c5fd', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.06em' }}>
                  {selectedTasks.length} Task{selectedTasks.length !== 1 ? 's' : ''}
                </div>
              </div>
              {selectedTasks.map(t => (
                <div key={t.id} style={{ padding: '10px 12px', background: 'var(--surface2)', borderLeft: '3px solid #3b82f6', borderRadius: '4px', marginBottom: '6px' }}>
                  <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 600, textDecoration: t.status === 'Done' ? 'line-through' : 'none', opacity: t.status === 'Done' ? 0.6 : 1 }}>
                    {t.title}
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)', marginTop: '4px' }}>
                    {t.status}{t.priority ? ' \u00b7 ' + t.priority : ''}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {loading && <div style={{ fontSize: '11px', color: 'var(--muted)', textAlign: 'center', padding: '10px', fontFamily: 'IBM Plex Mono, monospace' }}>LOADING...</div>}
    </div>
  )
}

const btnStyle = {
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)',
  borderRadius: '6px', padding: '7px 8px', cursor: 'pointer', fontSize: '12px'
}