# -*- coding: utf-8 -*-
"""The limited partner equity marketing deck.

Deliberately indicative. The asset, the business plan, the market evidence and the uses of
capital are stated in full; the size of the LP check and the whole of the structure are left to
be negotiated. A target equity multiple is stated as an objective, with the disclaimer that goes
with it, and nothing else about the economics is proposed.
"""
import io
import re

from v7_lib import *
from v7_lib import SHARED
from v7_tranche import tbl, darkpage, META, TAIL
from v7_pages import dkv, bigcol, blk
from figs_v7 import (KEYS, VAL, PRO, GP_CASH, FIXED_USES, TOTAL, COST_BASIS, COST_BASIS_KEY,
                     CLOSING, SELL_COST)

def pg(name):
    """The page a section lands on in this deck's final order."""
    return ORDER.index(name) + 1


LABEL = 'LP Equity'
EYEBROW = 'Confidential &middot; LP Equity'
DATE = 'November 17, 2026'

EQ_LOW, EQ_HIGH = 3_500_000, 13_255_085      # common slice, through to funding the close alone
TARGET_MULT, TARGET_HOLD = 2.0, 36
# This package runs on the combined pro forma: the hotel plus Dogwood Cove, with the parcel
# carrying its own expenses. 2029 is the first stabilized year under it.
#
# Yield on cost puts combined income against a basis that includes the parcel. The estimated
# values are for the hotel alone, so the implied cap is struck on hotel income only; mixing the
# two would flatter the rate.
from v7_addenda import RECON_STAB, HOTEL_STAB

STAB_NOI = RECON_STAB
YIELD_ON_COST = STAB_NOI / COST_BASIS
IMPLIED_CAP = HOTEL_STAB / VAL['stab']

PLAN_USES = [('Existing loan payoff', 10_714_782),
             ('Hotel renovation program', 3_003_000),
             ('Dogwood Cove acquisition', 1_100_000),
             ('Dogwood Cove renovation', 300_000),
             ('Working capital', 500_000),
             ('Closing, legal and other', 130_100)]

assert sum(a for _, a in PLAN_USES) == FIXED_USES
assert abs(YIELD_ON_COST - 0.1308) < 0.0005 and abs(IMPLIED_CAP - 0.0777) < 0.0005

META['eq'] = dict(
  label=LABEL, eyebrow=EYEBROW, kicker='Limited Partner Equity &middot; Target 2.0x',
  amount=EQ_HIGH, color='#456EAB', date=DATE,
  lede=('A <strong>limited partner equity investment</strong> in a 58-key waterfront resort in '
        'Talbot County, Maryland &mdash; retiring the existing debt, funding a complete renovation '
        'and acquiring the adjacent waterfront parcel, alongside '
        f'<strong>${GP_CASH:,.0f} of sponsor cash already in the asset</strong>. The sponsor is '
        f'targeting a <strong>{TARGET_MULT:.1f}x equity multiple over a {TARGET_HOLD}-month '
        'hold</strong>. The size of the investment and the whole of the return structure are open '
        'and will be negotiated with the lead investor.'),
  stats=[('Target Multiple', f'{TARGET_MULT:.1f}x'),
         ('Target Hold', f'{TARGET_HOLD} months'),
         ('Structure', 'Negotiable')])

TILES = [
  ('Target Equity Multiple', f'{TARGET_MULT:.1f}x',
   f'Objective over a {TARGET_HOLD}-month hold &mdash; not a projection', 1),
  ('Equity Required', f'${EQ_LOW/1e6:,.1f}M &ndash; ${EQ_HIGH/1e6:,.1f}M',
   'Depending on the senior and preferred capital placed alongside', 1),
  ('Total Capital Requirement', f'${TOTAL/1e6:,.1f}M', 'Indicative, at the current capital plan', 0),
  ('Sponsor Cash in the Asset', f'${GP_CASH/1e6:,.2f}M', 'Invested outside loan proceeds, staying in', 0),
  ('Yield on Cost &middot; Stabilized', f'{YIELD_ON_COST:.2%}',
   f'${STAB_NOI:,.0f} combined against a ${COST_BASIS:,.0f} basis', 0),
  ('Basis per Key', f'${COST_BASIS_KEY:,.0f}',
   f'Against a ${round(VAL["stab"]/KEYS):,} stabilized estimate', 0),
  ('Renovation Program', '$3.30M', 'Funded from the capital raised at closing', 0),
  ('Structure', 'Negotiable',
   'Preferred return, waterfall, promote and ownership all open', 1)]


