import { useState, useRef } from 'react'
import { supabase } from '../lib/supabase'
import { X, Upload, CheckCircle, AlertCircle, FileText } from 'lucide-react'

function parseOutlookCSV(text) {
  const lines = text.split(/\r?\n/).filter(l => l.trim())
  if (lines.length < 2) return []
  function parseRow(line) {
    const cols = [], c = { cur: '', inQ: false }
    for (let i = 0; i < line.length; i++) {
      const ch = line[i]
      if (ch === '"') c.inQ = !c.inQ
      else if (ch === ',' && !c.inQ) { cols.push(c.cur.trim()); c.cur = '' }
      else c.cur += ch
    }
    cols.push(c.cur.trim())
    return cols
  }
  const headers = parseRow(lines[0]).map(h => h.replace(/^"|"$/g, '').toLowerCase().trim())
  return lines.slice(1).map(line => {
    const cols = parseRow(line)
    const row = {}
    headers.forEach((h, i) => { row[h] = (cols[i] || '').replace(/^"|"$/g, '').trim() })
    return {
      firstName: row['first name'] || row['given name'] || row['firstname'] || '',
      lastName: row['last name'] || row['surname'] || row['family name'] || row['lastname'] || '',
      company: row['company'] || row['organization'] || row['company name'] || '',
      email: row['e-mail address'] || row['email address'] || row['email'] || row['e-mail'] || '',
      phone: row['business phone'] || row['mobile phone'] || row['primary phone'] || row['phone'] || '',
      notes: row['notes'] || row['body'] || ''
    }
  }).filter(c => c.firstName || c.lastName || c.email || c.company)
}

