import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { X } from 'lucide-react'

const PRIORITIES = ['High', 'Medium', 'Low']
const STATUSES = ['To Do', 'In Progress', 'Done']
const EMPTY = { title: '', description: '', assigned_to: '', status: 'To Do', priority: 'Medium', due_date: '', deal_id: '', client_id: '' }

export default function TaskModal({ task, session, teamMembers, deals, clients, onClose, onSaved }) {
  const [form, setForm] = useState(() => {
    if (!task) return { ...EMPTY }
    const f = { ...EMPTY, ...task }
    Object.keys(f).forEach(k => { if (f[k] === null || f[k] === undefined) f[k] = '' })
    return f
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function set(k, v) { setForm(f => ({ ...f, [k]: v })) }

  async function handleSave() {
    if (!form.title.trim()) { setError('Title is required.'); return }
    setSaving(true); setError('')
    const payload = {
      title: form.title.trim(),
      description: form.description.trim() || null,
      assigned_to: form.assigned_to || null,
      status: form.status,
      priority: form.priority,
      due_date: form.due_date || null,
      deal_id: form.deal_id || null,
      client_id: form.client_id || null,
      updated_at: new Date().toISOString(),
    }
    let err
    if (task?.id) { ;({ error: err } = await supabase.from('tasks').update(payload).eq('id', task.id)) }
    else { ;({ error: err } = await supabase.from('tasks').insert({ ...payload, created_by: session.user.id })) }
    if (err) { setError(err.message); setSaving(false); return }
    onSaved(); onClose()
  }

  const IS = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '8px 12px', fontSize: '13px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }
  const LS = { display: 'block', marginBottom: '6px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.09em' }

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '560px', maxHeight: '90vh', display: 'flex', flexDirection: 'column', boxShadow: '0 32px 80px rgba(0,0,0,0.7)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '18px 24px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '16px', color: 'var(--text)' }}>{task ? 'Edit Task' : 'New Task'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
        </div>
        <div style={{ overflowY: 'auto', flex: 1, padding: '22px 24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div><label style={LS}>Title *</label><input value={form.title} onChange={e => set('title', e.target.value)} placeholder="What needs to be done?" style={IS} /></div>
          <div><label style={LS}>Description</label><textarea value={form.description} onChange={e => set('description', e.target.value)} rows={3} placeholder="Add details, context, or instructions..." style={{ ...IS, resize: 'vertical', lineHeight: 1.6 }} /></div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div><label style={LS}>Assigned To</label>
              <select value={form.assigned_to} onChange={e => set('assigned_to', e.target.value)} style={IS}>
                <option value="">Unassigned</option>
                {teamMembers.map(m => <option key={m.id} value={m.name}>{m.name}</option>)}
              </select>
            </div>
            <div><label style={LS}>Priority</label>
              <select value={form.priority} onChange={e => set('priority', e.target.value)} style={IS}>
                {PRIORITIES.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
            <div><label style={LS}>Status</label>
              <select value={form.status} onChange={e => set('status', e.target.value)} style={IS}>
                {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div><label style={LS}>Due Date</label><input type="date" value={form.due_date} onChange={e => set('due_date', e.target.value)} style={IS} /></div>
          </div>
          <div style={{ height: '1px', background: 'var(--border)' }} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div><label style={LS}>Link to Deal</label>
              <select value={form.deal_id} onChange={e => set('deal_id', e.target.value)} style={IS}>
                <option value="">None</option>
                {deals.map(d => <option key={d.id} value={d.id}>{d.borrower_name}{d.property_address ? ` — ${d.property_address}` : ''}</option>)}
              </select>
            </div>
            <div><label style={LS}>Link to Client</label>
              <select value={form.client_id} onChange={e => set('client_id', e.target.value)} style={IS}>
                <option value="">None</option>
                {clients.map(c => <option key={c.id} value={c.id}>{c.first_name} {c.last_name || ''}{c.company ? ` — ${c.company}` : ''}</option>)}
              </select>
            </div>
          </div>
          {error && <div style={{ padding: '10px 14px', borderRadius: '6px', background: 'rgba(248,81,73,0.08)', border: '1px solid rgba(248,81,73,0.25)', color: 'var(--danger)', fontSize: '13px' }}>{error}</div>}
        </div>
        <div style={{ padding: '14px 24px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'flex-end', gap: '10px', flexShrink: 0 }}>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', letterSpacing: '0.04em' }}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{ background: saving ? 'var(--gold-dim)' : 'var(--gold)', border: 'none', color: '#000', padding: '8px 24px', borderRadius: '6px', cursor: saving ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>{saving ? 'SAVING...' : task ? 'SAVE CHANGES' : 'CREATE TASK'}</button>
        </div>
      </div>
    </div>
  )
}
