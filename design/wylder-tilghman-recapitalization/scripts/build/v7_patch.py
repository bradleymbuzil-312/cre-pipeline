# -*- coding: utf-8 -*-
"""Per-package edits to the shared core, so no shared page carries another tranche's economics."""
import re
from figs_v7 import *

ATTACH = {
 'senior': ('Senior loan &middot; last dollar', SENIOR, 'Senior Loan vs As-Is Estimate',
            'the senior loan attaches at', 'one hundred seventy-two thousand four hundred fourteen'),
 'pref':   ('Debt and preferred &middot; last dollar', SENIOR + PREF,
            'Debt + Preferred vs As-Is Estimate', 'the preferred last dollar attaches at',
            'two hundred thirty-nine thousand seven hundred twenty-five'),
 'common': ('Total capitalization', TOTAL, 'Capitalization vs As-Is Estimate',
            'the capitalization attaches at',
            'three hundred thousand and seventy')}
ATTACH['hm'] = ATTACH['senior']


def value_positioning(b, t):
    lab, amt, stat_lab, prose, spoken = ATTACH[t]
    reps = [
      # the attachment row
      ('<span style="font-family:var(--font-body);font-size:17px;color:var(--ink-900);">LP equity</span>'
       '<span style="font-family:var(--font-mono);font-size:17px;text-align:right;color:var(--ink-900);">'
       '$13.26M</span><span style="font-family:var(--font-mono);font-size:17px;text-align:right;'
       'color:var(--ink-900);">$228,536</span>',
       f'<span style="font-family:var(--font-body);font-size:17px;color:var(--ink-900);">{lab}</span>'
       '<span style="font-family:var(--font-mono);font-size:17px;text-align:right;color:var(--ink-900);">'
       f'${amt/1e6:,.2f}M</span><span style="font-family:var(--font-mono);font-size:17px;'
       f'text-align:right;color:var(--ink-900);">${amt/KEYS:,.0f}</span>'),
      # net capital in the asset -> total cost basis, restated on the current model
      ('>Net capital in the asset</span>'
       '<span style="font-family:var(--font-mono);font-size:17px;text-align:right;color:var(--ink-900);">'
       '$18.18M</span><span style="font-family:var(--font-mono);font-size:17px;text-align:right;'
       'color:var(--ink-900);">$313,529</span>',
       '>Total cost basis</span>'
       '<span style="font-family:var(--font-mono);font-size:17px;text-align:right;color:var(--ink-900);">'
       f'${COST_BASIS/1e6:,.2f}M</span><span style="font-family:var(--font-mono);font-size:17px;'
       f'text-align:right;color:var(--ink-900);">${COST_BASIS_KEY:,.0f}</span>'),
      # the prose
      ('Net capital in the asset of <strong style="color:var(--mm-navy-900);">$313,529 per key remains '
       'below the as-is estimate</strong>, and the LP equity attaches at $228,536 per key.',
       f'The total cost basis of <strong style="color:var(--mm-navy-900);">${COST_BASIS_KEY:,.0f} per key '
       f'remains below the as-is estimate</strong>, and {prose} ${amt/KEYS:,.0f} per key.'),
      # the stat tile
      ('>LP Equity vs As-Is Estimate</div><div style="font-family:var(--font-display);font-weight:700;'
       'font-size:34px;color:var(--mm-orange-700);line-height:1.1;">61.9%</div>',
       f'>{stat_lab}</div><div style="font-family:var(--font-display);font-weight:700;'
       'font-size:34px;color:var(--mm-orange-700);line-height:1.1;">'
       f'{amt/VAL["is"]:.1%}</div>'),
      # the speaker notes
      ('Net capital in the asset is three hundred thirteen thousand five hundred twenty-nine dollars per '
       'key, below the as-is estimate, and the LP equity attaches at two hundred twenty-eight thousand '
       'five hundred thirty-six per key.',
       'Total cost basis is three hundred thirty-one thousand eight hundred sixty dollars per key, below '
       f'the as-is estimate, and {prose} {spoken} per key.')]
    for old, new in reps:
        assert b.count(old) == 1, ('value_positioning', t, old[:70], b.count(old))
        b = b.replace(old, new)
    return b


