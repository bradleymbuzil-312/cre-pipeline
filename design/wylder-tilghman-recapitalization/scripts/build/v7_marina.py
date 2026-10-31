# -*- coding: utf-8 -*-
"""Marina valuation — the figures, the page for the debt packages, and the standalone deck.

Values cover the slips and their riparian rights only. They exclude the hotel, the Dogwood Cove
residence and any upland business value, and they are not carried in the estimated hotel values.
"""
from v7_lib import *
from v7_tranche import tbl, darkpage, DATE, TAIL
from v7_pages import dkv, bigcol, blk

# ───────────────────────────────── the subject
SLIPS_W, SLIPS_D, SLIPS_T = 23, 24, 47
LOW, REC, HIGH = 25_000, 30_000, 40_000
DOGWOOD_ASIS = 280_000                      # contract price less the parcel's residential assessment
DOGWOOD_CONTRACT, DOGWOOD_ASSESSED = 1_100_000, 820_833
SLIP_REV_2028_W = SLIP_REV_2028_D = 179_648
SLIP_REV_2028 = SLIP_REV_2028_W + SLIP_REV_2028_D
MARINA_PIP = 250_000

# ───────────────────────────────── slip-focused sales, time-adjusted at 3% a year
TIME_ADJ = 0.03
SLIP_SALES = [
    ('DiMillo&rsquo;s on the Chesapeake East', 'Oxford', '45 min', 'May 2021',  2_450_000,  60,
     40_833, 48_019, '1.71 ac, service yard'),
    ('Gateway Marina', 'Trappe', '40 min', 'Jun 2021',  2_950_000, 112,
     26_339, 30_837, 'Two parcels, 4.6 ac, fuel, service'),
    ('Mears Point Marina', 'Kent Narrows', '55 min', 'May 2020', 11_950_000, 540,
     22_130, 26_800, '42.7 ac, pool, restaurant, 75-ton lift'),
]
MEDIAN_ADJ, MEAN_ADJ = 30_837, 35_219
TALBOT_AVG_ADJ = 39_428                     # the two Talbot County slip sales, adjusted

# ───────────────────────────────── full-service and hospitality trades (context, not slip prices)
CONTEXT_SALES = [
    ('Lowe&rsquo;s Wharf Marina Inn', 'Sherwood', '10 min', 'Aug 2024',  4_050_000,  22, 184_091,
     '10 rooms, restaurant and bar, 6 BR house, fuel'),
    ('St. Michaels Marina and three restaurants', 'St. Michaels', '25 min', 'Dec 2021',
     7_709_500,  55, 140_173, 'Resold 32 months after an Apr 2019 sale at $5,750,000'),
    ('Campbell&rsquo;s Boatyard at Bachelor Point', 'Oxford', '45 min', 'Jun 2025',  7_000_000,  56,
     125_000, '17.9 ac, full-service yard, dry storage'),
    ('Bay Bridge Marina', 'Stevensville', '60 min', 'Feb 2025', 22_848_000, 243,  94_025,
     '28.5 ac, yard, indoor heated storage'),
]

# ───────────────────────────────── income approach, market rent case
GROSS_SLIP, OCCUPANCY, OPEX_PC = 4_500, 0.85, 0.40
NOI_SLIP = round(GROSS_SLIP * OCCUPANCY * (1 - OPEX_PC))          # 2,295
CAP_LOW, CAP, CAP_HIGH = 0.0700, 0.0850, 0.1000
INCOME_SLIP = round(NOI_SLIP / CAP / 1000) * 1000                 # 27,000
INCOME_GRID = [3_500, 4_500, 5_500]

# ───────────────────────────────── income approach, sponsor model case
MODEL_OPEX, UW_OPEX = 0.171, 0.350
MODEL_NOI = round(SLIP_REV_2028 * (1 - MODEL_OPEX))               # 297,856
UW_NOI    = round(SLIP_REV_2028 * (1 - UW_OPEX))                  # 233,542

val = lambda noi, c: round(noi / c)
per = lambda n, d: round(n / d)

# ───────────────────────────────── checks
assert SLIPS_W + SLIPS_D == SLIPS_T
for n, v in ((LOW, 1_175_000), (REC, 1_410_000), (HIGH, 1_880_000)):
    assert SLIPS_T * n == v, (n, v)
assert SLIPS_W * REC == 690_000 and SLIPS_D * REC == 720_000
assert SLIPS_W * LOW == 575_000 and SLIPS_D * LOW == 600_000
assert SLIPS_W * HIGH == 920_000 and SLIPS_D * HIGH == 960_000
assert abs(DOGWOOD_CONTRACT - DOGWOOD_ASSESSED - DOGWOOD_ASIS) < 1_000
for *_, price, slips, ps, adj, _n in SLIP_SALES:
    assert abs(price / slips - ps) < 1, (price, slips, ps)
    assert adj > ps
for *_, price, slips, ps, _n in CONTEXT_SALES:
    assert abs(price / slips - ps) < 1, (price, slips, ps)
assert sorted(s[7] for s in SLIP_SALES)[1] == MEDIAN_ADJ
assert abs(sum(s[7] for s in SLIP_SALES) / 3 - MEAN_ADJ) < 1
assert NOI_SLIP == 2_295 and INCOME_SLIP == 27_000
assert per(SLIP_REV_2028, SLIPS_T) == 7_645
assert per(SLIP_REV_2028_W, SLIPS_W) == 7_811 and per(SLIP_REV_2028_D, SLIPS_D) == 7_485
assert MODEL_NOI == 297_856 and UW_NOI == 233_542
assert val(MODEL_NOI, CAP) == 3_504_188 and val(UW_NOI, CAP) == 2_747_553
assert per(val(MODEL_NOI, CAP), SLIPS_T) == 74_557
assert per(val(UW_NOI, CAP), SLIPS_T) == 58_459
assert INCOME_SLIP * SLIPS_W == 621_000 and INCOME_SLIP * SLIPS_T == 1_269_000

if __name__ == '__main__':
    print(f'  recommended  ${REC:,}/slip  ·  Wylder ${SLIPS_W*REC:,}  Dogwood ${SLIPS_D*REC:,}  '
          f'combined ${SLIPS_T*REC:,}')
    print(f'  range        ${LOW:,}-${HIGH:,}/slip  ·  ${SLIPS_T*LOW:,} to ${SLIPS_T*HIGH:,}')
    print(f'  slip comps   median adj ${MEDIAN_ADJ:,}  mean adj ${MEAN_ADJ:,}  '
          f'Talbot avg ${TALBOT_AVG_ADJ:,}')
    print(f'  income       ${INCOME_SLIP:,}/slip  ·  combined ${INCOME_SLIP*SLIPS_T:,}  '
          f'({INCOME_SLIP/REC-1:+.1%} vs recommendation)')
    print(f'  model upside ${val(UW_NOI, CAP):,} to ${val(MODEL_NOI, CAP):,}  '
          f'(${per(val(UW_NOI,CAP),SLIPS_T):,} to ${per(val(MODEL_NOI,CAP),SLIPS_T):,}/slip)')
    print('  all marina figures reconcile')
    _SUMMARY_ONLY = False


