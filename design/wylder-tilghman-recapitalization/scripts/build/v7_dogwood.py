# -*- coding: utf-8 -*-
"""The Dogwood Cove acquisition in detail — the page that follows the narrative page.

Page 5 says what the parcel is and why it matters. This page carries the deal: the purchase and
sale agreement, what the money buys, what it earns, and why a parcel that was once part of the
hotel is available to buy back.
"""
import re

from v7_lib import *

PRICE, RENOVATION, DEPOSIT = 1_100_000, 300_000, 15_000
CLOSING_PC = 0.03                      # transfer, recordation and title; not yet verified
CLOSING_COSTS = round(PRICE * CLOSING_PC)
ALL_IN = PRICE + CLOSING_COSTS + RENOVATION
# the Change in Terms Addendum of October 22, 2026 moves settlement from October 30
CLOSING = 'November 16, 2026'
ACRES = 3
SLIPS_NEW, SLIPS_TOTAL = 24, 47
RESIDENCE_ADR, RESIDENCE_OCC = 1_500, 0.35
RESIDENCE_REVENUE = 191_625            # 2029 and after; 2028 is a leap year at $192,150

# the parcel's own pro forma, unlevered: what it earns against what it costs to buy and open.
# No appraisal allocates value to this parcel, so the page states yield on cost rather than a
# capitalized value.
DOG_NOI = {2028: 222_159, 2029: 223_734, 2030: 225_784, 2031: 231_860}
YOC = {y: n / ALL_IN for y, n in DOG_NOI.items()}
# value references, none of them an opinion of value
ASSESSED = 820_833                     # Maryland SDAT residential assessment
SLIPS_ASIS, SLIPS_COMMERCIAL = 280_000, 720_000
# without approval for commercial use of the 24 slips, the parcel's 2029 income falls to this
DOG_NOI_NO_SLIPS = 80_195

assert ALL_IN == 1_433_000
assert round(RESIDENCE_ADR * 365 * RESIDENCE_OCC) == RESIDENCE_REVENUE
assert abs(YOC[2029] - 0.1561) < 0.0005 and abs(YOC[2028] - 0.1550) < 0.0005