CELL = re.compile(r'(<div style="padding:7px 3px;[^"]*">)([^<]*)(</div>)')


def _cells(b, label, n=12):
    """The n value cells that follow a row's label cell, left to right."""
    i = b.index(f'>{label}</div>') + len(label) + 7
    out, pos = [], i
    for _ in range(n):
        m = CELL.search(b, pos)
        assert m, (label, len(out))
        out.append(m)
        pos = m.end()
    return out


def _read(b, label):
    return [m.group(2).replace(',', '').replace('(', '-').replace(')', '').replace('$', '')
            for m in _cells(b, label)]


def _write(b, label, vals):
    for m, v in reversed(list(zip(_cells(b, label), vals))):
        b = b[:m.start()] + m.group(1) + v + m.group(3) + b[m.end():]
    return b


def _stat(b, note, val):
    pat = re.compile(r'(>)([^<>]{1,12})(</div>\s*<div[^>]*>' + re.escape(note) + ')')
    m = pat.search(b)
    assert m, note
    return b[:m.start()] + m.group(1) + val + m.group(3) + b[m.end():]


def extended_cash_flow(b, t):
    """Re-derive the senior debt service block from the request actually being made.

    The page is lifted from an earlier deck, where the debt service row, the two coverage rows
    and the debt yield row were fixed to a different loan. All four are recomputed here from
    SR_ADS and SENIOR, along with the four summary measures beneath the table. The senior
    package states the rate; the others see the dollar debt service only.
    """
    noi = [float(v) for v in _read(b, 'Net operating income')]           # thousands
    ncf = [float(v) for v in _read(b, 'Net cash flow at a 4.0% reserve')]
    ds = SR_ADS / 1000.0
    b = _write(b, 'Debt service', [f'({ds:,.0f})'] * len(noi))
    b = _write(b, 'Coverage on net operating income', [f'{n / ds:.2f}x' for n in noi])
    b = _write(b, 'Coverage at a 4.0% reserve', [f'{c / ds:.2f}x' for c in ncf])
    b = _write(b, 'Debt yield', [f'{n / (SENIOR / 1000.0):.1%}' for n in noi])
    b = _stat(b, 'Minimum coverage over the period, in 2030', f'{noi[0] / ds:.2f}x')
    b = _stat(b, 'Minimum coverage with the reserve stepped to 4.0%', f'{ncf[0] / ds:.2f}x')
    b = _stat(b, 'Aggregate cash flow after debt service, 2031 to 2041',
              f'${(sum(noi[1:]) - ds * (len(noi) - 1)) / 1000:,.1f}M')
    reps = [(f'Debt service is the $10,000,000 senior loan held flat and interest-only at 12.00%.',
             f'Debt service is the ${SENIOR:,} senior loan held flat and interest-only at '
             f'{ALLIN:.2%}.' if t in ('senior', 'hm')
             else 'Debt service is the senior loan held flat and interest-only.'),
            ('Debt service is the ten million dollar senior loan held flat and interest-only at twelve '
             'percent, one million two hundred thousand dollars a year.',
             'Debt service is the senior loan held flat and interest-only at '
             f'${SR_ADS:,} a year.')]
    for old, new in reps:
        assert b.count(old) == 1, ('extended_cash_flow', t, old[:60], b.count(old))
        b = b.replace(old, new)
    return b


def adjacent_acquisition(b, t):
    """Lender decks describe the owning entity, not the partnership."""
    if t not in ('senior', 'hm'):
        return b
    reps = [('so the parcel comes into the partnership rather than a separate venture',
             'so the parcel comes into the borrowing entity rather than a separate venture'),
            ('so the parcel comes into the partnership rather than a separate venture',
             'so the parcel comes into the borrowing entity rather than a separate venture')]
    for old, new in reps[:1]:
        assert b.count(old) >= 1, ('adjacent_acquisition', t, b.count(old))
        b = b.replace(old, new)
    return b


PATCH = {'VALUE POSITIONING': value_positioning, 'EXTENDED CASH FLOW': extended_cash_flow,
         'ADJACENT ACQUISITION': adjacent_acquisition}
