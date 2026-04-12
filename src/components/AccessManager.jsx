import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { UserPlus, Shield, ShieldOff, Trash2, Copy, Check, Users, Loader } from 'lucide-react'

export default function AccessManager({ session }) {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [bootstrapping, setBootstrapping] = useState(false)
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ email: '', display_name: '', role: 'member', password: '' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [copied, setCopied] = useState(null)
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => { fetchUsers() }, [])

  async function fetchUsers() {
    setLoading(true)
    const { data } = await supabase.from('user_access').select('*').order('created_at')
    const list = data || []

    // Auto-register current user as admin if table is empty
    if (list.length === 0) {
      setBootstrapping(true)
      const { error: insertErr } = await supabase.from('user_access').insert({
        user_id: session.user.id,
        email: session.user.email,
        display_name: session.user.user_metadata?.display_name || session.user.email.split('@')[0],
        role: 'admin',
        is_active: true,
        invited_by: session.user.id
      })
      setBootstrapping(false)
      if (!insertErr) {
        // Re-fetch after auto-registration
        const { data: refreshed } = await supabase.from('user_access').select('*').order('created_at')
        setUsers(refreshed || [])
        setIsAdmin(true)
        setLoading(false)
        return
      }
    }

    const me = list.find(u => u.user_id === session.user.id)
    setIsAdmin(!list.length || me?.role === 'admin')
    setUsers(list)
    setLoading(false)
  }

  async function handleAdd() {
    if (!form.email.trim() || !form.display_name.trim() || !form.password.trim()) {
      setError('Email, name, and password are all required.'); return
    }
    setAdding(true); setError(''); setSuccess('')
    const { data: signUpData, error: signUpErr } = await supabase.auth.signUp({
      email: form.email.trim(),
      password: form.password.trim(),
      options: { data: { display_name: form.display_name.trim() } }
    })
    if (signUpErr) { setError(signUpErr.message); setAdding(false); return }
    const { error: accessErr } = await supabase.from('user_access').insert({
      user_id: signUpData.user?.id || null,
      email: form.email.trim(),
      display_name: form.display_name.trim(),
      role: form.role,
      is_active: true,
      invited_by: session.user.id
    })
    if (accessErr) { setError(accessErr.message); setAdding(false); return }
    setSuccess(`Account created for ${form.display_name}. Share their login: ${form.email} / ${form.password}`)
    setForm({ email: '', display_name: '', role: 'member', password: '' })
    setAdding(false)
    fetchUsers()
  }

  async function toggleActive(user) {
    await supabase.from('user_access').update({ is_active: !user.is_active }).eq('id', user.id)
    fetchUsers()
  }

  async function changeRole(user, role) {
    await supabase.from('user_access').update({ role }).eq('id', user.id)
    fetchUsers()
  }

  async function removeUser(user) {
    if (!window.confirm(`Remove ${user.display_name || user.email}'s access? They will be immediately locked out.`)) return
    await supabase.from('user_access').delete().eq('id', user.id)
    fetchUsers()
  }

  function generatePassword() {
    const chars = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#'
    setForm(f => ({ ...f, password: Array.from({length: 12}, () => chars[Math.floor(Math.random() * chars.length)]).join('') }))
  }

  const IS = { width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--text)', borderRadius: '6px', padding: '8px 12px', fontSize: '13px', fontFamily: 'DM Sans, sans-serif', boxSizing: 'border-box' }
  const LS = { display: 'block', marginBottom: '6px', fontSize: '10px', fontWeight: 700, color: 'var(--muted)', fontFamily: 'Syne, sans-serif', textTransform: 'uppercase', letterSpacing: '0.09em' }

  if (loading || bootstrapping) {
    return (
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '12px' }}>
        <Loader size={20} color="var(--gold)" style={{ animation: 'spin 1s linear infinite' }} />
        <div style={{ fontSize: '12px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', letterSpacing: '0.1em' }}>
          {bootstrapping ? 'SETTING UP YOUR ADMIN ACCESS...' : 'LOADING...'}
        </div>
        <style>{`@keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }`}</style>
      </div>
    )
  }

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '24px' }}>
      <div style={{ maxWidth: '720px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>

        <div>
          <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '20px', color: 'var(--text)', marginBottom: '4px' }}>Team Access</div>
          <div style={{ fontSize: '13px', color: 'var(--muted)' }}>Manage who can log in and what they can do. All team members share the same pipeline data.</div>
        </div>

        {/* Current users */}
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden' }}>
          <div style={{ padding: '14px 18px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Users size={14} color="var(--muted)" />
            <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Current Access ({users.length})</span>
          </div>
          {users.map((u, i) => (
            <div key={u.id} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '12px 18px', borderBottom: i < users.length - 1 ? '1px solid var(--border)' : 'none' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: u.role === 'admin' ? 'var(--gold)' : 'var(--surface2)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', color: u.role === 'admin' ? '#000' : 'var(--muted)', flexShrink: 0 }}>
                {(u.display_name || u.email).charAt(0).toUpperCase()}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '13px', color: u.is_active ? 'var(--text)' : 'var(--muted)', textDecoration: u.is_active ? 'none' : 'line-through' }}>
                  {u.display_name || u.email}
                  {u.user_id === session.user.id && <span style={{ marginLeft: '6px', fontSize: '9px', background: 'var(--gold)', color: '#000', borderRadius: '3px', padding: '1px 5px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }}>YOU</span>}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>{u.email}</div>
              </div>
              <span style={{ fontSize: '9px', padding: '2px 8px', borderRadius: '3px', background: u.role === 'admin' ? 'rgba(212,168,67,0.15)' : 'var(--surface2)', border: `1px solid ${u.role === 'admin' ? 'var(--gold-dim)' : 'var(--border)'}`, color: u.role === 'admin' ? 'var(--gold)' : 'var(--muted)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', flexShrink: 0 }}>{u.role}</span>
              <span style={{ fontSize: '9px', padding: '2px 8px', borderRadius: '3px', background: u.is_active ? 'rgba(58,212,96,0.1)' : 'rgba(248,81,73,0.1)', border: `1px solid ${u.is_active ? 'rgba(58,212,96,0.3)' : 'rgba(248,81,73,0.3)'}`, color: u.is_active ? '#3ad460' : 'var(--danger)', fontFamily: 'Syne, sans-serif', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', flexShrink: 0 }}>{u.is_active ? 'Active' : 'Suspended'}</span>
              {isAdmin && u.user_id !== session.user.id && (
                <div style={{ display: 'flex', gap: '4px', flexShrink: 0 }}>
                  <button onClick={() => changeRole(u, u.role === 'admin' ? 'member' : 'admin')} title={u.role === 'admin' ? 'Demote to Member' : 'Promote to Admin'} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: 'var(--muted)', display: 'flex', alignItems: 'center' }} onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--gold-dim)'; e.currentTarget.style.color = 'var(--gold)' }} onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--muted)' }}>
                    {u.role === 'admin' ? <ShieldOff size={12} /> : <Shield size={12} />}
                  </button>
                  <button onClick={() => toggleActive(u)} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 8px', cursor: 'pointer', color: u.is_active ? 'var(--danger)' : '#3ad460', fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700 }} onMouseEnter={e => e.currentTarget.style.background = 'var(--surface2)'} onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                    {u.is_active ? 'SUSPEND' : 'RESTORE'}
                  </button>
                  <button onClick={() => removeUser(u)} style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: '4px', padding: '4px 6px', cursor: 'pointer', color: 'var(--danger)', display: 'flex', alignItems: 'center' }} onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--danger)'; e.currentTarget.style.background = 'rgba(248,81,73,0.08)' }} onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'transparent' }}>
                    <Trash2 size={12} />
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Add new user */}
        {isAdmin && (
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', overflow: 'hidden' }}>
            <div style={{ padding: '14px 18px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <UserPlus size={14} color="var(--muted)" />
              <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', color: 'var(--text)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Add Team Member</span>
            </div>
            <div style={{ padding: '18px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
                <div><label style={LS}>Full Name *</label><input value={form.display_name} onChange={e => setForm(f => ({...f, display_name: e.target.value}))} placeholder="John Smith" style={IS} /></div>
                <div><label style={LS}>Role</label><select value={form.role} onChange={e => setForm(f => ({...f, role: e.target.value}))} style={IS}><option value="member">Member</option><option value="admin">Admin</option></select></div>
                <div><label style={LS}>Email *</label><input type="email" value={form.email} onChange={e => setForm(f => ({...f, email: e.target.value}))} placeholder="john@company.com" style={IS} /></div>
                <div><label style={LS}>Temporary Password *</label>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <input value={form.password} onChange={e => setForm(f => ({...f, password: e.target.value}))} placeholder="Set a password" style={{ ...IS, flex: 1 }} />
                    <button onClick={generatePassword} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--muted)', borderRadius: '6px', padding: '0 10px', cursor: 'pointer', fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 600, whiteSpace: 'nowrap', flexShrink: 0 }}>AUTO</button>
                  </div>
                </div>
              </div>
              {error && <div style={{ padding: '10px 14px', borderRadius: '6px', background: 'rgba(248,81,73,0.08)', border: '1px solid rgba(248,81,73,0.25)', color: 'var(--danger)', fontSize: '13px' }}>{error}</div>}
              {success && (
                <div style={{ padding: '12px 14px', borderRadius: '6px', background: 'rgba(58,212,96,0.08)', border: '1px solid rgba(58,212,96,0.25)', color: '#3ad460', fontSize: '12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
                  <span>{success}</span>
                  <button onClick={() => { navigator.clipboard.writeText(success); setCopied('success') }} style={{ background: 'transparent', border: '1px solid rgba(58,212,96,0.4)', borderRadius: '4px', padding: '4px 8px', cursor: 'pointer', color: '#3ad460', fontSize: '10px', fontFamily: 'Syne, sans-serif', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', flexShrink: 0 }}>
                    {copied === 'success' ? <><Check size={10} /> COPIED</> : <><Copy size={10} /> COPY</>}
                  </button>
                </div>
              )}
              <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <button onClick={handleAdd} disabled={adding} style={{ background: adding ? 'var(--gold-dim)' : 'var(--gold)', border: 'none', color: '#000', padding: '9px 24px', borderRadius: '6px', cursor: adding ? 'not-allowed' : 'pointer', fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '12px', letterSpacing: '0.04em' }}>
                  {adding ? 'CREATING...' : 'CREATE ACCESS'}
                </button>
              </div>
            </div>
          </div>
        )}

        <div style={{ padding: '14px 18px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '12px', color: 'var(--muted)', lineHeight: 1.6 }}>
          <strong style={{ color: 'var(--text)', fontFamily: 'Syne, sans-serif' }}>How it works:</strong> Each team member logs in at cre-pipeline.vercel.app with their own email and password. All members share the same pipeline. Suspending a member locks them out immediately without deleting their account.
        </div>
      </div>
    </div>
  )
}
