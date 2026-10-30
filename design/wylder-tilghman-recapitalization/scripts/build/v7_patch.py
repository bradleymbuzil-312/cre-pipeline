# -*- coding: utf-8 -*-
"""Per-package edits to the shared core, so no shared page carries another tranche's economics."""
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


def extended_cash_flow(b, t):
    """The senior package states the rate; the others see the dollar debt service only."""
    if t == 'senior':
        return b
    reps = [('Debt service is the $10,000,000 senior loan held flat and interest-only at 12.00%.',
             'Debt service is the senior loan held flat and interest-only.'),
            ('Debt service is the ten million dollar senior loan held flat and interest-only at twelve '
             'percent, one million two hundred thousand dollars a year.',
             'Debt service is the senior loan held flat and interest-only at one million two hundred '
             'thousand dollars a year.')]
    for old, new in reps:
        assert b.count(old) == 1, ('extended_cash_flow', t, old[:70], b.count(old))
        b = b.replace(old, new)
    return b


PATCH = {'VALUE POSITIONING': value_positioning, 'EXTENDED CASH FLOW': extended_cash_flow}
