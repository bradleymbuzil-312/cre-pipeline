# -*- coding: utf-8 -*-
"""The Dogwood Cove acquisition in detail — the page that follows the narrative page.

Page 5 says what the parcel is and why it matters. This page carries the deal: the purchase and
sale agreement, what the money buys, what it earns, and why a parcel that was once part of the
hotel is available to buy back.
"""
import re

from v7_lib import *

PRICE, RENOVATION, DEPOSIT = 1_100_000, 300_000, 15_000
ALL_IN = PRICE + RENOVATION
PSA_DAYS = 45
CLOSING = 'November 18, 2026'
ACRES = 3
SLIPS_NEW, SLIPS_TOTAL = 24, 47
RESIDENCE_ADR, RESIDENCE_OCC = 1_500, 0.35
RESIDENCE_REVENUE = 191_625
CAP, EBITDA = 0.0700, 300_000
IMPLIED_VALUE = round(EBITDA / CAP)
ABOVE_COST = IMPLIED_VALUE - ALL_IN

assert ALL_IN == 1_400_000
assert round(RESIDENCE_ADR * 365 * RESIDENCE_OCC) == RESIDENCE_REVENUE
assert IMPLIED_VALUE == 4_285_714 and ABOVE_COST == 2_885_714


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
     'from day one, roughly doubling projected slip revenue. None of this value is carried in the '
     'estimated hotel values, which are for the hotel alone; the strategic case is on page 5.</p>\n'
     '    </div>\n')

    R = dict(pad=7, fs='16px')
    right = (sub('The Purchase and Sale Agreement')
     + row('Purchase price', f'${PRICE:,}', **R)
     + row('Deposit', f'${DEPOSIT:,}', **R)
     + row('Closing period under the PSA', f'{PSA_DAYS} days', **R)
     + row('Contemplated closing', CLOSING, vfs='15px', **R)
     + row('Buyer and title', '21551 Tilghman Investors LLC &middot; fee simple', vfs='14.5px',
           kind='sub', **R)
     + '      <div style="height:11px;"></div>\n'
     + sub(f'What the ${ALL_IN:,} Buys')
     + row('Four-bedroom residence', 'The 58th key', vfs='15px', **R)
     + row('Land', f'Approximately {ACRES} acres', vfs='15px', **R)
     + row('Boat slips', f'{SLIPS_NEW}, usable day one', vfs='15px', **R)
     + row('Renovation to bring it online', f'${RENOVATION:,}', **R)
     + row('Total all-in cost', f'${ALL_IN:,}', kind='sub', **R)
     + '      <div style="height:11px;"></div>\n'
     + sub('What It Earns')
     + row('Residence &middot; average daily rate', f'${RESIDENCE_ADR:,}', **R)
     + row('Residence &middot; occupancy', f'{RESIDENCE_OCC:.0%}', **R)
     + row('Residence revenue at stabilization', f'${RESIDENCE_REVENUE:,}', **R)
     + row('Marina slips after the acquisition', f'{SLIPS_TOTAL}', kind='sub', **R)
     + '      <div style="margin-top:auto;padding-top:13px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('All-In Cost', f'${ALL_IN:,}', f'${PRICE:,} plus ${RENOVATION:,}',
            pad='13px 13px 0 0')
     + stat('Implied Value', f'${IMPLIED_VALUE:,}', f'~${EBITDA:,} of EBITDA at a {CAP:.1%} cap',
            pad='13px 13px 0 13px', vc='var(--mm-orange)')
     + stat('Above Cost', f'${ABOVE_COST:,}', f'{IMPLIED_VALUE/ALL_IN:.1f}x on cost', br=False,
            pad='13px 0 0 13px')
     + '      </div>\n      </div>\n')

    sn = ('The Dogwood Cove acquisition in detail. One million one hundred thousand dollars for a '
          'four-bedroom residence, approximately three acres and twenty-four boat slips, with a '
          'fifteen thousand dollar deposit and a forty-five day closing period under the purchase '
          'and sale agreement, contemplated to close November eighteenth, twenty twenty-six. The '
          'buyer is twenty-one thousand five hundred fifty-one Tilghman Investors LLC, the same '
          'entity that owns the hotel. Three hundred thousand of renovation brings it online, so '
          'the all-in cost is one million four hundred thousand. The residence becomes the '
          'fifty-eighth key at fifteen hundred dollars a night and thirty-five percent occupancy, '
          'one hundred ninety-one thousand six hundred twenty-five of revenue at stabilization, and '
          'the twenty-four slips are in good condition and usable from day one, taking the marina '
          'to forty-seven slips and roughly doubling projected slip revenue. The parcel was part of '
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
