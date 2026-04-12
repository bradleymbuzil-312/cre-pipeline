import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { Edit2, Trash2, Phone, Mail, Clock, AlertCircle, MessageSquare, Download } from 'lucide-react'

function exportVCard(client) {
  const lines = [
    'BEGIN:VCARD',
    'VERSION:3.0',
    `FN:${[client.first_name, client.last_name].filter(Boolean).join(' ')}`,
    `N:${client.last_name || ''};${client.first_name || ''};;;`,
    client.company ? `ORG:${client.company}` : '',
    client.email ? `EMAIL;TYPE=INTERNET:${client.email}` : '',
    client.phone ? `TEL;TYPE=WORK:${client.phone}` : '',
    client.notes ? `NOTE:${client.notes.replace(/\n/g, '\\n')}` : '',
    `CATEGORIES:${client.client_type || 'Contact'}`,
    'END:VCARD'
  ].filter(Boolean).join('\r\n')

  const blob = new Blob([lines], { type: 'text/vcard;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${[client.first_name, client.last_name].filter(Boolean).join('_') || 'contact'}.vcf`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export default function ClientCard({ client, onEdit, onDelete, onRefresh, session }) {
  const [logOpen, setLogOpen] = useState(false)
  const [logNote, setLogNote] = useState('')
  const [saving, setSaving] = useState(false)
  const [exported, setExported] = useState(false)
  const today = new Date().toISOString().split('T')[0]
  const isOverdue = client.follow_up_date && client.follow_up_date < today
  const isDueToday = client.follow_up_date === today
  const followUpColor = isOverdue ? 'var(--danger)' : isDueToday ? 'var(--gold)' : 'var(--muted)'

  async function logContact() {
    if (saving) return
    setSaving(true)
    await supabase.from('contact_log').insert({ client_id: client.id, note: logNote.trim() || null, logged_by: session.user.id })
    await supabase.from('clients').update({ last_contacted_at: new Date().toISOString(), updated_at: new Date().toISOString() }).eq('id', client.id)
    setLogNote(''); setLogOpen(false); setSaving(false); onRefresh()
  }

  function handleExport() {
    exportVCard(client)
    setExported(true)
    setTimeout(() => setExported(false), 2000)
  }

  return (
    <div style={{ background: 'var(--surface)', border: `1px solid ${isOverdue ? 'rgba(248,81,73,0.3)' : isDueToday ? 'rgba(212,168,67,0.3)' : 'var(--border)'}`, borderRadius: '10px', padding: '14px', transition: 'border-color 0.15s, box-shadow 0.15s' }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = isOverdue ? 'rgba(248,81,73,0.6)' : isDueToday ? 'var(--gold-dim)' : 'var(--border-hover)'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.3)' }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = isOverdue ? 'rgba(248,81,73,0.3)' : isDueToday ? 'rgba(212,168,67,0.3)' : 'var(--border)'; e.currentTarget.style.boxShadow = 'none' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
        <div>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '14px', color: 'var(--text)', marginBottom: '2px' }}>{client.first_name} {client.last_name || ''}</div>
          {client.company && <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{client.company}</div>}
        </div>
        <div style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
          <TypeBadge type={client.client_type} />
          <Btn icon={Edit2} onClick={onEdit} title="Edit" />
          <Btn icon={Trash2} onClick={onDelete} danger title="Delete" />
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '10px' }}>
        {client.email && <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Mail size={10} color="var(--muted)" /><a href={`mailto:${client.email}`} style={{ fontSize: '11px', color: 'var(--muted)', textDecoration: 'none' }}>{client.email}</a></div>}
        {client.phone && <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Phone size={10} color="var(--muted)" /><a href={`tel:${client.phone}`} style={{ fontSize: '11px', color: 'var(--muted)', textDecoration: 'none' }}>{client.phone}</a></div>}
        {client.referral_source && <div style={{ fontSize: '11px', color: 'var(--muted)' }}>Referred by: {client.referral_source}</div>}
      </div>

      {client.notes && <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '10px', padding: '7px 9px', background: 'var(--surface2)', borderRadius: '5px', borderLeft: '2px solid var(--border)', lineHeight: 1.5, overflow: 'hidden' }}>{client.notes}</div>}

      <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', marginBottom: '8px' }}>
        {client.last_contacted_at ? `Last contact: ${new Date(client.last_contacted_at).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'2-digit'})}` : 'Never contacted'}
      </div>

      {client.follow_up_date && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '6px 8px', borderRadius: '5px', background: isOverdue ? 'rgba(248,81,73,0.08)' : isDueToday ? 'rgba(212,168,67,0.08)' : 'var(--surface2)', border: `1px solid ${isOverdue ? 'rgba(248,81,73,0.2)' : isDueToday ? 'rgba(212,168,67,0.2)' : 'var(--border)'}`, marginBottom: '10px' }}>
          {isOverdue ? <AlertCircle size={11} color="var(--danger)" /> : <Clock size={11} color={isDueToday ? 'var(--gold)' : 'var(--muted)'} />}
          <span style={{ fontSize: '11px', color: followUpColor, fontFamily: 'IBM Plex Mono, monospace' }}>
            {isOverdue ? 'OVERDUE: ' : isDueToday ? 'DUE TODAY: ' : 'Follow-up: '}
            {new Date(client.follow_up_date + 'T00:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'2-digit'})}
          </span>
        </div>
      )}

      {client.follow_up_note && <div style={{ fontSize: '11px', color: followUpColor, marginBottom: '10px', opacity: 0.8 }}>{client.follow_up_note}</div>}

      {/* Action buttons row */}
      <div style={{ display: 'flex', gap: '6px', marginBottom: logOpen ? '8px' : '0' }}>
        {!logOpen && (
          <button onClick={() => setLogOpen(true)} style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px', background: 'transparent', border: '1px solid var(--border)', borderRadius: '5px', color: 'var(--muted)', fontSize: '10px', padding: '5px 8px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.03em', transition: 'all 0.15s' }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--gold-dim)'; e.currentTarget.style.color = 'var(--gold)'; e.currentTarget.style.background = 'rgba(212,168,67,0.05)' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.background = 'transparent' }}
          >
            <MessageSquare size={10} /> LOG CONTACT
          </button>
        )}
        <button onClick={handleExport} title="Download as .vcf to import into Outlook" style={{ flex: logOpen ? 1 : 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px', background: exported ? 'rgba(58,212,96,0.1)' : 'transparent', border: `1px solid ${exported ? 'rgba(58,212,96,0.4)' : 'var(--border)'}`, borderRadius: '5px', color: exported ? '#3ad460' : 'var(--muted)', fontSize: '10px', padding: '5px 8px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, letterSpacing: '0.03em', transition: 'all 0.15s', whiteSpace: 'nowrap' }}
          onMouseEnter={e => { if (!exported) { e.currentTarget.style.borderColor = 'rgba(58,212,96,0.4)'; e.currentTarget.style.color = '#3ad460'; e.currentTarget.style.background = 'rgba(58,212,96,0.05)' } }}
          onMouseLeave={e => { if (!exported) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.background = 'transparent' } }}
        >
          <Download size={10} /> {exported ? 'DOWNLOADED' : 'OUTLOOK'}
        </button>
      </div>

      {logOpen && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <textarea autoFocus value={logNote} onChange={e => setLogNote(e.target.value)} placeholder="Note about call / meeting..." rows={2}
            style={{ width: '100%', background: 'var(--surface2)', border: '1px solid var(--gold-dim)', color: 'var(--text)', borderRadius: '5px', padding: '7px 9px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', resize: 'none', boxSizing: 'border-box' }} />
          <div style={{ display: 'flex', gap: '6px' }}>
            <button onClick={logContact} disabled={saving} style={{ flex: 1, background: 'var(--gold)', border: 'none', color: '#000', padding: '6px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px' }}>{saving ? 'SAVING...' : 'LOG IT'}</button>
            <button onClick={() => { setLogOpen(false); setLogNote('') }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '6px 10px', borderRadius: '5px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif' }}>CANCEL</button>
          </div>
        </div>
      )}
    </div>
  )
}

function TypeBadge({ type }) {
  const c = { 'Borrower': { bg: '#0e1f3d', border: '#1e3d6e', text: '#6b9ff7' }, 'Referral Source': { bg: '#001a08', border: '#005218', text: '#3ad460' }, 'Broker': { bg: '#2a1800', border: '#6b3a00', text: '#f09a3a' }, 'Lender': { bg: '#1e1030', border: '#3d1e68', text: '#b07ef7' } }[type] || { bg: 'var(--surface2)', border: 'var(--border)', text: 'var(--muted)' }
  return <span style={{ fontSize: '9px', padding: '2px 6px', borderRadius: '3px', background: c.bg, border: `1px solid ${c.border}`, color: c.text, fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{type}</span>
}

function Btn({ icon: Icon, onClick, danger, title }) {
  return (
    <button onClick={onClick} title={title} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: danger ? 'var(--danger)' : 'var(--muted)', display: 'flex', alignItems: 'center', transition: 'all 0.15s' }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = danger ? 'var(--danger)' : 'var(--border-hover)'; e.currentTarget.style.background = danger ? 'rgba(248,81,73,0.08)' : 'var(--surface2)' }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'transparent' }}
    ><Icon size={12} /></button>
  )
}
