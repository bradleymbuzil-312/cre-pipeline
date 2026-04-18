import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { X, Clipboard, ExternalLink, Check, AlertCircle } from 'lucide-react'
import { PROPERTY_TYPES } from '../lib/constants'
import { useToast } from './Toast'

const EMPTY = { address: '', city: '', state: '', zip: '', property_type: '', total_units: '', sq_ft: '', year_built: '', borrower_id: '', notes: '' }

// ===== Reonomy parser =====
// Parses pasted text from Reonomy property pages into structured fields.
// Does NOT scrape Reonomy's site directly (user-initiated copy/paste only).
function parseReonomyText(raw) {
  if (!raw || !raw.trim()) return {}
  const text = raw.replace(/\u00a0/g, ' ')
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean)
  const pairs = {}

  // Pass 1: same-line 'Key: Value' or 'Key Value' pairs
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    // 'Key: Value' or 'Key\tValue'
    const kv = line.match(/^([A-Za-z][A-Za-z0-9 ()/&.'-]{1,50})[:\t]\s*(.+)$/)
    if (kv) {
      const key = kv[1].toLowerCase().replace(/[\s_-]+/g, ' ').trim()
      if (!pairs[key]) pairs[key] = kv[2].trim()
      continue
    }
    // Two-line format: label on one line, value on next (Reonomy stacks this way)
    if (i + 1 < lines.length) {
      const label = line
      const next = lines[i + 1]
      // label looks like a label (short, no digits except in parens), value looks like data
      if (label.length < 40 && !/^\d/.test(label) && /[a-zA-Z]/.test(label) && !/^[A-Z]{3,}$/.test(label) && next) {
        const key = label.toLowerCase().replace(/[\s_-]+/g, ' ').replace(/[:]/g, '').trim()
        if (!pairs[key]) pairs[key] = next
      }
    }
  }

  // Helpers
  const getByLabels = labels => {
    for (const l of labels) { if (pairs[l]) return pairs[l] }
    return null
  }
  const numeric = v => {
    if (!v) return null
    const m = String(v).replace(/[^\d.-]/g, '')
    const n = parseFloat(m)
    return isNaN(n) ? null : n
  }
  const integer = v => { const n = numeric(v); return n != null ? Math.round(n) : null }
  const cleanText = v => v ? String(v).trim().replace(/\s+/g, ' ') : null
  const dateISO = v => {
    if (!v) return null
    const s = String(v).trim()
    // Try MM/DD/YYYY
    const us = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})/)
    if (us) {
      const mm = us[1].padStart(2, '0'); const dd = us[2].padStart(2, '0')
      let yy = us[3]; if (yy.length === 2) yy = (parseInt(yy) > 30 ? '19' : '20') + yy
      return yy + '-' + mm + '-' + dd
    }
    // Try YYYY-MM-DD
    if (/^\d{4}-\d{2}-\d{2}/.test(s)) return s.slice(0, 10)
    // Try 'Month DD, YYYY'
    const d = new Date(s.replace(/,/g, ''))
    if (!isNaN(d.getTime())) return d.toISOString().slice(0, 10)
    return null
  }

  const result = {}

  // Address — Reonomy often shows full address as 'Property Address' or just at top
  const rawAddr = getByLabels(['property address', 'address', 'street address'])
  if (rawAddr) {
    // Split '123 Main St, Los Angeles, CA 90001' format
    const parts = rawAddr.split(',').map(p => p.trim())
    if (parts.length >= 3) {
      result.address = parts[0]
      result.city = parts[1]
      const sz = parts[parts.length - 1].match(/([A-Z]{2})\s+(\d{5})/)
      if (sz) { result.state = sz[1]; result.zip = sz[2] }
    } else {
      result.address = rawAddr
    }
  }
  if (!result.city) { const c = getByLabels(['city']); if (c) result.city = cleanText(c) }
  if (!result.state) { const s = getByLabels(['state']); if (s) result.state = cleanText(s) }
  if (!result.zip) { const z = getByLabels(['zip', 'zip code', 'postal code']); if (z) result.zip = cleanText(String(z).match(/\d{5}/)?.[0] || z) }

  // Property type
  const ptype = getByLabels(['property type', 'use type', 'asset type', 'type', 'property use', 'subtype'])
  if (ptype) {
    const t = String(ptype).toLowerCase()
    const match = PROPERTY_TYPES.find(pt => t.includes(pt.toLowerCase()))
    result.property_type = match || cleanText(ptype)
  }

  // Year built
  const yb = getByLabels(['year built', 'built', 'construction year', 'year'])
  if (yb) {
    const y = integer(yb)
    if (y && y > 1700 && y < 2100) result.year_built = y
  }

  // Units
  const units = getByLabels(['total units', 'units', 'unit count', 'number of units', 'residential units', 'apartment units'])
  if (units) result.total_units = integer(units)

  // Square footage (building)
  const sqft = getByLabels(['building size', 'gross building area', 'total sq ft', 'building sf', 'total building area', 'gla', 'sq ft', 'square feet', 'building square feet'])
  if (sqft) result.sq_ft = numeric(sqft)

  // Extras to stuff into notes (owner, assessed value, last sale, lot size)
  const extras = {}
  const owner = getByLabels(['owner', 'owner name', 'current owner', 'true owner', 'owner(s)', 'owners'])
  if (owner) extras['Owner'] = cleanText(owner)
  const mailing = getByLabels(['mailing address', 'owner mailing address', 'owner address'])
  if (mailing) extras['Owner Mailing'] = cleanText(mailing)
  const assessed = getByLabels(['assessed value', 'total assessed value', 'assessment', 'total assessment'])
  if (assessed) extras['Assessed Value'] = '$' + numeric(assessed)?.toLocaleString()
  const saleDate = getByLabels(['last sale date', 'sale date', 'most recent sale date', 'recorded date', 'last transfer date'])
  const salePrice = getByLabels(['last sale price', 'sale price', 'most recent sale price', 'last transfer price'])
  if (saleDate || salePrice) {
    const sd = dateISO(saleDate)
    const sp = numeric(salePrice)
    extras['Last Sale'] = (sd || '?') + (sp ? ' \u00b7 $' + sp.toLocaleString() : '')
  }
  const lot = getByLabels(['lot size', 'lot square feet', 'lot sf', 'parcel size', 'land size', 'lot area'])
  if (lot) {
    const lv = numeric(lot)
    if (lv) extras['Lot Size'] = lv.toLocaleString() + ' sq ft'
  }
  const apn = getByLabels(['apn', 'parcel id', 'parcel number', 'assessor parcel number'])
  if (apn) extras['APN'] = cleanText(apn)
  const zoning = getByLabels(['zoning', 'zoning code'])
  if (zoning) extras['Zoning'] = cleanText(zoning)

  result._extras = extras
  return result
}