export default function ImportModal({ session, onClose, onImported }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState([])
  const [importing, setImporting] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState('')
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef()

  function handleFile(f) {
    if (!f) return
    if (!f.name.endsWith('.csv')) { setError('Please upload a .csv file exported from Outlook.'); return }
    setError(''); setFile(f)
    const reader = new FileReader()
    reader.onload = e => {
      const contacts = parseOutlookCSV(e.target.result)
      setPreview(contacts)
      if (!contacts.length) setError('No contacts found. Make sure this is an Outlook CSV export.')
    }
    reader.readAsText(f)
  }

  function handleDrop(e) {
    e.preventDefault(); setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  async function handleImport() {
    if (!preview.length) return
    setImporting(true)
    let imported = 0, skipped = 0, errors = 0
    for (const c of preview) {
      const { error } = await supabase.from('clients').insert({
        first_name: c.firstName || 'Unknown',
        last_name: c.lastName || null,
        company: c.company || null,
        email: c.email || null,
        phone: c.phone || null,
        notes: c.notes || null,
        client_type: 'Borrower',
        created_by: session.user.id
      })
      if (error) { if (error.code === '23505') skipped++; else errors++ }
      else imported++
    }
    setResults({ imported, skipped, errors })
    setImporting(false)
    if (imported > 0) onImported()
  }

  const IS = { background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '8px 12px', fontSize: '12px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box', width: '100%' }

  return (
    <div onClick={e => { if (e.target === e.currentTarget) onClose() }} style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '12px', width: '100%', maxWidth: '580px', maxHeight: '88vh', display: 'flex', flexDirection: 'column', boxShadow: '0 24px 60px rgba(0,0,0,0.15)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '18px 24px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <div>
            <h2 style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '16px', color: 'var(--text)', marginBottom: '2px' }}>Import from Outlook</h2>
            <p style={{ fontSize: '12px', color: 'var(--muted)' }}>Upload a .csv file exported from Outlook Contacts</p>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', cursor: 'pointer', padding: '5px', borderRadius: '6px', display: 'flex', alignItems: 'center' }}><X size={15} /></button>
        </div>
        <div style={{ overflowY: 'auto', flex: 1, padding: '22px 24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {!file && (
            <div style={{ padding: '12px 14px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '8px', fontSize: '12px', color: 'var(--muted)', lineHeight: 1.7 }}>
              <strong style={{ color: 'var(--text)', fontFamily: 'Syne, sans-serif', display: 'block', marginBottom: '4px' }}>How to export from Outlook:</strong>
              1. File &rarr; Open &amp; Export &rarr; Import/Export<br/>
              2. Export to a file &rarr; Comma Separated Values<br/>
              3. Select Contacts folder &rarr; Save the .csv<br/>
              4. Upload it below
            </div>
          )}
          {!results && (
            <div onClick={() => fileRef.current && fileRef.current.click()}
              onDragOver={e => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              style={{ border: ('2px dashed ' + (dragOver ? '#2563eb' : 'var(--border)')), borderRadius: '10px', padding: '32px', textAlign: 'center', cursor: 'pointer', transition: 'all 0.15s', background: dragOver ? '#eff6ff' : 'var(--surface2)' }}>
              <input ref={fileRef} type='file' accept='.csv' onChange={e => handleFile(e.target.files[0])} style={{ display: 'none' }} />
              {file ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                  <FileText size={20} color='#2563eb' />
                  <div style={{ textAlign: 'left' }}>
                    <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: 'var(--text)' }}>{file.name}</div>
                    <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{preview.length} contacts found</div>
                  </div>
                </div>
              ) : (
                <>
                  <Upload size={24} color='var(--muted)' style={{ marginBottom: '10px' }} />
                  <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: 'var(--text)', marginBottom: '4px' }}>Drop your Outlook CSV here</div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)' }}>or click to browse</div>
                </>
              )}
            </div>
          )}
          {error && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 14px', borderRadius: '6px', background: '#fef2f2', border: '1px solid #fecaca', color: '#ef4444', fontSize: '12px' }}>
              <AlertCircle size={14} /> {error}
            </div>
          )}
          {preview.length > 0 && !results && (
            <div>
              <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '11px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>
                Preview &mdash; {preview.length} contacts
              </div>
              <div style={{ border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden', maxHeight: '240px', overflowY: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                  <thead>
                    <tr style={{ background: 'var(--surface2)' }}>
                      {['Name', 'Company', 'Email', 'Phone'].map(col => (
                        <th key={col} style={{ padding: '8px 12px', textAlign: 'left', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '10px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', borderBottom: '1px solid var(--border)' }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {preview.slice(0, 50).map((c, i) => (
                      <tr key={i} style={{ borderBottom: i < preview.length - 1 ? '1px solid var(--border)' : 'none', background: i % 2 === 0 ? 'transparent' : 'var(--surface2)' }}>
                        <td style={{ padding: '7px 12px', color: 'var(--text)', fontWeight: 500 }}>{[c.firstName, c.lastName].filter(Boolean).join(' ') || '\u2014'}</td>
                        <td style={{ padding: '7px 12px', color: 'var(--muted)' }}>{c.company || '\u2014'}</td>
                        <td style={{ padding: '7px 12px', color: 'var(--muted)' }}>{c.email || '\u2014'}</td>
                        <td style={{ padding: '7px 12px', color: 'var(--muted)' }}>{c.phone || '\u2014'}</td>
                      </tr>
                    ))}
                    {preview.length > 50 && (
                      <tr><td colSpan={4} style={{ padding: '8px 12px', color: 'var(--muted)', fontSize: '11px', textAlign: 'center' }}>+ {preview.length - 50} more</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {results && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'center', padding: '24px' }}>
              <CheckCircle size={40} color='#16a34a' />
              <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '18px', color: 'var(--text)' }}>Import Complete</div>
              <div style={{ display: 'flex', gap: '24px', marginTop: '8px' }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'IBM Plex Mono, monospace', color: '#16a34a' }}>{results.imported}</div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Imported</div>
                </div>
                {results.skipped > 0 && (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'IBM Plex Mono, monospace', color: 'var(--muted)' }}>{results.skipped}</div>
                    <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Skipped</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        <div style={{ padding: '14px 24px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexShrink: 0 }}>
          {!results ? (
            <>
              <button onClick={() => { setFile(null); setPreview([]); setError('') }} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--muted)', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 600, fontSize: '12px' }}>
                {file ? 'CLEAR' : 'CANCEL'}
              </button>
              <button onClick={preview.length ? handleImport : () => fileRef.current && fileRef.current.click()} disabled={importing}
                style={{ background: importing ? '#93c5fd' : '#2563eb', border: 'none', color: '#fff', padding: '8px 24px', borderRadius: '6px', cursor: importing ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>
                {importing ? 'IMPORTING...' : preview.length ? ('IMPORT ' + preview.length + ' CONTACTS') : 'CHOOSE FILE'}
              </button>
            </>
          ) : (
            <button onClick={onClose} style={{ background: '#2563eb', border: 'none', color: '#fff', padding: '8px 24px', borderRadius: '6px', cursor: 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em', marginLeft: 'auto' }}>
              DONE
            </button>
          )}
        </div>
      </div>
    </div>
  )
}