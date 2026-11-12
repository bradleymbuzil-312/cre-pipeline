# -*- coding: utf-8 -*-
"""Assemble the three packages and audit each for cross-tranche economic leakage."""
import io, os, re, sys
from v7_lib import load_sections, write_deck, SHARED, DECKDIR
from v7_common import capital_structure, sources_and_uses
from v7_pages import total_basis
from v7_patch import PATCH
from v7_num import renumber
import v7_tranche as T
from v7_marina import *
from v7_dogwood import page as dogwood_page, shift_page_refs
from figs_v7 import *
from figs_v7 import SENIOR as SENIOR_AMT, PREF as PREF_AMT, COMMON as COMMON_AMT

OLD_CORE = SHARED[:15]                     # THE ASSET .. MARKET AND DEMAND
# the acquisition detail page follows the narrative page it belongs to
CORE = OLD_CORE[:3] + ['DOGWOOD COVE'] + OLD_CORE[3:]
CLOSE = ['TOTAL BASIS', 'VALUE POSITIONING', 'SALE COMPARABLES', 'RECENT TRANSACTIONS', 'CONTACT']
# the debt packages carry the marina valuation, directly after the hotel value positioning
DEBT_CLOSE = ['TOTAL BASIS', 'VALUE POSITIONING', 'MARINA VALUATION', 'SALE COMPARABLES',
              'RECENT TRANSACTIONS', 'CONTACT']

