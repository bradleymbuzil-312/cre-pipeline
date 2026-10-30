# -*- coding: utf-8 -*-
"""Assemble the three packages and audit each for cross-tranche economic leakage."""
import io, re, sys
from v7_lib import load_sections, write_deck, SHARED, DECKDIR
from v7_common import capital_structure, sources_and_uses
from v7_pages import total_basis
from v7_patch import PATCH
from v7_num import renumber
import v7_tranche as T
from figs_v7 import *
from figs_v7 import SENIOR as SENIOR_AMT, PREF as PREF_AMT, COMMON as COMMON_AMT

CORE = SHARED[:15]                         # THE ASSET .. MARKET AND DEMAND
CLOSE = ['TOTAL BASIS', 'VALUE POSITIONING', 'SALE COMPARABLES', 'RECENT TRANSACTIONS', 'CONTACT']

PKG = {
 'senior': dict(file='Wylder Tilghman Island - Senior Debt.dc.html', label='Senior Debt',
   pages=[('SENIOR LOAN TERMS', T.senior_terms), ('DEBT SERVICE COVERAGE', T.senior_coverage),
          ('SENIOR RETURNS', lambda: T.returns_page('senior')),
          ('CREDIT CONSIDERATIONS', T.senior_credit)],
   dark={'SENIOR LOAN TERMS', 'CREDIT CONSIDERATIONS'}),
 'hm': dict(file='Wylder Tilghman Island - Senior Debt (Hard Money).dc.html', label='Senior Debt',
   pages=[('SENIOR LOAN TERMS', T.hm_terms), ('DEBT SERVICE COVERAGE', T.senior_coverage),
          ('CREDIT CONSIDERATIONS', T.hm_credit)],
   dark={'SENIOR LOAN TERMS', 'CREDIT CONSIDERATIONS'}),
 'pref': dict(file='Wylder Tilghman Island - Preferred Equity.dc.html', label='Preferred Equity',
   pages=[('PREFERRED EQUITY TERMS', T.pref_terms), ('CASH SWEEP AND BALANCE', T.pref_sweep),
          ('PREFERRED RETURNS', lambda: T.returns_page('pref')),
          ('POSITION AND PROTECTIONS', T.pref_position)],
   dark={'PREFERRED EQUITY TERMS', 'POSITION AND PROTECTIONS'}),
 'common': dict(file='Wylder Tilghman Island - Common Equity.dc.html', label='Common Equity',
   pages=[('PARTNERSHIP TERMS', T.common_terms), ('DISTRIBUTION WATERFALL', T.common_waterfall),
          ('LP RETURNS', lambda: T.returns_page('common')),
          ('SPONSOR ALIGNMENT', T.common_alignment)],
   dark={'PARTNERSHIP TERMS', 'SPONSOR ALIGNMENT'})}

# ─────────────────────────────────────────── what each package may never contain
# Phrases are exact and high-signal; amounts are figures unique to one tranche's economics.
# Capital AMOUNTS, position in the stack and leverage ratios are deliberately shown to all three.
SENIOR = dict(
  phrases=['12.00%', 'SOFR', '8.21%', '3.79%', 'Broker fee', f'{SR_KICKER:.2%} of equity value',
           'Senior origination fee', 'Senior loan &mdash; total cash received',
           'Senior loan &mdash; profit', 'All-In Rate', 'all-in rate', 'Annual debt service'],
  amounts=[SR_NET, SR_BASIS, SR_INT_3Y] + SR_KICK + SR_CASH + SR_PROFIT)
PREF = dict(
  phrases=[f'{PF_RATE_PIK:.2%}', f'{PF_KICKER:.2%} of equity value', 'Preferred origination fee',
           'placement fee', 'Accrual rate', 'Accrual Rate', 'accruing at',
           'Preferred equity &mdash; total cash received', 'Preferred equity &mdash; profit',
           'Cash swept', 'cash sweep', 'Cash sweep'],
  amounts=[PF_ORIG, PF_NET, PF_DUE_AT_EXIT, PF_SWEEP_3Y] + PF_KICK + PF_CASH + PF_PROFIT)
COMMON = dict(
  phrases=[f'{CE_PREF:.2%} cumulative', '50 / 50', 'residual split', 'Residual Split', 'promote',
           'ownership interest', 'LP &mdash; total cash received', 'LP &mdash; profit',
           'Preferred return', 'preferred return'],
  amounts=[LP_PREF, GP_PREF, WF_PREF, WF_RESID, WF_SPLIT] + CE_RESID + LP_CASH + GP_CASH_OUT
          + LP_PROFIT + GP_PROFIT)