function formatExtrasAsNotes(extras) {
  const keys = Object.keys(extras)
  if (!keys.length) return ''
  const today = new Date().toISOString().slice(0, 10)
  return '--- REONOMY DATA (pasted ' + today + ') ---\n' + keys.map(k => k + ': ' + extras[k]).join('\n')
}

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
  const [pasteOpen, setPasteOpen] = useState(false)
  const [pasteText, setPasteText] = useState('')
  const [pasteResult, setPasteResult] = useState(null)
  const [pasteError, setPasteError] = useState('')
  const { toast } = useToast()

  useEffect(() => {
    supabase.from('clients').select('id, first_name, last_name, company').eq('client_type', 'Borrower').order('first_name').then(({data}) => setBorrowers(data || []))
  }, [])

  function set(k, v) { setForm(f => ({ ...f, [k]: v })) }
  function num(v) { return v !== '' ? parseFloat(v) : null }
  function int(v) { return v !== '' ? parseInt(v) : null }
  function str(v) { return v?.trim() || null }

  function handleParsePaste() {
    setPasteError('')
    if (!pasteText.trim()) { setPasteError('Paste content from Reonomy first.'); return }
    try {
      const parsed = parseReonomyText(pasteText)
      const fieldCount = Object.keys(parsed).filter(k => k !== '_extras' && parsed[k] != null && parsed[k] !== '').length
      const extraCount = parsed._extras ? Object.keys(parsed._extras).length : 0
      if (fieldCount === 0 && extraCount === 0) {
        setPasteError('Could not find any recognizable fields. Try copying the full property details section, or paste a different part of the page.')
        return
      }
      setPasteResult(parsed)
    } catch (e) {
      setPasteError('Parse error: ' + e.message)
    }
  }

  function handleApplyPaste() {
    if (!pasteResult) return
    const extras = pasteResult._extras || {}
    setForm(f => {
      const updated = { ...f }
      for (const [k, v] of Object.entries(pasteResult)) {
        if (k === '_extras' || v == null || v === '') continue
        updated[k] = v
      }
      const extraNotes = formatExtrasAsNotes(extras)
      if (extraNotes) {
        updated.notes = f.notes ? (f.notes.trim() + '\n\n' + extraNotes) : extraNotes
      }
      return updated
    })
    setPasteOpen(false)
    setPasteText('')
    setPasteResult(null)
    toast('Fields filled from Reonomy', 'success')
  }

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
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '680px', maxHeight: '92vh', display: 'flex', flexDirection: 'column', boxShadow: '0 24px 60px rgba(0,0,0,0.15)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 22px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '16px', color: 'var(--text)' }}>{property ? 'Edit Property' : 'New Property'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
        </div>

        <div style={{ overflowY: 'auto', flex: 1, padding: '16px 22px' }}>

          {/* Reonomy actions row */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '14px', flexWrap: 'wrap' }}>
            <button onClick={() => setPasteOpen(o => !o)} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: pasteOpen ? '#2563eb' : 'var(--surface2)', color: pasteOpen ? '#fff' : 'var(--text)', border: '1px solid ' + (pasteOpen ? '#2563eb' : 'var(--border)'), padding: '7px 12px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', cursor: 'pointer', letterSpacing: '0.04em' }}>
              <Clipboard size={12} /> PASTE FROM REONOMY
            </button>
            <button onClick={openReonomySearch} disabled={!form.address} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--surface2)', color: form.address ? 'var(--text)' : 'var(--muted)', border: '1px solid var(--border)', padding: '7px 12px', borderRadius: '6px', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px', cursor: form.address ? 'pointer' : 'not-allowed', letterSpacing: '0.04em', opacity: form.address ? 1 : 0.5 }}>
              <ExternalLink size={12} /> SEARCH ON REONOMY
            </button>
          </div>

          {/* Paste panel */}
          {pasteOpen && (
            <div style={{ background: 'var(--surface2)', border: '1px solid #2563eb', borderRadius: '8px', padding: '14px', marginBottom: '16px' }}>
              <div style={{ fontSize: '12px', color: 'var(--text)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>Paste Reonomy Property Details</div>
              <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '10px', lineHeight: 1.5 }}>Copy the property details section from Reonomy (Ctrl+A on the details panel works well) and paste it below. The parser will extract address, year built, units, sq ft, owner, assessed value, and last sale info.</div>
              <textarea value={pasteText} onChange={e => setPasteText(e.target.value)} rows={6} placeholder="Paste here..." style={{ ...IS, resize: 'vertical', lineHeight: 1.5, fontFamily: 'IBM Plex Mono, monospace', fontSize: '11px' }} />
              {pasteError && <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', color: '#b91c1c', fontSize: '11px', borderRadius: '5px', marginTop: '8px' }}><AlertCircle size={12} /> {pasteError}</div>}

              {pasteResult && (
                <div style={{ marginTop: '10px', padding: '10px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}>
                  <div style={{ fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>Preview</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {Object.entries(pasteResult).filter(([k, v]) => k !== '_extras' && v != null && v !== '').map(([k, v]) => (
                      <div key={k} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}>
                        <Check size={11} color="#16a34a" />
                        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 600, color: 'var(--muted)', textTransform: 'capitalize', minWidth: '110px' }}>{k.replace(/_/g, ' ')}:</span>
                        <span style={{ color: 'var(--text)', fontFamily: 'IBM Plex Mono, monospace' }}>{String(v)}</span>
                      </div>
                    ))}
                    {pasteResult._extras && Object.entries(pasteResult._extras).map(([k, v]) => (
                      <div key={'x-'+k} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}>
                        <Check size={11} color="#2563eb" />
                        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 600, color: 'var(--muted)', minWidth: '110px' }}>{k}:</span>
                        <span style={{ color: 'var(--text)', fontFamily: 'IBM Plex Mono, monospace' }}>{v}</span>
                      </div>
                    ))}
                  </div>
                  {pasteResult._extras && Object.keys(pasteResult._extras).length > 0 && (
                    <div style={{ fontSize: '10px', color: 'var(--muted)', marginTop: '8px', fontStyle: 'italic' }}>Blue items will be added to the Notes field (no dedicated columns yet).</div>
                  )}
                </div>
              )}

              <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end', marginTop: '10px' }}>
                <button onClick={() => { setPasteOpen(false); setPasteText(''); setPasteResult(null); setPasteError('') }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '6px 14px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px' }}>CANCEL</button>
                {!pasteResult ? (
                  <button onClick={handleParsePaste} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '6px 16px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px' }}>PARSE</button>
                ) : (
                  <button onClick={handleApplyPaste} style={{ background: '#16a34a', border: 'none', color: '#fff', padding: '6px 16px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px' }}>APPLY TO FORM</button>
                )}
              </div>
            </div>
          )}

          {/* Form grid */}
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