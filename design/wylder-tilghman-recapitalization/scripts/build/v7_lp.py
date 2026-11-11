# -*- coding: utf-8 -*-
"""The limited partner recapitalization deck.

A request for investment, not an offer of terms. The LP funds the entire closing; a senior
refinance in month three funds the business plan and returns capital. The deck carries no senior
debt request details and no LP economics: no preferred return, no splits, no promote, no
projected return. The structure and the waterfall are stated as open.
"""
import io
import re

from v7_lib import *
from v7_tranche import tbl, darkpage, META, DATE, TAIL
from v7_pages import dkv, bigcol, blk
from figs_lp import *

LABEL = 'LP Recapitalization'
EYEBROW = 'Confidential &middot; LP Recapitalization'

META['lp'] = dict(
  label=LABEL, eyebrow=EYEBROW,
  kicker=f'LP Recapitalization &middot; ${LP_EQUITY:,.0f}',
  amount=LP_EQUITY, color='#456EAB', date='November 11, 2026',
  lede=(f'A <strong>${LP_EQUITY:,.0f} limited partner recapitalization</strong> of the equity in a '
        '58-key waterfront resort in Talbot County, Maryland &mdash; retiring the existing loan and '
        'the merchant cash advance in full and acquiring the adjacent waterfront parcel. '
        '<strong>The LP funds the entire closing and no debt sits ahead of it.</strong> The asset, '
        'the business plan and the capital requirement are set out in full; the return structure '
        'and the distribution waterfall are open and will be set with the lead investor.'),
  stats=[('LP Equity', f'${LP_EQUITY:,.0f}'),
         ('Debt at Closing', '$0'),
         ('Return Structure', 'To be determined')])

TILES = [
  ('LP Equity', f'${LP_EQUITY/1e6:,.2f}M',
   f'{LP_EQUITY/VAL["is"]:.2%} of as-is value &middot; ${round(LP_EQUITY/KEYS):,} per key', 1),
  ('Debt at Closing', '$0', 'The existing loan and the MCA are retired in full', 0),
  ('Total Capital', f'${TOTAL_CAPITAL/1e6:,.2f}M',
   f'With the ${SENIOR:,.0f} senior refinance in month three', 0),
  ('Net Capital in the Asset', f'${NET_CAPITAL/1e6:,.2f}M',
   f'${round(NET_CAPITAL/KEYS):,} per key on 58 keys', 0),
  ('Returned at the Refinance', f'${RETURN_OF_CAP/1e6:,.2f}M',
   f'{RETURN_OF_CAP/LP_NET:.1%} of net cash invested, inside 90 days', 0),
  ('Renovation Program', f'${RENOVATION/1e6:,.2f}M',
   'Funded from the refinance, not from closing equity', 0),
  ('Estimated Value &middot; Stabilized', f'${VAL["stab"]/1e6:,.2f}M',
   f'${round(VAL["stab"]/KEYS):,} per key &middot; April 2029', 0),
  ('Return Structure', 'Open', 'Preferred return, waterfall and promote to be determined', 1)]