OTHERS = {'senior': [PREF, COMMON], 'hm': [PREF, COMMON],
          'pref': [SENIOR, COMMON], 'common': [SENIOR, PREF]}
# the hard money package quotes no participation and projects no lender return
NO_RETURN = ['Exit participation', 'exit participation', 'equity kicker',
             'participation in equity', f'{SR_KICKER:.2%}', 'IRR', 'irr',
             'Equity multiple', 'equity multiple', 'Projected Return', 'projected return',
             'total cash received', 'Base-Case', 'Net Funded Basis', 'not for distribution',
             f'${SR_BASIS:,.0f}', f'${SR_INT_3Y:,.0f}'] \
            + [f'${v:,.0f}' for v in SR_KICK + SR_CASH + SR_PROFIT] \
            + [f'{v:.2f}x' for v in SR_MULT] + [f'{v:.1%}' for v in SR_IRR]
# amounts every package is entitled to see: the tranche sizes, the stack, the basis, the aggregate
ALLOWED = {SENIOR_AMT, PREF_AMT, COMMON_AMT, GP_CASH, TOTAL, PARTNERSHIP, SR_PF_DEDUCT, COST_BASIS}
LOSS = [f'${EXITS[0]:,.0f}', f'${EXITS[0]/1e6:,.0f}M', f'${PARTNERSHIP_BREAKEVEN:,.0f}',
        f'${abs(LP_PROFIT[0]):,.0f}', f'${abs(GP_PROFIT[0]):,.0f}',
        f'{LP_MULT[0]:.2f}x', f'{GP_MULT[0]:.2f}x', f'{LP_IRR[0]:.1%}', f'{GP_IRR[0]:.1%}']

def build(t):
    head, body = load_sections()
    for name, fn in PATCH.items():
        body[name] = fn(body[name], t)
    body['TITLE'] = T.title(t)
    body['THE OPPORTUNITY'] = T.opportunity(t)
    body['CAPITAL STRUCTURE'] = capital_structure(t)
    body['SOURCES AND USES'] = sources_and_uses(t)
    body['TOTAL BASIS'] = total_basis(t)
    body['CONTACT'] = T.contact(t)
    p = PKG[t]
    for name, fn in p['pages']:
        body[name] = fn()
    order = (['TITLE', 'THE OPPORTUNITY'] + CORE + ['CAPITAL STRUCTURE', 'SOURCES AND USES']
             + [n for n, _ in p['pages']] + CLOSE)
    path = f'{DECKDIR}/{p["file"]}'
    n = write_deck(path, head, order, body, p['label'])
    renumber(path, p['label'], dark=p['dark'])
    return path, n, order


def audit(path, t):
    s = io.open(path, encoding='utf-8').read()
    leaks = []
    for other in OTHERS[t]:
        leaks += [p for p in other['phrases'] if p in s]
        leaks += [f'${a:,.0f}' for a in other['amounts']
                  if a not in ALLOWED and f'${a:,.0f}' in s]
    out = [f'  cross-tranche leaks: {sorted(set(leaks)) if leaks else "none"}']
    if t == 'hm':
        hits = sorted({v for v in NO_RETURN if v in s})
        out.append(f'  participation / lender return: {hits if hits else "none"}')
        out.append(f'  returns page present: {"&mdash; total cash received" in s}')
    if t == 'common':
        hits = sorted({f for f in LOSS if f in s})
        out.append(f'  loss-level references: {hits if hits else "none"}')
    for word in ('appraisal', 'appraised', 'LWHA', 'Newmark', 'CBRE', 'New Day'):
        if re.search(word, s, re.I):
            out.append(f'  !! FORBIDDEN SOURCE REFERENCE: {word}')
    for brit in ('utilise', 'organis', 'centre', 'labour', 'metres', 'colour', 'favour',
                 'analyse', 'programme'):
        if brit in s.lower():
            out.append(f'  !! BRITISH SPELLING: {brit}')
    bad_keys = [m for m in re.findall(r'[^ ]{0,30}57 keys', s)
                if '58 with Dogwood Cove' not in s[s.index(m):s.index(m) + 90]
                and 'the 57 hotel keys' not in s[max(0, s.index(m) - 20):s.index(m) + 30]]
    if bad_keys:
        out.append(f'  !! key count: {bad_keys}')
    grids = s.count('&mdash; total cash received')
    out.append(f'  returns rows: {grids} (1 for debt and pref, 2 for common with the GP column)')
    return '\n'.join(out)


if __name__ == '__main__':
    for t in ('senior', 'hm', 'pref', 'common'):
        path, n, order = build(t)
        print(f'\n{PKG[t]["file"][:-8]}  —  {n} pages')
        print(audit(path, t))
