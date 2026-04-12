import { useState } from 'react'
import { Edit2, Trash2, Calendar, ChevronDown, AlertCircle, User } from 'lucide-react'

const PRIORITY_COLORS = {
  High:   { color: '#f85149', bg: 'rgba(248,81,73,0.1)' },
  Medium: { color: '#f09a3a', bg: 'rgba(240,154,58,0.1)' },
  Low:    { color: '#6b9ff7', bg: 'rgba(107,159,247,0.1)' },
}

export default function TaskCard({ task, teamMembers, deals, clients, onEdit, onDelete, onStatusChange, statuses }) {
  const [statusOpen, setStatusOpen] = useState(false)
  const today = new Date().toISOString().split('T')[0]
  const isOverdue = task.due_date && task.due_date < today && task.status !== 'Done'
  const isDueToday = task.due_date === today && task.status !== 'Done'
  const p = PRIORITY_COLORS[task.priority] || PRIORITY_COLORS.Medium
  const deal = deals.find(d => d.id === task.deal_id)
  const client = clients.find(c => c.id === task.client_id)

  return (
    <div style={{ background: 'var(--surface)', border: `1px solid ${isOverdue ? 'rgba(248,81,73,0.3)' : 'var(--border)'}`, borderRadius: '8px', padding: '12px', transition: 'all 0.15s', position: 'relative' }}
      onMouseEnter={e => { e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)'; e.currentTarget.style.borderColor = isOverdue ? 'rgba(248,81,73,0.5)' : 'var(--border-hover)' }}
      onMouseLeave={e => { e.currentTarget.style.boxShadow = 'none'; e.currentTarget.style.borderColor = isOverdue ? 'rgba(248,81,73,0.3)' : 'var(--border)' }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
        <div style={{ flex: 1, marginRight: '8px' }}>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: task.status === 'Done' ? 'var(--muted)' : 'var(--text)', textDecoration: task.status === 'Done' ? 'line-through' : 'none', lineHeight: 1.3, marginBottom: '4px' }}>{task.title}</div>
          <span style={{ fontSize: '9px', padding: '1px 6px', borderRadius: '3px', background: p.bg, color: p.color, fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{task.priority}</span>
        </div>
        <div style={{ display: 'flex', gap: '4px' }}>
          <button onClick={onEdit} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 5px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }} onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.background = 'var(--surface2)' }} onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'transparent' }}><Edit2 size={11} /></button>
          <button onClick={onDelete} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 5px', cursor: 'pointer', color: 'var(--danger)', display: 'flex', alignItems: 'center' }} onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--danger)'; e.currentTarget.style.background = 'rgba(248,81,73,0.08)' }} onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'transparent' }}><Trash2 size={11} /></button>
        </div>
      </div>

      {/* Description */}
      {task.description && <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '8px', lineHeight: 1.5 }}>{task.description}</div>}

      {/* Linked deal/client */}
      {(deal || client) && (
        <div style={{ fontSize: '10px', color: 'var(--muted)', marginBottom: '6px', fontFamily: 'IBM Plex Mono, monospace', padding: '4px 7px', background: 'var(--surface2)', borderRadius: '4px' }}>
          {deal ? `Deal: ${deal.borrower_name}` : `Client: ${client.first_name} ${client.last_name || ''}`}
        </div>
      )}

      {/* Footer */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Assignee */}
          {task.assigned_to && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <div style={{ width: '18px', height: '18px', borderRadius: '50%', background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '9px', fontWeight: 700, color: '#000', fontFamily: 'Syne, sans-serif' }}>{task.assigned_to.charAt(0).toUpperCase()}</div>
              <span style={{ fontSize: '10px', color: 'var(--muted)' }}>{task.assigned_to}</span>
            </div>
          )}
          {/* Due date */}
          {task.due_date && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '3px', color: isOverdue ? 'var(--danger)' : isDueToday ? 'var(--gold)' : 'var(--muted)' }}>
              {isOverdue && <AlertCircle size={10} />}
              {!isOverdue && <Calendar size={10} />}
              <span style={{ fontSize: '10px', fontFamily: 'IBM Plex Mono, monospace' }}>
                {new Date(task.due_date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            </div>
          )}
        </div>

        {/* Status changer */}
        <div style={{ position: 'relative' }}>
          <button onClick={() => setStatusOpen(o => !o)} style={{ display: 'flex', alignItems: 'center', gap: '3px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '4px', padding: '3px 7px', cursor: 'pointer', fontSize: '9px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
            {task.status} <ChevronDown size={9} />
          </button>
          {statusOpen && (
            <div style={{ position: 'absolute', bottom: '100%', right: 0, marginBottom: '4px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', overflow: 'hidden', zIndex: 100, boxShadow: '0 8px 24px rgba(0,0,0,0.4)', minWidth: '120px' }}>
              {statuses.map(s => (
                <button key={s} onClick={() => { onStatusChange(task.id, s); setStatusOpen(false) }} style={{ width: '100%', textAlign: 'left', padding: '8px 12px', background: task.status === s ? 'var(--surface2)' : 'transparent', border: 'none', color: task.status === s ? 'var(--text)' : 'var(--muted)', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, display: 'block' }} onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'} onMouseLeave={e => e.currentTarget.style.background = task.status === s ? 'var(--surface2)' : 'transparent'}>
                  {s}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
