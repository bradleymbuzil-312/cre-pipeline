import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { X } from 'lucide-react'
import { useToast } from './Toast'

const LENDER_TYPES = ['Bank', 'Credit Union', 'Life Company', 'Agency', 'CMBS', 'Debt Fund', 'SBA', 'Bridge Lender', 'Private', 'Other']
const ASSET_TYPES = ['Multifamily', 'Industrial', 'Office', 'Retail', 'Mixed-Use', 'Hospitality', 'Self-Storage', 'Medical Office', 'Manufactured Housing', 'Student Housing', 'Senior Housing', 'Land']
const LOAN_TYPES = ['Permanent', 'Bridge', 'Construction', 'Mini-Perm', 'CMBS', 'Agency', 'SBA', 'Mezzanine', 'Preferred Equity']

const EMPTY = {
  name: '', type: '', contact_name: '', email: '', phone: '',
  asset_types: [], geographies: '', loan_types: [],
  min_loan: '', max_loan: '', max_ltv: '', min_dscr: '',
  rate_spread: '', win_rate: '', notes: ''
}

export default function LenderModal({ lender, session, onClose, onSaved }) {
  const [form, setForm] = useState(() => {
    if (!lender) return { ...EMPTY }
    const f = { ...EMPTY, ...lender }
    f.asset_types = Array.isArray(lender.asset_types) ? lender.asset_types : []
    f.loan_types = Array.isArray(lender.loan_types) ? lender.loan_types : []
    f.geographies = Array.isArray(lender.geographies) ? lender.geographies.join(', ') : (lender.geographies || '')
    Object.keys(f).forEach(k => { if (f[k] === null || f[k] === undefined) f[k] = (Array.isArray(EMPTY[k]) ? [] : '') })
    return f
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const { toast } = useToast()

  function set(k, v) { setForm(f => ({ ...f, [k]: v })) }
  function num(v) { return v !== '' ? parseFloat(v) : null }
  function str(v) { return (typeof v === 'string' ? v.trim() : v) || null }

  function toggleArr(key, value) {
    setForm(f => {
      const arr = f[key] || []
      const next = arr.includes(value) ? arr.filter(x => x !== value) : [...arr, value]
      return { ...f, [key]: next }
    })
  }

  async function handleSave() {
    if (!form.name.trim()) { setError('Lender name is required.'); return }
    setSaving(true); setError('')
    const geoArr = form.geographies
      ? form.geographies.split(',').map(s => s.trim()).filter(Boolean)
      : null
    const payload = {
      name: str(form.name),
      type: str(form.type),
      contact_name: str(form.contact_name),
      email: str(form.email),
      phone: str(form.phone),
      asset_types: form.asset_types.length ? form.asset_types : null,
      geographies: geoArr,
      loan_types: form.loan_types.length ? form.loan_types : null,
      min_loan: num(form.min_loan),
      max_loan: num(form.max_loan),
      max_ltv: num(form.max_ltv),
      min_dscr: num(form.min_dscr),
      rate_spread: str(form.rate_spread),
      win_rate: num(form.win_rate),
      notes: str(form.notes),
      updated_at: new Date().toISOString(),
    }
    let err
    if (lender?.id) {
      ;({ error: err } = await supabase.from('lenders').update(payload).eq('id', lender.id))
    } else {
      ;({ error: err } = await supabase.from('lenders').insert({ ...payload, created_by: session.user.id }))
    }
    if (err) { setError(err.message); setSaving(false); return }
    toast(lender?.id ? 'Lender saved' : 'Lender created', 'success')
    onSaved(); onClose()
  }

  const IS = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '7px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }
  const LS = { display: 'block', marginBottom: '4px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.08em' }

  function Chip({ label, active, onClick }) {
    return (
      <button type="button" onClick={onClick} style={{
        padding: '4px 9px', borderRadius: '14px', fontSize: '11px', cursor: 'pointer',
        fontFamily: 'Syne, sans-serif', fontWeight: 600,
        border: '1px solid ' + (active ? '#2563eb' : 'var(--border)'),
        background: active ? '#2563eb' : 'transparent',
        color: active ? '#fff' : 'var(--muted)'
      }}>{label}</button>
    )
  }

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '720px', maxHeight: '92vh', display: 'flex', flexDirection: 'column', boxShadow: '0 24px 60px rgba(0,0,0,0.15)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 22px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '16px', color: 'var(--text)' }}>{lender ? 'Edit Lender' : 'New Lender'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
        </div>

        <div style={{ overflowY: 'auto', flex: 1, padding: '16px 22px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 14px', marginBottom: '18px' }}>
            <div style={{ gridColumn: '1 / -1' }}><label style={LS}>Lender Name *</label><input value={form.name} onChange={e => set('name', e.target.value)} style={IS} placeholder="Pacific Western Bank" /></div>
            <div><label style={LS}>Lender Type</label><select value={form.type} onChange={e => set('type', e.target.value)} style={IS}><option value="">Select...</option>{LENDER_TYPES.map(t => <option key={t} value={t}>{t}</option>)}</select></div>
            <div><label style={LS}>Contact Name</label><input value={form.contact_name} onChange={e => set('contact_name', e.target.value)} style={IS} placeholder="Jennifer Wu" /></div>
            <div><label style={LS}>Email</label><input type="email" value={form.email} onChange={e => set('email', e.target.value)} style={IS} placeholder="jwu@pwbank.com" /></div>
            <div><label style={LS}>Phone</label><input value={form.phone} onChange={e => set('phone', e.target.value)} style={IS} placeholder="(310) 555-7800" /></div>
          </div>

          <div style={{ padding: '12px 14px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '8px' }}>
            <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '12px' }}>Lender Box \u2014 Matching Criteria</div>

            <div style={{ marginBottom: '14px' }}>
              <label style={LS}>Asset Types</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                {ASSET_TYPES.map(t => <Chip key={t} label={t} active={form.asset_types.includes(t)} onClick={() => toggleArr('asset_types', t)} />)}
              </div>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <label style={LS}>Loan Types</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                {LOAN_TYPES.map(t => <Chip key={t} label={t} active={form.loan_types.includes(t)} onClick={() => toggleArr('loan_types', t)} />)}
              </div>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <label style={LS}>Geographies (comma-separated, e.g. CA, AZ, NV)</label>
              <input value={form.geographies} onChange={e => set('geographies', e.target.value)} style={IS} placeholder="CA, AZ, NV" />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '10px 12px' }}>
              <div><label style={LS}>Min Loan ($)</label><input type="number" value={form.min_loan} onChange={e => set('min_loan', e.target.value)} style={IS} placeholder="2000000" /></div>
              <div><label style={LS}>Max Loan ($)</label><input type="number" value={form.max_loan} onChange={e => set('max_loan', e.target.value)} style={IS} placeholder="35000000" /></div>
              <div><label style={LS}>Max LTV (%)</label><input type="number" value={form.max_ltv} onChange={e => set('max_ltv', e.target.value)} style={IS} step="0.1" placeholder="70" /></div>
              <div><label style={LS}>Min DSCR</label><input type="number" value={form.min_dscr} onChange={e => set('min_dscr', e.target.value)} style={IS} step="0.01" placeholder="1.25" /></div>
              <div style={{ gridColumn: '1 / 3' }}><label style={LS}>Rate Spread</label><input value={form.rate_spread} onChange={e => set('rate_spread', e.target.value)} style={IS} placeholder="T+200-275" /></div>
              <div style={{ gridColumn: '3 / 5' }}><label style={LS}>Win Rate (0-1)</label><input type="number" value={form.win_rate} onChange={e => set('win_rate', e.target.value)} style={IS} step="0.01" placeholder="0.42" /></div>
            </div>
          </div>

          <div style={{ marginTop: '14px' }}>
            <label style={LS}>Notes</label>
            <textarea value={form.notes} onChange={e => set('notes', e.target.value)} rows={3} placeholder="Relationship notes, flexibility, past deals..." style={{ ...IS, resize: 'vertical', lineHeight: 1.5, fontFamily: 'DM Sans, sans-serif' }} />
          </div>

          {error && <div style={{ marginTop: '14px', padding: '10px 14px', borderRadius: '6px', background: '#fef2f2', border: '1px solid #fecaca', color: '#ef4444', fontSize: '13px' }}>{error}</div>}
        </div>

        <div style={{ padding: '12px 22px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'flex-end', gap: '10px', flexShrink: 0 }}>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px' }}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{ background: saving ? '#93c5fd' : '#2563eb', border: 'none', color: '#fff', padding: '8px 24px', borderRadius: '6px', cursor: saving ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>{saving ? 'SAVING...' : lender ? 'SAVE CHANGES' : 'ADD LENDER'}</button>
        </div>
      </div>
    </div>
  )
}