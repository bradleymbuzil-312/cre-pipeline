import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { ExternalLink, Plus, Trash2, FileText, Link as LinkIcon } from 'lucide-react'
import { useToast } from './Toast'

const DOC_LABELS = [
  'OM / Marketing Package',
  'T-12 / Financials',
  'Rent Roll',
  'Appraisal',
  'PCA / ESA',
  'Title',
  'Survey',
  'Term Sheet',
  'LOI',
  'PSA / Contract',
  'Operating Agreement',
  'Loan Docs',
  'Closing Docs',
  'Other',
]

export default function DealLinks({ dealId, session }) {
  const [links, setLinks] = useState([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [newLabel, setNewLabel] = useState('OM / Marketing Package')
  const [newUrl, setNewUrl] = useState('')
  const [customLabel, setCustomLabel] = useState('')
  const [error, setError] = useState('')
  const { toast } = useToast()

  useEffect(() => { if (dealId) fetchLinks() }, [dealId])

  async function fetchLinks() {
    const { data } = await supabase.from('deal_links').select('*').eq('deal_id', dealId).order('created_at', { ascending: false })
    setLinks(data || [])
    setLoading(false)
  }

  async function addLink() {
    const url = newUrl.trim()
    if (!url) { setError('URL is required.'); return }
    if (!/^https?:\/\//i.test(url)) { setError('URL must start with http:// or https://'); return }
    const label = newLabel === 'Other' ? (customLabel.trim() || 'Other') : newLabel
    const { error: err } = await supabase.from('deal_links').insert({
      deal_id: dealId,
      label,
      url,
      added_by: session.user.id,
      added_by_email: session.user.email,
    })
    if (err) { setError(err.message); return }
    setNewUrl('')
    setCustomLabel('')
    setError('')
    setAdding(false)
    fetchLinks()
    toast('Document link added', 'success')
  }

  async function deleteLink(id) {
    if (!window.confirm('Remove this document link?')) return
    const { error: err } = await supabase.from('deal_links').delete().eq('id', id)
    if (err) { toast('Error removing link', 'error'); return }
    fetchLinks()
    toast('Link removed', 'success')
  }

  function hostFromUrl(url) {
    try { return new URL(url).hostname.replace('www.', '') } catch { return '' }
  }

  function isOneDrive(url) {
    const h = hostFromUrl(url).toLowerCase()
    return h.includes('sharepoint') || h.includes('onedrive') || h.includes('1drv')
  }

  const IS = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '7px 10px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }
  const LS = { display: 'block', marginBottom: '4px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.08em' }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {loading ? (
        <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>LOADING...</div>
      ) : links.length === 0 && !adding ? (
        <div style={{ fontSize: '12px', color: 'var(--muted)', padding: '16px', background: 'var(--surface2)', borderRadius: '6px', textAlign: 'center', lineHeight: 1.6 }}>
          No documents yet. Paste a OneDrive or SharePoint share link to start tracking documents for this deal.
        </div>
      ) : (
        links.map(link => (
          <div key={link.id} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px 12px', background: 'var(--surface2)', borderRadius: '6px', border: '1px solid var(--border)' }}>
            <FileText size={14} color={isOneDrive(link.url) ? '#2563eb' : 'var(--muted)'} style={{ flexShrink: 0 }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <a href={link.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', textDecoration: 'none', display: 'block', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
                onMouseEnter={e => e.currentTarget.style.color = '#2563eb'}
                onMouseLeave={e => e.currentTarget.style.color = 'var(--text)'}>
                {link.label || 'Document'}
              </a>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', marginTop: '2px' }}>
                <LinkIcon size={9} />
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{hostFromUrl(link.url) || link.url}</span>
                {link.added_by_email && <>
                  <span>\u00b7</span>
                  <span>{link.added_by_email.split('@')[0]}</span>
                </>}
              </div>
            </div>
            <a href={link.url} target="_blank" rel="noopener noreferrer" title="Open in new tab" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', color: 'var(--muted)', display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.color = '#2563eb' }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
              <ExternalLink size={11} />
            </a>
            <button onClick={() => deleteLink(link.id)} title="Remove link" style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = '#ef4444'; e.currentTarget.style.color = '#ef4444' }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
              <Trash2 size={11} />
            </button>
          </div>
        ))
      )}

      {adding && (
        <div style={{ background: 'var(--surface2)', border: '1px solid #2563eb', borderRadius: '8px', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: newLabel === 'Other' ? '1fr 1fr' : '1fr', gap: '8px' }}>
            <div>
              <label style={LS}>Document Type</label>
              <select value={newLabel} onChange={e => setNewLabel(e.target.value)} style={IS}>
                {DOC_LABELS.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>
            {newLabel === 'Other' && (
              <div>
                <label style={LS}>Custom Label</label>
                <input value={customLabel} onChange={e => setCustomLabel(e.target.value)} placeholder="e.g. Zoning Report" style={IS} />
              </div>
            )}
          </div>
          <div>
            <label style={LS}>OneDrive or SharePoint Share Link</label>
            <input value={newUrl} onChange={e => setNewUrl(e.target.value)} placeholder="https://marcusmillichap-my.sharepoint.com/..." style={IS} onKeyDown={e => e.key === 'Enter' && addLink()} autoFocus />
          </div>
          {error && <div style={{ fontSize: '11px', color: '#ef4444', padding: '6px 10px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '5px' }}>{error}</div>}
          <div style={{ display: 'flex', gap: '6px', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '10px', color: 'var(--muted)', lineHeight: 1.5 }}>
              In OneDrive: right-click file \u2192 Share \u2192 Copy link \u2192 paste above.
            </div>
            <div style={{ display: 'flex', gap: '6px' }}>
              <button onClick={() => { setAdding(false); setNewUrl(''); setCustomLabel(''); setError('') }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '6px 12px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '11px' }}>CANCEL</button>
              <button onClick={addLink} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '6px 16px', borderRadius: '5px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px' }}>ADD LINK</button>
            </div>
          </div>
        </div>
      )}

      {!adding && (
        <button onClick={() => setAdding(true)} style={{ display: 'flex', alignItems: 'center', gap: '5px', background: 'transparent', border: '1px dashed var(--border)', borderRadius: '6px', color: 'var(--muted)', padding: '8px 12px', cursor: 'pointer', fontSize: '11px', fontFamily: 'Syne, sans-serif', fontWeight: 600, width: '100%', justifyContent: 'center', letterSpacing: '0.04em' }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563eb'; e.currentTarget.style.color = '#2563eb' }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
          <Plus size={11} /> ADD DOCUMENT LINK
        </button>
      )}
    </div>
  )
}