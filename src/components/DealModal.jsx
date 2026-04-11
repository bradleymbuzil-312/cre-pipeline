import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { X } from 'lucide-react'
import { STAGES, PROPERTY_TYPES } from '../lib/constants'

const FIELDS = [
  { key: 'borrower_name',       label: 'Borrower Name',        type: 'text',     required: true, span: 2 },
  { key: 'property_address',    label: 'Property Address',     type: 'text',     span: 2 },
  { key: 'property_type',       label: 'Property Type',        type: 'select',   options: PROPERTY_TYPES },
  { key: 'stage',               label: 'Stage',                type: 'select',   options: STAGES },
  { key: 'loan_amount',         label: 'Loan Amount ($)',      type: 'number',   placeholder: 'e.g. 5500000' },
  { key: 'commission_fee',      label: 'Commission / Fee ($)', type: 'number',   placeholder: 'e.g. 55000' },
  { key: 'ltv',                 label: 'LTV (%)',              type: 'number',   placeholder: 'e.g. 65', step: '0.1' },
  { key: 'dscr',                label: 'DSCR',                 type: 'number',   placeholder: 'e.g. 1.25', step: '0.01' },
  { key: 'lender_name',         label: 'Lender Name',          type: 'text' },
  { key: 'expected_close_date', label: 'Expected Close Date',  type: 'date' },
  { key: 'notes',               label: 'Notes / Next Steps',   type: 'textarea', span: 2 },
]

const EMPTY = {
  borrower_name: '', property_address: '', property_type: '',
  stage: 'Prospecting', loan_amount: '', commission_fee: '',
  ltv: '', dscr: '', lender_name: '', expected_close_date: '', notes: '',
}

