# -*- coding: utf-8 -*-
"""Cover, summary, terms, mechanics, returns, position and contact — one set per tranche.

Nothing on these pages discloses another tranche's rate, fee, participation, promote or return.
"""
from v7_lib import *
from v7_common import TRANCHE_COLOR
from v7_pages import returns_grid, dkv, bigcol, blk
from figs_v7 import *

DATE = 'October 30, 2026'
TAIL = '\n\n</x-import>\n</x-dc>\n</body>\n</html>\n'

META = {
 'senior': dict(label='Senior Debt', eyebrow='Confidential &middot; Senior Debt Placement',
   kicker=f'Senior Loan &middot; ${SENIOR:,.0f} &middot; First Trust Deed',
   amount=SENIOR, color='#032D67',
   lede=(f'A <strong>${SENIOR:,.0f} senior loan</strong>, first trust deed, on a 58-key waterfront '
         f'resort in Talbot County, Maryland &mdash; {LTV["is"]:.2%} of as-is value and {LTC:.2%} of '
         f'total cost. Interest-only at {ALLIN:.2%} for a {SR_TERM}-year term, with a twelve-month '
         f'interest and carry reserve funded at close. ${PREF+COMMON:,.0f} of subordinate capital '
         f'closes concurrently and ${GP_CASH:,.0f} of sponsor cash is already invested. Projected '
         f'{SR_MULT[B]:.2f}x and {SR_IRR[B]:.1%} IRR.'),
   stats=[('Loan Amount', f'${SENIOR:,.0f}'), ('All-In Rate', f'{ALLIN:.2%}'),
          ('LTV &middot; As-Is', f'{LTV["is"]:.2%}')]),
 'pref': dict(label='Preferred Equity', eyebrow='Confidential &middot; Preferred Equity Placement',
   kicker=f'Preferred Equity &middot; ${PREF:,.0f}',
   amount=PREF, color='#957551',
   lede=(f'A <strong>${PREF:,.0f} preferred equity investment</strong> in a 58-key waterfront resort in '
         f'Talbot County, Maryland, accruing at {PF_RATE_PIK:.2%} with no current-pay obligation and a '
         f'{PF_KICKER:.2%} participation in equity value at exit. ${SENIOR:,.0f} of senior debt sits '
         f'ahead of it; ${PARTNERSHIP:,.0f} of common capital, including ${GP_CASH:,.0f} of sponsor '
         f'cash, stands beneath it. Debt and preferred together are {(SENIOR+PREF)/VAL["is"]:.2%} of '
         f'as-is value. Projected {PF_MULT[B]:.2f}x and {PF_IRR[B]:.1%} IRR.'),
   stats=[('Commitment', f'${PREF:,.0f}'), ('Accrual Rate', f'{PF_RATE_PIK:.2%}'),
          ('Exit Participation', f'{PF_KICKER:.2%}')]),
 'common': dict(label='Common Equity', eyebrow='Confidential &middot; Common Equity Placement',
   kicker=f'Common Equity &middot; ${COMMON:,.0f} Limited Partner',
   amount=COMMON, color='#456EAB',
   lede=(f'A <strong>${COMMON:,.0f} limited partner investment</strong> in a 58-key waterfront resort in '
         f'Talbot County, Maryland, alongside <strong>${GP_CASH:,.0f} of sponsor cash on identical pari '
         f'passu terms</strong>. The LP earns a {CE_PREF:.2%} cumulative preferred return and its capital '
         f'back in full before any residual is split 50/50. The GP holds a 51% ownership interest and '
         f'takes nothing until the LP has been paid. Projected {LP_MULT[B]:.2f}x and {LP_IRR[B]:.1%} '
         'IRR on a 36-month hold.'),
   stats=[('LP Commitment', f'${COMMON:,.0f}'), ('Preferred Return', f'{CE_PREF:.2%}'),
          ('Residual Split', '50 / 50')])}


def title(t):
    m = META[t]
    sn = {'hm': ('A ten million dollar senior loan, first trust deed, at twelve percent floating and '
                 'interest-only for a three-year term. Forty-six point seven percent of as-is value and '
                 'fifty-seven point five percent of total cost, and the only debt on the asset.'),
          'senior': ('A ten million dollar senior loan, first trust deed, at twelve percent floating and '
                     'interest-only for a three-year term. Forty-six point seven percent of as-is value '
                     'and fifty-seven point five percent of total cost.'),
          'pref': ('A three million nine hundred four thousand dollar preferred equity investment '
                   'accruing at seventeen percent with no current pay and a ten percent participation in '
                   'equity value at exit, behind ten million of senior debt and ahead of five million '
                   'five hundred thousand of common capital.'),
          'common': ('A three million five hundred thousand dollar limited partner investment alongside '
                     'two million of sponsor cash on identical terms, earning a fifteen percent '
                     'cumulative preferred return and capital back before a fifty-fifty residual '
                     'split.')}[t]
    return ('<section data-label="Title" data-screen-label="Title" '
     f'data-speaker-notes="Wylder Hotel Tilghman Island, a fifty-eight key waterfront resort in Talbot '
     f'County, Maryland. {sn} Marcus and Millichap Capital Corporation is the exclusive capital advisor." '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;color:#fff;'
     'font-family:var(--font-body);display:flex;flex-direction:column;justify-content:space-between;'
     'padding:90px 100px;">\n'
     '  <img src="assets/wt-aerial-spring.png" alt="Wylder Hotel Tilghman Island aerial" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,17,34,.74) 0%,'
     'rgba(0,17,34,.46) 42%,rgba(0,17,34,.62) 74%,rgba(0,17,34,.92) 100%);"></div>\n'
     '  <div style="position:absolute;right:0;top:0;bottom:0;width:12px;display:flex;'
     'flex-direction:column;">\n'
     '    <div style="flex:0 0 60%;background:#F0720E;"></div>\n'
     f'    <div style="flex:0 0 40%;background:{m["color"]};"></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.28);padding-bottom:28px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:60px;">\n'
     '    <div style="display:flex;align-items:center;gap:20px;">'
     f'<span style="{CON}font-size:15px;letter-spacing:.26em;color:var(--mm-orange-100);">'
     f'{m["eyebrow"]}</span>'
     '<span style="font-family:var(--font-mono);font-size:15px;font-weight:700;letter-spacing:.08em;'
     'color:rgba(255,255,255,.62);padding-left:20px;border-left:1px solid rgba(255,255,255,.32);">01'
     '</span></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;flex:1;display:flex;flex-direction:column;'
     'justify-content:center;margin-left:-100px;padding:0 150px 0 100px;background:linear-gradient(90deg,'
     'rgba(0,18,40,.82) 0%,rgba(0,18,40,.76) 56%,rgba(0,18,40,.46) 82%,rgba(0,18,40,0) 100%);'
     'max-width:1500px;">\n'
     f'    <div style="{CON}font-size:19px;letter-spacing:.30em;color:var(--mm-orange);'
     f'margin-bottom:24px;">{m["kicker"]}</div>\n'
     f'    <h1 style="{DISP}font-weight:700;font-size:104px;line-height:0.97;letter-spacing:-0.018em;'
     'margin:0;text-shadow:0 2px 30px rgba(0,17,34,.45);">Wylder Hotel<br>Tilghman Island.</h1>\n'
     '    <div style="width:120px;height:3px;background:var(--mm-orange);margin:34px 0 26px;"></div>\n'
     f'    <div style="{DISP}font-style:italic;font-weight:400;font-size:29px;color:#fff;line-height:1.34;'
     f'max-width:1080px;text-shadow:0 2px 20px rgba(0,17,34,.5);">{m["lede"]}</div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:flex-end;border-top:1px solid rgba(255,255,255,.28);padding-top:28px;">\n'
     '    <div>\n'
     f'      <div style="{DISP}font-size:28px;font-weight:700;line-height:1;">Bradley M. Buzil</div>\n'
     f'      <div style="{CON}font-size:15px;letter-spacing:.2em;color:var(--mm-navy-100);'
     'margin-top:8px;">Senior Director &middot; Exclusive Capital Advisor</div>\n    </div>\n'
     '    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:12px;">\n'
     '      <div style="display:flex;flex-direction:column;align-items:center;">\n'
     '        <span style="font-family:var(--font-serif);font-weight:400;font-size:46px;line-height:0.82;'
     'color:#fff;letter-spacing:.01em;">wylder</span>\n'
     '        <span style="width:46px;height:1.5px;background:var(--mm-orange);margin:10px 0 7px;">'
     '</span>\n'
     f'        <span style="{CON}font-size:13px;letter-spacing:.38em;color:#fff;padding-left:.38em;">'
     'Tilghman Island</span>\n      </div>\n'
     f'      <div style="{MONO}font-size:15px;color:var(--mm-navy-100);letter-spacing:.04em;">'
     f'{DATE} &middot; Tilghman Island, MD</div>\n    </div>\n  </div>\n</section>')