def opportunity():
    lede = ('Marcus &amp; Millichap Capital Corporation is seeking a '
            '<strong style="color:var(--mm-navy-900);">limited partner equity investment</strong> '
            'in Wylder Hotel Tilghman Island. The capital retires the existing debt, funds the '
            'renovation in full and acquires the adjacent waterfront parcel. The sponsor is '
            f'<strong style="color:var(--mm-navy-900);">targeting a {TARGET_MULT:.1f}x equity '
            f'multiple over a {TARGET_HOLD}-month hold</strong>. The size of the investment '
            'depends on the senior and preferred capital placed alongside it, and '
            '<strong style="color:var(--mm-navy-900);">the structure is open for '
            'negotiation</strong>.')
    sn = ('The sponsor is targeting a two times equity multiple over a thirty-six month hold. That '
          'is an objective, not a projection. The equity required is between about three and a half '
          'and thirteen point three million dollars, depending on the senior and preferred capital '
          'placed alongside it, within a total capital requirement of about seventeen point four '
          'million. Two million of sponsor cash is already in the asset. Stabilized net operating '
          'income of two million six hundred seventy thousand six hundred eleven is a thirteen '
          'point nine percent yield on a nineteen million two hundred forty-seven thousand dollar '
          'basis, three hundred thirty-one thousand eight hundred sixty a key against a five '
          'hundred eight thousand six hundred twenty-one stabilized estimate. The structure is open '
          'for negotiation.')
    return ('<section data-label="The Opportunity" data-screen-label="The Opportunity" '
     f'data-speaker-notes="{sn}" ' + sec(pad='64px 88px 44px') + '>\n'
     + h2('Summary of the equity opportunity.', fs='48px', mb='0', pb='18px')
     + f'  <p style="{BODY}max-width:none;font-size:21px;line-height:1.5;color:var(--ink-700);'
       f'margin:22px 0 6px;">{lede}</p>\n'
     + '  <div style="display:grid;grid-template-columns:repeat(4,1fr);flex:1;'
       'font-variant-numeric:tabular-nums;">\n' + tiles(TILES) + '  </div>\n@@FOOTER@@\n</section>')


