import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { X } from 'lucide-react'

const CLIENT_TYPES = ['Borrower', 'Referral Source', 'Broker', 'Lender', 'Other']
const EMPTY = { first_name: '', last_name: '', company: '', email: '', phone: '', client_type: 'Borrower', referral_source: '', follow_up_date: '', follow_up_note: '', notes: '' }

export default function ClientModal({ client, session, onClose, onSaved }) {
  const [form, setForm] = useState(client ? { ...EMPTY, ...client, follow_up_date: client.follow_up_date || '', follow_up_note: client.follow_up_note || '' } : { ...EMPTY })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function set(key, value) { setForm(f => ({ ...f, [key]: value })) }

  async function handleSave() {
    if (!form.first_name.trim()) { setError('First name is required.'); return }
    setSaving(true); setError('')
    const payload = {
      first_name: form.first_name.trim(), last_name: form.last_name.trim() || null,
      company: form.company.trim() || null, email: form.email.trim() || null,
      phone: form.phone.trim() || null, client_type: form.client_type,
      referral_source: form.referral_source.trim() || null,
      follow_up_date: form.follow_up_date || null, follow_up_note: form.follow_up_note.trim() || null,
      notes: form.notes.trim() || null, updated_at: new Date().toISOString(),
    }
    let err
    if (client?.id) { ;({ error: err } = await supabase.from('clients').update(payload).eq('id', client.id)) }
    else { ;({ error: err } = await supabase.from('clients').insert({ ...payload, created_by: session.user.id })) }
    if (err) { setError(err.message); setSaving(false); return }
    onSaved(); onClose()
  }

  const inputStyle = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '8px 12px', fontSize: '13px', fontFamily: 'DM Sans, sans-serif', transition: 'border-color 0.15s', boxSizing: 'border-box' }
  const labelStyle = { display: 'block', marginBottom: '6px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.09em' }

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '620px', maxHeight: '92vh', display: 'flex', flexDirection: 'column', boxShadow: '0 32px 80px rgba(0,0,0,0.7)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '18px 24px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '17px', color: 'var(--text)' }}>{client ? 'Edit Client' : 'New Client'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={16} /></button>
        </div>

        <div style={{ overflowY: 'auto', flex: 1, padding: '22px 24px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div><label style={labelStyle}>First Name <span style={{ color: 'var(--gold)' }}>*</span></label><input value={form.first_name} onChange={e => set('first_name', e.target.value)} style={inputStyle} placeholder="John" /></div>
            <div><label style={labelStyle}>Last Name</label><input value={form.last_name} onChange={e => set('last_name', e.target.value)} style={inputStyle} placeholder="Smith" /></div>
            <div style={{ gridColumn: '1 / -1' }}><label style={labelStyle}>Company</label><input value={form.company} onChange={e => set('company', e.target.value)} style={inputStyle} placeholder="Acme Real Estate LLC" /></div>
            <div><label style={labelStyle}>Email</label><input type="email" value={form.email} onChange={e => set('email', e.target.value)} style={inputStyle} placeholder="john@example.com" /></div>
            <div><label style={labelStyle}>Phone</label><input value={form.phone} onChange={e => set('phone', e.target.value)} style={inputStyle} placeholder="(310) 555-0100" /></div>
            <div><label style={labelStyle}>Client Type</label><select value={form.client_type} onChange={e => set('client_type', e.target.value)} style={inputStyle}>{CLIENT_TYPES.map(t => <option key={t} value={t}>{t}</option>)}</select></div>
            <div><label style={labelStyle}>Referred By</label><input value={form.referral_source} onChange={e => set('referral_source', e.target.value)} style={inputStyle} placeholder="Name or company" /></div>
            <div style={{ gridColumn: '1 / -1', height: '1px', background: 'var(--border)', margin: '4px 0' }} />
            <div><label style={labelStyle}>Follow-up Date</label><input type="date" value={form.follow_up_date} onChange={e => set('follow_up_date', e.target.value)} style={inputStyle} /></div>
            <div><label style={labelStyle}>Follow-up Note</label><input value={form.follow_up_note} onChange={e => set('follow_up_note', e.target.value)} style={inputStyle} placeholder="What to discuss..." /></div>
            <div style={{ gridColumn: '1 / -1' }}><label style={labelStyle}>Deal Notes</label><textarea value={form.notes} onChange={e => set('notes', e.target.value)} rows={4} placeholder="Key deal details, preferences, history, outstanding items..." style={{ ...inputStyle, resize: 'vertical', lineHeight: 1.6 }} /></div>
          </div>
          {error && <div style={{ marginTop: '16px', padding: '10px 14px', borderRadius: '6px', background: 'rgba(248,81,73,0.08)', border: '1px solid rgba(248,81,73,0.25)', color: 'var(--danger)', fontSize: '13px' }}>{error}</div>}
        </div>

        <div style={{ padding: '14px 24px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'flex-end', gap: '10px', flexShrink: 0 }}>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', letterSpacing: '0.04em' }}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{ background: saving ? 'var(--gold-dim)' : 'var(--gold)', border: 'none', color: '#000', padding: '8px 24px', borderRadius: '6px', cursor: saving ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>{saving ? 'SAVING...' : client ? 'SAVE CHANGES' : 'ADD CLIENT'}</button>
        </div>
      </div>
    </div>
  )
}