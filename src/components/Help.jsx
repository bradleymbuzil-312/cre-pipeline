import { HelpCircle, Search, Plus, Edit, Trash2, Calendar as CalIcon } from 'lucide-react'

const SHORTCUTS = [
  { keys: ['Ctrl', 'K'], altKeys: ['⌘', 'K'], label: 'Open global search' },
  { keys: ['Esc'], label: 'Close any open modal' },
  { keys: ['Tab'], label: 'Move between form fields' },
]

const TIPS = [
  { icon: Plus, title: 'Creating deals fast', body: 'In the Active or Prospecting pipeline, click + NEW DEAL. Fill in borrower, property, loan amount, and stage. The rest can wait.' },
  { icon: Edit, title: 'Editing cards', body: 'Click any deal card or lender card to open the full editor. Your changes save when you click SAVE CHANGES.' },
  { icon: CalIcon, title: 'Maturity Watch + Calendar', body: 'Loans maturing in the next 12 months show up in Maturity Watch. The Calendar tab lets you see them alongside task deadlines by day.' },
  { icon: Search, title: 'Lender matching', body: 'In a deal\u2019s Capital Details section, click MATCH LENDERS to rank your lender database by fit. Click a match to auto-fill the lender name.' },
  { icon: Trash2, title: 'Deleting data', body: 'Deletes are permanent and immediate. Back up via the Supabase dashboard if you need history.' },
]

export default function Help() {
  return (
    <div style={{ padding: '24px', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ margin: 0, fontSize: '22px', color: 'var(--text)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '10px' }}>
          <HelpCircle size={18} color="var(--brand)" /> Help & Shortcuts
        </h2>
        <div style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '4px' }}>
          Quick reference for using the CRE Pipeline tool.
        </div>
      </div>

      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '20px', marginBottom: '16px' }}>
        <h3 style={{ margin: '0 0 14px', fontSize: '13px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 700 }}>
          Keyboard Shortcuts
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {SHORTCUTS.map((s, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 0', borderBottom: i < SHORTCUTS.length - 1 ? '1px solid var(--border)' : 'none' }}>
              <span style={{ fontSize: '13px', color: 'var(--text)' }}>{s.label}</span>
              <div style={{ display: 'flex', gap: '4px' }}>
                {s.keys.map((k, j) => (
                  <kbd key={j} style={{ fontFamily: 'IBM Plex Mono, monospace', fontSize: '11px', background: 'var(--surface2)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: '4px', padding: '2px 8px', minWidth: '28px', textAlign: 'center' }}>
                    {k}
                  </kbd>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '20px', marginBottom: '16px' }}>
        <h3 style={{ margin: '0 0 14px', fontSize: '13px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 700 }}>
          Tips & Workflows
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {TIPS.map((tip, i) => {
            const Icon = tip.icon
            return (
              <div key={i} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                <div style={{ flexShrink: 0, width: '32px', height: '32px', borderRadius: '6px', background: 'var(--surface2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--brand)' }}>
                  <Icon size={14} />
                </div>
                <div>
                  <div style={{ fontSize: '13px', color: 'var(--text)', fontWeight: 600, marginBottom: '2px' }}>{tip.title}</div>
                  <div style={{ fontSize: '12px', color: 'var(--muted)', lineHeight: 1.5 }}>{tip.body}</div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '10px', padding: '20px' }}>
        <h3 style={{ margin: '0 0 10px', fontSize: '13px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 700 }}>
          About
        </h3>
        <div style={{ fontSize: '12px', color: 'var(--muted)', lineHeight: 1.6 }}>
          Internal CRE deal pipeline tool for MMCC. Data lives in your team\u2019s Supabase project. Built on React and deployed via Vercel.
          <br /><br />
          Questions or bugs? Open an issue in the <a href="https://github.com/bradleymbuzil-312/cre-pipeline/issues" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--brand)' }}>GitHub repo</a>.
        </div>
      </div>
    </div>
  )
}