def uses():
    left = sub('Uses of Capital')
    for lab, amt in PLAN_USES:
        left += row(lab, f'${amt:,.0f}', pad=18, fs='17.5px')
    left += row('The plan', f'${FIXED_USES:,.0f}', pad=18, fs='18px', kind='sub')
    left += row('Financing reserves, fees and costs', 'Varies with the structure placed', pad=18,
                fs='17.5px', vfs='15px')
    left += row('Total capital requirement', f'~${TOTAL:,.0f}', pad=18, fs='19px', kind='tot',
                note='Indicative, at the current capital plan')
    left += para('The six lines above do not move. What moves is the financing layer on top of '
                 'them &mdash; the reserves and fees that come with whatever senior and preferred '
                 'capital is placed &mdash; and with it the size of the equity check.',
                 fs='15.5px', auto=True)

    right = (sub('What the Capital Does')
     + ''.join(
        f'      <div style="padding:17px 0;border-bottom:{HAIR};flex:1;">'
        f'<div style="{CON}font-size:12.5px;letter-spacing:.16em;color:var(--mm-orange);">{t}</div>'
        f'<p style="{BODY}max-width:none;font-size:16.5px;line-height:1.48;color:var(--ink-700);'
        f'margin:8px 0 0;">{x}</p></div>\n'
        for t, x in [
          ('Clears the Balance Sheet',
           'The $10,714,782 existing loan is retired in full. What replaces it is the subject of '
           'the senior and preferred placements running alongside this one.'),
          ('Funds the Renovation in Full',
           '$3,003,000 for the hotel and $300,000 for the Dogwood Cove residence, with $258,000 of '
           'contingency inside it. The program is designed, priced and scheduled; the schedule by '
           f'trade is on page {pg("RENOVATION SCHEDULE")}, and the draw on '
           f'page {pg("RENOVATION CASH FLOW")}.'),
          ('Buys Back the Adjacent Parcel',
           '$1,100,000 for the residence, roughly three acres and 24 boat slips, plus $300,000 to '
           'bring it online. It was part of the hotel until a bankruptcy sale about ten years ago. '
           f'The detail is on page {pg("DOGWOOD COVE")}.'),
          ('Carries the Asset Through the Work',
           '$500,000 of working capital, plus whatever interest and carry reserve the financing '
           'requires, so the renovation does not depend on operating cash flow.')])
     + '      <div style="margin-top:auto;padding-top:18px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('The Plan', f'${FIXED_USES:,.0f}', 'Does not move', pad='16px 14px 0 0')
     + stat('Total Requirement', f'~${TOTAL:,.0f}', 'At the current plan',
            pad='16px 14px 0 14px', vc='var(--mm-orange)')
     + stat('Sponsor Cash In', f'${GP_CASH:,.0f}', 'Already invested, staying in', br=False,
            pad='16px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('What the capital funds. Ten million seven hundred fourteen thousand seven hundred '
          'eighty-two retires the existing loan. Three million three thousand funds the hotel '
          'renovation and three hundred thousand the Dogwood Cove residence. One million one '
          'hundred thousand buys the adjacent parcel. Five hundred thousand is working capital and '
          'one hundred thirty thousand one hundred is closing costs. That is fifteen million seven '
          'hundred forty-seven thousand eight hundred eighty-two and it does not move. On top of it '
          'sit the reserves and fees that come with whatever senior and preferred capital is '
          'placed, taking the total requirement to about seventeen point four million at the '
          'current plan.')
    return ('<section data-label="Uses of Capital" data-screen-label="Uses of Capital" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2('What the capital funds.', fs='44px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.06fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def requirement():
    R = dict(pad=22)
    c = (bigcol('Equity Required', f'${EQ_LOW/1e6:,.1f}M – ${EQ_HIGH/1e6:,.1f}M',
          'Depending on the senior and preferred capital placed alongside it',
          dkv('Total capital requirement', f'~${TOTAL:,.0f}', **R)
          + dkv('Senior and preferred capital', 'To be placed', **R)
          + dkv('Sponsor cash already in the asset', f'${GP_CASH:,.0f}', **R)
          + dkv('LP commitment', 'To be negotiated', **R)
          + dkv('Funding', 'In full at close', accent=True, last=True, **R),
          'first', fs='52px')
     + bigcol('Target Return', f'{TARGET_MULT:.1f}x',
          f'Equity multiple over a {TARGET_HOLD}-month hold',
          dkv('Target equity multiple', f'{TARGET_MULT:.1f}x', **R)
          + dkv('Target hold', f'{TARGET_HOLD} months', **R)
          + dkv('Stabilized yield on cost', f'{YIELD_ON_COST:.2%}', **R)
          + dkv('Implied cap on the stabilized estimate', f'{IMPLIED_CAP:.2%}', **R)
          + dkv('An objective, not a projection', f'See page {pg("TARGET RETURN")}',
                accent=True, last=True, **R),
          'mid', fs='86px')
     + bigcol('Structure', 'Open',
          'Every economic term is negotiable',
          dkv('Preferred return', 'To be negotiated', **R)
          + dkv('Return of capital', 'To be negotiated', **R)
          + dkv('Residual split', 'To be negotiated', **R)
          + dkv('Sponsor promote', 'To be negotiated', **R)
          + dkv('Ownership and governance', 'To be negotiated', accent=True, last=True, **R),
          'last', fs='86px'))
    b = (blk('What Is Fixed', 'The asset, the business plan and the renovation program; the six '
             f'lines of the plan on page {pg("SOURCES AND USES")}, totalling '
             f'${FIXED_USES:,.0f}; and the '
             f'${GP_CASH:,.0f} of sponsor cash already in the asset and staying in through the '
             'hold.')
     + blk('What Is Open', 'The size of the LP commitment, which falls as senior and preferred '
           'capital is placed alongside it, and every economic term: the preferred return, the '
           'waterfall, the residual split, the promote, the ownership percentages and the '
           'governance. Nothing here is pre-set.')
     + blk('Next Step', 'An indication of interest on size and structure. A term sheet, the full '
           'financial model, the historical operating statements, the purchase and sale agreement '
           'on the adjacent parcel and sponsor materials follow on request.'))
    sn = ('The equity requirement. Between about three and a half and thirteen point three million '
          'dollars, depending on how much senior and preferred capital is placed alongside it, '
          'within a total requirement of about seventeen point four million. Two million of sponsor '
          'cash is already in the asset. The sponsor is targeting a two times equity multiple over '
          'a thirty-six month hold; that is an objective, not a projection, and the basis for it is '
          'on the next page. Stabilized net operating income is a thirteen point nine percent yield '
          'on cost against an implied nine point zero five percent cap on the stabilized estimate. '
          'Every economic term is open: the preferred return, the return of capital, the residual '
          'split, the promote, the ownership and the governance.')
    return darkpage('The Equity Requirement', 'What is being sought, and what is negotiable.',
                    sn, c, b)


TIERS = [('Tier 1', 'Preferred return',
          'A cumulative return accruing on contributed capital, paid before any capital is '
          'returned.', 'Rate and compounding to be negotiated'),
         ('Tier 2', 'Return of capital',
          'Contributed capital returned in full before any residual is shared.',
          'Order and priority to be negotiated'),
         ('Tier 3', 'Residual split',
          'What remains, divided between the limited partner and the sponsor.',
          'Split and any hurdles to be negotiated'),
         ('Promote', 'Sponsor promote',
          'Any share of the residual the sponsor earns above its contributed capital.',
          'Structure and thresholds to be negotiated')]


DEPENDS = [
  ('The renovation lands', 'the last guestroom wave and the public spaces delivered on budget by '
                           'the end of June, for the back half of the 2027 season'),
  ('Rate and occupancy ramp', 'the asset reaches the stabilized case set out on page @@PRO@@, '
                              'not a higher one'),
  ('The marina expands', 'Dogwood Cove closes and the slip count reaches 47 across the two '
                         'properties'),
  ('The structure is agreed', 'senior and preferred capital placed at or inside the plan, so the '
                              'LP is not diluted by a larger raise'),
  ('The market holds', 'an exit at or near the stabilized estimate, which is struck at a '
                       f'{IMPLIED_CAP:.2%} cap on the hotel&rsquo;s stabilized income'),
  ('The slips are approved', 'hotel use of the Dogwood Cove slips clears county zoning, Critical '
                            'Area and riparian review; without it the parcel earns materially '
                            'less')]


def target():
    left = (sub('What a 2.0x Has to Come From')
     + row('Total cost basis', f'${COST_BASIS:,.0f}', pad=8, fs='16.5px',
           note=f'${COST_BASIS_KEY:,.0f} per key on 58 keys')
     + row('Stabilized net operating income', f'${STAB_NOI:,.0f}', pad=8, fs='16.5px',
           note='2029, hotel and the adjacent parcel combined')
     + row('Yield on cost at stabilization', f'{YIELD_ON_COST:.2%}', pad=8, fs='16.5px', kind='sub')
     + row('Estimated value upon stabilization', f'${VAL["stab"]:,.0f}', pad=8, fs='16.5px',
           note=f'${round(VAL["stab"]/KEYS):,} per key &middot; April 2029')
     + row('Implied cap on that estimate', f'{IMPLIED_CAP:.2%}', pad=8, fs='16.5px',
           note=f'Hotel income only &middot; ${HOTEL_STAB:,.0f}')
     + row('Spread, basis to stabilized estimate', f'{VAL["stab"]/COST_BASIS-1:.1%}', pad=8,
           fs='16.5px', kind='tot')
     + para(f'A {TARGET_MULT:.1f}x is an objective built on that spread: a basis of '
            f'${COST_BASIS_KEY:,.0f} a key against a stabilized estimate of '
            f'${round(VAL["stab"]/KEYS):,}, with the asset stabilizing at a {YIELD_ON_COST:.2%} '
            'yield on cost. The estimate covers the hotel alone, so the parcel&rsquo;s income '
            'sits in the yield on cost but not in the estimate.', fs='14.5px', mt='16px')
     + '      <div style="margin-top:14px;">\n'
     + sub('What the Target Depends On', pb='7px')
     + ''.join(
         f'      <div style="display:grid;grid-template-columns:28px 1fr;gap:12px;padding:5px 0;'
         f'{"" if i == len(DEPENDS) - 1 else f"border-bottom:{HAIR};"}align-items:baseline;">\n'
         f'        <div style="{MONO}font-size:13px;color:var(--mm-orange);">{i + 1:02d}</div>\n'
         f'        <div><span style="{BODY}font-size:15px;color:var(--mm-navy-900);'
         f'font-weight:600;">{k}</span>'
         f'<span style="{BODY}font-size:14px;color:var(--ink-700);"> &mdash; '
         f'{v.replace("@@PRO@@", str(pg("PROJECTIONS")))}</span></div>\n'
         '      </div>\n' for i, (k, v) in enumerate(DEPENDS))
     + '      </div>\n')

    right = sub('The Waterfall, Open')
    for i, (tier, name, desc, tbd) in enumerate(TIERS):
        bb = '' if i == len(TIERS) - 1 else f'border-bottom:{HAIR};'
        right += (f'      <div style="display:grid;grid-template-columns:96px 1fr;gap:18px;'
                  f'padding:19px 0;{bb}align-items:start;flex:1;">\n'
                  f'        <div style="{CON}font-size:12.5px;letter-spacing:.14em;'
                  f'color:var(--mm-orange);padding-top:4px;">{tier}</div>\n        <div>\n'
                  f'          <div style="{DISP}font-weight:700;font-size:21px;'
                  f'color:var(--mm-navy-900);">{name}</div>\n'
                  f'          <p style="{BODY}max-width:none;font-size:15.5px;line-height:1.45;'
                  f'color:var(--ink-700);margin:7px 0 0;">{desc}</p>\n'
                  f'          <div style="{MONO}font-size:14px;color:var(--mm-orange-700);'
                  f'margin-top:8px;">{tbd}</div>\n        </div>\n      </div>\n')
    right += ('      <div style="margin-top:auto;padding-top:16px;">\n'
     f'      <div style="background:var(--mm-navy-900);color:#fff;padding:20px 24px;">\n'
     f'        <div style="{CON}font-size:13px;letter-spacing:.18em;color:var(--mm-orange);'
     'margin-bottom:9px;">Target Returns Are Objectives</div>\n'
     f'        <p style="{BODY}max-width:none;font-size:15.5px;line-height:1.5;'
     f'color:rgba(255,255,255,.88);margin:0;">The {TARGET_MULT:.1f}x stated in this package is a '
     '<strong style="color:#fff;">target, not a projection, a forecast or a guarantee</strong>. '
     'No return is promised. It depends on the capital structure finally agreed, on execution of '
     'the business plan, on the sale price achieved and on market conditions at exit, none of '
     'which is within the sponsor&rsquo;s control. The estimated values in this package are '
     'stated for underwriting purposes and are subject to completion of the renovation and '
     'stabilization of operations.</p>\n      </div>\n      </div>\n')
    sn = ('What a two times has to come from. The total cost basis is nineteen million two hundred '
          'forty-seven thousand eight hundred eighty-two, three hundred thirty-one thousand eight '
          'hundred sixty a key. Stabilized net operating income of two million six hundred seventy '
          'thousand six hundred eleven is a thirteen point eight seven percent yield on that cost. '
          'The estimated value upon stabilization is twenty-nine million five hundred thousand, '
          'five hundred eight thousand six hundred twenty-one a key, which is a nine point zero '
          'five percent cap on the same income. The spread from basis to stabilized estimate is '
          'fifty-three percent. The waterfall is shown in order, with every rate and split left to '
          'be negotiated. The target is an objective, not a projection, a forecast or a guarantee, '
          'and no return is promised.')
    return ('<section data-label="Target Return and Structure" data-screen-label="Target Return" '
     f'data-speaker-notes="{sn}" ' + sec(pad='54px 92px 40px') + '>\n'
     + h2(f'A {TARGET_MULT:.1f}x target, and a structure still to be written.',
          fs='42px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.08fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Page order.  No CAPITAL STRUCTURE page (the stack is not yet fixed), no EXTENDED CASH FLOW
# (it carries a leverage assumption this package deliberately leaves open) and no terms page.
# ─────────────────────────────────────────────────────────────────────────────────────────────
CORE = ['THE ASSET', 'PROPERTY OVERVIEW', 'ADJACENT ACQUISITION', 'DOGWOOD COVE', 'THE SPONSOR',
        'WYLDER BRAND & RESUME', 'BUSINESS PLAN', 'RENOVATION SCHEDULE', 'RENOVATION CASH FLOW',
        'BRAND AFFILIATION', 'SLH MEMBERSHIP', 'PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS',
        'DEPARTMENTAL BENCHMARKS', 'HISTORICAL OPERATIONS', 'CASH FLOW HISTORICALS',
        'COMPETITIVE MARKET', 'MARKET AND DEMAND']
# the four slides this package carries and no other
ADDENDA = ['RENOVATION CASH FLOW', 'SLH MEMBERSHIP', 'CASH FLOW HISTORICALS', 'VALUATION DETAIL']
ORDER = (['TITLE', 'THE OPPORTUNITY'] + CORE
         + ['SOURCES AND USES', 'THE INVESTMENT REQUEST', 'TARGET RETURN', 'TOTAL BASIS',
            'VALUE POSITIONING', 'VALUATION DETAIL', 'MARINA VALUATION', 'SALE COMPARABLES',
            'RECENT TRANSACTIONS', 'CONTACT'])
DARK = {'THE INVESTMENT REQUEST'}

# The reference baseline: the order the shared slides' "page N" numbers were written against.
# Only those slides are renumbered; the four pages written here already carry this deck's
# numbers and must be left alone.
OLD_REF_ORDER = [
    'TITLE', 'THE OPPORTUNITY', 'THE ASSET', 'PROPERTY OVERVIEW', 'ADJACENT ACQUISITION',
    'THE SPONSOR', 'WYLDER BRAND & RESUME', 'BUSINESS PLAN', 'RENOVATION SCHEDULE',
    'BRAND AFFILIATION', 'PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS', 'EXTENDED CASH FLOW',
    'DEPARTMENTAL BENCHMARKS', 'HISTORICAL OPERATIONS', 'COMPETITIVE MARKET', 'MARKET AND DEMAND',
    'CAPITAL STRUCTURE', 'SOURCES AND USES', 'SENIOR LOAN TERMS', 'DEBT SERVICE COVERAGE',
    'SENIOR RETURNS', 'CREDIT CONSIDERATIONS', 'TOTAL BASIS', 'VALUE POSITIONING',
    'MARINA VALUATION', 'SALE COMPARABLES', 'RECENT TRANSACTIONS', 'CONTACT']


def build_deck():
    from v7_lib import load_sections, write_deck, DECKDIR
    from v7_num import renumber
    from v7_patch import value_positioning, adjacent_acquisition, business_plan_window
    from v7_pages import total_basis
    from v7_dogwood import page as dogwood_page, shift_page_refs
    from v7_tranche import title, contact
    from v7_marina import marina_page
    from v7_addenda import (historicals, renovation_schedule, renovation_cash_flow, cbre, slh,
                            restate_years, restate_proforma, restate_parcel, correct_all,
                            EQ_BASIS_DATES)
    head, body = load_sections()
    body = correct_all(body)
    body['VALUE POSITIONING'] = value_positioning(body['VALUE POSITIONING'], 'eq')
    body['BUSINESS PLAN'] = business_plan_window(body['BUSINESS PLAN'], 'eq')
    body['ADJACENT ACQUISITION'] = restate_parcel(
        adjacent_acquisition(body['ADJACENT ACQUISITION'], 'eq'))
    # renumber the carried-over slides only, resolving each reference by section
    moved = []
    for _n in [c for c in CORE if c not in ADDENDA and c != 'DOGWOOD COVE'] + ['VALUE POSITIONING']:
        body[_n], _m = shift_page_refs(body[_n], OLD_REF_ORDER, ORDER)
        moved += _m
    body['DOGWOOD COVE'] = dogwood_page()
    body['TITLE'] = title('eq')
    body['THE OPPORTUNITY'] = opportunity()
    body['SOURCES AND USES'] = uses()
    body['THE INVESTMENT REQUEST'] = requirement()
    body['TARGET RETURN'] = target()
    # total_basis writes its page numbers against the same baseline as the carried-over slides
    body['TOTAL BASIS'], _m = shift_page_refs(total_basis('eq', dates=EQ_BASIS_DATES),
                                              OLD_REF_ORDER, ORDER)
    moved += _m
    # the four addenda, and this package's own renovation schedule
    body['RENOVATION SCHEDULE'] = renovation_schedule()
    body['RENOVATION CASH FLOW'] = renovation_cash_flow()
    body['SLH MEMBERSHIP'] = slh()
    body['CASH FLOW HISTORICALS'] = historicals(basis_page=pg('TOTAL BASIS'))
    body['VALUATION DETAIL'] = cbre(hist_page=pg('CASH FLOW HISTORICALS'))
    # the shared projection pages are labelled a year early against the actuals now carried
    # the reconciled model first, then the year labels it is stated against
    _hits = 0
    for _n in ('PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS', 'DEPARTMENTAL BENCHMARKS'):
        body[_n], _h = restate_proforma(body[_n], _n)
        _hits += _h
    assert _hits >= 25, ('pro forma restatement did not take', _hits)
    for _n in ('PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS', 'DEPARTMENTAL BENCHMARKS'):
        body[_n] = restate_years(body[_n])
    body['HISTORICAL OPERATIONS'] = restate_years(body['HISTORICAL OPERATIONS'], stats_only=True)
    # this package does present 2026, on the slide that follows
    _old = '2026 is a transition year and is not presented.'
    _new = (f'The trailing twelve months to September 2026, and the full departmental statement '
            f'behind all four periods, are on page {pg("CASH FLOW HISTORICALS")}.')
    assert body['HISTORICAL OPERATIONS'].count(_old) == 1
    body['HISTORICAL OPERATIONS'] = body['HISTORICAL OPERATIONS'].replace(_old, _new)
    body['MARINA VALUATION'] = marina_page(values_page=ORDER.index('VALUE POSITIONING') + 1)
    body['CONTACT'] = contact('eq')
    path = f'{DECKDIR}/Wylder Tilghman Island - LP Equity.dc.html'
    n = write_deck(path, head, ORDER, body, LABEL)
    renumber(path, LABEL, dark=DARK)
    return path, n, sorted(set(moved))


if __name__ == '__main__':
    path, n, moved = build_deck()
    s = io.open(path, encoding='utf-8').read()
    # CBRE is named on the valuation slide by instruction; it must appear nowhere else, and
    # LWHA, the superseded appraisal, must appear nowhere at all
    import re as _re
    parts = _re.split(r'<!-- ═+ \d+ · ([^═]*?) ═+ -->', s)
    elsewhere = ''.join(parts[i + 1] for i in range(1, len(parts), 2)
                        if parts[i] != 'VALUATION DETAIL')
    bad = [w for w in ('appraisal', 'appraised', 'LWHA', 'Newmark', 'CBRE', 'New Day')
           if w.lower() in elsewhere.lower()]
    on_slide = [w for w in ('CBRE', 'LWHA', 'Newmark') if w in s]
    # nothing about the senior request, and no proposed economics beyond the stated target
    econ = [w for w in ('SOFR', 'all-in rate', 'Debt yield', 'DSCR', 'Loan to value',
                        'Loan to cost', 'preferred return of', 'promote of', '% / ', 'Projected IRR',
                        'Equity multiple of', '12.00%', '$10,000,000 senior')
            if w in s]
    print(f'  {path.split("/")[-1]}  —  {n} pages')
    print(f'  forbidden references outside the valuation slide: {bad or "none"}')
    print(f'  named sources anywhere: {on_slide}')
    print(f'  senior-request or proposed economics: {econ or "none"}')
    print(f'  "to be negotiated" markers: {s.lower().count("to be negotiated")}')
    print(f'  target {TARGET_MULT:.1f}x stated: {s.count(f"{TARGET_MULT:.1f}x")} times')
    print(f'  page references renumbered: {", ".join(moved) if moved else "none"}')
