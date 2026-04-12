import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Plus, Users, Settings } from 'lucide-react'
import TaskCard from './TaskCard'
import TaskModal from './TaskModal'

const STATUSES = ['To Do', 'In Progress', 'Done']
const STATUS_COLORS = {
  'To Do':      { bg: '#0e1f3d', border: '#1e3d6e', text: '#6b9ff7' },
  'In Progress':{ bg: '#2a1800', border: '#6b3a00', text: '#f09a3a' },
  'Done':       { bg: '#001a08', border: '#005218', text: '#3ad460' },
}

export default function Tasks({ session }) {
  const [tasks, setTasks] = useState([])
  const [teamMembers, setTeamMembers] = useState([])
  const [deals, setDeals] = useState([])
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [teamOpen, setTeamOpen] = useState(false)
  const [newMember, setNewMember] = useState({ name: '', email: '', role: '' })
  const [filter, setFilter] = useState('All')

  useEffect(() => {
    fetchAll()
  }, [])

  async function fetchAll() {
    const [t, m, d, c] = await Promise.all([
      supabase.from('tasks').select('*').order('due_date', { ascending: true, nullsFirst: false }),
      supabase.from('team_members').select('*').order('name'),
      supabase.from('deals').select('id, borrower_name, property_address').order('borrower_name'),
      supabase.from('clients').select('id, first_name, last_name, company').order('first_name'),
    ])
    setTasks(t.data || [])
    setTeamMembers(m.data || [])
    setDeals(d.data || [])
    setClients(c.data || [])
    setLoading(false)
  }

  async function addTeamMember() {
    if (!newMember.name.trim()) return
    await supabase.from('team_members').insert({ ...newMember, created_by: session.user.id })
    setNewMember({ name: '', email: '', role: '' })
    fetchAll()
  }

  async function removeTeamMember(id) {
    if (!window.confirm('Remove this team member?')) return
    await supabase.from('team_members').delete().eq('id', id)
    fetchAll()
  }

  async function updateStatus(id, status) {
    await supabase.from('tasks').update({ status, updated_at: new Date().toISOString() }).eq('id', id)
    setTasks(prev => prev.map(t => t.id === id ? { ...t, status } : t))
  }

  async function deleteTask(id) {
    if (!window.confirm('Delete this task?')) return
    await supabase.from('tasks').delete().eq('id', id)
    setTasks(prev => prev.filter(t => t.id !== id))
  }

  const members = ['All', ...teamMembers.map(m => m.name)]
  const filtered = filter === 'All' ? tasks : tasks.filter(t => t.assigned_to === filter)

  const totalOpen = tasks.filter(t => t.status !== 'Done').length
  const totalDone = tasks.filter(t => t.status === 'Done').length
  const overdue = tasks.filter(t => t.due_date && t.due_date < new Date().toISOString().split('T')[0] && t.status !== 'Done').length

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* Toolbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 24px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Stat label="Open" value={totalOpen} />
          <Sep /><Stat label="Done" value={totalDone} highlight />
          <Sep /><Stat label="Overdue" value={overdue} danger={overdue > 0} />
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button onClick={() => setTeamOpen(o => !o)} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '7px 12px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', letterSpacing: '0.04em', transition: 'all 0.15s' }} onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.color = 'var(--text)' }} onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
            <Users size={12} /> TEAM ({teamMembers.length})
          </button>
          <button onClick={() => { setEditingTask(null); setModalOpen(true) }} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--gold)', color: '#000', border: 'none', padding: '7px 14px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', cursor: 'pointer', letterSpacing: '0.04em' }}>
            <Plus size={13} strokeWidth={2.5} /> NEW TASK
          </button>
        </div>
      </div>

      {/* Team panel */}
      {teamOpen && (
        <div style={{ padding: '14px 24px', background: 'var(--surface2)', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>Team Members</div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '10px' }}>
            {teamMembers.map(m => (
              <div key={m.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', padding: '6px 10px' }}>
                <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '10px', color: '#000' }}>{m.name.charAt(0).toUpperCase()}</div>
                <div>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text)', fontFamily: 'Syne, sans-serif' }}>{m.name}</div>
                  {m.role && <div style={{ fontSize: '10px', color: 'var(--muted)' }}>{m.role}</div>}
                </div>
                <button onClick={() => removeTeamMember(m.id)} style={{ background: 'transparent', border: 'none', color: 'var(--muted)', cursor: 'pointer', fontSize: '14px', lineHeight: 1, padding: '0 2px' }}>×</button>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <input value={newMember.name} onChange={e => setNewMember(m => ({...m, name: e.target.value}))} placeholder="Name *" style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', width: '130px' }} />
            <input value={newMember.role} onChange={e => setNewMember(m => ({...m, role: e.target.value}))} placeholder="Role (e.g. Analyst)" style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', width: '160px' }} />
            <input value={newMember.email} onChange={e => setNewMember(m => ({...m, email: e.target.value}))} placeholder="Email" style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '6px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', width: '200px' }} />
            <button onClick={addTeamMember} style={{ background: 'var(--gold)', color: '#000', border: 'none', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px' }}>ADD</button>
          </div>
        </div>
      )}

      {/* Filter by assignee */}
      <div style={{ display: 'flex', gap: '6px', padding: '10px 24px', background: 'var(--bg)', borderBottom: '1px solid var(--border)', flexShrink: 0, overflowX: 'auto' }}>
        {members.map(m => (
          <button key={m} onClick={() => setFilter(m)} style={{ background: filter === m ? 'var(--gold)' : 'var(--surface2)', color: filter === m ? '#000' : 'var(--muted)', border: `1px solid ${filter === m ? 'var(--gold)' : 'var(--border)'}`, borderRadius: '20px', padding: '4px 12px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', letterSpacing: '0.04em', whiteSpace: 'nowrap', transition: 'all 0.15s' }}>
            {m}
          </button>
        ))}
      </div>

      {/* Kanban columns */}
      <div style={{ flex: 1, display: 'flex', gap: '0', overflow: 'hidden' }}>
        {STATUSES.map(status => {
          const col = filtered.filter(t => t.status === status)
          const sc = STATUS_COLORS[status]
          return (
            <div key={status} style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)', overflow: 'hidden' }}>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', background: 'var(--surface)', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '10px', padding: '2px 8px', borderRadius: '10px', background: sc.bg, border: `1px solid ${sc.border}`, color: sc.text, fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{status}</span>
                </div>
                <span style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', fontWeight: 700 }}>{col.length}</span>
              </div>
              <div style={{ flex: 1, overflowY: 'auto', padding: '12px' }}>
                {loading ? (
                  <div style={{ color: 'var(--muted)', fontSize: '11px', fontFamily: 'IBM Plex Mono, monospace', textAlign: 'center', marginTop: '20px' }}>LOADING...</div>
                ) : col.length === 0 ? (
                  <div style={{ color: 'var(--muted)', fontSize: '11px', textAlign: 'center', marginTop: '20px', opacity: 0.5 }}>No tasks</div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {col.map(task => (
                      <TaskCard key={task.id} task={task} teamMembers={teamMembers} deals={deals} clients={clients}
                        onEdit={() => { setEditingTask(task); setModalOpen(true) }}
                        onDelete={() => deleteTask(task.id)}
                        onStatusChange={updateStatus}
                        statuses={STATUSES}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {modalOpen && (
        <TaskModal task={editingTask} session={session} teamMembers={teamMembers} deals={deals} clients={clients}
          onClose={() => setModalOpen(false)} onSaved={fetchAll} />
      )}
    </div>
  )
}

function Stat({ label, value, highlight, danger }) {
  return (
    <div>
      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'IBM Plex Mono, monospace', color: danger ? 'var(--danger)' : highlight ? '#3ad460' : 'var(--text)' }}>{value}</div>
    </div>
  )
}
function Sep() { return <div style={{ width: '1px', height: '28px', background: 'var(--border)' }} /> }