def opportunity():
    lede = (f'Marcus &amp; Millichap Capital Corporation is placing a '
            f'<strong style="color:var(--mm-navy-900);">${LP_EQUITY:,.0f} limited partner '
            'recapitalization</strong> of the equity in Wylder Hotel Tilghman Island. The LP funds '
            'the entire closing, retiring the existing loan and the merchant cash advance in full '
            f'and buying the adjacent parcel; a ${SENIOR:,.0f} senior refinance in month three '
            f'funds the renovation and returns ${RETURN_OF_CAP:,.0f} of capital inside 90 days. '
            '<strong style="color:var(--mm-navy-900);">The return structure and the distribution '
            'waterfall are to be determined</strong> and are open for discussion with the lead '
            'investor.')
    sn = ('Thirteen million two hundred fifty-five thousand eighty-five dollars of limited partner '
          'equity, two hundred twenty-eight thousand five hundred thirty-six a key, sixty-two '
          'percent of the as-is estimate. The LP funds the entire closing and no debt sits ahead of '
          'it: the existing loan and the merchant cash advance are retired in full. A seven million '
          'dollar senior refinance in month three funds the renovation and returns two million '
          'seventy thousand three hundred eighty-four of capital inside ninety days, sixteen percent '
          'of net cash invested. Total capital is twenty million two hundred fifty-five thousand '
          'eighty-five and net capital in the asset is eighteen million one hundred eighty-four '
          'thousand seven hundred one, three hundred thirteen thousand five hundred twenty-nine a '
          'key. The return structure is open.')
    return ('<section data-label="The Opportunity" data-screen-label="The Opportunity" '
     f'data-speaker-notes="{sn}" ' + sec(pad='64px 88px 44px') + '>\n'
     + h2('Summary of the recapitalization.', fs='48px', mb='0', pb='18px')
     + f'  <p style="{BODY}max-width:none;font-size:21px;line-height:1.5;color:var(--ink-700);'
       f'margin:22px 0 6px;">{lede}</p>\n'
     + '  <div style="display:grid;grid-template-columns:repeat(4,1fr);flex:1;'
       'font-variant-numeric:tabular-nums;">\n' + tiles(TILES) + '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────────── 18 · capital structure
def capital_structure():
    bar = '    <div style="display:flex;flex-direction:column;flex:1;min-height:0;">\n'
    for lab, amt, col, on, note in [
            ('LP equity &middot; at closing', LP_EQUITY, '#456EAB', True,
             'The only source at closing'),
            ('Senior refinance &middot; month three', SENIOR, '#032D67', False,
             'Funds the business plan and returns capital')]:
        pc = amt / TOTAL_CAPITAL
        mark = ('<div style="position:absolute;left:0;top:0;bottom:0;width:7px;'
                'background:var(--mm-orange);"></div>') if on else ''
        bar += (f'      <div style="position:relative;flex:0 0 {pc*100:.2f}%;background:{col};'
                f'{"" if on else "opacity:.42;"}box-sizing:border-box;padding:24px 30px;'
                'display:flex;flex-direction:column;justify-content:flex-end;min-height:0;'
                f'overflow:hidden;">\n        {mark}\n'
                f'        <div style="{DISP}font-weight:700;font-size:24px;color:#fff;">{lab}</div>\n'
                f'        <div style="{BODY}font-size:15px;color:rgba(255,255,255,.72);'
                f'margin-top:4px;">{note}</div>\n'
                '        <div style="display:flex;justify-content:space-between;align-items:baseline;'
                'margin-top:8px;gap:14px;">'
                f'<span style="{CON}font-size:13px;letter-spacing:.16em;color:rgba(255,255,255,.82);">'
                f'${amt:,.0f}</span>'
                f'<span style="{MONO}font-size:19px;font-weight:700;color:#fff;">{pc:.2%}</span>'
                '</div>\n      </div>\n')
    bar += ('    </div>\n    <div style="display:flex;justify-content:space-between;'
            f'align-items:baseline;margin-top:14px;padding-top:12px;border-top:{NAVY2};">'
            f'<span style="{CON}font-size:13px;letter-spacing:.18em;color:var(--mm-navy);">'
            'Total Capital</span>'
            f'<span style="{MONO}font-size:28px;font-weight:700;color:var(--mm-navy-900);">'
            f'${TOTAL_CAPITAL:,.0f}</span></div>\n')

    meas = (sub('Capital Measures')
     + row('LP equity &middot; gross', f'${LP_EQUITY:,.0f}', pad=5, kind='hi')
     + row('LP net cash invested', f'${LP_NET:,.0f}', pad=5,
           note=f'After the {LP_ORIG_PC:.2%} origination fee retained at funding')
     + row('Senior debt at closing', '$0', pad=5)
     + row('Senior refinance &middot; month three', f'${SENIOR:,.0f}', pad=5)
     + row('Total capital', f'${TOTAL_CAPITAL:,.0f}', pad=5, kind='sub')
     + row('Return of capital at the refinance', f'(${RETURN_OF_CAP:,.0f})', pad=5)
     + row('Net capital in the asset', f'${NET_CAPITAL:,.0f}', pad=5, kind='sub')
     + row('LP equity to as-is value', f'{LP_EQUITY/VAL["is"]:.2%}', pad=5)
     + row('Net capital to as-is value', f'{NET_CAPITAL/VAL["is"]:.2%}', pad=5)
     + row('Net capital to stabilized value', f'{NET_CAPITAL/VAL["stab"]:.2%}', pad=5)
     + row('LP equity per key &middot; 58 keys', f'${round(LP_EQUITY/KEYS):,}', pad=5, kind='sub'))

    terms = ('      <div style="height:12px;"></div>\n' + sub('Structure', pb='7px')
     + row('Preferred return', 'To be determined', pad=5, vfs='15px')
     + row('Distribution waterfall', 'To be determined', pad=5, vfs='15px')
     + row('Ownership and promote', 'To be determined', pad=5, vfs='15px')
     + row('Governance terms', 'To be determined', pad=5, vfs='15px', kind='sub')
     + para('The LP contributes 100% of the capital at closing and no debt sits ahead of it. The '
            'ownership split, the preferred return, the waterfall and the promote are open and '
            'will be set with the lead investor; the framework is on page 22. The ownership entity '
            'is 21551 Tilghman Investors LLC, with Wylder Hotels as operator and managing member.',
            fs='15px', auto=True))

    sn = ('The capital plan. Thirteen million two hundred fifty-five thousand eighty-five dollars of '
          'LP equity is the only source at closing, sixty-five percent of total capital, and no debt '
          'sits ahead of it. A seven million dollar senior refinance in month three brings total '
          'capital to twenty million two hundred fifty-five thousand eighty-five and returns two '
          'million seventy thousand three hundred eighty-four, leaving eighteen million one hundred '
          'eighty-four thousand seven hundred one of net capital in the asset, eighty-five percent '
          'of the as-is estimate and sixty-two percent of the stabilized estimate. The ownership '
          'split, the preferred return, the waterfall and the promote are all open.')
    return ('<section data-label="Capital Structure" data-screen-label="Capital Structure" '
     f'data-speaker-notes="{sn}" ' + sec(pad='60px 96px 44px') + '>\n'
     + h2(f'A ${LP_EQUITY:,.0f} LP recapitalization of the equity.',
          fs='44px', mb='15px', pb='13px')
     + '  <div style="display:grid;grid-template-columns:1.02fr 1fr;gap:50px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;min-height:0;">\n' + bar + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + meas + terms + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────────── 19 · sources and uses
def sources_and_uses():
    src = (sub('Sources')
     + row('LP equity &middot; gross', f'${LP_EQUITY:,.0f}', pad=15, fs='18px',
           note=f'100% of sources &middot; ${round(LP_EQUITY/KEYS):,} per key')
     + row('Senior debt at closing', '$0', pad=15, fs='18px',
           note='The existing loan and the merchant cash advance are retired in full')
     + row('Sponsor capital at closing', '$0', pad=15, fs='18px')
     + row('Total sources', f'${LP_EQUITY:,.0f}', pad=15, fs='18px', kind='sub')
     + '      <div style="height:18px;"></div>\n' + sub('Closing, Legal and Other Detail')
     + ''.join(row(k, f'${v:,.0f}', pad=10) for k, v in CLOSING_DETAIL)
     + row('Total closing, legal and other', '$130,100', pad=10, kind='sub')
     + para(f'Fees total <strong style="color:var(--mm-navy-900);">${FEES_TOTAL:,.0f}</strong>, or '
            f'{(LP_ORIG+MMCC_FEE)/LP_EQUITY:.2%} of gross LP equity &mdash; a {LP_ORIG_PC:.2%} '
            f'origination fee retained by the LP at funding and a {MMCC_PC:.2%} placement fee to '
            'Marcus &amp; Millichap Capital Corporation. Totals may differ by $1 from the sum of '
            'components due to rounding.', fs='15px', auto=True))
    uses = sub('Uses')
    for lab, amt in USES_CLOSE:
        uses += row(lab, f'${amt:,.0f}', pad=13, fs='17px')
    uses += row('Total uses', f'${LP_EQUITY:,.0f}', pad=13, fs='17px', kind='sub')
    uses += row('Sources less uses', '$0', pad=13, fs='17px', kind='hi')
    uses += ('      <div style="margin-top:auto;padding-top:18px;">\n' + sub('What the Equity Does',
             ind=8)
     + para('The LP equity <strong style="color:var(--mm-navy-900);">clears the balance '
            f'sheet</strong>: it retires the $10,714,782 existing loan and the $530,000 merchant '
            'cash advance, buys the adjacent parcel at 21441 Dogwood Cove for $1,100,000 and funds '
            '$250,000 of working capital. The renovation is funded from the senior refinance on '
            'page 21, not from closing equity.', fs='15.5px', ind=8)
     + '      </div>\n')
    sn = ('Sources and uses at closing. LP equity of thirteen million two hundred fifty-five '
          'thousand eighty-five is the only source; there is no senior debt and no sponsor capital '
          'at closing. The uses retire the ten million seven hundred fourteen thousand seven hundred '
          'eighty-two dollar existing loan and the five hundred thirty thousand dollar merchant cash '
          'advance, buy the adjacent parcel for one million one hundred thousand, fund two hundred '
          'fifty thousand of working capital and one hundred thirty thousand one hundred of closing '
          'costs, and pay the two origination and placement fees. Sources equal uses. The renovation '
          'is funded from the refinance, not from closing equity.')
    return ('<section data-label="Sources &amp; Uses" data-screen-label="Sources &amp; Uses" '
     f'data-speaker-notes="{sn}" ' + sec(pad='60px 96px 42px') + '>\n'
     + h2('Sources and uses of funds at closing.', fs='44px', mb='20px', pb='16px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.06fr;gap:50px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + src + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + uses + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────────── 20 · the investment request
def request():
    R = dict(pad=22)
    c = (bigcol('LP Equity Sought', f'${LP_EQUITY/1e6:,.2f}M',
          f'${round(LP_EQUITY/KEYS):,} per key &middot; 100% of sources at closing',
          dkv('Gross LP equity', f'${LP_EQUITY:,.0f}', **R)
          + dkv(f'Less origination fee &middot; {LP_ORIG_PC:.2%}', f'(${LP_ORIG:,.0f})', **R)
          + dkv('Net cash invested', f'${LP_NET:,.0f}', **R)
          + dkv('Debt ahead of it at closing', '$0', **R)
          + dkv('To as-is value', f'{LP_EQUITY/VAL["is"]:.2%}', accent=True, last=True, **R),
          'first', fs='74px')
     + bigcol('What It Clears', f'${11_244_782/1e6:,.2f}M',
          'The existing loan and the merchant cash advance, retired in full',
          dkv('Existing loan payoff', '$10,714,782', **R)
          + dkv('Merchant cash advance', '$530,000', **R)
          + dkv('Dogwood Cove acquisition', '$1,100,000', **R)
          + dkv('Working capital', '$250,000', **R)
          + dkv('Balance sheet at closing', 'Clear', accent=True, last=True, **R),
          'mid', fs='74px')
     + bigcol('Return Structure', 'Open',
          'Preferred return, waterfall and promote to be determined',
          dkv('Preferred return', 'To be determined', **R)
          + dkv('Return of capital', 'To be determined', **R)
          + dkv('Residual split', 'To be determined', **R)
          + dkv('Sponsor promote', 'To be determined', **R)
          + dkv('Ownership and governance', 'To be determined', accent=True, last=True, **R),
          'last', fs='74px'))
    b = (blk('What Is Fixed', 'The asset, the business plan and the renovation program; the '
             f'${LP_EQUITY:,.0f} capital requirement and the uses of funds on page 19; the '
             f'${SENIOR:,.0f} senior refinance that funds the plan and returns '
             f'${RETURN_OF_CAP:,.0f} of capital in month three. All of it is set out in the pages '
             'that follow.')
     + blk('What Is Open', 'The preferred return, the order and mechanics of the distribution '
           'waterfall, the residual split, the promote, the ownership percentages and the '
           'governance terms. None of it is pre-set, and the framework on page 22 is deliberately '
           'left without rates.')
     + blk('Next Step', 'An indication of interest on size and structure. A term sheet, the full '
           'financial model, the historical operating statements, the purchase and sale agreement '
           'on the adjacent parcel and sponsor materials follow on request.'))
    sn = ('The investment request. Thirteen million two hundred fifty-five thousand eighty-five '
          'dollars of gross LP equity, twelve million nine hundred eighty-nine thousand nine hundred '
          'eighty-four net of the two percent origination fee retained at funding, sixty-two percent '
          'of the as-is estimate, with no debt ahead of it at closing. It clears the balance sheet: '
          'ten million seven hundred fourteen thousand seven hundred eighty-two of existing loan and '
          'five hundred thirty thousand of merchant cash advance retired in full, the adjacent '
          'parcel bought for one million one hundred thousand and two hundred fifty thousand of '
          'working capital funded. What is open is the preferred return, the return of capital, the '
          'residual split, the promote, the ownership percentages and the governance terms. The next '
          'step is an indication of interest on size and structure.')
    return darkpage('The Investment Request', 'What is being sought, and what is still open.',
                    sn, c, b)


# ───────────────────────────────────────────────────── 21 · what the refinance funds
def refinance():
    left = sub('Allocation of Senior Refinance Proceeds')
    for lab, amt in REFI_ALLOC:
        left += row(lab, f'${amt:,.0f}', pad=30, fs='17px',
                    kind=('hi' if lab.startswith('Return of capital') else ''))
    left += row('Total', f'${SENIOR:,.0f}', pad=30, fs='18px', kind='sub')
    left += para('The senior refinance funds in month three, approximately 90 days after closing. '
                 '<strong style="color:var(--mm-navy-900);">Its terms are not part of this '
                 'request</strong> and are being arranged separately; the allocation above is what '
                 'the proceeds do for the business plan.', fs='15.5px', auto=True)

    right = (sub('What It Does for the Plan')
     + ''.join(
        f'      <div style="padding:17px 0;border-bottom:{HAIR};flex:1;">'
        f'<div style="{CON}font-size:12.5px;letter-spacing:.16em;color:var(--mm-orange);">{t}</div>'
        f'<p style="{BODY}max-width:none;font-size:16.5px;line-height:1.48;color:var(--ink-700);'
        f'margin:8px 0 0;">{x}</p></div>\n'
        for t, x in [
          ('It Funds the Renovation',
           '$3,003,000 for the hotel capital improvement plan and $300,000 for the Dogwood Cove '
           'residence are held back by the lender and drawn against the work, so the renovation is '
           'not a call on closing equity. The schedule by trade is on page 9.'),
          ('It Returns Capital Early',
           f'${RETURN_OF_CAP:,.0f} goes back to the LP in month three &mdash; '
           f'{RETURN_OF_CAP/LP_NET:.1%} of net cash invested, inside 90 days &mdash; which is why '
           f'net capital in the asset is ${NET_CAPITAL:,.0f} rather than the full amount raised.'),
          ('It Carries Itself Through the Work',
           'A 15-month interest reserve and a $500,000 working capital reserve are funded from the '
           'same proceeds, so no operating cash is required to carry the loan while the asset is '
           'down for the renovation.'),
          ('It Is the Only Debt in the Plan',
           'The balance is modeled flat for the full hold, with no further draw and no second '
           'refinance assumed. The extended cash flow on page 13 carries it at that level.')])
     + '      <div style="margin-top:auto;padding-top:18px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Returned in Month Three', f'${RETURN_OF_CAP:,.0f}',
            f'{RETURN_OF_CAP/LP_NET:.1%} of net cash invested', pad='16px 14px 0 0',
            vc='var(--mm-orange)')
     + stat('Held Back for the Work', f'${3_303_000:,.0f}', 'Hotel plan and Dogwood Cove',
            pad='16px 14px 0 14px')
     + stat('Debt at Closing', '$0', 'The LP funds the close alone', br=False, pad='16px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('What the senior refinance funds. Seven million dollars in month three, about ninety days '
          'after closing. Three million three thousand is held back for the hotel capital '
          'improvement plan and three hundred thousand for the Dogwood Cove residence, drawn against '
          'the work. Two million seventy thousand three hundred eighty-four returns to the LP, '
          'sixteen percent of net cash invested. A fifteen-month interest reserve of seven hundred '
          'thirty-two thousand four hundred thirty-four and a five hundred thousand dollar working '
          'capital reserve come from the same proceeds, so no operating cash carries the loan '
          'through the renovation. Lender fees, recordation, title and legal are three hundred '
          'ninety-four thousand one hundred eighty-two. The terms of that loan are not part of this '
          'request and are being arranged separately.')
    return ('<section data-label="Business Plan Financing" data-screen-label="Refinance" '
     f'data-speaker-notes="{sn}" ' + sec(pad='54px 92px 40px') + '>\n'
     + h2(f'A ${SENIOR:,.0f} senior refinance funds the business plan.',
          fs='42px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.08fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────────── 22 · the open waterfall
TIERS = [('Tier 1', 'Preferred return',
          'A cumulative return accruing on contributed capital, paid before any capital is '
          'returned.', 'Rate and compounding to be determined'),
         ('Tier 2', 'Return of capital',
          'Contributed capital returned in full before any residual is shared. The month-three '
          'refinance already returns part of it.', 'Order and priority to be determined'),
         ('Tier 3', 'Residual split',
          'What remains after the preferred return and the return of capital, divided between the '
          'limited partner and the sponsor.', 'Split and any hurdles to be determined'),
         ('Promote', 'Sponsor promote',
          'Any share of the residual the sponsor earns above its contributed capital.',
          'Structure and thresholds to be determined')]

SETTERS = [
  ('Hold Period and Exit',
   'The projections on pages 11 to 13 carry a three-year hold and a stabilized year, with the cash '
   'flow extended to 2041 so an exit can be underwritten. The hold assumed in the waterfall '
   'follows from what the lead investor wants.'),
  ('The LP Funds the Whole Closing',
   f'${LP_EQUITY:,.0f} of LP equity is 100% of sources at closing and no debt sits ahead of it. '
   f'The ${SENIOR:,.0f} refinance arrives in month three and returns ${RETURN_OF_CAP:,.0f}, so '
   'the capital at risk falls early in the hold.'),
  ('Sponsor Capital and Control',
   'Wylder Hotels is the operator and managing member. Whether the sponsor contributes capital, '
   'and how any existing equity is credited, is part of the structure to be agreed rather than '
   'something assumed here.'),
  ('Governance',
   'Major-decision consents over a sale, a refinance, the budget, replacement of the manager and '
   'additional debt, together with removal rights, reporting and the treatment of future capital '
   'calls, are to be documented alongside the economics.'),
  ('What Is Available Now',
   'The full financial model, the historical operating statements, the purchase and sale agreement '
   'on the adjacent parcel and sponsor materials are available on request, so the structure can be '
   'priced against the numbers rather than around them.')]


def structure():
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
     + stat('LP Equity Sought', f'${LP_EQUITY:,.0f}', '100% of sources at closing',
            pad='16px 14px 0 0', vc='var(--mm-orange)')
     + stat('Net Cash Invested', f'${LP_NET:,.0f}', 'After the origination fee',
            pad='16px 14px 0 14px')
     + stat('Economics', 'Open', 'Nothing pre-set', br=False, pad='16px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('The waterfall framework. The order shown is the conventional one: a cumulative preferred '
          'return on contributed capital, then return of capital in full, then a split of what '
          'remains, with any sponsor promote above that. No rate, split, hurdle or promote is '
          'proposed. What will set the terms is the hold period and exit the lead investor wants, '
          'the fact that the LP funds the whole closing with no debt ahead of it and gets capital '
          'back in month three, whether and how the sponsor contributes capital, the governance '
          'terms, and the model and operating statements available now so the structure can be '
          'priced against the numbers.')
    return ('<section data-label="Structure and Waterfall" data-screen-label="Structure" '
     f'data-speaker-notes="{sn}" ' + sec(pad='54px 92px 40px') + '>\n'
     + h2('The distribution waterfall, with the terms left open.', fs='42px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1.08fr 1fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────────── assembly
CORE = ['THE ASSET', 'PROPERTY OVERVIEW', 'ADJACENT ACQUISITION', 'THE SPONSOR',
        'WYLDER BRAND & RESUME', 'BUSINESS PLAN', 'RENOVATION SCHEDULE', 'BRAND AFFILIATION',
        'PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS', 'EXTENDED CASH FLOW',
        'DEPARTMENTAL BENCHMARKS', 'HISTORICAL OPERATIONS', 'COMPETITIVE MARKET',
        'MARKET AND DEMAND']
ORDER = (['TITLE', 'THE OPPORTUNITY'] + CORE
         + ['CAPITAL STRUCTURE', 'SOURCES AND USES', 'THE INVESTMENT REQUEST',
            'BUSINESS PLAN FINANCING', 'STRUCTURE AND WATERFALL', 'TOTAL BASIS',
            'VALUE POSITIONING', 'MARINA VALUATION', 'SALE COMPARABLES', 'RECENT TRANSACTIONS',
            'CONTACT'])
DARK = {'THE INVESTMENT REQUEST'}
VALUES_PAGE = ORDER.index('VALUE POSITIONING') + 1


def build_deck():
    from v7_lib import load_sections, write_deck, DECKDIR
    from v7_num import renumber
    from v7_patch import extended_cash_flow, lp_funding
    from v7_tranche import title, contact
    from v7_marina import marina_page
    head, body = load_sections()
    # the extended cash flow carries this plan's senior loan, and no debt yield
    body['EXTENDED CASH FLOW'] = extended_cash_flow(body['EXTENDED CASH FLOW'], 'lp', ads=SENIOR_ADS,
                                                    loan=SENIOR)
    for _n in ('BUSINESS PLAN', 'ADJACENT ACQUISITION'):
        body[_n] = lp_funding(body[_n], _n)
    body['TITLE'] = title('lp')
    body['THE OPPORTUNITY'] = opportunity()
    body['CAPITAL STRUCTURE'] = capital_structure()
    body['SOURCES AND USES'] = sources_and_uses()
    body['THE INVESTMENT REQUEST'] = request()
    body['BUSINESS PLAN FINANCING'] = refinance()
    body['STRUCTURE AND WATERFALL'] = structure()
    body['MARINA VALUATION'] = marina_page(values_page=VALUES_PAGE)
    body['CONTACT'] = contact('lp')
    path = f'{DECKDIR}/Wylder Tilghman Island - LP Recapitalization.dc.html'
    n = write_deck(path, head, ORDER, body, LABEL)
    renumber(path, LABEL, dark=DARK)
    return path, n


if __name__ == '__main__':
    path, n = build_deck()
    s = io.open(path, encoding='utf-8').read()
    bad = [w for w in ('appraisal', 'appraised', 'LWHA', 'Newmark', 'CBRE', 'New Day')
           if w.lower() in s.lower()]
    econ = [w for w in ('12.0% pref', '2.0x', '20% IRR', '2.06x', '37.3%', 'SOFR', 'Equity multiple',
                        'Projected IRR', 'preferred return of', '51% /', '/ 49%')
            if w in s]
    print(f'  {path.split("/")[-1]}  —  {n} pages')
    print(f'  forbidden references: {bad or "none"}')
    print(f'  economics or debt request detail: {econ or "none"}')
    print(f'  "to be determined" markers: {s.lower().count("to be determined")}')