OPP = {
 'senior': ('Summary of the senior loan request.',
   f'Marcus &amp; Millichap Capital Corporation is placing a <strong style="color:var(--mm-navy-900);">'
   f'${SENIOR:,.0f} senior loan</strong>, first trust deed, on Wylder Hotel Tilghman Island. The loan is '
   f'{LTV["is"]:.2%} of as-is value and {LTC:.2%} of total cost, interest-only for a {SR_TERM}-year term, '
   f'with a twelve-month interest and carry reserve funded at close. '
   f'<strong style="color:var(--mm-navy-900);">${PREF+COMMON:,.0f} of subordinate capital</strong> closes '
   f'concurrently and ${GP_CASH:,.0f} of sponsor cash is already invested and remains in the deal.',
   [('Senior Loan', f'${SENIOR/1e6:,.2f}M', f'First trust deed &middot; ${SENIOR/KEYS:,.0f} per key', 1),
    ('LTV &middot; As-Is', f'{LTV["is"]:.2%}', f'{LTV["stab"]:.2%} of the stabilized estimate', 0),
    ('Loan to Cost', f'{LTC:.2%}', f'On the ${TOTAL:,.0f} capitalization', 0),
    ('All-In Rate', f'{ALLIN:.2%}', f'SOFR {SOFR:.2%} plus {SPREAD:.2%}, floating', 0),
    ('Term &amp; Amortization', f'{SR_TERM} yr &middot; IO', 'Single advance funded at close', 0),
    ('Debt Yield &middot; 2027', f'{DY[2027]:.2%}', f'{DY[2028]:.2%} in 2028', 0),
    ('DSCR &middot; 2027', f'{DSCR[2027]:.2f}x', f'{DSCR[2028]:.2f}x in 2028 &middot; reserve covers 2026', 0),
    ('Projected Return', f'{SR_MULT[B]:.2f}x', f'{SR_IRR[B]:.1%} IRR &middot; base case, {HOLD}-year hold', 1)]),
 'pref': ('Summary of the preferred equity placement.',
   f'Marcus &amp; Millichap Capital Corporation is placing <strong style="color:var(--mm-navy-900);">'
   f'${PREF:,.0f} of preferred equity</strong> in Wylder Hotel Tilghman Island, accruing at '
   f'{PF_RATE_PIK:.2%} with no current-pay obligation and a {PF_KICKER:.2%} participation in equity value '
   f'at exit. <strong style="color:var(--mm-navy-900);">${SENIOR:,.0f} of senior debt</strong> sits ahead '
   f'of it and <strong style="color:var(--mm-navy-900);">${PARTNERSHIP:,.0f} of common capital</strong> '
   f'stands beneath it, including ${GP_CASH:,.0f} of sponsor cash already invested.',
   [('Commitment', f'${PREF/1e6:,.2f}M', f'${PREF/KEYS:,.0f} per key &middot; funded at close', 1),
    ('Accrual Rate', f'{PF_RATE_PIK:.2%}', 'Compounding &middot; no current pay', 0),
    ('Exit Participation', f'{PF_KICKER:.2%}', 'Of equity value at exit', 0),
    ('Senior Debt Ahead', f'${SENIOR/1e6:,.2f}M', f'{LTV["is"]:.2%} of as-is value', 0),
    ('Debt &amp; Preferred to Value', f'{(SENIOR+PREF)/VAL["is"]:.2%}', 
     f'{(SENIOR+PREF)/VAL["stab"]:.2%} of the stabilized estimate', 0),
    ('Capital Beneath', f'${PARTNERSHIP/1e6:,.2f}M', f'Including ${GP_CASH:,.0f} of sponsor cash', 0),
    ('Last-Dollar Exposure', f'${(SENIOR+PREF)/KEYS:,.0f}', 'Per key, on 58 keys', 0),
    ('Projected Return', f'{PF_MULT[B]:.2f}x', f'{PF_IRR[B]:.1%} IRR &middot; base case, {HOLD}-year hold', 1)]),
 'common': ('Summary of the common equity placement.',
   f'Marcus &amp; Millichap Capital Corporation is placing a <strong style="color:var(--mm-navy-900);">'
   f'${COMMON:,.0f} limited partner investment</strong> in Wylder Hotel Tilghman Island, alongside '
   f'<strong style="color:var(--mm-navy-900);">${GP_CASH:,.0f} of sponsor cash on identical pari passu '
   f'terms</strong>. The LP earns a {CE_PREF:.2%} cumulative preferred return and its capital back in '
   f'full before any residual is split 50/50. The GP holds a 51% ownership interest and takes no '
   'distribution until the LP has been paid.',
   [('LP Commitment', f'${COMMON/1e6:,.2f}M', f'${COMMON/KEYS:,.0f} per key &middot; funded at close', 1),
    ('Partnership Capital', f'${PARTNERSHIP/1e6:,.2f}M', 
     f'LP ${COMMON/1e6:,.2f}M plus ${GP_CASH/1e6:,.2f}M sponsor cash', 0),
    ('Preferred Return', f'{CE_PREF:.2%}', 'Cumulative &middot; LP and GP pari passu', 0),
    ('Residual Split', '50 / 50', 'After the preferred return and capital', 0),
    ('Ownership &middot; GP / LP', '51% / 49%', 'GP takes nothing until the LP is paid', 0),
    ('Senior &amp; Preferred Ahead', f'${SENIOR+PREF:,.0f}'.replace('$13,904,044','$13.90M'),
     f'{(SENIOR+PREF)/VAL["is"]:.2%} of as-is value', 0),
    ('Adjacent Parcel Value', '$2.89M', '$4.29M of value on $1.40M of cost', 0),
    ('Projected Return', f'{LP_MULT[B]:.2f}x', f'{LP_IRR[B]:.1%} IRR &middot; base case, {HOLD}-year hold', 1)])}


def opportunity(t):
    h, lede, items = OPP[t]
    sn = {'hm': ('Ten million dollar senior loan, forty-six point seven percent of as-is value and '
                 'fifty-seven point five percent of cost, at twelve percent all-in, interest-only for '
                 'three years. Debt yield is twenty-three percent on year-two net operating income and '
                 'coverage is one point nine three times, rising to two point two three times in twenty '
                 'twenty-eight. The twelve-month reserve covers the renovation year. Nine million four '
                 'hundred four thousand of capital stands beneath the loan, forty-eight point nine '
                 'percent of total basis.'),
          'senior': ('Ten million dollar senior loan, forty-six point seven percent of as-is value and '
                     'fifty-seven point five percent of cost, at twelve percent all-in, interest-only '
                     'for three years. Debt yield is twenty-three percent on year-two net operating '
                     'income and coverage is one point nine three times, rising to two point two three '
                     'times in twenty twenty-eight. The twelve-month reserve covers the renovation year. '
                     'Seven million four hundred four thousand of subordinate capital closes beneath the '
                     'loan. Projected one point four eight times and fifteen point six percent.'),
          'pref': ('Three million nine hundred four thousand of preferred equity accruing at seventeen '
                   'percent with no current pay, plus a ten percent participation in equity value at '
                   'exit. Ten million of senior debt sits ahead; five million five hundred thousand of '
                   'common capital stands beneath, including two million of sponsor cash. Debt and '
                   'preferred are sixty-five percent of as-is value and forty-seven percent of the '
                   'stabilized estimate. Last-dollar exposure is two hundred thirty-nine thousand seven '
                   'hundred twenty-five per key. Projected one point nine seven times and thirty-one '
                   'point five percent.'),
          'common': ('Three million five hundred thousand from the LP alongside two million of sponsor '
                     'cash on identical pari passu terms, a five million five hundred thousand dollar '
                     'partnership. Fifteen percent cumulative preferred return, capital back in full, '
                     'then a fifty-fifty residual split. The GP holds fifty-one percent of the ownership '
                     'and takes nothing until the LP has been paid. Thirteen point nine million of senior '
                     'and preferred capital sits ahead of the partnership. Projected two point three '
                     'three times and thirty-two point six percent.')}[t]
    return ('<section data-label="The Opportunity" data-screen-label="The Opportunity" '
     f'data-speaker-notes="{sn}" ' + sec(pad='64px 88px 44px') + '>\n'
     + h2(h, fs='48px', mb='0', pb='18px')
     + f'  <p style="{BODY}max-width:none;font-size:21px;line-height:1.5;color:var(--ink-700);'
       f'margin:22px 0 6px;">{lede}</p>\n'
     + '  <div style="display:grid;grid-template-columns:repeat(4,1fr);flex:1;'
       'font-variant-numeric:tabular-nums;">\n' + tiles(items) + '  </div>\n@@FOOTER@@\n</section>')


