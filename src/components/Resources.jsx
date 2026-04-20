import { ExternalLink } from 'lucide-react'

const LINKS = [
  {
    name: 'MMCC Salesforce Lightning Experience',
    url: 'https://marcusmillichap.lightning.force.com/',
    icon: '\u2601\ufe0f',
    desc: 'CRM \u2014 deals, contacts, activity logs',
  },
  {
    name: 'My files \u2014 OneDrive',
    url: 'https://onedrive.live.com/',
    icon: '\ud83d\udcc1',
    desc: 'Cloud storage \u2014 deal docs, offering memos, rent rolls',
  },
  {
    name: 'CoStar',
    url: 'https://www.costar.com/',
    icon: '\ud83c\udfe2',
    desc: 'Commercial real estate information, comps, market data',
  },
  {
    name: 'Reonomy',
    url: 'https://www.reonomy.com/',
    icon: '\ud83d\udd0e',
    desc: 'Property intelligence \u2014 ownership, debt, tenants',
  },
  {
    name: 'Capitalize',
    url: 'https://www.capitalize.com/',
    icon: '\ud83d\udcc8',
    desc: 'Lender database \u2014 turn data into deals',
  },
  {
    name: 'CRE Pipeline GitHub',
    url: 'https://github.com/bradleymbuzil-312/cre-pipeline',
    icon: '\ud83d\udcbb',
    desc: 'Source code for this app \u2014 report bugs, request features',
  },
]

export default function Resources() {
  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ margin: 0, fontSize: '22px', color: 'var(--text)', fontWeight: 700 }}>Resources</h2>
        <div style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '4px' }}>Quick links to external tools and databases you use day to day.</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '14px' }}>
        {LINKS.map(l => (
          <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer" style={{
            display: 'block',
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: '10px',
            padding: '16px',
            textDecoration: 'none',
            color: 'var(--text)',
            transition: 'border-color 0.15s, transform 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--brand)'; e.currentTarget.style.transform = 'translateY(-1px)' }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.transform = 'translateY(0)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
              <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text)' }}>
                <span style={{ marginRight: '6px' }}>{l.icon}</span>{l.name}
              </div>
              <ExternalLink size={13} style={{ color: 'var(--dim)', flexShrink: 0, marginTop: '2px' }} />
            </div>
            <div style={{ fontSize: '12px', color: 'var(--muted)', lineHeight: 1.5 }}>{l.desc}</div>
          </a>
        ))}
      </div>
    </div>
  )
}