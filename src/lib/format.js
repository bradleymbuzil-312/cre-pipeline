export function formatCurrency(val) {
  if (val === null || val === undefined || val === '') return '—'
  const n = parseFloat(val)
  if (isNaN(n)) return '—'
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`
  return `$${n.toLocaleString()}`
}

export function formatDate(d) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: '2-digit',
  })
}

export function formatPct(val) {
  if (val === null || val === undefined || val === '') return '—'
  return `${parseFloat(val).toFixed(1)}%`
}

export function formatDscr(val) {
  if (val === null || val === undefined || val === '') return '—'
  return `${parseFloat(val).toFixed(2)}x`
}