def contact(t):
    m = META[t]
    sn = ('The model, historical operating statements, the purchase and sale agreement on the adjacent '
          'parcel and sponsor materials are available on request. Bradley M. Buzil, Senior Director, '
          'The TRANCHE Group at Marcus and Millichap Capital Corporation.')
    st = ''
    for i, (lab, val) in enumerate(m['stats']):
        pad = ('18px 40px 0 0' if i == 0 else ('18px 40px 0' if i == 1 else '18px 0 0 40px'))
        bl = '' if i == 0 else 'border-left:1px solid rgba(255,255,255,.2);'
        lc = 'var(--mm-orange-100)' if i == 2 else 'var(--mm-navy-100)'
        vc = 'var(--mm-orange)' if i == 2 else '#fff'
        st += (f'      <div style="padding:{pad};{bl}">'
               f'<div style="{CON}font-size:13px;letter-spacing:.18em;color:{lc};">{lab}</div>'
               f'<div style="{MONO}font-size:26px;font-weight:700;color:{vc};margin-top:6px;">{val}'
               '</div></div>\n')
    return ('<section data-label="Next Steps" data-screen-label="Contact" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;color:#fff;'
     'font-family:var(--font-body);display:flex;flex-direction:column;justify-content:space-between;'
     'padding:88px 100px;">\n'
     '  <img src="assets/wt-aerial.png" alt="Wylder Hotel Tilghman Island aerial" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,17,34,.86) 0%,'
     'rgba(0,17,34,.66) 45%,rgba(0,17,34,.92) 100%);"></div>\n'
     '  <div style="position:absolute;left:0;right:0;top:0;height:14px;display:flex;">'
     '<div style="flex:0 0 60%;background:#F0720E;"></div>'
     f'<div style="flex:0 0 40%;background:{m["color"]};"></div></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;padding-top:16px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:56px;">\n'
     '    <div style="display:flex;align-items:center;gap:20px;">'
     f'<span style="{CON}font-size:15px;letter-spacing:.26em;color:var(--mm-orange-100);">'
     f'{m["eyebrow"]}</span>'
     '<span style="font-family:var(--font-mono);font-size:15px;font-weight:700;letter-spacing:.08em;'
     'color:rgba(255,255,255,.62);padding-left:20px;border-left:1px solid rgba(255,255,255,.32);">28'
     '</span></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;max-width:1220px;">\n'
     f'    <h2 style="{DISP}font-weight:700;font-size:72px;line-height:1.02;letter-spacing:-0.015em;'
     'margin:0 0 26px;text-shadow:0 2px 24px rgba(0,17,34,.5);">Contact and next steps.</h2>\n'
     f'    <p style="{BODY}font-size:25px;line-height:1.55;color:#fff;margin:0 0 26px;max-width:90ch;'
     'text-shadow:0 1px 12px rgba(0,17,34,.4);">The financial model, historical operating statements, the '
     'purchase and sale agreement on the adjacent parcel and sponsor materials are available on '
     'request.</p>\n'
     '    <div style="display:flex;gap:0;border-top:1px solid rgba(255,255,255,.28);'
     f'font-variant-numeric:tabular-nums;">\n{st}    </div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:flex-end;border-top:1px solid rgba(255,255,255,.28);padding-top:28px;">\n'
     '    <div style="display:flex;align-items:center;gap:26px;">\n'
     '      <img src="assets/buzil.jpg" alt="Bradley M. Buzil" style="width:104px;height:104px;'
     'object-fit:cover;border-radius:2px;border:1px solid rgba(255,255,255,.35);flex:0 0 auto;">\n'
     '      <div>\n'
     f'        <div style="{DISP}font-size:36px;font-weight:700;line-height:1;">Bradley M. Buzil</div>\n'
     f'        <div style="{CON}font-size:15px;letter-spacing:.2em;color:var(--mm-navy-100);'
     'margin:10px 0 14px;">Senior Director &middot; The TRANCHE Group</div>\n'
     f'        <div style="display:flex;gap:26px;{MONO}font-size:19px;color:#fff;letter-spacing:.02em;">\n'
     '          <span>310.909.5473</span>\n'
     '          <span>bradley.buzil@marcusmillichap.com</span>\n        </div>\n'
     f'        <div style="{CON}font-size:13px;letter-spacing:.18em;color:var(--mm-navy-300);'
     'margin-top:12px;">CA DRE Lic. 01927157</div>\n      </div>\n    </div>\n'
     '    <div style="text-align:right;">\n'
     f'      <div style="{CON}font-size:14px;letter-spacing:.22em;color:var(--mm-navy-100);">'
     'Marcus &amp; Millichap Capital Corporation</div>\n'
     f'      <div style="{MONO}font-size:15px;color:var(--mm-navy-100);letter-spacing:.04em;'
     f'margin-top:10px;">Exclusive Capital Advisor &middot; {m["label"]}</div>\n'
     '    </div>\n  </div>\n</section>' + TAIL)