PKG = {
 'senior': dict(file='Wylder Tilghman Island - Senior Debt.dc.html', label='Senior Debt',
   pages=[('SENIOR LOAN TERMS', T.senior_terms), ('DEBT SERVICE COVERAGE', T.senior_coverage),
          ('SENIOR RETURNS', lambda: T.returns_page('senior')),
          ('CREDIT CONSIDERATIONS', T.senior_credit)],
   dark={'SENIOR LOAN TERMS', 'CREDIT CONSIDERATIONS'}),
 'hm': dict(file=f'Wylder Tilghman Island - Senior Debt - {SENIOR_AMT/1_000_000:g}M Request.dc.html', label='Senior Debt',
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
          'pref': [SENIOR, COMMON], 'common': [SENIOR, PREF],
          }
# The LP deck is a request for investment, not an offer. It may name the terms that are open
# ("preferred return", "promote", "residual split") but must carry no number for any of them, and
# none of the senior debt request detail.
LP_FORBID = (['12.00%', 'SOFR', '8.21%', '3.79%', '17.00%', f'{CE_PREF:.2%}', '50 / 50',
              f'{SR_KICKER:.2%} of equity value', f'{PF_KICKER:.2%} of equity value',
              'Senior origination fee', 'Broker fee', 'Preferred origination fee', 'placement fee',
              'Accrual rate', 'Annual debt service', 'Debt service coverage', 'Debt yield',
              'Equity multiple', 'Projected Return', 'total cash received', 'Net Funded Basis',
              'not for distribution', 'Exit participation',
              f'${SR_NET:,.0f}', f'${PF_NET:,.0f}', f'${LP_PREF:,.0f}']
             + [f'${v:,.0f}' for v in SR_KICK + PF_KICK + SR_CASH + PF_CASH + LP_CASH
                + GP_CASH_OUT + SR_PROFIT + PF_PROFIT + LP_PROFIT + GP_PROFIT + CE_RESID]
             )   # bare multiples are left out: they collide with the coverage ratios
LP_REQUIRED = ['To be determined', 'to be determined', f'${COMMON_AMT:,.0f}', f'${TOTAL:,.0f}',
               f'${GP_CASH:,.0f}']
# the lender-facing packages carry no partnership, GP or LP vocabulary at all
PARTNERSHIP_WORDS = ['partnership', 'Partnership', 'pari passu', 'general partner',
                     'General Partner', 'limited partner', 'Limited Partner', '&middot; LP',
                     'GP co-investment', 'GP &mdash;', 'GP share', 'GP ownership', 'LP share',
                     'LP commitment', 'promote', 'residual split', 'preferred return']
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
# marina slip values, which collide by coincidence with tranche figures: 47 slips at the $40,000
# top of the range is $1,880,000, and so is the preferred's base-case exit participation.
ALLOWED_STR = {f'${SLIPS_T * v:,.0f}' for v in (LOW, REC, HIGH)} | {f'${DOGWOOD_ASIS:,.0f}',
               f'${SLIPS_W * REC:,.0f}', f'${SLIPS_D * REC:,.0f}', f'${SLIPS_W * HIGH:,.0f}',
               f'${SLIPS_D * HIGH:,.0f}', f'${SLIPS_W * LOW:,.0f}', f'${SLIPS_D * LOW:,.0f}',
               f'${INCOME_SLIP * SLIPS_T:,.0f}', f'${INCOME_SLIP * SLIPS_W:,.0f}'}
ALLOWED |= {SLIPS_T * v for v in (LOW, REC, HIGH)} | {SLIPS_W * REC, SLIPS_D * REC,
            SLIPS_W * LOW, SLIPS_D * LOW, SLIPS_W * HIGH, SLIPS_D * HIGH,
            INCOME_SLIP * SLIPS_T, INCOME_SLIP * SLIPS_W, DOGWOOD_ASIS}
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
    lender = t in ('senior', 'hm')
    carries_marina = lender
    close = DEBT_CLOSE if carries_marina else CLOSE
    order = (['TITLE', 'THE OPPORTUNITY'] + CORE + ['CAPITAL STRUCTURE', 'SOURCES AND USES']
             + [n for n, _ in p['pages']] + close)
    # every builder writes page numbers against the order before the insertion; one pass at the
    # end resolves each reference by section and renumbers it
    old_order = [n for n in order if n != 'DOGWOOD COVE']
    body['DOGWOOD COVE'] = dogwood_page()
    if carries_marina:
        body['MARINA VALUATION'] = marina_page(
            values_page=old_order.index('VALUE POSITIONING') + 1)
    path = f'{DECKDIR}/{p["file"]}'
    n = write_deck(path, head, order, body, p['label'])
    html, moved = shift_page_refs(io.open(path, encoding='utf-8').read(), old_order, order)
    io.open(path, 'w', encoding='utf-8').write(html)
    renumber(path, p['label'], dark=p['dark'])
    return path, n, order, moved


def audit(path, t):
    s = io.open(path, encoding='utf-8').read()
    leaks = []
    for other in OTHERS[t]:
        leaks += [p for p in other['phrases'] if p in s]
        leaks += [f'${a:,.0f}' for a in other['amounts']
                  if a not in ALLOWED and f'${a:,.0f}' in s]
    out = [f'  cross-tranche leaks: {sorted(set(leaks)) if leaks else "none"}']
    if t == 'lp':
        hits = sorted({v for v in LP_FORBID if v in s and v not in ALLOWED_STR})
        out.append(f'  economics or debt request detail: {hits if hits else "none"}')
        miss = [v for v in LP_REQUIRED if v not in s]
        out.append(f'  states the request and that terms are open: {"yes" if not miss else miss}')
        out.append(f'  "to be determined" markers: {s.lower().count("to be determined")}')
    if t in ('senior', 'hm'):
        pw = sorted({w for w in PARTNERSHIP_WORDS if w in s})
        out.append(f'  partnership / GP / LP vocabulary: {pw if pw else "none"}')
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


# At a request other than the solved $10,000,000 the exit waterfall is not available, so only the
# lender-facing package — which shows no return and no participation — can be built.
TRANCHES = ('senior', 'hm', 'pref', 'common') if WATERFALL_OK else ('hm',)

if __name__ == '__main__':
    if not WATERFALL_OK:
        print(f'${SENIOR_AMT:,} request — lender-facing package only '
              '(the exit waterfall is solved at $10,000,000)')
    for t in TRANCHES:
        path, n, order, moved = build(t)
        print(f'\n{PKG[t]["file"][:-8]}  —  {n} pages')
        print(f'  page references renumbered: {", ".join(moved) if moved else "none"}')
        print(audit(path, t))
