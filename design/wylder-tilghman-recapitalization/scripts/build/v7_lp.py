# -*- coding: utf-8 -*-
"""The limited partner investment deck.

A request for investment, not an offer of terms. It carries the asset, the business plan, the
capital requirement and the uses of funds, and it states plainly that the return structure and
the distribution waterfall are open. It contains no senior debt request details and no LP
economics: no preferred return, no splits, no promote, no projected return.
"""
from v7_lib import *
from v7_tranche import tbl, darkpage, META, OPP, DATE, TAIL
from v7_pages import dkv, bigcol, blk
from figs_v7 import *

AHEAD = SENIOR + PREF

META['lp'] = dict(
  label='Limited Partner Investment', eyebrow='Confidential &middot; Limited Partner Investment',
  kicker=f'Limited Partner Investment &middot; ${COMMON:,.0f}',
  amount=COMMON, color='#456EAB', date='November 11, 2026',
  lede=(f'A <strong>${COMMON:,.0f} limited partner investment</strong> in a 58-key waterfront resort '
        f'in Talbot County, Maryland, alongside <strong>${GP_CASH:,.0f} of sponsor cash already in '
        'the asset</strong> &mdash; recapitalizing the existing debt, funding a complete renovation '
        'and acquiring the adjacent waterfront parcel. The asset, the business plan and the capital '
        'requirement are set out in full. <strong>The return structure and the distribution '
        'waterfall are open</strong> and will be set with the lead investor.'),
  stats=[('Investment Sought', f'${COMMON:,.0f}'),
         ('Total Capitalization', f'${TOTAL:,.0f}'),
         ('Return Structure', 'To be determined')])

OPP['lp'] = ('Summary of the investment.',
  f'Marcus &amp; Millichap Capital Corporation is seeking a <strong style="color:var(--mm-navy-900);">'
  f'${COMMON:,.0f} limited partner investment</strong> in Wylder Hotel Tilghman Island, alongside '
  f'<strong style="color:var(--mm-navy-900);">${GP_CASH:,.0f} of sponsor cash already in the '
  f'asset</strong>. The investment sits within a ${TOTAL:,.0f} capitalization that retires the '
  'existing debt, funds the renovation in full and acquires the adjacent waterfront parcel. '
  '<strong style="color:var(--mm-navy-900);">The return structure and the distribution waterfall '
  'are to be determined</strong> and are open for discussion with the lead investor.',
  [('Investment Sought', f'${COMMON/1e6:,.2f}M', f'${COMMON/KEYS:,.0f} per key &middot; funded at close', 1),
   ('Total Capitalization', f'${TOTAL/1e6:,.2f}M', 'All three tranches funded at close', 0),
   ('Sponsor Cash in the Asset', f'${GP_CASH/1e6:,.2f}M', 'Invested outside loan proceeds, staying in', 0),
   ('Capital Ahead', f'${AHEAD/1e6:,.2f}M', f'{AHEAD/VAL["is"]:.2%} of the as-is estimate', 0),
   ('Renovation Program', '$3.30M', f'${3_303_000/KEYS:,.0f} per key &middot; funded at close', 0),
   ('Total Cost Basis', f'${COST_BASIS/1e6:,.2f}M', f'${COST_BASIS_KEY:,.0f} per key on 58 keys', 0),
   ('Estimated Value &middot; Stabilized', f'${VAL["stab"]/1e6:,.2f}M',
    f'${VAL["stab"]/KEYS:,.0f} per key &middot; April 2029', 0),
   ('Return Structure', 'Open', 'Preferred return, waterfall and promote to be determined', 1)])