# ═══════════════════════════════════════════════════════════ shared table helper
def tbl(cols, rows_, fs='16px', pad=13, lw='1.5fr'):
    """cols: list of header strings (first is the stub). rows_: (label, [vals], kind)."""
    g = (f'    <div style="display:grid;grid-template-columns:{lw} repeat({len(cols)-1},1fr);'
         'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(cols):
        al = '' if i == 0 else 'text-align:right;'
        bl = '' if i == 0 else f'border-left:{HAIR};'
        pd = '12px 4px 12px 0' if i == 0 else '12px 8px'
        cc = 'var(--ink-500)' if i == 0 else 'var(--mm-navy)'
        g += (f'      <div style="padding:{pd};border-bottom:{NAVY2};{bl}{CON}font-size:13.5px;'
              f'letter-spacing:.12em;color:{cc};{al}">{c}</div>\n')
    for lab, vals, kind in rows_:
        bb = {'': HAIR, 'sub': NAVY2, 'tot': '3px double var(--mm-navy)'}[kind]
        lw_ = 'font-weight:600;color:var(--ink-900);' if kind else 'color:var(--ink-700);'
        g += (f'      <div style="padding:{pad}px 4px {pad}px 0;border-bottom:{bb};{BODY}font-size:{fs};'
              f'{lw_}">{lab}</div>\n')
        for v in vals:
            vc = 'var(--mm-navy)' if kind == 'sub' else ('var(--mm-orange)' if kind == 'tot'
                                                         else 'var(--ink-900)')
            fw = 'font-weight:700;' if kind else ''
            g += (f'      <div style="padding:{pad}px 8px;border-bottom:{bb};border-left:{HAIR};{MONO}'
                  f'font-size:{fs};text-align:right;color:{vc};{fw}">{v}</div>\n')
    return g + '    </div>\n'


def darkpage(label, title_, sn, cols, blocks, pad='74px 96px 56px'):
    return (f'<section data-label="{label}" data-screen-label="{label}" data-speaker-notes="{sn}" '
     + sec(dark=True, pad=pad) + '>\n' + h2(title_, dark=True, fs='46px', mb='34px', pb='22px')
     + '  <div style="display:grid;grid-template-columns:repeat(3,1fr);flex:1;min-height:0;">\n'
     + cols + '  </div>\n'
     + f'  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:34px;'
       f'padding-top:28px;border-top:{DRULE};">\n' + blocks + '  </div>\n@@FOOTER@@\n</section>')


# ═══════════════════════════════════════════════════════════ SENIOR DEBT
def senior_terms():
    c = (bigcol('Loan Amount', f'${SENIOR/1e6:,.1f}M', f'${SENIOR/KEYS:,.0f} per key',
          dkv('Gross loan amount', f'${SENIOR:,.0f}')
          + dkv('Origination fee', '2.00%')
          + dkv('Interest and carry reserve', f'${SR_RESERVE:,.0f}')
          + dkv('Net proceeds at close', f'${SR_NET:,.0f}', accent=True, last=True), 'first')
     + bigcol('All-In Rate', f'{ALLIN:.2%}', f'SOFR plus {SPREAD:.2%}, floating',
          dkv('Index &middot; SOFR', f'{SOFR:.2%}')
          + dkv('Spread', f'{SPREAD:.2%}')
          + dkv('Annual debt service', f'${SR_ADS:,.0f}')
          + dkv('Amortization', 'Interest-only', accent=True, last=True), 'mid')
     + bigcol('Term', f'{SR_TERM} years', 'Exit at the end of year three',
          dkv('Collateral', 'First trust deed')
          + dkv('Funding', 'Single advance at close')
          + dkv('Loan to cost', f'{LTC:.2%}')
          + dkv('Exit participation', f'{SR_KICKER:.2%}', accent=True, last=True), 'last'))
    b = (blk('Position', f'The loan is the only debt on the asset and is secured by a first trust deed. '
             f'${PREF+COMMON:,.0f} of subordinate capital funds concurrently at close and '
             f'${GP_CASH:,.0f} of sponsor cash is already invested, giving a '
             f'{(PREF+COMMON+GP_CASH)/COST_BASIS:.1%} cushion beneath the loan on total basis.')
     + blk('Reserve and Carry', f'A ${SR_RESERVE:,.0f} interest and carry reserve &mdash; twelve months '
           'of debt service &mdash; is funded from the capitalization at close and covers the renovation '
           'period in full, before the asset reopens under the brand.')
     + blk('Participation', f'The lender participates in {SR_KICKER:.2%} of equity value at exit, paid '
           'from sale proceeds after the principal is repaid. The projected return on page 22 includes '
           'it at every exit value shown.'))
    sn = ('Senior loan terms. Ten million dollars, gross, less a two percent origination fee and a one '
          'million two hundred thousand dollar interest and carry reserve, for eight million six hundred '
          'thousand of net proceeds at close. All-in rate twelve percent: SOFR at three point seven nine '
          'plus an eight point two one spread, floating, interest-only, one million two hundred thousand '
          'of annual debt service. Three-year term, first trust deed, single advance, fifty-seven point '
          'five percent of cost, with a five percent participation in equity value at exit.')
    return darkpage('Senior Loan Terms', 'Terms of the senior loan.', sn, c, b)


def senior_coverage():
    yrs = [p[0] for p in PRO]
    noi = {p[0]: p[5] for p in PRO}
    rev = {p[0]: p[4] for p in PRO}
    left = (sub('Coverage and Leverage by Year')
     + tbl(['Measure'] + [str(y) for y in yrs],
       [('Total revenue', [f'${rev[y]:,.0f}' for y in yrs], ''),
        ('Net operating income', [f'${noi[y]:,.0f}' for y in yrs], 'sub'),
        ('Senior debt service &middot; interest-only', [f'${SR_ADS:,.0f}' for y in yrs], ''),
        ('Cash flow after debt service', [f'${noi[y]-SR_ADS:,.0f}' for y in yrs], ''),
        ('Debt service coverage', [f'{DSCR[y]:.2f}x' for y in yrs], 'sub'),
        ('Debt yield', [f'{DY[y]:.2%}' for y in yrs], 'sub'),
        ('Occupancy', [f'{p[1]:.0%}' for p in PRO], ''),
        ('Average daily rate', [f'${p[2]:,.0f}' for p in PRO], ''),
        ('RevPAR', [f'${p[3]:,.0f}' for p in PRO], 'sub')], pad=11)
     + para(f'2026 is the renovation year: the asset is down for the program and coverage is '
            f'{DSCR[2026]:.2f}x. The ${SR_RESERVE:,.0f} interest and carry reserve funded at close pays '
            'twelve months of debt service in full, so '
            + ('the shortfall is pre-funded and does not depend on operations. '
               if DSCR[2026] < 1 else
               'the renovation year does not depend on operations at all. ')
            + f'Coverage reaches {DSCR[2027]:.2f}x in the first full year after reopening.',
            fs='15px', auto=True))
    right = (sub('Leverage Against Estimated Value')
     + tbl(['Stage', 'Value', 'Per Key', 'Senior LTV'],
       [('As-is', [f'${VAL["is"]/1e6:,.1f}M', f'${VAL["is"]/KEYS:,.0f}', f'{LTV["is"]:.2%}'], ''),
        ('Upon completion &middot; April 2027',
         [f'${VAL["complete"]/1e6:,.1f}M', f'${VAL["complete"]/KEYS:,.0f}', f'{LTV["complete"]:.2%}'], ''),
        ('Upon stabilization &middot; April 2029',
         [f'${VAL["stab"]/1e6:,.1f}M', f'${VAL["stab"]/KEYS:,.0f}', f'{LTV["stab"]:.2%}'], 'sub')],
       fs='15.5px', pad=11, lw='1.7fr')
     + '      <div style="height:18px;"></div>\n'
     + sub('Permanent Takeout Test')
     + tbl(['Measure'] + [str(y) for y in yrs],
       [('Indicative permanent rate', [f'{PERM_RATE:.2%}' for y in yrs], ''),
        ('Annual debt service &middot; 30-yr amortizing', [f'${PERM_ADS:,.0f}' for y in yrs], ''),
        ('Coverage on the permanent loan', [f'{PERM_DSCR[y]:.2f}x' for y in yrs], 'sub')],
       fs='15.5px', pad=11, lw='1.7fr')
     + '      <div style="height:16px;"></div>\n'
     + '      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Debt Yield · 2027', f'{DY[2027]:.2%}', 'On year-two NOI', pad='14px 14px 0 0')
     + stat('DSCR · 2028', f'{DSCR[2028]:.2f}x', 'Stabilizing year', pad='14px 14px 0 14px',
            vc='var(--mm-orange)')
     + stat('LTV · Stabilized', f'{LTV["stab"]:.2%}', 'On the estimate', br=False, pad='14px 0 0 14px')
     + '      </div>\n'
     + para(f'The loan is sized so that a conventional permanent takeout clears comfortably: at an '
            f'indicative {PERM_RATE:.2%} on a 30-year amortizing basis, debt service is ${PERM_ADS:,.0f} '
            f'and coverage is {PERM_DSCR[2027]:.2f}x on 2027 cash flow. Estimated values are for '
            'underwriting and exclude the adjacent Dogwood Cove parcel.', fs='15px', auto=True))
    sn = (f'Coverage and leverage on a ${SENIOR:,} request. Twenty twenty-six is the renovation year, '
          f'so coverage is {DSCR[2026]:.2f} times and the twelve-month reserve funded at close pays debt '
          f'service in full. Coverage is {DSCR[2027]:.2f} times in twenty twenty-seven and '
          f'{DSCR[2028]:.2f} times in twenty twenty-eight, with debt yield at {DY[2027]:.2%} and '
          f'{DY[2028]:.2%}. Senior leverage falls from {LTV["is"]:.2%} of as-is value to '
          f'{LTV["stab"]:.2%} of the stabilized estimate. On a conventional permanent takeout at six '
          f'point five percent, thirty-year amortizing, coverage is {PERM_DSCR[2027]:.2f} times on '
          'twenty twenty-seven cash flow.')
    return ('<section data-label="Debt Service Coverage" data-screen-label="Debt Service Coverage" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 40px') + '>\n'
     + h2('Coverage, debt yield and leverage.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1fr 1fr;gap:46px;flex:1;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ═══════════════════════════════════════════════════════════ returns pages (one per tranche)
RET = {
 'senior': dict(
   label='Senior loan', title='Senior loan return across exit values.', idx=list(range(7)),
   mult=SR_MULT, irr=SR_IRR, cash=SR_CASH, profit=SR_PROFIT, basis=SR_BASIS,
   extra=[('Principal repaid at exit', [f'${SENIOR:,.0f}'] * 7),
          ('Interest received over the term', [f'${SR_INT_3Y:,.0f}'] * 7),
          (f'Exit participation &middot; {SR_KICKER:.2%}', [f'${v:,.0f}' for v in SR_KICK]),
          ('Senior loan to exit value', [f'{v:.2%}' for v in SR_EXIT_LTV])],
   stats=[('Base-Case Multiple', f'{SR_MULT[B]:.2f}x', f'${BASE_EXIT/1e6:,.0f}M exit'),
          ('Base-Case IRR', f'{SR_IRR[B]:.1%}', f'{HOLD}-year hold'),
          ('Net Funded Basis', f'${SR_BASIS:,.0f}', 'Gross loan less the fee'),
          ('Total Cash Received', f'${SR_CASH[B]:,.0f}', 'Principal, interest, participation')],
   note=(f'Return is measured on the <strong style="color:var(--mm-navy-900);">${SR_BASIS:,.0f} net '
         f'funded basis</strong> &mdash; the ${SENIOR:,.0f} gross loan less the 2.00% origination fee. '
         f'Cash received is the principal, ${SR_INT_3Y:,.0f} of interest over the {SR_TERM}-year term and '
         f'the {SR_KICKER:.2%} participation in equity value at exit. The participation is the only '
         'variable: principal and interest are unchanged at every exit value shown, and the loan is '
         f'repaid in full at the lowest value on the page, where senior leverage is '
         f'{SR_EXIT_LTV[0]:.2%} of gross proceeds.')),
 'pref': dict(
   label='Preferred equity', title='Preferred equity return across exit values.', idx=list(range(7)),
   mult=PF_MULT, irr=PF_IRR, cash=PF_CASH, profit=PF_PROFIT, basis=PF_BASIS,
   extra=[('Cash swept over the term', [f'${PF_SWEEP_3Y:,.0f}'] * 7),
          ('Accrued balance repaid at exit', [f'${PF_DUE_AT_EXIT:,.0f}'] * 7),
          (f'Exit participation &middot; {PF_KICKER:.2%}', [f'${v:,.0f}' for v in PF_KICK]),
          ('Last-dollar exposure to exit value', [f'{v:.2%}' for v in PF_LAST_DOLLAR])],
   stats=[('Base-Case Multiple', f'{PF_MULT[B]:.2f}x', f'${BASE_EXIT/1e6:,.0f}M exit'),
          ('Base-Case IRR', f'{PF_IRR[B]:.1%}', f'{HOLD}-year hold'),
          ('Net Funded Basis', f'${PF_BASIS:,.0f}', 'Commitment less the fee'),
          ('Total Cash Received', f'${PF_CASH[B]:,.0f}', 'Sweep, balance, participation')],
   note=(f'Return is measured on the <strong style="color:var(--mm-navy-900);">${PF_BASIS:,.0f} net '
         f'funded basis</strong> &mdash; the ${PREF:,.0f} commitment less the 2.00% origination fee. '
         f'Cash received is ${PF_SWEEP_3Y:,.0f} swept against the balance over the term, the '
         f'${PF_DUE_AT_EXIT:,.0f} accrued balance repaid at exit and the {PF_KICKER:.2%} participation '
         'in equity value at exit. The participation is the only variable: the sweep and the accrued '
         'balance are unchanged at every exit value shown. Last-dollar exposure is the senior and '
         'preferred capital as a share of gross exit value.')),
 'common': dict(
   label='LP', title='Limited partner return across exit values.', idx=list(range(1, 7)),
   mult=LP_MULT, irr=LP_IRR, cash=LP_CASH, profit=LP_PROFIT, basis=LP_BASIS,
   extra=[('Residual to the partnership', [f'${v:,.0f}' for v in CE_RESID]),
          ('LP share of partnership cash', [f'{LP_CASH[i]/CE_RESID[i]:.1%}' for i in range(7)]),
          ('GP &mdash; total cash received', [f'${v:,.0f}' for v in GP_CASH_OUT]),
          ('GP &mdash; equity multiple', [f'{v:.2f}x' for v in GP_MULT])],
   stats=[('Base-Case LP Multiple', f'{LP_MULT[B]:.2f}x', f'${BASE_EXIT/1e6:,.0f}M exit'),
          ('Base-Case LP IRR', f'{LP_IRR[B]:.1%}', f'{HOLD}-year hold'),
          ('LP Capital', f'${LP_BASIS:,.0f}', f'{COMMON/PARTNERSHIP:.2%} of the partnership'),
          ('Total LP Cash Received', f'${LP_CASH[B]:,.0f}', 'Preferred, capital, residual')],
   note=(f'Return is measured on the <strong style="color:var(--mm-navy-900);">${LP_BASIS:,.0f} LP '
         f'commitment</strong>. Cash received is the {CE_PREF:.2%} cumulative preferred return, return of '
         'capital in full and the LP half of the residual, in that order &mdash; the waterfall is on '
         f'page 21. The GP columns are shown for alignment: the GP earns its {GP_MULT[B]:.2f}x only after '
         'the LP has been paid its preferred return and its capital back, and it has '
         f'${GP_CASH:,.0f} of its own cash in the same position.'))}


def returns_page(t):
    r = RET[t]
    g = returns_grid(r['label'], r['idx'], r['mult'], r['irr'], r['cash'], r['profit'],
                     extra_rows=r['extra'])
    st = ''
    for i, (lab, val, nt) in enumerate(r['stats']):
        last = (i == len(r['stats']) - 1)
        pad = '16px 20px 0 0' if i == 0 else ('16px 0 0 20px' if last else '16px 20px 0 20px')
        st += stat(lab, val, nt, br=not last, pad=pad,
                   vc=('var(--mm-orange)' if i < 2 else None), vfs='28px')
    lo, hi = EXITS[r['idx'][0]], EXITS[r['idx'][-1]]
    sn = {'senior': ('Senior loan return across exit values from eighteen to thirty-six million. The base '
                     'case is a thirty million dollar exit: one point four eight times and fifteen point '
                     'six percent on a nine million eight hundred thousand dollar net funded basis. '
                     'Principal and three million six hundred thousand of interest are fixed; only the '
                     'five percent participation varies.'),
          'pref': ('Preferred equity return across exit values from eighteen to thirty-six million. The '
                   'base case is a thirty million dollar exit: one point nine seven times and thirty-one '
                   'point five percent on a three million eight hundred twenty-five thousand nine hundred '
                   'sixty-three dollar net funded basis. The sweep and the accrued balance are fixed; '
                   'only the ten percent participation varies.'),
          'common': ('Limited partner return across exit values from twenty-one to thirty-six million. '
                     'The base case is a thirty million dollar exit: two point three three times and '
                     'thirty-two point six percent on three million five hundred thousand of LP capital, '
                     'eight million one hundred sixty-four thousand eight hundred twenty-three dollars of '
                     'cash. The general partner columns are shown for alignment and are earned only after '
                     'the LP preferred return and capital are paid in full.')}[t]
    return (f'<section data-label="Returns" data-screen-label="Returns" data-speaker-notes="{sn}" '
     + sec(pad='56px 92px 42px') + '>\n'
     + h2(r['title'], fs='42px', mb='6px', pb='15px')
     + f'  <div style="{CON}font-size:13px;letter-spacing:.2em;color:var(--mm-orange);'
       f'margin:0 0 14px;">For the {META[t]["label"].lower()} investor &middot; not for distribution'
       '</div>\n'
     + g
     + f'  <div style="display:grid;grid-template-columns:repeat(4,1fr);align-items:start;'
       f'border-top:{NAVY2};margin-top:20px;">\n' + st + '  </div>\n'
     + f'  <p style="{BODY}max-width:none;font-size:15px;line-height:1.5;color:var(--ink-500);'
       f'margin:16px 0 0;">{r["note"]} Exit values span ${lo/1e6:,.0f}M to ${hi/1e6:,.0f}M on a '
       f'{SELL_COST:.1%} cost of sale and a {HOLD}-year hold. Implied cap rates are on year-three net '
       'operating income.</p>\n@@FOOTER@@\n</section>')


def senior_credit():
    beneath = PREF + COMMON + GP_CASH
    c = (bigcol('Capital Beneath the Loan', f'${(PREF+COMMON)/1e6:,.2f}M',
          f'Plus ${GP_CASH:,.0f} of sponsor cash already invested',
          dkv('Subordinate capital at close', f'${PREF+COMMON:,.0f}')
          + dkv('Sponsor cash invested', f'${GP_CASH:,.0f}')
          + dkv('Total beneath the loan', f'${beneath:,.0f}')
          + dkv('Share of total basis', f'{beneath/COST_BASIS:.2%}', accent=True, last=True),
          'first', fs='70px')
     + bigcol('Loan to Stabilized Value', f'{LTV["stab"]:.2%}', 'On the April 2029 estimate',
          dkv('As-is', f'{LTV["is"]:.2%}')
          + dkv('Upon completion', f'{LTV["complete"]:.2%}')
          + dkv('Upon stabilization', f'{LTV["stab"]:.2%}')
          + dkv('Loan per key &middot; 58 keys', f'${SENIOR/KEYS:,.0f}', accent=True, last=True),
          'mid', fs='70px')
     + bigcol('Coverage at the Lowest Exit Shown', f'{NET_PROCEEDS[0]/SENIOR:.2f}x',
          f'Net proceeds to principal at a ${EXITS[0]/1e6:,.0f}M sale',
          dkv('Gross exit value', f'${EXITS[0]:,.0f}')
          + dkv('Net of a 4.0% cost of sale', f'${NET_PROCEEDS[0]:,.0f}')
          + dkv('Senior principal', f'${SENIOR:,.0f}')
          + dkv('Proceeds to principal', f'{NET_PROCEEDS[0]/SENIOR:.2f}x', accent=True, last=True),
          'last', fs='70px'))
    b = (blk('Renovation Risk', f'The ${3_003_000:,.0f} program is funded in full at close, with '
             f'${258_000:,.0f} of contingency inside it, and the twelve-month interest and carry reserve '
             'pays debt service through completion. The schedule by trade is on page 9.')
     + blk('Ramp and Seasonality', f'Coverage is {DSCR[2026]:.2f}x in the renovation year and '
           f'{DSCR[2027]:.2f}x in the first full year of operation. The business plan targets 83% of '
           'market RevPAR at stabilization, a level still below the competitive average on page 16.')
     + blk('Brand and Management', 'The asset operates under the Wylder brand with the sponsor as '
           'operator. The brand resume and the affiliation terms are on pages 7 and 10, and historical '
           'operating results are on page 15.'))
    sn = ('Credit considerations. Seven million four hundred four thousand of subordinate capital closes '
          'beneath the loan and two million of sponsor cash is already invested, nine million four hundred '
          'four thousand in total, forty-eight point nine percent of the nineteen million two hundred '
          'forty-seven thousand dollar basis. Leverage falls from forty-six point seven percent of as-is '
          'value to thirty-three point nine percent of the stabilized estimate. Even at an eighteen '
          'million dollar sale, net proceeds cover principal one point seven three times. The renovation '
          'is fully funded with contingency and the reserve pays debt service through completion.')
    return darkpage('Credit Considerations', 'Credit considerations and downside coverage.', sn, c, b)


# ═══════════════════════════════════════════════════════════ PREFERRED EQUITY
def pref_terms():
    c = (bigcol('Commitment', f'${PREF/1e6:,.2f}M', f'${PREF/KEYS:,.0f} per key',
          dkv('Commitment', f'${PREF:,.0f}')
          + dkv('Origination fee', '2.00%')
          + dkv('Net funded at close', f'${PF_NET:,.0f}')
          + dkv('Share of capitalization', f'{PREF/TOTAL:.2%}', accent=True, last=True), 'first')
     + bigcol('Accrual Rate', f'{PF_RATE_PIK:.2%}', 'Compounding &middot; no current pay',
          dkv('Current pay', 'None')
          + dkv('Cash sweep', 'Against the balance')
          + dkv('Accrued balance at exit', f'${PF_DUE_AT_EXIT:,.0f}')
          + dkv('Term', f'{HOLD} years', accent=True, last=True), 'mid')
     + bigcol('Exit Participation', f'{PF_KICKER:.2%}', 'Of equity value at exit',
          dkv('Priority', 'Behind the senior loan')
          + dkv('Capital beneath', f'${PARTNERSHIP:,.0f}')
          + dkv('Last-dollar to as-is value', f'{(SENIOR+PREF)/VAL["is"]:.2%}')
          + dkv('Last-dollar per key', f'${(SENIOR+PREF)/KEYS:,.0f}', accent=True, last=True), 'last'))
    b = (blk('Priority', f'The preferred sits behind a single ${SENIOR:,.0f} senior loan and ahead of all '
             f'common capital. ${PARTNERSHIP:,.0f} of common capital funds beneath it at close, including '
             f'${GP_CASH:,.0f} of sponsor cash that stays in the deal.')
     + blk('Sweep Mechanics', 'There is no current-pay obligation. Property cash flow available after '
           'senior debt service sweeps against the preferred balance, reducing it in every year of the '
           'term. The roll-forward is on page 21.')
     + blk('Participation', f'The preferred participates in {PF_KICKER:.2%} of equity value at exit, paid '
           'from sale proceeds after the senior principal is repaid and alongside the return of the '
           'accrued balance. The projected return on page 22 includes it at every exit value shown.'))
    sn = ('Preferred equity terms. Three million nine hundred four thousand dollar commitment, less a two '
          'percent origination fee, three million eight hundred twenty-five thousand nine hundred '
          'sixty-three funded at close, twenty-two point four percent of the capitalization. Accruing at '
          'seventeen percent, compounding, with no current pay; property cash flow sweeps against the '
          'balance, leaving one million nine hundred thirty-one thousand six hundred sixty-six accrued at '
          'exit. Ten percent participation in equity value at exit. Last-dollar exposure is sixty-five '
          'percent of as-is value, two hundred thirty-nine thousand seven hundred twenty-five per key.')
    return darkpage('Preferred Equity Terms', 'Terms of the preferred equity.', sn, c, b)


def pref_sweep():
    yrs = [p[0] for p in PRO]
    noi = {p[0]: p[5] for p in PRO}
    res = {2026: SR_RESERVE, 2027: 0, 2028: 0}
    left = (sub('Cash Available to Sweep')
     + tbl(['Source'] + [str(y) for y in yrs],
       [('Net operating income', [f'${noi[y]:,.0f}' for y in yrs], ''),
        ('Senior debt service', [f'(${SR_ADS:,.0f})' for y in yrs], ''),
        ('Funded from the interest and carry reserve',
         [f'${res[y]:,.0f}' if res[y] else '&mdash;' for y in yrs], ''),
        ('Cash available to the preferred', [f'${r[3]:,.0f}' for r in PF_SCHED], 'sub')], pad=13)
     + '      <div style="height:18px;"></div>\n'
     + sub('Operating Build')
     + tbl(['Measure'] + [str(y) for y in yrs],
       [('Occupancy', [f'{p[1]:.0%}' for p in PRO], ''),
        ('Average daily rate', [f'${p[2]:,.0f}' for p in PRO], ''),
        ('RevPAR', [f'${p[3]:,.0f}' for p in PRO], ''),
        ('Total revenue', [f'${p[4]:,.0f}' for p in PRO], ''),
        ('Net operating income', [f'${p[5]:,.0f}' for p in PRO], 'sub')], fs='15.5px', pad=11)
     + para(f'2026 is the renovation year. Senior debt service is paid from the interest and carry '
            f'reserve funded at close, so the full ${PF_SCHED[0][3]:,.0f} of net operating income is '
            'available to sweep against the preferred balance in year one.', fs='15px', auto=True))
    rows_ = []
    for yr, beg, pik, sweep, end in PF_SCHED:
        rows_.append((f'Year {yr} &middot; {2025 + yr}',
                      [f'${beg:,.0f}', f'${pik:,.0f}', f'(${sweep:,.0f})', f'${end:,.0f}'], ''))
    rows_.append(('Accrued balance repaid at exit',
                  ['&mdash;', '&mdash;', '&mdash;', f'${PF_DUE_AT_EXIT:,.0f}'], 'sub'))
    right = (sub('Preferred Balance Roll-Forward')
     + tbl(['Period', 'Beginning', f'Accrued {PF_RATE_PIK:.2%}', 'Swept', 'Ending'], rows_,
           fs='15px', pad=15, lw='1.3fr')
     + '      <div style="height:16px;"></div>\n'
     + '      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Total Swept', f'${PF_SWEEP_3Y:,.0f}', f'Over the {HOLD}-year term', pad='14px 14px 0 0',
            vc='var(--mm-orange)')
     + stat('Balance at Exit', f'${PF_DUE_AT_EXIT:,.0f}',
            f'{PF_DUE_AT_EXIT/PREF:.0%} of the commitment', pad='14px 14px 0 14px')
     + stat('Balance Reduction', f'{1-PF_DUE_AT_EXIT/PREF:.0%}', 'From sweep over the term', br=False,
            pad='14px 0 0 14px')
     + '      </div>\n'
     + para(f'The sweep reduces the preferred balance from ${PREF:,.0f} at close to '
            f'${PF_DUE_AT_EXIT:,.0f} at exit &mdash; a {1-PF_DUE_AT_EXIT/PREF:.0%} reduction &mdash; '
            f'even though the position accrues at {PF_RATE_PIK:.2%} throughout and carries no '
            'current-pay obligation. Cash flow detail is on pages 12 and 13.',
            fs='15px', auto=True))
    sn = ('The cash sweep and the preferred balance. In twenty twenty-six, senior debt service is paid '
          'from the reserve funded at close, so the full one million one hundred twenty-nine thousand '
          'three hundred fourteen of net operating income sweeps against the preferred. In twenty '
          'twenty-seven and twenty twenty-eight, cash available after senior debt service is one million '
          'one hundred fifteen thousand nineteen and one million four hundred seventy thousand six '
          'hundred eleven. Three million seven hundred fourteen thousand nine hundred forty-four is swept '
          'over the term, taking the balance from three million nine hundred four thousand to one million '
          'nine hundred thirty-one thousand six hundred sixty-six, a fifty-one percent reduction, while '
          'accruing at seventeen percent.')
    return ('<section data-label="Cash Sweep and Balance" data-screen-label="Cash Sweep" '
     f'data-speaker-notes="{sn}" ' + sec(pad='58px 92px 42px') + '>\n'
     + h2('The cash sweep and the preferred balance.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1.04fr 1fr;gap:46px;flex:1;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def pref_position():
    c = (bigcol('Capital Beneath the Preferred', f'${PARTNERSHIP/1e6:,.2f}M',
          f'Including ${GP_CASH:,.0f} of sponsor cash',
          dkv('Common equity &middot; LP', f'${COMMON:,.0f}')
          + dkv('Sponsor cash invested', f'${GP_CASH:,.0f}')
          + dkv('Total beneath the preferred', f'${PARTNERSHIP:,.0f}')
          + dkv('Share of total basis', f'{PARTNERSHIP/COST_BASIS:.2%}', accent=True, last=True),
          'first', fs='70px')
     + bigcol('Last-Dollar to Stabilized Value', f'{(SENIOR+PREF)/VAL["stab"]:.2%}',
          'On the April 2029 estimate',
          dkv('As-is', f'{(SENIOR+PREF)/VAL["is"]:.2%}')
          + dkv('Upon completion', f'{(SENIOR+PREF)/VAL["complete"]:.2%}')
          + dkv('Upon stabilization', f'{(SENIOR+PREF)/VAL["stab"]:.2%}')
          + dkv('Last-dollar per key', f'${(SENIOR+PREF)/KEYS:,.0f}', accent=True, last=True),
          'mid', fs='70px')
     + bigcol('Coverage at the Lowest Exit Shown', f'{NET_PROCEEDS[0]/(SENIOR+PF_DUE_AT_EXIT):.2f}x',
          f'Net proceeds to senior principal and the accrued balance at a ${EXITS[0]/1e6:,.0f}M sale',
          dkv('Gross exit value', f'${EXITS[0]:,.0f}')
          + dkv('Net of a 4.0% cost of sale', f'${NET_PROCEEDS[0]:,.0f}')
          + dkv('Senior principal and accrued balance', f'${SENIOR+PF_DUE_AT_EXIT:,.0f}')
          + dkv('Proceeds to that total', f'{NET_PROCEEDS[0]/(SENIOR+PF_DUE_AT_EXIT):.2f}x',
                accent=True, last=True), 'last', fs='70px'))
    b = (blk('Position', f'A single ${SENIOR:,.0f} senior loan sits ahead of the preferred and there is '
             f'no other debt on the asset. ${PARTNERSHIP:,.0f} of common capital stands beneath it, '
             f'including ${GP_CASH:,.0f} of sponsor cash already invested and remaining in the deal.')
     + blk('Deleveraging', f'The sweep takes the balance down {1-PF_DUE_AT_EXIT/PREF:.0%} over the term '
           f'while the estimated value rises from ${VAL["is"]/1e6:,.1f}M to ${VAL["stab"]/1e6:,.1f}M, so '
           f'last-dollar exposure falls from {(SENIOR+PREF)/VAL["is"]:.2%} to '
           f'{(SENIOR+PREF)/VAL["stab"]:.2%} of estimated value.')
     + blk('Funded Risk', f'The ${3_003_000:,.0f} renovation program and the twelve-month interest and '
           f'carry reserve are both funded from the capitalization at close, with ${258_000:,.0f} of '
           'contingency. Neither depends on operating cash flow during the program.'))
    sn = ('Position and protections. Five million five hundred thousand of common capital stands beneath '
          'the preferred, including two million of sponsor cash already invested, twenty-eight point six '
          'percent of the basis. Last-dollar exposure falls from sixty-five percent of as-is value to '
          'forty-seven percent of the stabilized estimate as the sweep reduces the balance fifty-one '
          'percent. Even at an eighteen million dollar sale, net proceeds cover the senior principal and '
          'the accrued preferred balance one point four five times.')
    return darkpage('Position and Protections', 'Position in the stack and downside coverage.', sn, c, b)


# ═══════════════════════════════════════════════════════════ COMMON EQUITY
def common_terms():
    c = (bigcol('LP Commitment', f'${COMMON/1e6:,.2f}M', f'${COMMON/KEYS:,.0f} per key',
          dkv('LP commitment', f'${COMMON:,.0f}')
          + dkv('GP co-investment', f'${GP_CASH:,.0f}')
          + dkv('Partnership capital', f'${PARTNERSHIP:,.0f}')
          + dkv('LP share of capital', f'{COMMON/PARTNERSHIP:.2%}', accent=True, last=True), 'first')
     + bigcol('Preferred Return', f'{CE_PREF:.2%}', 'Cumulative &middot; LP and GP pari passu',
          dkv('Compounding', 'Annual')
          + dkv(f'Cumulative over {HOLD} years', f'{(1+CE_PREF)**HOLD-1:.2%}')
          + dkv('LP preferred at the base case', f'${LP_PREF:,.0f}')
          + dkv('Priority', 'Ahead of all capital', accent=True, last=True), 'mid')
     + bigcol('Residual Split', '50 / 50', 'After the preferred return and capital',
          dkv('GP ownership interest', '51%')
          + dkv('LP ownership interest', '49%')
          + dkv('GP share of capital', f'{GP_CASH/PARTNERSHIP:.2%}')
          + dkv('GP share of base-case cash', f'{GP_CASH_OUT[B]/CE_RESID[B]:.1%}',
                accent=True, last=True), 'last', fs='66px'))
    b = (blk('Alignment', f'The GP has ${GP_CASH:,.0f} of its own cash in the deal on identical pari '
             f'passu terms &mdash; {GP_CASH/PARTNERSHIP:.2%} of partnership capital. It holds a 51% '
             'ownership interest but receives '
             f'{GP_CASH_OUT[B]/CE_RESID[B]:.1%} of partnership cash at the base case, because the '
             'economics follow the waterfall rather than the ownership split.')
     + blk('Order of Distributions', f'Partnership cash is distributed in three tiers: the {CE_PREF:.2%} '
           'cumulative preferred return to the LP and GP pari passu on contributed capital, then return '
           'of capital in full, then a 50/50 split of what remains. The tiers are set out on page 21.')
     + blk('Subordination', 'The GP takes no distribution of any kind until the LP has received its '
           f'{CE_PREF:.2%} preferred return and its ${COMMON:,.0f} of capital back in full. There is no '
           'GP fee, catch-up or clawback ahead of those two tiers.'))
    sn = ('Partnership terms. The LP commits three million five hundred thousand and the general partner '
          'contributes two million of its own cash on identical pari passu terms, a five million five '
          'hundred thousand dollar partnership in which the LP holds sixty-three point six four percent '
          'of the capital. A fifteen percent cumulative preferred return accrues to both, fifty-two point '
          'zero nine percent over three years, ahead of all capital. Capital is then returned in full and '
          'the residual is split fifty-fifty. The general partner holds a fifty-one percent ownership '
          'interest, contributes thirty-six point four percent of the capital and receives forty-one '
          'point nine percent of partnership cash at the base case.')
    return darkpage('Partnership Terms', 'Terms of the partnership.', sn, c, b)


def common_waterfall():
    left = (sub('From Sale Price to Partnership Cash')
     + row('Gross exit value', f'${BASE_EXIT:,.0f}', pad=13, fs='18px')
     + row(f'Less cost of sale &middot; {SELL_COST:.1%}', f'(${BASE_EXIT*SELL_COST:,.0f})',
           pad=13, fs='18px')
     + row('Net sale proceeds', f'${NET_PROCEEDS[B]:,.0f}', pad=13, fs='18px', kind='sub')
     + row('Less senior loan principal', f'(${SENIOR:,.0f})', pad=13, fs='18px')
     + row('Less senior and preferred capital costs and participations',
           f'(${SR_PF_DEDUCT:,.0f})', pad=13, fs='18px')
     + row('Residual to the partnership', f'${CE_RESID[B]:,.0f}', pad=13, fs='19px', kind='tot')
     + '      <div style="height:18px;"></div>\n'
     + sub('Residual at Other Exit Values')
     + tbl(['Gross exit value', 'Net proceeds', 'Residual to the partnership'],
           [(f'${EXITS[i]/1e6:,.0f}M', [f'${NET_PROCEEDS[i]:,.0f}', f'${CE_RESID[i]:,.0f}'],
             'sub' if i == B else '') for i in range(1, 7)], fs='15.5px', pad=10, lw='1fr')
     + para('The deduction above is the senior and preferred capital ahead of the partnership together '
            'with its cost and participations, shown as a single amount. Partnership cash is what remains '
            f'after it. At the ${BASE_EXIT/1e6:,.0f}M base case that is '
            f'<strong style="color:var(--mm-navy-900);">${CE_RESID[B]:,.0f}</strong>, against '
            f'${PARTNERSHIP:,.0f} of contributed capital.', fs='15px', auto=True))
    right = (sub('Distribution Tiers at the Base Case')
     + tbl(['Tier', 'Total', 'LP', 'GP'],
       [(f'1 &middot; {CE_PREF:.2%} cumulative preferred return',
         [f'${WF_PREF:,.0f}', f'${LP_PREF:,.0f}', f'${GP_PREF:,.0f}'], ''),
        ('2 &middot; Return of capital',
         [f'${WF_CAP:,.0f}', f'${COMMON:,.0f}', f'${GP_CASH:,.0f}'], ''),
        ('3 &middot; 50 / 50 residual split',
         [f'${WF_RESID:,.0f}', f'${WF_SPLIT:,.0f}', f'${WF_SPLIT:,.0f}'], ''),
        ('Total distributed',
         [f'${CE_RESID[B]:,.0f}', f'${LP_CASH[B]:,.0f}', f'${GP_CASH_OUT[B]:,.0f}'], 'sub'),
        ('Share of partnership cash',
         ['100.0%', f'{LP_CASH[B]/CE_RESID[B]:.1%}', f'{GP_CASH_OUT[B]/CE_RESID[B]:.1%}'], ''),
        ('Share of contributed capital',
         ['100.0%', f'{COMMON/PARTNERSHIP:.1%}', f'{GP_CASH/PARTNERSHIP:.1%}'], ''),
        ('Equity multiple', ['&mdash;', f'{LP_MULT[B]:.2f}x', f'{GP_MULT[B]:.2f}x'], 'tot')],
       fs='15.5px', pad=13, lw='1.6fr')
     + '      <div style="height:16px;"></div>\n'
     + '      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('LP Preferred Return', f'{CE_PREF:.2%}', 'Cumulative, paid first', pad='14px 14px 0 0')
     + stat('LP Cash at Base Case', f'${LP_CASH[B]:,.0f}', f'{LP_MULT[B]:.2f}x on capital',
            pad='14px 14px 0 14px', vc='var(--mm-orange)')
     + stat('GP Ownership vs Cash', f'51% / {GP_CASH_OUT[B]/CE_RESID[B]:.0%}', 'Owns more, takes less',
            br=False, pad='14px 0 0 14px')
     + '      </div>\n'
     + para('The GP receives nothing in tiers one or two until the LP has been paid alongside it on the '
            'same pari passu terms, and nothing in tier three until all contributed capital has been '
            f'returned. Its 50% of the residual on {GP_CASH/PARTNERSHIP:.2%} of the capital is the whole '
            'of its promote.', fs='15px', auto=True))
    sn = ('The distribution waterfall. At a thirty million dollar exit, net sale proceeds are twenty-eight '
          'million eight hundred thousand after a four percent cost of sale. After the senior loan '
          'principal and the senior and preferred capital costs and participations, fourteen million '
          'forty-eight thousand three hundred thirty-four is residual to the partnership. That is '
          'distributed in three tiers: a fifteen percent cumulative preferred return of two million eight '
          'hundred sixty-four thousand eight hundred thirteen, pari passu; return of the five million five '
          'hundred thousand of capital; then a fifty-fifty split of the five million six hundred '
          'eighty-three thousand five hundred twenty-one that remains. The LP receives eight million one '
          'hundred sixty-four thousand eight hundred twenty-three, two point three three times, and the '
          'general partner five million eight hundred eighty-three thousand five hundred eleven.')
    return ('<section data-label="Distribution Waterfall" data-screen-label="Waterfall" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 40px') + '>\n'
     + h2('How sale proceeds reach the partnership.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.06fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def common_alignment():
    c = (bigcol('Sponsor Cash in the Deal', f'${GP_CASH/1e6:,.2f}M',
          'Invested outside loan proceeds, on the LP&rsquo;s terms',
          dkv('GP co-investment', f'${GP_CASH:,.0f}')
          + dkv('Share of partnership capital', f'{GP_CASH/PARTNERSHIP:.2%}')
          + dkv('Terms', 'Identical to the LP')
          + dkv('Priority', 'Pari passu', accent=True, last=True), 'first', fs='74px')
     + bigcol('GP Ownership vs Cash', f'51% / {GP_CASH_OUT[B]/CE_RESID[B]:.0%}',
          'Owns a majority, receives less than it owns',
          dkv('GP ownership interest', '51%')
          + dkv('GP share of capital', f'{GP_CASH/PARTNERSHIP:.2%}')
          + dkv('GP share of base-case cash', f'{GP_CASH_OUT[B]/CE_RESID[B]:.1%}')
          + dkv('LP share of base-case cash', f'{LP_CASH[B]/CE_RESID[B]:.1%}',
                accent=True, last=True), 'mid', fs='56px')
     + bigcol('LP Paid First', f'{CE_PREF:.2%}', 'Cumulative preferred return, then capital in full',
          dkv('Tier 1', f'{CE_PREF:.2%} preferred return')
          + dkv('Tier 2', 'Return of capital')
          + dkv('Tier 3', '50 / 50 residual')
          + dkv('GP promote before tier 3', 'None', accent=True, last=True), 'last', fs='74px'))
    b = (blk('Skin in the Game', f'${GP_CASH:,.0f} of sponsor cash is already invested in the asset, '
             'outside loan proceeds, and stays in through the hold on exactly the terms offered to the '
             f'LP. It is {GP_CASH/PARTNERSHIP:.2%} of partnership capital and is included in the '
             f'${COST_BASIS:,.0f} basis on page 24.')
     + blk('Ratios Given Up', 'The GP holds 51% of the partnership but has accepted a waterfall that '
           f'pays it {GP_CASH_OUT[B]/CE_RESID[B]:.1%} of partnership cash at the base case &mdash; less '
           'than its ownership &mdash; so the LP hurdles are met before any promote is earned.')
     + blk('Operator and Brand', 'The sponsor owns and operates the Wylder brand and manages the asset '
           'directly. The brand resume is on page 7, the business plan on page 8 and the renovation '
           'schedule on page 9.'))
    sn = ('Sponsor alignment. Two million of sponsor cash is already invested outside loan proceeds and '
          'stays in through the hold on exactly the terms offered to the LP, thirty-six point four percent '
          'of partnership capital. The general partner holds a fifty-one percent ownership interest but '
          'receives forty-one point nine percent of partnership cash at the base case. The LP is paid its '
          'fifteen percent cumulative preferred return and its capital back in full before the general '
          'partner earns any promote.')
    return darkpage('Sponsor Alignment', 'Sponsor alignment and the GP position.', sn, c, b)


# ═══════════════════════════════════════════════════════════ SENIOR DEBT · NO PARTICIPATION
# The same loan offered without an equity kicker, for hard money lenders. No projected return
# appears anywhere in this package and there is no returns page.
META['hm'] = dict(
  label='Senior Debt', eyebrow='Confidential &middot; Senior Debt Placement',
  kicker=f'Senior Loan &middot; ${SENIOR:,.0f} &middot; First Trust Deed',
  amount=SENIOR, color='#032D67',
  lede=(f'A <strong>${SENIOR:,.0f} senior loan</strong>, first trust deed, on a 58-key waterfront '
        f'resort in Talbot County, Maryland &mdash; {LTV["is"]:.2%} of as-is value and {LTC:.2%} of '
        f'total cost. Interest-only at {ALLIN:.2%} for a three-year term, with a twelve-month '
        f'interest and carry reserve funded at close. ${PREF+COMMON:,.0f} of subordinate capital '
        f'closes concurrently and ${GP_CASH:,.0f} of sponsor cash is already invested. The loan is '
        'the only debt on the asset.'),
  stats=[('Loan Amount', f'${SENIOR:,.0f}'), ('All-In Rate', f'{ALLIN:.2%}'),
         ('LTV &middot; As-Is', f'{LTV["is"]:.2%}')])

OPP['hm'] = ('Summary of the senior loan request.',
  f'Marcus &amp; Millichap Capital Corporation is placing a <strong style="color:var(--mm-navy-900);">'
  f'${SENIOR:,.0f} senior loan</strong>, first trust deed, on Wylder Hotel Tilghman Island. The loan is '
  f'{LTV["is"]:.2%} of as-is value and {LTC:.2%} of total cost, interest-only for a {SR_TERM}-year term, '
  f'with a twelve-month interest and carry reserve funded at close. '
  f'<strong style="color:var(--mm-navy-900);">${PREF+COMMON:,.0f} of subordinate capital</strong> closes '
  f'concurrently and ${GP_CASH:,.0f} of sponsor cash is already invested and remains in the deal.',
  [('Senior Loan', f'${SENIOR/1e6:,.2f}M', f'First trust deed &middot; ${SENIOR/KEYS:,.0f} per key', 1),
   ('LTV &middot; As-Is', f'{LTV["is"]:.2%}', f'{LTV["stab"]:.2%} of the stabilized estimate', 0),
   ('Loan to Cost', f'{LTC:.2%}', f'On the ${TOTAL:,.0f} capitalization', 0),
   ('All-In Rate', f'{ALLIN:.2%}', f'SOFR {SOFR:.2%} plus {SPREAD:.2%}, floating', 0),
   ('Term &amp; Amortization', f'{SR_TERM} yr &middot; IO', 'Single advance funded at close', 0),
   ('Debt Yield &middot; 2027', f'{DY[2027]:.2%}', f'{DY[2028]:.2%} in 2028', 0),
   ('DSCR &middot; 2027', f'{DSCR[2027]:.2f}x', f'{DSCR[2028]:.2f}x in 2028 &middot; reserve covers 2026', 0),
   ('Capital Beneath the Loan', f'${(PREF+COMMON+GP_CASH)/1e6:,.2f}M',
    f'{(PREF+COMMON+GP_CASH)/COST_BASIS:.1%} of total basis', 1)])


def hm_terms():
    c = (bigcol('Loan Amount', f'${SENIOR/1e6:,.1f}M', f'${SENIOR/KEYS:,.0f} per key',
          dkv('Gross loan amount', f'${SENIOR:,.0f}')
          + dkv('Origination fee', '2.00%')
          + dkv('Interest and carry reserve', f'${SR_RESERVE:,.0f}')
          + dkv('Net proceeds at close', f'${SR_NET:,.0f}', accent=True, last=True), 'first')
     + bigcol('All-In Rate', f'{ALLIN:.2%}', f'SOFR plus {SPREAD:.2%}, floating',
          dkv('Index &middot; SOFR', f'{SOFR:.2%}')
          + dkv('Spread', f'{SPREAD:.2%}')
          + dkv('Annual debt service', f'${SR_ADS:,.0f}')
          + dkv('Amortization', 'Interest-only', accent=True, last=True), 'mid')
     + bigcol('Term', f'{SR_TERM} years', 'Exit at the end of year three',
          dkv('Collateral', 'First trust deed')
          + dkv('Funding', 'Single advance at close')
          + dkv('Loan to cost', f'{LTC:.2%}')
          + dkv('Position', 'Only debt on the asset', accent=True, last=True), 'last'))
    b = (blk('Position', f'The loan is the only debt on the asset and is secured by a first trust deed. '
             f'${PREF+COMMON:,.0f} of subordinate capital funds concurrently at close and '
             f'${GP_CASH:,.0f} of sponsor cash is already invested, giving a '
             f'{(PREF+COMMON+GP_CASH)/COST_BASIS:.1%} cushion beneath the loan on total basis.')
     + blk('Reserve and Carry', f'A ${SR_RESERVE:,.0f} interest and carry reserve &mdash; twelve months '
           'of debt service &mdash; is funded from the capitalization at close and covers the renovation '
           'period in full, before the asset reopens under the brand.')
     + blk('Takeout', f'At an indicative {PERM_RATE:.2%} on a 30-year amortizing basis, debt service is '
           f'${PERM_ADS:,.0f} and coverage is {PERM_DSCR[2027]:.2f}x on 2027 cash flow, so a conventional '
           'permanent loan clears the balance at maturity. The test is on page 21.'))
    sn = ('Senior loan terms. Ten million dollars, gross, less a two percent origination fee and a one '
          'million two hundred thousand dollar interest and carry reserve, for eight million six hundred '
          'thousand of net proceeds at close. All-in rate twelve percent: SOFR at three point seven nine '
          'plus an eight point two one spread, floating, interest-only, one million two hundred thousand '
          'of annual debt service. Three-year term, first trust deed, single advance, fifty-seven point '
          'five percent of cost, and the only debt on the asset.')
    return darkpage('Senior Loan Terms', 'Terms of the senior loan.', sn, c, b)


def hm_credit():
    beneath = PREF + COMMON + GP_CASH
    c = (bigcol('Capital Beneath the Loan', f'${(PREF+COMMON)/1e6:,.2f}M',
          f'Plus ${GP_CASH:,.0f} of sponsor cash already invested',
          dkv('Subordinate capital at close', f'${PREF+COMMON:,.0f}')
          + dkv('Sponsor cash invested', f'${GP_CASH:,.0f}')
          + dkv('Total beneath the loan', f'${beneath:,.0f}')
          + dkv('Share of total basis', f'{beneath/COST_BASIS:.2%}', accent=True, last=True),
          'first', fs='70px')
     + bigcol('Loan to Stabilized Value', f'{LTV["stab"]:.2%}', 'On the April 2029 estimate',
          dkv('As-is', f'{LTV["is"]:.2%}')
          + dkv('Upon completion', f'{LTV["complete"]:.2%}')
          + dkv('Upon stabilization', f'{LTV["stab"]:.2%}')
          + dkv('Loan per key &middot; 58 keys', f'${SENIOR/KEYS:,.0f}', accent=True, last=True),
          'mid', fs='70px')
     + bigcol(f'Coverage at an ${EXITS[0]/1e6:,.0f}M Sale', f'{NET_PROCEEDS[0]/SENIOR:.2f}x',
          'Net proceeds to principal, well below the as-is estimate',
          dkv('Gross sale value', f'${EXITS[0]:,.0f}')
          + dkv('Net of a 4.0% cost of sale', f'${NET_PROCEEDS[0]:,.0f}')
          + dkv('Senior principal', f'${SENIOR:,.0f}')
          + dkv('Proceeds to principal', f'{NET_PROCEEDS[0]/SENIOR:.2f}x', accent=True, last=True),
          'last', fs='70px'))
    b = (blk('Renovation Risk', f'The ${3_003_000:,.0f} program is funded in full at close, with '
             f'${258_000:,.0f} of contingency inside it, and the twelve-month interest and carry reserve '
             'pays debt service through completion. The schedule by trade is on page 9.')
     + blk('Ramp and Seasonality', f'Coverage is {DSCR[2026]:.2f}x in the renovation year and '
           f'{DSCR[2027]:.2f}x in the first full year of operation. The business plan targets 83% of '
           'market RevPAR at stabilization, a level still below the competitive average on page 16.')
     + blk('Brand and Management', 'The asset operates under the Wylder brand with the sponsor as '
           'operator. The brand resume and the affiliation terms are on pages 7 and 10, and historical '
           'operating results are on page 15.'))
    sn = ('Credit considerations. Seven million four hundred four thousand of subordinate capital closes '
          'beneath the loan and two million of sponsor cash is already invested, nine million four hundred '
          'four thousand in total, forty-eight point nine percent of the nineteen million two hundred '
          'forty-seven thousand dollar basis. Leverage falls from forty-six point seven percent of as-is '
          'value to thirty-three point nine percent of the stabilized estimate. Even at an eighteen '
          'million dollar sale, well below the as-is estimate, net proceeds cover principal one point '
          'seven three times. The renovation is fully funded with contingency and the reserve pays debt '
          'service through completion.')
    return darkpage('Credit Considerations', 'Credit considerations and downside coverage.', sn, c, b)
