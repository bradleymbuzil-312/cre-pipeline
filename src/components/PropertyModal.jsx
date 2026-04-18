import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { X, ExternalLink } from 'lucide-react'
import { PROPERTY_TYPES } from '../lib/constants'
import { useToast } from './Toast'

const EMPTY = { address: '', city: '', state: '', zip: '', property_type: '', total_units: '', sq_ft: '', year_built: '', borrower_id: '', notes: '' }

export default function PropertyModal({ property, session, onClose, onSaved }) {
  const [form, setForm] = useState(() => {
    if (!property) return { ...EMPTY }
    const f = { ...EMPTY, ...property }
    Object.keys(f).forEach(k => { if (f[k] === null || f[k] === undefined) f[k] = '' })
    return f
  })
  const [borrowers, setBorrowers] = useState([])
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const { toast } = useToast()

  useEffect(() => {
    supabase.from('clients').select('id, first_name, last_name, company').eq('client_type', 'Borrower').order('first_name').then(({data}) => setBorrowers(data || []))
  }, [])

  function set(k, v) { setForm(f => ({ ...f, [k]: v })) }
  function num(v) { return v !== '' ? parseFloat(v) : null }
  function int(v) { return v !== '' ? parseInt(v) : null }
  function str(v) { return v?.trim() || null }

  function openReonomySearch() {
    const q = [form.address, form.city, form.state].filter(Boolean).join(' ')
    if (!q) { toast('Enter an address first', 'info'); return }
    window.open('https://app.reonomy.com/!/search?q=' + encodeURIComponent(q), '_blank', 'noopener')
  }

  async function handleSave() {
    if (!form.address.trim()) { setError('Address is required.'); return }
    setSaving(true); setError('')
    const payload = {
      address: str(form.address),
      city: str(form.city),
      state: str(form.state),
      zip: str(form.zip),
      property_type: str(form.property_type),
      total_units: int(form.total_units),
      sq_ft: num(form.sq_ft),
      year_built: int(form.year_built),
      borrower_id: form.borrower_id || null,
      notes: str(form.notes),
      updated_at: new Date().toISOString(),
    }
    let err
    if (property?.id) {
      ;({ error: err } = await supabase.from('properties').update(payload).eq('id', property.id))
    } else {
      ;({ error: err } = await supabase.from('properties').insert({ ...payload, created_by: session.user.id }))
    }
    if (err) { setError(err.message); setSaving(false); return }
    toast(property?.id ? 'Property saved' : 'Property created', 'success')
    onSaved(); onClose()
  }

  const IS = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '7px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }
  const LS = { display: 'block', marginBottom: '4px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.08em' }

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '640px', maxHeight: '90vh', display: 'flex', flexDirection: 'column', boxShadow: '0 24px 60px rgba(0,0,0,0.15)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 22px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '16px', color: 'var(--text)' }}>{property ? 'Edit Property' : 'New Property'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
        </div>

        <div style={{ overflowY: 'auto', flex: 1, padding: '16px 22px' }}>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
            <button onClick={openReonomySearch} disabled={!form.address} title={form.address ? 'Open Reonomy with this address pre-filled' : 'Enter an address to enable'} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', color: form.address ? 'var(--text)' : 'var(--muted)', border: '1px solid var(--border)', padding: '7px 12px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', cursor: form.address ? 'pointer' : 'not-allowed', letterSpacing: '0.04em', opacity: form.address ? 1 : 0.5 }}>
              <ExternalLink size={12} /> LOOK UP ON REONOMY
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px 14px' }}>
            <div style={{ gridColumn: '1 / -1' }}><label style={LS}>Address *</label><input value={form.address} onChange={e => set('address', e.target.value)} placeholder="123 Main St" style={IS} /></div>
            <div><label style={LS}>City</label><input value={form.city} onChange={e => set('city', e.target.value)} style={IS} /></div>
            <div><label style={LS}>State</label><input value={form.state} onChange={e => set('state', e.target.value)} style={IS} /></div>
            <div><label style={LS}>Zip</label><input value={form.zip} onChange={e => set('zip', e.target.value)} style={IS} /></div>
            <div><label style={LS}>Property Type</label>
              <select value={form.property_type} onChange={e => set('property_type', e.target.value)} style={IS}>
                <option value="">Select...</option>
                {PROPERTY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div><label style={LS}>Total Units</label><input type="number" value={form.total_units} onChange={e => set('total_units', e.target.value)} style={IS} /></div>
            <div><label style={LS}>Sq Ft</label><input type="number" value={form.sq_ft} onChange={e => set('sq_ft', e.target.value)} style={IS} /></div>
            <div><label style={LS}>Year Built</label><input type="number" value={form.year_built} onChange={e => set('year_built', e.target.value)} style={IS} /></div>
            <div style={{ gridColumn: '1 / span 2' }}><label style={LS}>Borrower</label>
              <select value={form.borrower_id} onChange={e => set('borrower_id', e.target.value)} style={IS}>
                <option value="">No borrower assigned</option>
                {borrowers.map(b => <option key={b.id} value={b.id}>{b.first_name} {b.last_name || ''}{b.company ? ' \u2014 ' + b.company : ''}</option>)}
              </select>
            </div>
            <div style={{ gridColumn: '1 / -1' }}><label style={LS}>Notes</label><textarea value={form.notes} onChange={e => set('notes', e.target.value)} rows={5} placeholder="Property details, owner info, access notes, tenant info..." style={{ ...IS, resize: 'vertical', lineHeight: 1.5, fontFamily: 'DM Sans, sans-serif' }} /></div>
            {error && <div style={{ gridColumn: '1 / -1', padding: '10px 14px', borderRadius: '6px', background: '#fef2f2', border: '1px solid #fecaca', color: '#ef4444', fontSize: '13px' }}>{error}</div>}
          </div>
        </div>

        <div style={{ padding: '12px 22px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'flex-end', gap: '10px', flexShrink: 0 }}>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px' }}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{ background: saving ? '#93c5fd' : '#2563eb', border: 'none', color: '#fff', padding: '8px 24px', borderRadius: '6px', cursor: saving ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>{saving ? 'SAVING...' : property ? 'SAVE CHANGES' : 'ADD PROPERTY'}</button>
        </div>
      </div>
    </div>
  )
}