def lp_request():
    R = dict(pad=24)
    c = (bigcol('Investment Sought', f'${COMMON/1e6:,.2f}M', f'${COMMON/KEYS:,.0f} per key',
          dkv('LP commitment', f'${COMMON:,.0f}', **R)
          + dkv('Funded', 'In full at close', **R)
          + dkv('Share of capitalization', f'{COMMON/TOTAL:.2%}', **R)
          + dkv('Alongside sponsor cash', f'${GP_CASH:,.0f}', **R)
          + dkv('Partnership capital', f'${PARTNERSHIP:,.0f}', accent=True, last=True, **R),
          'first', fs='78px')
     + bigcol('Capital Ahead of It', f'${AHEAD/1e6:,.2f}M',
          'Senior debt and preferred equity, both funded at close',
          dkv('Senior debt', f'${SENIOR:,.0f}', **R)
          + dkv('Preferred equity', f'${PREF:,.0f}', **R)
          + dkv('Total ahead of the partnership', f'${AHEAD:,.0f}', **R)
          + dkv('Of the as-is estimate', f'{AHEAD/VAL["is"]:.2%}', **R)
          + dkv('Of the stabilized estimate', f'{AHEAD/VAL["stab"]:.2%}', accent=True, last=True, **R),
          'mid', fs='78px')
     + bigcol('Return Structure', 'Open',
          'Preferred return, waterfall and promote to be determined',
          dkv('Preferred return', 'To be determined', **R)
          + dkv('Return of capital', 'To be determined', **R)
          + dkv('Residual split', 'To be determined', **R)
          + dkv('Sponsor promote', 'To be determined', **R)
          + dkv('Governance terms', 'To be determined', accent=True, last=True, **R),
          'last', fs='78px'))
    b = (blk('What Is Fixed', 'The asset, the business plan and the renovation program; the '
             f'${TOTAL:,.0f} capital requirement and the uses of funds on page 19; the '
             f'${GP_CASH:,.0f} of sponsor cash already in the asset; and the capital that sits '
             'ahead of the partnership. All of it is set out in the pages that follow.')
     + blk('What Is Open', 'The preferred return, the order and mechanics of the distribution '
           'waterfall, the residual split, the promote, the ownership percentages and the '
           'governance terms. None of it is pre-set, and the framework on page 21 is deliberately '
           'left without rates.')
     + blk('Next Step', 'An indication of interest on size and structure. A term sheet, the full '
           'financial model, the historical operating statements, the purchase and sale agreement '
           'on the adjacent parcel and sponsor materials follow on request.'))
    sn = ('The investment request. Three million five hundred thousand dollars is sought from a '
          'limited partner, funded in full at close, twenty point one percent of a seventeen million '
          'four hundred four thousand dollar capitalization, alongside two million of sponsor cash '
          'for a five million five hundred thousand dollar partnership. Thirteen million nine '
          'hundred four thousand of senior and preferred capital sits ahead of it, sixty-five '
          'percent of the as-is estimate and forty-seven percent of the stabilized estimate. What is '
          'fixed is the asset, the business plan, the capital requirement and the uses of funds. '
          'What is open is the preferred return, the return of capital, the residual split, the '
          'promote and the governance terms. The next step is an indication of interest on size and '
          'structure.')
    return darkpage('The Investment Request', 'What is being sought, and what is still open.',
                    sn, c, b)


TIERS = [('Tier 1', 'Preferred return',
          'A cumulative return accruing on contributed capital, paid before any capital is '
          'returned.', 'Rate and compounding to be determined'),
         ('Tier 2', 'Return of capital',
          'Contributed capital returned in full before any residual is shared.',
          'Order and priority to be determined'),
         ('Tier 3', 'Residual split',
          'What remains after the preferred return and the return of capital, divided between the '
          'limited partner and the sponsor.', 'Split and any hurdles to be determined'),
         ('Promote', 'Sponsor promote',
          'Any share of the residual the sponsor earns above its contributed capital.',
          'Structure and thresholds to be determined')]