# ═══════════════════════════════════════════════ the page carried by the debt packages
def marina_page(values_page=24):
    left = (sub('Estimated Slip Value')
     + tbl(['Slips', f'Low &middot; ${LOW//1000}K', f'Recommended &middot; ${REC//1000}K',
            f'High &middot; ${HIGH//1000}K'],
       [(f'Wylder &middot; {SLIPS_W} slips',
         [f'${SLIPS_W*LOW:,}', f'${SLIPS_W*REC:,}', f'${SLIPS_W*HIGH:,}'], ''),
        (f'Dogwood Cove &middot; {SLIPS_D} slips, upon approval',
         [f'${SLIPS_D*LOW:,}', f'${SLIPS_D*REC:,}', f'${SLIPS_D*HIGH:,}'], ''),
        (f'Combined &middot; {SLIPS_T} slips',
         [f'${SLIPS_T*LOW:,}', f'${SLIPS_T*REC:,}', f'${SLIPS_T*HIGH:,}'], 'sub')],
       fs='16px', pad=14, lw='1.9fr')
     + '      <div style="height:14px;"></div>\n'
     + row(f'Dogwood Cove &middot; {SLIPS_D} slips, as they stand today', f'${DOGWOOD_ASIS:,}',
           pad=10, fs='16px', kind='hi',
           note=f'About ${per(DOGWOOD_ASIS, SLIPS_D):,} per slip &mdash; the ${DOGWOOD_CONTRACT:,} '
                f'contract price less the parcel&rsquo;s ${DOGWOOD_ASSESSED:,} residential '
                'assessment. The slips reach hotel slip value only once commercial use is approved.')
     + '      <div style="height:10px;"></div>\n' + sub('Income Cross-Check')
     + row('Gross revenue per slip', f'${GROSS_SLIP:,}', pad=6, fs='15px')
     + row('Occupancy', f'{OCCUPANCY:.0%}', pad=6, fs='15px')
     + row('Operating expense', f'{OPEX_PC:.0%} of effective gross income', pad=6, fs='15px')
     + row('Net operating income per slip', f'${NOI_SLIP:,}', pad=6, fs='15px')
     + row('Capitalization rate', f'{CAP:.2%}', pad=6, fs='15px')
     + row('Indicated value per slip', f'${INCOME_SLIP:,}', pad=6, fs='15px', kind='sub',
           note=f'${INCOME_SLIP*SLIPS_T:,} combined &mdash; {1-INCOME_SLIP/REC:.0%} below the '
                'recommendation, which is weighted to the local sales')
     + para('These are estimates stated for underwriting purposes, not a formal opinion of value. '
            'They cover the slips and their riparian rights only and exclude the hotel, the Dogwood '
            'Cove residence and any upland business value.', fs='14.5px', auto=True))

    right = (sub('Comparable Slip Sales &middot; Within an Hour of Tilghman')
     + tbl(['Property', 'Date', 'Price', 'Slips', 'Per Slip', 'Adjusted'],
       [(f'{n}<div style="{BODY}font-size:12.5px;color:var(--ink-500);margin-top:2px;">'
         f'{loc} &middot; {drive} &middot; {note}</div>',
         [d, f'${p/1e6:,.2f}M', f'{s}', f'${ps:,}', f'${adj:,}'], '')
        for n, loc, drive, d, p, s, ps, adj, note in SLIP_SALES]
       + [('Median &middot; adjusted to today',
           ['&mdash;', '&mdash;', '&mdash;', '&mdash;', f'${MEDIAN_ADJ:,}'], 'sub'),
          ('Mean &middot; adjusted to today',
           ['&mdash;', '&mdash;', '&mdash;', '&mdash;', f'${MEAN_ADJ:,}'], '')],
       fs='14.5px', pad=11, lw='2.5fr')
     + para(f'Deed consideration from the Maryland state assessment file, adjusted to today at '
            f'{TIME_ADJ:.0%} a year. The recommendation sits on the adjusted median. The two Talbot '
            f'County sales average ${TALBOT_AVG_ADJ:,} per slip; Mears Point at ${26_800:,} carries '
            'a 540-slip volume discount that does not apply here. Four further local trades &mdash; '
            'full-service boatyards and marinas sold with hotel or restaurant operations &mdash; '
            f'run ${94_025:,} to ${184_091:,} per slip. They show what bay frontage with a business '
            'on it commands locally, but they are not slip prices.', fs='14.5px', mt='12px')
     + '      <div style="margin-top:auto;padding-top:14px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Recommended', f'${REC:,}', 'Per slip · the adjusted median', pad='14px 14px 0 0')
     + stat(f'Combined · {SLIPS_T} Slips', f'${SLIPS_T*REC:,}', 'Upon approval of Dogwood Cove',
            pad='14px 14px 0 14px', vc='var(--mm-orange)')
     + stat('Not in the Hotel Values', 'None of it',
            f"The estimates on page {values_page} exclude the marina", br=False, pad='14px 0 0 14px')
     + '      </div>\n      </div>\n')

    sn = ('The marina as collateral. Forty-seven slips on completion: twenty-three at the hotel and '
          'twenty-four with the Dogwood Cove parcel. At thirty thousand dollars a slip, the adjusted '
          'median of three deed-verified slip sales within an hour of Tilghman, that is six hundred '
          'ninety thousand for the Wylder slips, seven hundred twenty thousand for Dogwood Cove once '
          'commercial use is approved, and one million four hundred ten thousand combined, in a range '
          'of twenty-five to forty thousand a slip. Until the Dogwood Cove slips are approved for '
          'commercial use they carry about two hundred eighty thousand, the contract price less the '
          'parcel&rsquo;s residential assessment. An income cross-check on market seasonal rents '
          'supports twenty-seven thousand a slip, ten percent below the recommendation. None of this '
          'value is carried in the estimated hotel values.')
    return ('<section data-label="Marina Valuation" data-screen-label="Marina Valuation" '
     f'data-speaker-notes="{sn}" ' + sec(pad='52px 88px 38px') + '>\n'
     + h2(f'The {SLIPS_T}-slip marina is collateral the value estimates do not carry.',
          fs='40px', mb='16px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.14fr;gap:44px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ═══════════════════════════════════════════════ the standalone marina valuation deck
MARINA_LABEL = 'Marina Valuation'
EYEBROW = 'Confidential &middot; Marina Valuation'


def m_title():
    sn = ('Marina valuation for Wylder Hotel Tilghman Island and the adjacent Dogwood Cove parcel, '
          'dated October thirtieth, twenty twenty-six. Forty-seven slips across the two properties. '
          'The recommendation is thirty thousand dollars a slip, one million four hundred ten '
          'thousand for the combined marina, in a range of twenty-five to forty thousand.')
    return ('<section data-label="Title" data-screen-label="Title" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:space-between;padding:90px 100px;">\n'
     '  <img src="assets/wt-aerial-spring.png" alt="Wylder Hotel Tilghman Island aerial" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,17,34,.74) 0%,'
     'rgba(0,17,34,.46) 42%,rgba(0,17,34,.62) 74%,rgba(0,17,34,.92) 100%);"></div>\n'
     '  <div style="position:absolute;right:0;top:0;bottom:0;width:12px;display:flex;'
     'flex-direction:column;">\n    <div style="flex:0 0 60%;background:#F0720E;"></div>\n'
     '    <div style="flex:0 0 40%;background:#456EAB;"></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.28);padding-bottom:28px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:60px;">\n'
     '    <div style="display:flex;align-items:center;gap:20px;">'
     f'<span style="{CON}font-size:15px;letter-spacing:.26em;color:var(--mm-orange-100);">'
     f'{EYEBROW}</span>'
     '<span style="font-family:var(--font-mono);font-size:15px;font-weight:700;letter-spacing:.08em;'
     'color:rgba(255,255,255,.62);padding-left:20px;border-left:1px solid rgba(255,255,255,.32);">01'
     '</span></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;flex:1;display:flex;flex-direction:column;'
     'justify-content:center;margin-left:-100px;padding:0 150px 0 100px;background:'
     'linear-gradient(90deg,rgba(0,18,40,.82) 0%,rgba(0,18,40,.76) 56%,rgba(0,18,40,.46) 82%,'
     'rgba(0,18,40,0) 100%);max-width:1500px;">\n'
     f'    <div style="{CON}font-size:19px;letter-spacing:.30em;color:var(--mm-orange);'
     f'margin-bottom:24px;">{SLIPS_T} Slips &middot; ${REC:,} Per Slip &middot; '
     f'${SLIPS_T*REC:,}</div>\n'
     f'    <h1 style="{DISP}font-weight:700;font-size:96px;line-height:0.99;letter-spacing:-0.018em;'
     'margin:0;text-shadow:0 2px 30px rgba(0,17,34,.45);">Wylder and Dogwood<br>Cove Marina.</h1>\n'
     '    <div style="width:120px;height:3px;background:var(--mm-orange);margin:34px 0 26px;"></div>\n'
     f'    <div style="{DISP}font-style:italic;font-weight:400;font-size:29px;color:#fff;'
     'line-height:1.34;max-width:1080px;text-shadow:0 2px 20px rgba(0,17,34,.5);">An estimate of '
     f'slip value for the <strong>{SLIPS_W} existing Wylder slips</strong> and the '
     f'<strong>{SLIPS_D} slips</strong> that come with the adjacent Dogwood Cove parcel, on seven '
     'deed-verified marina sales within about an hour of Tilghman Island and an income cross-check '
     f'on market seasonal rents. Recommendation <strong>${REC:,} per slip</strong>, a range of '
     f'${LOW:,} to ${HIGH:,}, and <strong>${SLIPS_T*REC:,} for the combined {SLIPS_T}-slip '
     'marina</strong>.</div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:flex-end;border-top:1px solid rgba(255,255,255,.28);padding-top:28px;">\n'
     '    <div>\n'
     f'      <div style="{DISP}font-size:28px;font-weight:700;line-height:1;">Bradley M. Buzil</div>\n'
     f'      <div style="{CON}font-size:15px;letter-spacing:.2em;color:var(--mm-navy-100);'
     'margin-top:8px;">Senior Director &middot; The TRANCHE Group</div>\n    </div>\n'
     '    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:12px;">\n'
     '      <div style="display:flex;flex-direction:column;align-items:center;">\n'
     '        <span style="font-family:var(--font-serif);font-weight:400;font-size:46px;'
     'line-height:0.82;color:#fff;letter-spacing:.01em;">wylder</span>\n'
     '        <span style="width:46px;height:1.5px;background:var(--mm-orange);margin:10px 0 7px;">'
     '</span>\n'
     f'        <span style="{CON}font-size:13px;letter-spacing:.38em;color:#fff;'
     'padding-left:.38em;">Tilghman Island</span>\n      </div>\n'
     f'      <div style="{MONO}font-size:15px;color:var(--mm-navy-100);letter-spacing:.04em;">'
     'October 30, 2026 &middot; Tilghman Island, MD</div>\n    </div>\n  </div>\n</section>')


def m_conclusion():
    left = (sub('Recommended Slip Value')
     + tbl(['Slips', f'Low &middot; ${LOW//1000}K', f'Recommended &middot; ${REC//1000}K',
            f'High &middot; ${HIGH//1000}K'],
       [(f'Wylder &middot; {SLIPS_W} slips',
         [f'${SLIPS_W*LOW:,}', f'${SLIPS_W*REC:,}', f'${SLIPS_W*HIGH:,}'], ''),
        (f'Dogwood Cove &middot; {SLIPS_D} slips, upon approval',
         [f'${SLIPS_D*LOW:,}', f'${SLIPS_D*REC:,}', f'${SLIPS_D*HIGH:,}'], ''),
        (f'Combined &middot; {SLIPS_T} slips',
         [f'${SLIPS_T*LOW:,}', f'${SLIPS_T*REC:,}', f'${SLIPS_T*HIGH:,}'], 'sub')],
       fs='17px', pad=17, lw='1.9fr')
     + '      <div style="height:16px;"></div>\n'
     + row(f'Dogwood Cove &middot; {SLIPS_D} slips, as they stand today', f'${DOGWOOD_ASIS:,}',
           pad=12, fs='17px', kind='hi',
           note=f'About ${per(DOGWOOD_ASIS, SLIPS_D):,} per slip &mdash; the ${DOGWOOD_CONTRACT:,} '
                f'contract price less the parcel&rsquo;s ${DOGWOOD_ASSESSED:,} residential '
                'assessment')
     + para('All values cover the slips and their riparian rights only. They exclude the hotel, the '
            'Dogwood Cove residence and any upland business value. They are estimates stated for '
            'underwriting purposes, not a formal opinion of value.', fs='16px', auto=True))
    right = (sub('What Supports It')
     + row('Slip-focused sales &middot; adjusted median', f'${MEDIAN_ADJ:,}', pad=13, fs='17px',
           note='Three deed-verified sales that are mostly slips, within about an hour of Tilghman')
     + row('Slip-focused sales &middot; adjusted mean', f'${MEAN_ADJ:,}', pad=13, fs='17px')
     + row('Talbot County sales &middot; adjusted average', f'${TALBOT_AVG_ADJ:,}', pad=13, fs='17px',
           note='Oxford and Trappe, the two closest slip trades')
     + row('Income approach &middot; market seasonal rents', f'${INCOME_SLIP:,}', pad=13, fs='17px',
           note=f'{1-INCOME_SLIP/REC:.0%} below the recommendation')
     + row('Recommendation', f'${REC:,}', pad=13, fs='18px', kind='tot',
           note='The adjusted median. The local sales are weighted more heavily because they price '
                'this specific shoreline')
     + '      <div style="height:16px;"></div>\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Combined Marina', f'${SLIPS_T*REC:,}', f'{SLIPS_T} slips upon approval',
            pad='16px 16px 0 0', vc='var(--mm-orange)', vfs='28px')
     + stat('Range', f'${SLIPS_T*LOW/1e6:,.2f}M &ndash; ${SLIPS_T*HIGH/1e6:,.2f}M',
            f'${LOW:,} to ${HIGH:,} per slip', pad='16px 16px 0 16px', vfs='24px')
     + stat('Comp Set', '7 sales', 'Deed-verified, plus the Dogwood Cove deed history', br=False,
            pad='16px 0 0 16px', vfs='28px')
     + '      </div>\n'
     + para('The four local trades that carry a full-service boatyard or hotel and restaurant '
            f'operations run ${94_025:,} to ${184_091:,} per slip. They show what bay frontage with '
            'a business on it commands locally, but they are not slip prices and none of that '
            'transfers to amenity slips.', fs='15.5px', auto=True))
    sn = ('The recommendation is thirty thousand dollars a slip: six hundred ninety thousand for the '
          'twenty-three Wylder slips, seven hundred twenty thousand for the twenty-four Dogwood Cove '
          'slips and one million four hundred ten thousand for the combined forty-seven slip marina, '
          'in a range of twenty-five to forty thousand a slip. The Dogwood Cove figure assumes its '
          'slips are approved for commercial use with the hotel; until then they carry about two '
          'hundred eighty thousand, the contract price less the parcel&rsquo;s residential '
          'assessment. The three slip-focused sales run twenty-six thousand eight hundred to '
          'forty-eight thousand a slip adjusted to today, with a median of thirty thousand eight '
          'hundred thirty-seven. The recommendation sits on that median. An income approach on market '
          'seasonal rents supports twenty-seven thousand, ten percent below.')
    return ('<section data-label="Conclusion" data-screen-label="Conclusion" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2(f'${REC:,} per slip, or ${SLIPS_T*REC:,} for the {SLIPS_T}-slip marina.',
          fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.02fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def m_subject():
    left = (sub('The Subject')
     + tbl(['Item', 'Wylder', 'Dogwood Cove', 'Combined'],
       [('Slips', [f'{SLIPS_W} existing', f'{SLIPS_D}', f'{SLIPS_T}'], 'sub'),
        ('Upland', ['Hotel, restaurant, boat bar', '4 BR residence, ~3 ac', '&mdash;'], ''),
        ('Condition', [f'Rebuilt in the ${MARINA_PIP:,} marina line', 'Good, usable day one',
                       '&mdash;'], ''),
        ('Model slip revenue, 2028',
         [f'${SLIP_REV_2028_W:,}', f'${SLIP_REV_2028_D:,}', f'${SLIP_REV_2028:,}'], ''),
        ('Revenue per slip', [f'${per(SLIP_REV_2028_W, SLIPS_W):,}',
                              f'${per(SLIP_REV_2028_D, SLIPS_D):,}',
                              f'${per(SLIP_REV_2028, SLIPS_T):,}'], 'sub')],
       fs='15.5px', pad=13, lw='1.5fr')
     + para('Slip counts come from the lender materials and the sponsor&rsquo;s tour notes, not a '
            'survey or the purchase and sale agreement. Every value in this analysis scales linearly '
            'with the count, so confirming them is the first open item. The model assumes 30% slip '
            f'occupancy across all {SLIPS_T} slips and doubles the existing slip line for Dogwood '
            'Cove.', fs='15.5px', mt='14px')
     + '      <div style="height:14px;"></div>\n' + sub('Dogwood Cove Deed History')
     + tbl(['Event', 'Date', 'Amount'],
       [('Recorded sale', ['Sep 2015', '$449,000'], ''),
        ('Recorded transfer &middot; non arm&rsquo;s length', ['Mar 2018', '$530,250'], ''),
        ('Current residential assessment', ['2026', f'${DOGWOOD_ASSESSED:,}'], ''),
        ('Under contract now', ['&mdash;', f'${DOGWOOD_CONTRACT:,}'], 'sub')],
       fs='15.5px', pad=11, lw='2.1fr')
     + para(f'2.74 acres. If the house and land carry roughly the assessed value, the contract '
            f'implies about <strong style="color:var(--mm-navy-900);">${DOGWOOD_ASIS:,}</strong>, or '
            f'${per(DOGWOOD_ASIS, SLIPS_D):,} a slip, for the {SLIPS_D} slips as they stand. The '
            'market prices them today as residential piers; they earn hotel slip value only once '
            'commercial use is approved.', fs='15.5px', auto=True))
    right = ('    <div style="flex:1;position:relative;overflow:hidden;min-height:300px;">\n'
     '      <img src="assets/wt-pier.png" alt="Wylder Hotel Tilghman Island waterfront" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '      <div style="position:absolute;left:0;top:0;bottom:0;width:8px;display:flex;'
     'flex-direction:column;"><div style="flex:0 0 60%;background:var(--mm-orange);"></div>'
     '<div style="flex:0 0 40%;background:#456EAB;"></div></div>\n    </div>\n'
     '    <div style="background:var(--mm-navy-900);color:#fff;padding:22px 26px;">\n'
     f'      <div style="{CON}font-size:14px;letter-spacing:.18em;color:rgba(255,255,255,.9);'
     'border-bottom:1px solid rgba(255,255,255,.35);padding-bottom:9px;">What the Slips Are</div>\n'
     f'      <p style="{BODY}max-width:none;font-size:16px;line-height:1.5;'
     'color:rgba(255,255,255,.86);margin:14px 0 0;">These are <strong style="color:#fff;">hotel '
     'amenity slips</strong>, not a marina business. There is no boatyard, no dry stack, no service '
     'bays and no fuel operation across either property. That is why the slip-focused trades are the '
     'direct evidence and the full-service sales are context only.</p>\n'
     f'      <p style="{BODY}max-width:none;font-size:16px;line-height:1.5;'
     'color:rgba(255,255,255,.86);margin:14px 0 0;">The Wylder slips are rebuilt inside the '
     f'<strong style="color:#fff;">${MARINA_PIP:,} marina line</strong> of the renovation program, '
     f'about ${per(MARINA_PIP, SLIPS_W):,} per existing slip. Scope, permits and whether the slips '
     'are rebuilt or replaced all need confirming.</p>\n    </div>\n')
    sn = ('The subject. Twenty-three existing slips at the hotel, with a restaurant and boat bar on '
          'the upland, and twenty-four slips at Dogwood Cove with a four-bedroom residence on about '
          'three acres. Forty-seven combined. The model carries one hundred seventy-nine thousand six '
          'hundred forty-eight of slip revenue at each property in twenty twenty-eight, three hundred '
          'fifty-nine thousand two hundred ninety-six combined, about seven thousand six hundred '
          'forty-five a slip. Slip counts come from lender materials and tour notes, not a survey. '
          'Dogwood Cove sold for four hundred forty-nine thousand in twenty fifteen and is assessed '
          'at eight hundred twenty thousand eight hundred thirty-three as a residential parcel '
          'against an eleven hundred thousand dollar contract.')
    return ('<section data-label="The Subject" data-screen-label="The Subject" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2(f'{SLIPS_T} slips across two waterfront parcels.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1.42fr 1fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def _sale_rows(sales, adjusted):
    out = []
    for s in sales:
        n, loc, drive, d, p, slips, ps = s[:7]
        note = s[-1]
        lab = (f'{n}<div style="{BODY}font-size:12.5px;color:var(--ink-500);margin-top:3px;">'
               f'{loc} &middot; {drive} from Tilghman &middot; {note}</div>')
        vals = [d, f'${p:,}', f'{slips}', f'${ps:,}']
        if adjusted:
            vals.append(f'${s[7]:,}')
        out.append((lab, vals, ''))
    return out


def m_slip_sales():
    cols = ['Property', 'Deed Date', 'Price', 'Slips', 'Per Slip', 'Adjusted to Today']
    left = (sub('Slip-Focused Sales')
     + tbl(cols, _sale_rows(SLIP_SALES, True)
           + [('Median', ['&mdash;', '&mdash;', '&mdash;', '&mdash;', f'${MEDIAN_ADJ:,}'], 'sub'),
              ('Mean', ['&mdash;', '&mdash;', '&mdash;', '&mdash;', f'${MEAN_ADJ:,}'], '')],
           fs='15px', pad=15, lw='2.6fr')
     + para(f'Prices are the recorded deed consideration from the Maryland state assessment file; '
            f'slip counts come from press releases and marina directories. Adjusted to today at '
            f'{TIME_ADJ:.0%} a year, which is conservative: two local resales show faster '
            'appreciation, Bachelor Point at 3.4% a year from 2015 to 2025 and St. Michaels at 11.4% '
            'a year from 2019 to 2021.', fs='15px', auto=True))
    right = (sub('Why These Three Set the Price')
     + '      <div style="height:6px;"></div>\n'
     + ''.join(
        f'      <div style="padding:13px 0;border-bottom:{HAIR};">'
        f'<div style="{CON}font-size:12.5px;letter-spacing:.16em;color:var(--mm-orange);">{t}</div>'
        f'<p style="{BODY}max-width:none;font-size:16px;line-height:1.46;color:var(--ink-700);'
        f'margin:7px 0 0;">{x}</p></div>\n'
        for t, x in [
          ('Amenity Slips, Not a Marina Business',
           'The subject slips sit in front of a hotel with no boatyard, so the trades that are '
           'mostly slips are the direct evidence. After the time adjustment they run '
           f'${26_800:,} to ${48_019:,} a slip.'),
          ('Location Supports the Middle',
           f'The two Talbot County sales, Oxford and Trappe, average ${TALBOT_AVG_ADJ:,} a slip '
           f'adjusted. Mears Point at ${26_800:,} reflects a 540-slip volume discount that does not '
           f'apply to {SLIPS_W} or {SLIPS_D} slips.'),
          ('The Recommendation Sits on the Median',
           f'${REC:,} is the adjusted median of the three. The range of ${LOW:,} to ${HIGH:,} spans '
           'the set, with the top of the range reserved for the Wylder slips once the rebuild is '
           'complete.')])
     + '      <div style="margin-top:auto;padding-top:16px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Adjusted Median', f'${MEDIAN_ADJ:,}', 'The recommendation', pad='16px 14px 0 0',
            vc='var(--mm-orange)')
     + stat('Adjusted Mean', f'${MEAN_ADJ:,}', 'Pulled up by Oxford', pad='16px 14px 0 14px')
     + stat('Talbot County Average', f'${TALBOT_AVG_ADJ:,}', 'The two closest sales', br=False,
            pad='16px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('The three slip-focused sales. DiMillo&rsquo;s in Oxford, forty-five minutes away, sold in '
          'May twenty twenty-one for two million four hundred fifty thousand across sixty slips, '
          'forty thousand eight hundred thirty-three a slip, forty-eight thousand nineteen adjusted. '
          'Gateway Marina in Trappe sold a month later for two million nine hundred fifty thousand '
          'across one hundred twelve slips, thirty thousand eight hundred thirty-seven adjusted. '
          'Mears Point at Kent Narrows sold in May twenty twenty for eleven million nine hundred '
          'fifty thousand across five hundred forty slips, twenty-six thousand eight hundred '
          'adjusted, which carries a volume discount. The median is thirty thousand eight hundred '
          'thirty-seven and that is where the recommendation sits.')
    return ('<section data-label="Slip Sales" data-screen-label="Slip Sales" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2('Three deed-verified sales that are mostly slips.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1.46fr 1fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def m_context_sales():
    left = (sub('Full-Service and Hospitality Trades')
     + tbl(['Property', 'Deed Date', 'Price', 'Slips', 'Per Slip'],
           _sale_rows(CONTEXT_SALES, False), fs='15px', pad=16, lw='2.5fr')
     + para('These four are context, not slip prices. Each price bought a business as well as '
            'frontage: rooms and restaurants at Lowe&rsquo;s Wharf and St. Michaels, a full-service '
            'yard and dry storage at Bachelor Point and Bay Bridge. The subject has none of that.',
            fs='15px', auto=True))
    right = (sub('What They Prove, and What They Do Not')
     + '      <div style="height:6px;"></div>\n'
     + ''.join(
        f'      <div style="padding:14px 0;border-bottom:{HAIR};">'
        f'<div style="{CON}font-size:12.5px;letter-spacing:.16em;color:var(--mm-orange);">{t}</div>'
        f'<p style="{BODY}max-width:none;font-size:16px;line-height:1.46;color:var(--ink-700);'
        f'margin:7px 0 0;">{x}</p></div>\n'
        for t, x in [
          ('Business Value Is Local and Real',
           f'Lowe&rsquo;s Wharf, ten minutes from the subject, sold at ${184_091:,} a slip in August '
           '2024 because the price bought ten rooms, a restaurant and bar, a six-bedroom house and a '
           'fuel operation on 2.5 acres. It went at 81% of a $5.0M ask.'),
          ('Institutional Buyers Pay for Yards',
           f'Bachelor Point at ${125_000:,} and Bay Bridge at ${94_025:,} are both Hinckley '
           'acquisitions of full-service yards with dry and heated storage. Bachelor Point had sold '
           'for $5.0M in 2015, a 3.4% annual gain over ten years.'),
          ('None of It Transfers to Amenity Slips',
           f'The subject&rsquo;s {SLIPS_T} slips carry no dry stack, no service bays and no fuel '
           'business. Pricing them off these trades would be valuing a business that does not exist '
           'here. They are included because they price this shoreline, not because they set the '
           'number.')])
     + '      <div style="margin-top:auto;padding-top:16px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(2,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('Full-Service Range', f'${94_025:,} &ndash; ${184_091:,}', 'Per slip, four local trades',
            pad='16px 16px 0 0', vfs='26px')
     + stat('Amenity Slip Range', f'${26_800:,} &ndash; ${48_019:,}',
            'Per slip, adjusted — the evidence used here', br=False, pad='16px 0 0 16px',
            vc='var(--mm-orange)', vfs='26px')
     + '      </div>\n      </div>\n')
    sn = ('Four further local trades carry a full-service boatyard or hotel and restaurant '
          'operations. Lowe&rsquo;s Wharf Marina Inn in Sherwood, ten minutes away, sold in August '
          'twenty twenty-four for four million fifty thousand across twenty-two slips, one hundred '
          'eighty-four thousand ninety-one a slip, but the price bought ten rooms, a restaurant and '
          'bar, a six-bedroom house and fuel. St. Michaels Marina with three restaurants sold for '
          'seven million seven hundred nine thousand five hundred. Campbell&rsquo;s Boatyard at '
          'Bachelor Point sold to Hinckley for seven million, and Bay Bridge Marina for twenty-two '
          'million eight hundred forty-eight thousand. These show what bay frontage with a business '
          'on it commands locally. They are not slip prices and none of it transfers to amenity '
          'slips.')
    return ('<section data-label="Context Sales" data-screen-label="Context Sales" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2('Four local trades that bought a business, not slips.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1.46fr 1fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def m_income():
    grid = (f'    <div style="display:grid;grid-template-columns:1.3fr repeat(3,1fr);'
            'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(['Revenue per Slip', f'{CAP_LOW:.1%}', f'{CAP:.2%}', f'{CAP_HIGH:.1%}']):
        al = '' if i == 0 else 'text-align:right;'
        bl = '' if i == 0 else f'border-left:{HAIR};'
        cc = 'var(--ink-500)' if i == 0 else ('var(--mm-orange)' if i == 2 else 'var(--mm-navy)')
        grid += (f'      <div style="padding:12px 8px 12px 0;border-bottom:{NAVY2};{bl}{CON}'
                 f'font-size:13.5px;letter-spacing:.12em;color:{cc};{al}">{c}</div>\n')
    for rev in INCOME_GRID:
        noi = round(rev * OCCUPANCY * (1 - OPEX_PC))
        hi = (rev == GROSS_SLIP)
        bg = 'background:rgba(232,119,34,.07);' if hi else ''
        fw = 'font-weight:700;' if hi else ''
        grid += (f'      <div style="padding:17px 8px 17px 0;border-bottom:{HAIR};{bg}{BODY}'
                 f'font-size:16px;color:var(--ink-900);{fw}">${rev:,}</div>\n')
        for c in (CAP_LOW, CAP, CAP_HIGH):
            cc = 'var(--mm-orange-700)' if (hi and c == CAP) else 'var(--ink-900)'
            f2 = 'font-weight:700;' if (hi and c == CAP) else fw
            grid += (f'      <div style="padding:17px 8px;border-bottom:{HAIR};border-left:{HAIR};'
                     f'{bg}{MONO}font-size:16px;text-align:right;color:{cc};{f2}">'
                     f'${round(noi / c):,}</div>\n')
    grid += '    </div>\n'
    left = (sub('Market Rent Case &middot; Assumptions')
     + row('Gross revenue per slip', f'${GROSS_SLIP:,}', pad=11, fs='16px',
           note='Midpoint of cited regional seasonal rates plus some transient')
     + row('Occupancy', f'{OCCUPANCY:.0%}', pad=11, fs='16px')
     + row('Effective gross income per slip', f'${round(GROSS_SLIP*OCCUPANCY):,}', pad=11, fs='16px')
     + row('Operating expense', f'{OPEX_PC:.0%} of effective gross income', pad=11, fs='16px',
           note='Labor, insurance, dock repair and maintenance, utilities, reserves. Unverified')
     + row('Net operating income per slip', f'${NOI_SLIP:,}', pad=11, fs='16px', kind='sub')
     + row('Capitalization rate', f'{CAP:.2%}', pad=11, fs='16px',
           note=f'{CAP_LOW:.1%} to {CAP_HIGH:.1%} tested. Published ranges are wide and are not '
                'verified for this submarket')
     + row('Indicated value per slip', f'${INCOME_SLIP:,}', pad=11, fs='17px', kind='tot')
     + para(f'At ${INCOME_SLIP:,} a slip: Wylder ${INCOME_SLIP*SLIPS_W:,}, Dogwood Cove '
            f'${INCOME_SLIP*SLIPS_D:,}, combined '
            f'<strong style="color:var(--mm-navy-900);">${INCOME_SLIP*SLIPS_T:,}</strong> &mdash; '
            f'{1-INCOME_SLIP/REC:.0%} below the recommendation. Both the expense load and the cap '
            'rate are assumptions; a marina specialist broker opinion would firm them up.',
            fs='15px', auto=True))
    right = (sub('Value per Slip &middot; Revenue Against Cap Rate') + grid
     + para('Regional seasonal slip pricing runs roughly $2,700 to $7,000 a slip: Gratitude Marina '
            'in Rock Hall at $2,700 to $4,050 for 2026, Osprey Point at $5,950 to $7,000 including '
            'dues and electric, and Chestertown&rsquo;s municipal marina at $2,720 to $4,950. '
            'Transient rates in St. Michaels run about $2.60 to $3.95 per foot per night. The '
            '$4,500 case sits mid-range with some transient.', fs='15px', mt='14px')
     + '      <div style="margin-top:auto;padding-top:14px;">\n'
     + f'      <div style="display:grid;grid-template-columns:repeat(3,1fr);align-items:start;'
       f'border-top:{NAVY2};">\n'
     + stat('NOI per Slip', f'${NOI_SLIP:,}', f'{OCCUPANCY:.0%} occupancy, {OPEX_PC:.0%} expense',
            pad='14px 14px 0 0')
     + stat('Indicated Value', f'${INCOME_SLIP:,}', f'Per slip at {CAP:.2%}',
            pad='14px 14px 0 14px', vc='var(--mm-orange)')
     + stat('Against the Recommendation', f'{1-INCOME_SLIP/REC:.0%} below', 'Supports it, does not '
            'set it', br=False, pad='14px 0 0 14px')
     + '      </div>\n      </div>\n')
    sn = ('The income approach on market seasonal rents. Four thousand five hundred dollars of gross '
          'revenue a slip, eighty-five percent occupancy, forty percent operating expense, gives two '
          'thousand two hundred ninety-five of net operating income a slip. At an eight and a half '
          'percent cap rate that is twenty-seven thousand a slip: six hundred twenty-one thousand for '
          'Wylder, six hundred forty-eight thousand for Dogwood Cove, one million two hundred '
          'sixty-nine thousand combined. That is ten percent below the recommendation. The local '
          'sales are weighted more heavily because they price this specific shoreline, so the income '
          'approach supports the number rather than setting it. Both the expense load and the cap '
          'rate are assumptions.')
    return ('<section data-label="Income Approach" data-screen-label="Income Approach" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 92px 42px') + '>\n'
     + h2(f'Market seasonal rents support ${INCOME_SLIP:,} a slip.', fs='42px', mb='18px', pb='15px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.04fr;gap:46px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


def m_model_case():
    c = (bigcol('Model as Built', f'${val(MODEL_NOI, CAP)/1e6:,.2f}M',
          f'${per(val(MODEL_NOI, CAP), SLIPS_T):,} per slip at {CAP:.2%}',
          dkv('Slip revenue, 2028', f'${SLIP_REV_2028:,}')
          + dkv('Expense load', f'{MODEL_OPEX:.1%}')
          + dkv('Net operating income', f'${MODEL_NOI:,}')
          + dkv(f'Value at {CAP:.2%}', f'${val(MODEL_NOI, CAP):,}', accent=True, last=True),
          'first', fs='72px')
     + bigcol('Underwriter View', f'${val(UW_NOI, CAP)/1e6:,.2f}M',
          f'${per(val(UW_NOI, CAP), SLIPS_T):,} per slip at {CAP:.2%}',
          dkv('Slip revenue, 2028', f'${SLIP_REV_2028:,}')
          + dkv('Expense load', f'{UW_OPEX:.0%}')
          + dkv('Net operating income', f'${UW_NOI:,}')
          + dkv(f'Value at {CAP:.2%}', f'${val(UW_NOI, CAP):,}', accent=True, last=True),
          'mid', fs='72px')
     + bigcol('Carried Here', f'${SLIPS_T*REC/1e6:,.2f}M', f'${REC:,} per slip, on the local sales',
          dkv('Model revenue per slip', f'${per(SLIP_REV_2028, SLIPS_T):,}')
          + dkv('Market rent assumption', f'${GROSS_SLIP:,}')
          + dkv('The premium', f'{per(SLIP_REV_2028, SLIPS_T)/GROSS_SLIP:.1f}x')
          + dkv('Carried as collateral', f'${SLIPS_T*REC:,}', accent=True, last=True),
          'last', fs='72px'))
    b = (blk('The Premium Has to Be Earned',
             f'The model&rsquo;s ${per(SLIP_REV_2028, SLIPS_T):,} a slip is about '
             f'{per(SLIP_REV_2028, SLIPS_T)/GROSS_SLIP:.1f} times the market rent assumption. That '
             'only holds if hotel guests and transient boaters fill the slips at nightly rates, '
             'which is plausible for a resort marina but unproven here.')
     + blk('Upside, Not Collateral',
           f'At the underwriter expense load the model case still indicates ${val(UW_NOI, CAP):,} '
           f'to ${val(MODEL_NOI, CAP):,}, or ${per(val(UW_NOI, CAP), SLIPS_T):,} to '
           f'${per(val(MODEL_NOI, CAP), SLIPS_T):,} a slip &mdash; well above the recommendation. '
           'It is treated as upside to be proven, not value to lend against.')
     + blk('What Would Prove It',
           'A trailing three-year marina profit and loss statement. It was promised in earlier '
           'lender questions and is still the document that decides whether this case is credible. '
           'Until it exists the sales approach governs.'))
    sn = ('The sponsor model case. The model carries three hundred fifty-nine thousand two hundred '
          'ninety-six of slip revenue in twenty twenty-eight against a seventeen point one percent '
          'expense load, which is two hundred ninety-seven thousand eight hundred fifty-six of net '
          'operating income and three and a half million of value at eight and a half percent, '
          'seventy-four thousand five hundred fifty-seven a slip. Loading expenses to thirty-five '
          'percent to add insurance, dock repair and maintenance, labor and reserves gives two '
          'hundred thirty-three thousand five hundred forty-two and two million seven hundred '
          'forty-seven thousand, fifty-eight thousand four hundred fifty-nine a slip. Both are well '
          'above the thirty thousand carried here. The model implies seven thousand six hundred '
          'forty-five a slip of revenue, about one point seven times the market rent assumption. '
          'That is upside to be proven with a trailing marina profit and loss, not collateral value '
          'today.')
    return darkpage('Sponsor Model Case', 'What the model implies, and why it is not the number.',
                    sn, c, b)


def m_risks():
    items = [
      ('Slip Counts', f'Confirm {SLIPS_W} and {SLIPS_D} against a survey, the Dogwood Cove purchase '
       'and sale agreement and the riparian permits. Every value here scales linearly with the '
       'count.'),
      ('Commercial Use of the Dogwood Cove Slips', 'Using the 24 slips commercially as part of the '
       'hotel needs Talbot County zoning, Critical Area and state environmental confirmation. This '
       f'is the difference between about ${DOGWOOD_ASIS:,} and ${SLIPS_D*REC:,}.'),
      ('Marina Rebuild', f'The ${MARINA_PIP:,} marina line is about '
       f'${per(MARINA_PIP, SLIPS_W):,} per existing slip. Confirm scope, permits, and whether the '
       f'{SLIPS_W} slips are rebuilt in place or replaced.'),
      ('Historical Marina Revenue', 'The three-year marina schedule is the key open document. It '
       'decides whether the sponsor model case is credible.'),
      ('Cap Rate and Expense Load', 'Both are assumptions. Published marina cap rates run roughly '
       '8% to 14%; the expense load is unverified for this operation. A marina specialist broker '
       'opinion would firm both up.'),
      ('Comp Verification', 'Deed prices come from the state assessment file. Multiple-parcel deeds '
       'may include land beyond the marina, and one directory address should be reconciled against '
       f'the recorded parcel. Slip counts come from press releases and directories. The {TIME_ADJ:.0%} '
       'time adjustment is an assumption.'),
    ]
    cells = ''
    for i, (t, x) in enumerate(items):
        br = '' if i % 2 == 1 else f'border-right:{DRULE};'
        bb = f'border-bottom:{DRULE};' if i < 4 else ''
        pl = '0 40px 0 0' if i % 2 == 0 else '0 0 0 40px'
        cells += (f'    <div style="padding:{"26px" if i > 1 else "0"} 0 26px;{br}{bb}">\n'
                  f'      <div style="padding:{pl};">\n'
                  f'        <div style="{CON}font-size:13px;letter-spacing:.18em;'
                  f'color:var(--mm-orange);margin-bottom:9px;">{t}</div>\n'
                  f'        <p style="{BODY}max-width:none;font-size:16.5px;line-height:1.48;'
                  f'color:#fff;margin:0;">{x}</p>\n      </div>\n    </div>\n')
    sn = ('Risks and open items. Slip counts need confirming against a survey and the purchase and '
          'sale agreement, because every value scales with them. Commercial use of the Dogwood Cove '
          'slips needs county zoning, Critical Area and state environmental confirmation, and that is '
          'the difference between about two hundred eighty thousand and seven hundred twenty '
          'thousand. The marina rebuild scope and permits need confirming. The three-year marina '
          'revenue schedule is still outstanding. The cap rate and the expense load are both '
          'assumptions. And the comparable deed prices come from the state assessment file, so '
          'multiple-parcel deeds and slip counts from directories should be verified.')
    return ('<section data-label="Risks and Open Items" data-screen-label="Risks" '
     f'data-speaker-notes="{sn}" ' + sec(dark=True, pad='64px 96px 48px') + '>\n'
     + h2('Risks and open items.', dark=True, fs='46px', mb='26px', pb='20px')
     + '  <div style="display:grid;grid-template-columns:1fr 1fr;flex:1;align-content:start;">\n'
     + cells + '  </div>\n@@FOOTER@@\n</section>')


def m_contact():
    sn = ('The deed records, the rate sources and the comparable detail behind this analysis are '
          'available on request. Bradley M. Buzil, Senior Director, The TRANCHE Group at Marcus and '
          'Millichap Capital Corporation.')
    stats = [('Recommended', f'${REC:,} / slip'), (f'Combined · {SLIPS_T} Slips',
             f'${SLIPS_T*REC:,}'), ('Range', f'${LOW:,} &ndash; ${HIGH:,}')]
    st = ''
    for i, (lab, v) in enumerate(stats):
        pad = ('18px 40px 0 0' if i == 0 else ('18px 40px 0' if i == 1 else '18px 0 0 40px'))
        bl = '' if i == 0 else 'border-left:1px solid rgba(255,255,255,.2);'
        lc = 'var(--mm-orange-100)' if i == 2 else 'var(--mm-navy-100)'
        vc = 'var(--mm-orange)' if i == 2 else '#fff'
        st += (f'      <div style="padding:{pad};{bl}">'
               f'<div style="{CON}font-size:13px;letter-spacing:.18em;color:{lc};">{lab}</div>'
               f'<div style="{MONO}font-size:26px;font-weight:700;color:{vc};margin-top:6px;">{v}'
               '</div></div>\n')
    return ('<section data-label="Next Steps" data-screen-label="Contact" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:space-between;padding:88px 100px;">\n'
     '  <img src="assets/wt-aerial.png" alt="Wylder Hotel Tilghman Island aerial" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,17,34,.86) 0%,'
     'rgba(0,17,34,.66) 45%,rgba(0,17,34,.92) 100%);"></div>\n'
     '  <div style="position:absolute;left:0;right:0;top:0;height:14px;display:flex;">'
     '<div style="flex:0 0 60%;background:#F0720E;"></div>'
     '<div style="flex:0 0 40%;background:#456EAB;"></div></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;padding-top:16px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:56px;">\n'
     '    <div style="display:flex;align-items:center;gap:20px;">'
     f'<span style="{CON}font-size:15px;letter-spacing:.26em;color:var(--mm-orange-100);">'
     f'{EYEBROW}</span>'
     '<span style="font-family:var(--font-mono);font-size:15px;font-weight:700;letter-spacing:.08em;'
     'color:rgba(255,255,255,.62);padding-left:20px;border-left:1px solid rgba(255,255,255,.32);">09'
     '</span></div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;max-width:1220px;">\n'
     f'    <h2 style="{DISP}font-weight:700;font-size:72px;line-height:1.02;letter-spacing:-0.015em;'
     'margin:0 0 26px;text-shadow:0 2px 24px rgba(0,17,34,.5);">Contact and next steps.</h2>\n'
     f'    <p style="{BODY}font-size:25px;line-height:1.55;color:#fff;margin:0 0 26px;max-width:90ch;'
     'text-shadow:0 1px 12px rgba(0,17,34,.4);">The deed records, the rate sources and the '
     'comparable detail behind this analysis are available on request, along with the marina '
     'schedule once the sponsor provides it.</p>\n'
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
     f'margin-top:10px;">Exclusive Capital Advisor &middot; {MARINA_LABEL}</div>\n'
     '    </div>\n  </div>\n</section>' + TAIL)


MARINA_DECK = [('TITLE', m_title), ('CONCLUSION', m_conclusion), ('THE SUBJECT', m_subject),
               ('SLIP SALES', m_slip_sales), ('CONTEXT SALES', m_context_sales),
               ('INCOME APPROACH', m_income), ('SPONSOR MODEL CASE', m_model_case),
               ('RISKS AND OPEN ITEMS', m_risks), ('CONTACT', m_contact)]
MARINA_DARK = {'SPONSOR MODEL CASE', 'RISKS AND OPEN ITEMS'}


def build_marina_deck():
    """Write the standalone marina valuation deck beside the capitalization packages."""
    from v7_lib import load_sections, write_deck, DECKDIR
    from v7_num import renumber
    head, _ = load_sections()
    body = {n: fn() for n, fn in MARINA_DECK}
    path = f'{DECKDIR}/Wylder Tilghman Island - Marina Valuation.dc.html'
    n = write_deck(path, head, [k for k, _ in MARINA_DECK], body, MARINA_LABEL)
    renumber(path, MARINA_LABEL, dark=MARINA_DARK)
    import io as _io
    s = _io.open(path, encoding='utf-8').read()
    bad = [w for w in ('appraisal', 'appraised', 'appraiser', 'LWHA', 'Newmark', 'CBRE',
                       'AI search', 'New Day') if w.lower() in s.lower()]
    brit = [w for w in ('utilise', 'organis', 'centre', 'labour', 'metres', 'colour', 'favour',
                        'analyse') if w in s.lower()]
    print(f'  {path.split("/")[-1]}  —  {n} pages')
    print(f'  forbidden references: {bad or "none"}')
    print(f'  British spelling: {brit or "none"}')
    return path


if __name__ == '__main__':
    build_marina_deck()
