import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Clock } from 'lucide-react'

export default function ActivityLog({ dealId }) {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { if (dealId) fetchEvents() }, [dealId])

  async function fetchEvents() {
    const { data } = await supabase.from('deal_activity').select('*').eq('deal_id', dealId).order('created_at', { ascending: false }).limit(50)
    setEvents(data || [])
    setLoading(false)
  }

  if (loading) return <div style={{ fontSize: '11px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace' }}>LOADING HISTORY...</div>

  if (events.length === 0) return <div style={{ fontSize: '12px', color: 'var(--muted)', padding: '12px', background: 'var(--surface2)', borderRadius: '6px', textAlign: 'center' }}>No activity yet. Changes to this deal will appear here.</div>

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', maxHeight: '220px', overflowY: 'auto' }}>
      {events.map(e => (
        <div key={e.id} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', padding: '8px 10px', background: 'var(--surface2)', borderRadius: '6px', border: '1px solid var(--border)' }}>
          <Clock size={11} color="var(--muted)" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '12px', color: 'var(--text)', fontFamily: 'DM Sans, sans-serif', fontWeight: 500 }}>
              {e.description || e.action}
            </div>
            <div style={{ fontSize: '10px', color: 'var(--muted)', fontFamily: 'IBM Plex Mono, monospace', marginTop: '2px' }}>
              {e.user_email || 'unknown'} · {new Date(e.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

// Helper: log an activity event
export async function logActivity(dealId, userId, userEmail, action, description, oldValue, newValue) {
  if (!dealId) return
  await supabase.from('deal_activity').insert({
    deal_id: dealId,
    user_id: userId,
    user_email: userEmail,
    action,
    description,
    old_value: oldValue,
    new_value: newValue,
  })
}