SETTERS = [
  ('Hold Period and Exit',
   'The projections on pages 11 to 13 carry a three-year hold and a stabilized year, with the cash '
   'flow extended to 2041 so an exit can be underwritten. The hold assumed in the waterfall follows '
   'from what the lead investor wants.'),
  ('Capital Ahead of the Partnership',
   f'${AHEAD:,.0f} of senior and preferred capital funds at close, {AHEAD/VAL["is"]:.2%} of the '
   f'as-is estimate and {AHEAD/VAL["stab"]:.2%} of the stabilized estimate. The cost of that '
   'capital is met before any partnership distribution.'),
  ('Sponsor Co-Investment',
   f'${GP_CASH:,.0f} of sponsor cash is already in the asset, invested outside loan proceeds, and '
   f'is included in the ${COST_BASIS:,.0f} basis on page 22. Whether it ranks alongside the new '
   'investment or behind it is part of the structure to be agreed.'),
  ('Governance',
   'Major-decision consents, removal rights, reporting and the treatment of future capital calls '
   'are to be documented alongside the economics.'),
  ('What Is Available Now',
   'The full financial model, the historical operating statements, the purchase and sale agreement '
   'on the adjacent parcel and sponsor materials are available on request, so the structure can be '
   'priced against the numbers rather than around them.'),
]


def lp_structure():
    left = sub('The Waterfall Framework')
    for i, (tier, name, desc, tbd) in enumerate(TIERS):
        bb = '' if i == len(TIERS) - 1 else f'border-bottom:{HAIR};'
        left += (f'      <div style="display:grid;grid-template-columns:104px 1fr;gap:20px;'
                 f'padding:25px 0;{bb}align-items:start;flex:1;">\n'
                 f'        <div style="{CON}font-size:13px;letter-spacing:.14em;'
                 f'color:var(--mm-orange);padding-top:5px;">{tier}</div>\n        <div>\n'
                 f'          <div style="{DISP}font-weight:700;font-size:23px;'
                 f'color:var(--mm-navy-900);">{name}</div>\n'
                 f'          <p style="{BODY}max-width:none;font-size:16.5px;line-height:1.48;'
                 f'color:var(--ink-700);margin:8px 0 0;">{desc}</p>\n'
                 f'          <div style="{MONO}font-size:14.5px;color:var(--mm-orange-700);'
                 f'margin-top:10px;">{tbd}</div>\n        </div>\n      </div>\n')
    left += para('The order above is the conventional one and is shown so the mechanics are clear. '
                 '<strong style="color:var(--mm-navy-900);">No rate, split, hurdle or promote is '
                 'proposed here.</strong> Each is open and will be set with the lead investor '
                 'before a term sheet is drawn.', fs='16px', auto=True)

    right = (sub('What Will Set the Terms')
     + ''.join(
        f'      <div style="padding:17px 0;border-bottom:{HAIR};flex:1;">'
        f'<div style="{CON}font-size:12.5px;letter-spacing:.16em;color:var(--mm-orange);">{t}</div>'
        f'<p style="{BODY}max-width:none;font-size:16.5px;line-height:1.48;color:var(--ink-700);'
        f'margin:8px 0 0;">{x}</p></div>\n'
        for t, x in SETTERS)
     + '      <div style="margin-top:auto;padding-top:18px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Investment Sought', f'${COMMON:,.0f}', 'Funded in full at close', pad='16px 14px 0 0',
            vc='var(--mm-orange)')
     + stat('Partnership Capital', f'${PARTNERSHIP:,.0f}', 'With the sponsor cash in the asset',
            pad='16px 14px 0 14px')
     + stat('Economics', 'Open', 'Nothing pre-set', br=False, pad='16px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('The waterfall framework. The order shown is the conventional one: a cumulative preferred '
          'return on contributed capital, then return of capital in full, then a split of what '
          'remains, with any sponsor promote above that. No rate, split, hurdle or promote is '
          'proposed. What will set the terms is the hold period and exit the lead investor wants, '
          'the thirteen million nine hundred four thousand of senior and preferred capital ahead of '
          'the partnership, the two million of sponsor cash already in the asset and how it ranks, '
          'the governance terms to be documented alongside the economics, and the model and '
          'operating statements available now so the structure can be priced against the numbers.')
    return ('<section data-label="Structure and Waterfall" data-screen-label="Structure" '
     f'data-speaker-notes="{sn}" ' + sec(pad='54px 92px 40px') + '>\n'
     + h2('The distribution waterfall, with the terms left open.', fs='42px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1.08fr 1fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')