export default function DealModal({ deal, session, onClose, onSaved }) {
  const [form, setForm] = useState(deal ? {
    ...EMPTY,
    ...deal,
    loan_amount: deal.loan_amount ?? '',
    commission_fee: deal.commission_fee ?? '',
    ltv: deal.ltv ?? '',
    dscr: deal.dscr ?? '',
  } : { ...EMPTY })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function set(key, value) { setForm(f => ({ ...f, [key]: value })) }

  async function handleSave() {
    if (!form.borrower_name.trim()) { setError('Borrower name is required.'); return }
    setSaving(true); setError('')

    const payload = {
      borrower_name:       form.borrower_name.trim(),
      property_address:    form.property_address.trim() || null,
      property_type:       form.property_type || null,
      stage:               form.stage,
      loan_amount:         form.loan_amount !== '' ? parseFloat(form.loan_amount) : null,
      commission_fee:      form.commission_fee !== '' ? parseFloat(form.commission_fee) : null,
      ltv:                 form.ltv !== '' ? parseFloat(form.ltv) : null,
      dscr:                form.dscr !== '' ? parseFloat(form.dscr) : null,
      lender_name:         form.lender_name.trim() || null,
      expected_close_date: form.expected_close_date || null,
      notes:               form.notes.trim() || null,
      updated_at:          new Date().toISOString(),
    }

    let err
    if (deal?.id) {
      ;({ error: err } = await supabase.from('deals').update(payload).eq('id', deal.id))
    } else {
      ;({ error: err } = await supabase.from('deals').insert({ ...payload, created_by: session.user.id }))
    }

    if (err) { setError(err.message); setSaving(false); return }
    onSaved(); onClose()
  }

  return (
    <div
      onClick={e => { if (e.target === e.currentTarget) onClose() }}
      style={{
        position: 'fixed', inset: 0, zIndex: 1000,
        background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px'
      }}
    >
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--border)',
        borderRadius: '12px', width: '100%', maxWidth: '680px',
        maxHeight: '92vh', display: 'flex', flexDirection: 'column',
        boxShadow: '0 32px 80px rgba(0,0,0,0.7)',
      }}>

        {/* Modal header */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '18px 24px', borderBottom: '1px solid var(--border)', flexShrink: 0
        }}>
          <div>
            <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '17px', color: 'var(--text)' }}>
              {deal ? 'Edit Deal' : 'New Deal'}
            </h2>
            {deal && (
              <div style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '2px', fontFamily: 'IBM Plex Mono, monospace' }}>
                {deal.borrower_name}
              </div>
            )}
          </div>
          <button onClick={onClose} style={{
            background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)',
            cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center',
            transition: 'color 0.15s, border-color 0.15s'
          }}
          onMouseEnter={e => { e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.borderColor = 'var(--border-hover)' }}
          onMouseLeave={e => { e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.borderColor = 'var(--border)' }}
          >
            <X size={16} />
          </button>
        </div>

        {/* Form body */}
        <div style={{ overflowY: 'auto', flex: 1, padding: '22px 24px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            {FIELDS.map(field => (
              <div key={field.key} style={{ gridColumn: field.span === 2 ? '1 / -1' : 'auto' }}>
                <label style={{
                  display: 'block', marginBottom: '6px',
                  fontSize: '10px', fontWeight: 700, color: 'var(--muted)',
                  fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.09em'
                }}>
                  {field.label}
                  {field.required && <span style={{ color: 'var(--gold)', marginLeft: '3px' }}>*</span>}
                </label>

                {field.type === 'select' ? (
                  <select value={form[field.key] || ''} onChange={e => set(field.key, e.target.value)} style={inputStyle}>
                    <option value="">Select...</option>
                    {field.options.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                ) : field.type === 'textarea' ? (
                  <textarea
                    value={form[field.key] || ''}
                    onChange={e => set(field.key, e.target.value)}
                    rows={3}
                    placeholder="Key next steps, outstanding items, lender notes..."
                    style={{ ...inputStyle, resize: 'vertical', fontFamily: 'DM Sans, sans-serif', lineHeight: 1.5 }}
                  />
                ) : (
                  <input
                    type={field.type}
                    value={form[field.key] || ''}
                    onChange={e => set(field.key, e.target.value)}
                    step={field.step}
                    placeholder={field.placeholder}
                    style={inputStyle}
                    onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSave()}
                  />
                )}
              </div>
            ))}
          </div>

          {error && (
            <div style={{
              marginTop: '16px', padding: '10px 14px', borderRadius: '6px',
              background: 'rgba(248,81,73,0.08)', border: '1px solid rgba(248,81,73,0.25)',
              color: 'var(--danger)', fontSize: '13px'
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          padding: '14px 24px', borderTop: '1px solid var(--border)',
          display: 'flex', justifyContent: 'flex-end', gap: '10px', flexShrink: 0
        }}>
          <button onClick={onClose} style={{
            background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)',
            padding: '8px 20px', borderRadius: '6px', cursor: 'pointer',
            fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px', letterSpacing: '0.04em',
            transition: 'border-color 0.15s'
          }}
          onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--border-hover)'}
          onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
          >
            CANCEL
          </button>
          <button onClick={handleSave} disabled={saving} style={{
            background: saving ? 'var(--gold-dim)' : 'var(--gold)',
            border: 'none', color: '#000',
            padding: '8px 24px', borderRadius: '6px', cursor: saving ? 'not-allowed' : 'pointer',
            fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em',
            transition: 'background 0.15s'
          }}>
            {saving ? 'SAVING...' : deal ? 'SAVE CHANGES' : 'ADD DEAL'}
          </button>
        </div>
      </div>
    </div>
  )
}

const inputStyle = {
  width: '100%',
  background: 'var(--surface2)',
  border: '1px solid var(--border)',
  color: 'var(--text)',
  borderRadius: '6px',
  padding: '8px 12px',
  fontSize: '13px',
  fontFamily: 'IBM Plex Mono, monospace',
  transition: 'border-color 0.15s',
}