def page():
    left = ('    <div style="flex:1;position:relative;overflow:hidden;min-height:300px;">\n'
     '      <img src="assets/wt-dogwood-house.jpg" alt="21441 Dogwood Cove Road, adjacent to the '
     'hotel" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '      <div style="position:absolute;left:0;top:0;bottom:0;width:8px;display:flex;'
     'flex-direction:column;"><div style="flex:0 0 60%;background:var(--mm-orange);"></div>'
     '<div style="flex:0 0 40%;background:#456EAB;"></div></div>\n    </div>\n'
     '    <div style="background:var(--mm-navy-900);color:#fff;padding:22px 26px;">\n'
     f'      <div style="{CON}font-size:14px;letter-spacing:.18em;color:rgba(255,255,255,.9);'
     'border-bottom:1px solid rgba(255,255,255,.35);padding-bottom:9px;">Why It Is Available</div>\n'
     f'      <p style="{BODY}max-width:none;font-size:16px;line-height:1.5;'
     'color:rgba(255,255,255,.86);margin:14px 0 0;">The parcel was <strong style="color:#fff;">part '
     'of the hotel asset historically</strong>. It was separated and sold to a third party in '
     'bankruptcy proceedings about ten years ago. Buying it back reassembles the original '
     'assemblage under one owner, which is why a residence, three acres and two dozen slips sit '
     'immediately against the hotel and are available at all.</p>\n'
     f'      <p style="{BODY}max-width:none;font-size:15px;line-height:1.5;'
     'color:rgba(255,255,255,.72);margin:12px 0 0;">The 24 slips are in good condition and usable '
     'from day one, and the underwriting assumes they earn what the hotel&rsquo;s existing slips '
     'earn. <strong style="color:#fff;">Hotel use of them requires county zoning, Critical Area '
     'and riparian confirmation</strong>, and without it the parcel&rsquo;s stabilized income is '
     f'${DOG_NOI_NO_SLIPS:,}. None of this value sits in the estimated hotel values, which are '
     'for the hotel alone; the strategic case is on page 5.</p>\n'
     '    </div>\n')

    R = dict(pad=7, fs='16px')
    right = (sub('The Purchase and Sale Agreement')
     + row('Purchase price', f'${PRICE:,}', **R)
     + row('Deposit', f'${DEPOSIT:,}', **R)
     + row('Acquisition closing costs &middot; 3%', f'${CLOSING_COSTS:,}', **R)
     + row('Settlement per the addendum', CLOSING, vfs='15px', **R)
     + row('Buyer and title', '21551 Tilghman Investors LLC &middot; fee simple', vfs='14.5px',
           kind='sub', **R)
     + '      <div style="height:11px;"></div>\n'
     + sub(f'What the ${ALL_IN:,} Buys')
     + row('Four-bedroom residence', 'The 58th key', vfs='15px', **R)
     + row('Land', f'Approximately {ACRES} acres', vfs='15px', **R)
     + row('Boat slips', f'{SLIPS_NEW}, usable day one', vfs='15px', **R)
     + row('Renovation to bring it online', f'${RENOVATION:,}', **R)
     + row('Total project cost', f'${ALL_IN:,}', kind='sub', **R)
     + '      <div style="height:11px;"></div>\n'
     + sub('What It Earns')
     + row('Residence &middot; average daily rate', f'${RESIDENCE_ADR:,}', **R)
     + row('Residence &middot; occupancy', f'{RESIDENCE_OCC:.0%}', **R)
     + row('Residence revenue at stabilization', f'${RESIDENCE_REVENUE:,}', **R)
     + row('Parcel net operating income &middot; 2029', f'${DOG_NOI[2029]:,}', **R)
     + row('Marina slips after the acquisition', f'{SLIPS_TOTAL}', kind='sub', **R)
     + '      <div style="margin-top:auto;padding-top:13px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Total Project Cost', f'${ALL_IN:,}',
            f'${PRICE:,} price, ${CLOSING_COSTS:,} costs, ${RENOVATION:,} renovation',
            pad='13px 13px 0 0')
     + stat('Parcel NOI &middot; 2029', f'${DOG_NOI[2029]:,}', 'Unlevered, after its own expenses',
            pad='13px 13px 0 13px')
     + stat('Yield on Cost', f'{YOC[2029]:.2%}', 'On total project cost, not a cap rate',
            br=False, pad='13px 0 0 13px', vc='var(--mm-orange)')
     + '      </div>\n      </div>\n')

    sn = ('The Dogwood Cove acquisition in detail. One million one hundred thousand dollars for a '
          'four-bedroom residence, approximately three acres and twenty-four boat slips, with a '
          'fifteen thousand dollar deposit and settlement moved by addendum to November sixteenth, '
          'twenty twenty-six. The '
          'buyer is twenty-one thousand five hundred fifty-one Tilghman Investors LLC, the same '
          'entity that owns the hotel. Thirty-three thousand of closing costs and three hundred '
          'thousand of renovation take the total project cost to one million four hundred '
          'thirty-three thousand. The residence becomes the '
          'fifty-eighth key at fifteen hundred dollars a night and thirty-five percent occupancy, '
          'one hundred ninety-one thousand six hundred twenty-five of revenue at stabilization. '
          'The parcel earns two hundred twenty-three thousand seven hundred thirty-four in twenty '
          'twenty-nine against that cost, a fifteen point six percent yield on cost. Hotel use of '
          'the twenty-four slips requires county zoning, Critical Area and riparian confirmation. '
          'The parcel was part of '
          'the hotel historically and was separated and sold in bankruptcy about ten years ago, so '
          'buying it back reassembles the original assemblage.')
    return ('<section data-label="Dogwood Cove Acquisition" data-screen-label="Dogwood Cove" '
     f'data-speaker-notes="{sn}" ' + sec(pad='52px 88px 38px') + '>\n'
     + h2('21441 Dogwood Cove Road, in detail.', fs='42px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.12fr;gap:44px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────── keeping cross-references honest across an insertion
REF = re.compile(r'\bpages?\s+(\d+)(\s+(?:and|to)\s+)(\d+)|\bpage\s+(\d+)')


def shift_page_refs(html, old_order, new_order):
    """Rewrite every "page N" by what section N meant before, not by arithmetic.

    The builders write page numbers against the order they were written for. Inserting a slide
    moves the targets, so each reference is resolved to its section under the old order and
    renumbered to that section's place in the new order.
    """
    new_of = {n: i + 1 for i, n in enumerate(new_order)}
    moved = []

    def one(n):
        n = int(n)
        if not 1 <= n <= len(old_order):
            raise ValueError(f'page {n} is outside the {len(old_order)}-page deck')
        name = old_order[n - 1]
        if name not in new_of:
            raise ValueError(f'page {n} pointed at {name!r}, which is not in the new order')
        if new_of[name] != n:
            moved.append(f'{n}->{new_of[name]} ({name})')
        return str(new_of[name])

    def sub_(m):
        if m.group(4):
            return f'page {one(m.group(4))}'
        return f'pages {one(m.group(1))}{m.group(2)}{one(m.group(3))}'

    return REF.sub(sub_, html), sorted(set(moved))
