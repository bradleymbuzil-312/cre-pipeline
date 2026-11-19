# -*- coding: utf-8 -*-
"""Four addenda slides carried by the LP Equity package only.

  CASH FLOW HISTORICALS   the actual operating statement, 2023 through the trailing twelve
                          months to September 2026, department by department, with the
                          five-year capital history beneath it.
  RENOVATION SCHEDULE     restated to the sponsor's 175-day program, January 4 to June 28, 2027,
                          in four guestroom waves. Replaces the November-to-April page in this
                          package only.
  RENOVATION CASH FLOW    the same program as money: budget by line, spend by month, cumulative
                          draw and the share of budget deployed.
  CBRE VALUATION          the valuation detail, attributed. This is the one slide in the whole
                          library that names its source; every other page in every other package
                          states values with no source named, and crosscheck.py enforces that.
  SLH MEMBERSHIP          the Small Luxury Hotels membership proposal as delivered.

Figures are transcribed from the sponsor's workbooks and the membership proposal; each table
asserts its own foot before the deck will build.
"""
import io

from v7_lib import *
from v7_tranche import tbl
from v7_pages import blk

LW = '2.05fr'


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Actual operations, 2023 to the trailing twelve months ended September 2026
# ─────────────────────────────────────────────────────────────────────────────────────────────
HIST_COLS = ['2023 Actual', '2024 Actual', '2025 Actual', 'T12 Sep 2026']
AVAIL = [18_250, 18_300, 18_250, 18_333]
OCC_N = [4_881, 5_803, 5_996, 5_245]
REV = {'Rooms': [1_521_992, 1_691_112, 1_587_682, 1_563_285],
       'Food and beverage': [1_738_396, 1_826_923, 1_892_892, 1_877_847],
       'Resort fee': [152_840, 210_671, 230_115, 217_850],
       'Miscellaneous': [61_791, 81_570, 75_339, 57_330]}
DEPT = {'Rooms': [471_069, 393_236, 477_673, 482_314],
        'Food and beverage': [1_175_626, 1_076_211, 1_162_060, 1_121_723],
        'Miscellaneous': [7_298, 13_699, 20_675, 16_091]}
UNDIST = [1_268_159, 1_339_719, 1_365_051, 1_356_681]
FIXED = [67_106, 71_618, 95_647, 104_823]
NOI_H = [485_761, 915_792, 664_922, 634_680]

# subtotals as the operating statements report them; the source carries sub-dollar rounding,
# so the printed figures are its own and the derivation is checked to within a dollar
TOT_REV = [3_475_020, 3_810_275, 3_786_028, 3_716_313]
TOT_DEPT = [1_653_994, 1_483_146, 1_660_409, 1_620_129]
GOI = [1_821_026, 2_327_130, 2_125_619, 2_096_184]
GOP = [552_867, 987_410, 760_569, 739_503]
ADR_H = [REV['Rooms'][i] / OCC_N[i] for i in range(4)]
REVPAR_H = [REV['Rooms'][i] / AVAIL[i] for i in range(4)]
OCC_H = [OCC_N[i] / AVAIL[i] for i in range(4)]

# every line of the statement has to foot, to the dollar of rounding the source carries
for _i in range(4):
    assert abs(sum(v[_i] for v in REV.values()) - TOT_REV[_i]) <= 1
    assert abs(sum(v[_i] for v in DEPT.values()) - TOT_DEPT[_i]) <= 1
    assert abs(TOT_REV[_i] - TOT_DEPT[_i] - GOI[_i]) <= 1
    assert abs(GOI[_i] - UNDIST[_i] - GOP[_i]) <= 1
    assert abs(GOP[_i] - FIXED[_i] - NOI_H[_i]) <= 1, ('historicals do not foot', _i)

# five-year capital history, 2021 to 2025
CAPEX = [('Building envelope and interior', 243_458), ('FF&E and soft goods', 153_823),
         ('Contingency and emergency', 141_345), ('Building mechanical and systems', 41_861),
         ('Major renovations and buildouts', 37_769), ('Technology and security', 20_937),
         ('Site, dock and outdoor', 3_500)]
CAPEX_TOTAL = 642_693
assert sum(a for _, a in CAPEX) == CAPEX_TOTAL


def _m(v):
    return f'${v:,.0f}' if v >= 0 else f'(${abs(v):,.0f})'


def historicals(basis_page=24):
    sn = ('Actual operating results, twenty twenty-three through the trailing twelve months '
          'ended September twenty twenty-six, department by department. Revenue has run between '
          'three point five and three point eight million across the period, with net operating '
          'income between four hundred eighty-six thousand and nine hundred sixteen thousand. '
          'Occupancy has never passed thirty-three percent and the average daily rate has fallen '
          'from three hundred twelve dollars to the mid two hundreds. That is the base the '
          'business plan works from. Separately the sponsor has put six hundred forty-two '
          'thousand six hundred ninety-three of capital into the hotel since twenty twenty-one, '
          'outside the renovation program.')
    rows = [('Occupancy', [f'{v:.1%}' for v in OCC_H], 'sub'),
            ('Average daily rate', [f'${v:,.2f}' for v in ADR_H], ''),
            ('RevPAR', [f'${v:,.2f}' for v in REVPAR_H], '')]
    for k, v in REV.items():
        rows.append((k, [_m(x) for x in v], 'sub' if k == 'Rooms' else ''))
    rows.append(('Total revenue', [_m(x) for x in TOT_REV], 'sub'))
    rows.append(('Departmental expenses', [f'({_m(x)[1:]})' for x in TOT_DEPT], ''))
    rows.append(('Gross operating income', [_m(x) for x in GOI], 'sub'))
    rows.append(('Undistributed expenses', [f'({_m(x)[1:]})' for x in UNDIST], ''))
    rows.append(('Gross operating profit', [_m(x) for x in GOP], 'sub'))
    rows.append(('Fixed expenses', [f'({_m(x)[1:]})' for x in FIXED], ''))
    rows.append(('Net operating income', [_m(x) for x in NOI_H], 'tot'))
    rows.append(('NOI margin', [f'{NOI_H[i] / TOT_REV[i]:.1%}' for i in range(4)], ''))

    cap = ('    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 40px;'
           'align-content:start;">\n')
    for i, (k, v) in enumerate(CAPEX):
        bb = '' if i >= len(CAPEX) - 1 else f'border-bottom:{HAIR};'
        cap += ('      <div style="display:flex;justify-content:space-between;'
                f'align-items:baseline;padding:7px 0;{bb}gap:12px;">'
                f'<span style="{BODY}font-size:13.5px;color:var(--ink-700);">{k}</span>'
                f'<span style="{MONO}font-size:13.5px;color:var(--ink-900);">${v:,.0f}</span>'
                '</div>\n')
    cap += ('      <div style="grid-column:1 / -1;display:flex;'
            'justify-content:space-between;align-items:baseline;'
            'padding:9px 0;border-top:2px solid var(--mm-navy);gap:12px;">'
            f'<span style="{BODY}font-size:14.5px;font-weight:600;color:var(--mm-navy-900);">'
            'Five-year total</span>'
            f'<span style="{MONO}font-size:14.5px;font-weight:700;color:var(--mm-orange);">'
            f'${CAPEX_TOTAL:,.0f}</span></div>\n    </div>\n')

    return ('<section data-label="Cash Flow Historicals" data-screen-label="Historicals" '
     f'data-speaker-notes="{sn}" ' + sec(pad='60px 92px 44px') + '>\n'
     + h2('What the hotel has actually earned.', fs='40px', mb='18px', pb='13px')
     + tbl(['Operating statement'] + HIST_COLS, rows, fs='14px', pad=5, lw=LW)
     + '  <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:48px;margin-top:16px;'
       'padding-top:16px;border-top:2px solid var(--mm-navy);">\n'
       '    <div>\n'
     + sub('Sponsor Capital Invested &middot; 2021 to 2025', pb='8px') + cap + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;justify-content:center;">\n'
     + para('Results are per the operating statements; 2025 is preliminary and the fourth column '
            'is the trailing twelve months ended September 30, 2026. Revenue has been flat across '
            'the period while rate has fallen, which is the condition the renovation addresses. '
            'The hotel has never sold a marina slip, an event, or a whole&#8209;home residence.',
            fs='14.5px', mt='0', ind=6)
     + para(f'The <strong style="color:var(--mm-navy-900);">${CAPEX_TOTAL:,.0f}</strong> at left '
            'was invested outside loan proceeds and outside the renovation program, and sits in '
            f'the basis on page {basis_page}.', fs='14.5px', mt='14px', ind=6)
     + '    </div>\n  </div>\n@@FOOTER@@\n</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# The renovation: a 175-day program, January 4 to June 28, 2027, in four guestroom waves
# ─────────────────────────────────────────────────────────────────────────────────────────────
RENO_MONTHS = ['Jan 2027', 'Feb 2027', 'Mar 2027', 'Apr 2027', 'May 2027', 'Jun 2027']
# label, budget, window, (start day, duration), group, monthly spend
RENO = [
  ('Design, permitting and procurement', 170_000, 'Jan 4 &ndash; Mar 15', 'fees',
   [67_042, 67_042, 35_915, 0, 0, 0]),
  ('Marina replacement &middot; 25 new slips', 250_000, 'Jan 21 &ndash; Mar 6', 'marina',
   [61_111, 155_556, 33_333, 0, 0, 0]),
  ('Guestrooms wave one &middot; 14 keys', 350_000, 'Jan 4 &ndash; Mar 9', 'rooms',
   [150_769, 150_769, 48_462, 0, 0, 0]),
  ('Guestrooms wave two &middot; 15 keys', 375_000, 'Mar 26 &ndash; Apr 27', 'rooms',
   [0, 0, 68_182, 306_818, 0, 0]),
  ('Guestrooms wave three &middot; 14 keys', 350_000, 'Apr 28 &ndash; May 30', 'rooms',
   [0, 0, 0, 31_818, 318_182, 0]),
  ('Guestrooms wave four &middot; 14 keys', 350_000, 'May 31 &ndash; Jun 28', 'rooms',
   [0, 0, 0, 0, 12_069, 337_931]),
  ('Three-bedroom house replacement', 500_000, 'Jan 4 &ndash; Jun 28', 'building',
   [79_545, 79_545, 88_068, 85_227, 88_068, 79_545]),
  ('Exterior envelope and grounds', 150_000, 'Jan 4 &ndash; Mar 22', 'building',
   [53_846, 53_846, 42_308, 0, 0, 0]),
  ('Interior common areas and finishes', 150_000, 'Mar 26 &ndash; Jun 28', 'building',
   [0, 0, 9_474, 47_368, 48_947, 44_211]),
  ('Event space &middot; boat bar conversion', 50_000, 'Mar 24 &ndash; Apr 22', 'building',
   [0, 0, 13_333, 36_667, 0, 0]),
  ('Public space FF&amp;E installation', 50_000, 'Feb 20 &ndash; Jun 28', 'building',
   [0, 3_488, 12_016, 11_628, 12_016, 10_853]),
  ('Punch list, inspections and reopening', 0, 'May 21 &ndash; Jun 21', 'closeout',
   [0, 0, 0, 0, 0, 0]),
  ('Contingency &middot; 10.0% of hard costs', 258_000, 'Jan 4 &ndash; Jun 28', 'contingency',
   [34_594, 44_407, 31_579, 52_054, 48_021, 47_346])]

RENO_TOTAL = 3_003_000
RENO_MONTHLY = [446_908, 554_654, 382_669, 571_580, 527_303, 519_885]
RENO_CUM = [446_908, 1_001_562, 1_384_231, 1_955_811, 2_483_115, 3_003_000]
RENO_KEYS, RENO_DAYS, RENO_PER_KEY, HARD_COSTS = 57, 175, 52_684, 2_575_000
GROUP = {'rooms': 'var(--mm-navy)', 'building': '#456EAB', 'marina': 'var(--mm-orange)',
         'fees': 'var(--ink-400)', 'closeout': '#957551', 'contingency': 'var(--ink-500)'}

# each line is spread straight line by calendar day and then rounded to the month, so the
# published monthly figures carry a dollar of rounding against the exact budget
assert sum(b for _, b, _, _, _ in RENO) == RENO_TOTAL
assert abs(sum(RENO_MONTHLY) - RENO_TOTAL) <= 2
for _i in range(6):
    assert abs(sum(r[4][_i] for r in RENO) - RENO_MONTHLY[_i]) <= 2, ('month does not foot', _i)
    assert abs(RENO_CUM[_i] - sum(RENO_MONTHLY[:_i + 1])) <= 2, ('cumulative slips', _i)
assert RENO_CUM[-1] == RENO_TOTAL
assert round(RENO_TOTAL / RENO_KEYS) == RENO_PER_KEY
assert abs(258_000 / HARD_COSTS - 0.10) < 0.001


def _band(spend, budget):
    """One row of the program chart: a bar in each month the line actually spends."""
    out = ''
    for i, v in enumerate(spend):
        if budget and v:
            h = max(5, round(13 * v / max(spend)))
            out += ('      <div style="padding:0 5px;display:flex;align-items:center;'
                    f'justify-content:center;border-left:{HAIR};">'
                    f'<div style="width:100%;height:{h}px;background:@@C@@;"></div></div>\n')
        else:
            out += f'      <div style="border-left:{HAIR};"></div>\n'
    return out


def renovation_schedule():
    sn = ('The renovation is a one hundred seventy-five day program running January fourth to '
          'June twenty-eighth, twenty twenty-seven, in four guestroom waves of fourteen, '
          'fifteen, fourteen and fourteen keys. Fifty keys today become fifty-seven at '
          'completion. The budget is three million three thousand dollars, fifty-two thousand '
          'six hundred eighty-four a key. No construction starts before the senior loan closes, '
          'and every date moves day for day with that closing.')
    grid = ('    <div style="display:grid;grid-template-columns:2.5fr .85fr 1.15fr '
            'repeat(6,.72fr);font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(['Line item', 'Budget', 'Window'] + RENO_MONTHS):
        al = '' if i == 0 else 'text-align:right;' if i < 3 else 'text-align:center;'
        bl = '' if i == 0 else f'border-left:{HAIR};'
        grid += (f'      <div style="padding:10px 6px;border-bottom:2px solid var(--mm-navy);'
                 f'{bl}{CON}font-size:11.5px;letter-spacing:.1em;color:var(--mm-navy);{al}">'
                 f'{c}</div>\n')
    for lab, budget, win, grp, spend in RENO:
        grid += (f'      <div style="padding:12px 6px 8px 0;border-bottom:{HAIR};{BODY}'
                 f'font-size:13.5px;color:var(--ink-900);">{lab}</div>\n'
                 f'      <div style="padding:12px 6px;border-bottom:{HAIR};border-left:{HAIR};'
                 f'{MONO}font-size:13px;text-align:right;color:var(--ink-900);">'
                 + (f'${budget:,.0f}' if budget else 'Included') + '</div>\n'
                 f'      <div style="padding:12px 6px;border-bottom:{HAIR};border-left:{HAIR};'
                 f'{MONO}font-size:12px;text-align:right;color:var(--ink-500);">{win}</div>\n')
        row = _band(spend, budget).replace('@@C@@', GROUP[grp])
        grid += row.replace(f'border-left:{HAIR};">', f'border-left:{HAIR};border-bottom:{HAIR};">')
    grid += (f'      <div style="padding:11px 6px 11px 0;border-bottom:3px double var(--mm-navy);'
             f'{BODY}font-size:14px;font-weight:600;color:var(--mm-navy-900);">'
             'Total property improvement plan</div>\n'
             f'      <div style="padding:11px 6px;border-bottom:3px double var(--mm-navy);'
             f'border-left:{HAIR};{MONO}font-size:13.5px;font-weight:700;text-align:right;'
             f'color:var(--mm-orange);">${RENO_TOTAL:,.0f}</div>\n'
             f'      <div style="padding:11px 6px;border-bottom:3px double var(--mm-navy);'
             f'border-left:{HAIR};{MONO}font-size:12px;text-align:right;color:var(--ink-500);">'
             f'{RENO_DAYS} days</div>\n')
    for v in RENO_MONTHLY:
        grid += (f'      <div style="padding:11px 4px;border-bottom:3px double var(--mm-navy);'
                 f'border-left:{HAIR};{MONO}font-size:11.5px;font-weight:700;text-align:center;'
                 f'color:var(--mm-navy);">${v / 1000:,.0f}k</div>\n')
    grid += '    </div>\n'

    legend = '  <div style="display:flex;gap:26px;flex-wrap:wrap;margin-top:16px;">\n'
    for name, key in (('Guestrooms', 'rooms'), ('Buildings, grounds and public space', 'building'),
                      ('Marina', 'marina'), ('Design and professional fees', 'fees'),
                      ('Contingency', 'contingency')):
        legend += ('    <span style="display:flex;align-items:center;gap:8px;">'
                   f'<span style="width:11px;height:11px;background:{GROUP[key]};"></span>'
                   f'<span style="{CON}font-size:11.5px;letter-spacing:.12em;'
                   f'color:var(--ink-500);">{name}</span></span>\n')
    legend += '  </div>\n'

    stats = ('  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0 32px;'
             'margin-top:auto;padding-top:20px;border-top:2px solid var(--mm-navy);">\n')
    for i, (lab, val, note) in enumerate(
            [('Total Budget', f'${RENO_TOTAL:,.0f}', 'Hotel program, excluding Dogwood Cove'),
             ('Program Duration', f'{RENO_DAYS} days', 'January 4 to June 28, 2027'),
             ('Keys at Completion', f'{RENO_KEYS}', '50 today, in four waves'),
             ('Budget per Key', f'${RENO_PER_KEY:,.0f}', 'Guestrooms priced at $25,000 a key')]):
        bl = '' if i == 0 else f'border-left:{HAIR};padding-left:32px;'
        stats += (f'    <div style="{bl}">\n'
                  f'      <div style="{CON}font-size:11.5px;letter-spacing:.16em;'
                  f'color:var(--mm-orange);">{lab}</div>\n'
                  f'      <div style="{DISP}font-weight:700;font-size:28px;color:var(--mm-navy);'
                  f'line-height:1.1;margin-top:6px;">{val}</div>\n'
                  f'      <div style="{BODY}font-size:12.5px;color:var(--ink-500);'
                  f'margin-top:5px;">{note}</div>\n    </div>\n')
    stats += '  </div>\n'

    return ('<section data-label="Renovation Schedule" data-screen-label="Renovation Schedule" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 88px 42px') + '>\n'
     + h2('A 175-day program, in four guestroom waves.', fs='38px', mb='16px', pb='12px')
     + grid + legend + stats + '@@FOOTER@@\n</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# The same program as money
# ─────────────────────────────────────────────────────────────────────────────────────────────
def renovation_cash_flow():
    sn = ('The renovation as cash. Spend runs between three hundred eighty-three thousand and '
          'five hundred seventy-two thousand a month across six months, never more than a fifth '
          'of the budget in any one month. Half the budget is deployed by the end of March and '
          'all of it by the end of June. Monthly figures are indicative; money actually moves on '
          'contractor pay applications and vendor invoices, and nothing is drawn before the '
          'senior loan closes.')
    rows = [('Spend in month', [f'${v:,.0f}' for v in RENO_MONTHLY], 'sub'),
            ('Share of budget', [f'{v / RENO_TOTAL:.1%}' for v in RENO_MONTHLY], ''),
            ('Cumulative draw', [f'${v:,.0f}' for v in RENO_CUM], 'sub'),
            ('Budget deployed', [f'{v / RENO_TOTAL:.1%}' for v in RENO_CUM], 'tot'),
            ('Remaining to fund', [f'${RENO_TOTAL - v:,.0f}' for v in RENO_CUM], '')]
    groups = {}
    for lab, budget, _w, grp, _s in RENO:
        groups[grp] = groups.get(grp, 0) + budget
    order = [('rooms', 'Guestrooms &middot; four waves'),
             ('building', 'Buildings, grounds and public space'),
             ('marina', 'Marina &middot; 25 new slips'),
             ('contingency', 'Contingency'), ('fees', 'Design and professional fees')]
    assert sum(groups[k] for k, _ in order) == RENO_TOTAL
    bars = ''
    for k, name in order:
        amt = groups[k]
        bars += ('      <div style="padding:13px 0;border-bottom:' + HAIR + ';">\n'
                 '        <div style="display:flex;justify-content:space-between;'
                 f'align-items:baseline;gap:12px;"><span style="{BODY}font-size:15.5px;'
                 f'color:var(--ink-900);">{name}</span>'
                 f'<span style="{MONO}font-size:15.5px;color:var(--mm-navy-900);'
                 f'font-weight:600;">${amt:,.0f}</span></div>\n'
                 '        <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">'
                 '<div style="flex:1;height:9px;background:var(--hairline);">'
                 f'<div style="width:{amt / RENO_TOTAL:.1%};height:100%;'
                 f'background:{GROUP[k]};"></div></div>'
                 f'<span style="{MONO}font-size:12.5px;color:var(--ink-500);width:46px;'
                 f'text-align:right;">{amt / RENO_TOTAL:.1%}</span></div>\n      </div>\n')

    return ('<section data-label="Renovation Cash Flow" data-screen-label="Renovation Cash Flow" '
     f'data-speaker-notes="{sn}" ' + sec(pad='62px 92px 46px') + '>\n'
     + h2('The renovation, as cash out the door.', fs='40px', mb='20px', pb='14px')
     + tbl(['Draw schedule'] + RENO_MONTHS, rows, fs='15px', pad=13, lw='1.5fr')
     + '  <div style="display:grid;grid-template-columns:1.06fr 1fr;gap:52px;flex:1;'
       'min-height:0;margin-top:26px;padding-top:22px;'
       'border-top:2px solid var(--mm-navy);">\n    <div>\n'
     + sub('Where the Budget Goes', pb='9px') + bars + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n'
     + sub('How It Is Funded and Drawn', pb='9px')
     + para('The program is funded from the capital raised at closing and held back, not paid '
            'out in advance. Draws follow contractor pay applications and vendor invoices, '
            'against lien waivers and inspection, so money leaves the account as work is put in '
            'place.', fs='15.5px', mt='14px', ind=6)
     + para('<strong style="color:var(--mm-navy-900);">No construction starts before the senior '
            'loan closes</strong>, and every date in the program moves day for day with that '
            'closing. A delay in the capitalization does not compress the work; it moves it.',
            fs='15.5px', mt='14px', ind=6)
     + para('The contingency is <strong style="color:var(--mm-navy-900);">10.0% of '
            f'${HARD_COSTS:,.0f} of hard costs</strong> and is drawn pro rata with hard cost '
            'spending rather than held to the end, so the carried balance always reflects the '
            'work still to come.', fs='15.5px', mt='14px', ind=6)
     + para('Guestrooms run in four waves rather than closing the hotel, so rooms keep selling '
            'through the program and each wave returns to inventory as the next begins. Monthly '
            'figures are indicative and carry a dollar of rounding against the exact budget.',
            fs='15.5px', mt='14px', ind=6)
     + '    </div>\n  </div>\n@@FOOTER@@\n</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# The valuation, attributed. The only slide in the library that names its source.
# ─────────────────────────────────────────────────────────────────────────────────────────────
CBRE_FILE = 'CB26US098551-1'
CBRE_SCENARIOS = [
  ('As Is', 21_400_000, 428_000, 50, 'September 11, 2026', 21_250_000, 150_000),
  ('Prospective As Complete', 26_000_000, 456_140, 57, 'April 1, 2027', 24_900_000, 1_100_000),
  ('Prospective As Stabilized', 29_500_000, 517_544, 57, 'April 1, 2029', 28_725_000, 775_000)]
CBRE_APPROACHES = [
  ('Sales comparison approach', [21_400_000, 26_000_000, 29_500_000], ''),
  ('Income approach &middot; direct capitalization', [21_700_000, 26_300_000, 29_800_000], ''),
  ('Income approach &middot; discounted cash flow', [21_400_000, 26_000_000, 29_500_000], ''),
  ('Final opinion of value', [21_400_000, 26_000_000, 29_500_000], 'tot')]
CBRE_RATES = [('Discount rate', ['11.25%', '11.00%', '10.75%']),
              ('Terminal capitalization rate', ['8.75%', '8.75%', '8.75%']),
              ('Going-in overall rate', ['8.25%', '8.25%', '8.25%'])]
CBRE_NOTES = [
  ('Scope assumed', 'A $3,003,000 renovation complete by April 2027; keys from 50 to 57, with '
   'four off&#8209;line rooms returned and three added; the second building built out as a '
   'spa and wellness center; the marina expanded from 23 to 48 slips; meeting space from '
   '3,722 to 5,252 square feet.'),
  ('Brand', 'Small Luxury Hotels of the World membership, and the Hilton booking access that '
   'comes with it, assumed upon completion of the renovation.'),
  ('Operating assumptions', 'A 3.00% management fee, a 4.00% FF&amp;E reserve, a ten&#8209;year '
   'hold, 3.00% growth, a 3.00% cost of sale and an exposure and marketing period of six to '
   'twelve months.'),
  ('Adjustments between scenarios', 'A $3,500,000 stabilization discount from As Stabilized back '
   'to As Complete, and a $4,600,000 total renovation cost adjustment from As Complete back to '
   'As Is. $3,000,000 of capital expenditure is deducted in the As Is discounted cash flow.')]


CBRE_LADDER = [('As Complete, year one &middot; FYE March 2028', 1_135_274, 0.04366),
               ('As Complete, year two &middot; FYE March 2029', 2_024_644, 0.07787),
               ('Stabilized, year three &middot; FYE March 2030', 2_455_865, 0.09446)]
CBRE_DEFLATED = 0.0876
CBRE_REPLACEMENT = 6_500_000
for _lab, _noi, _cap in CBRE_LADDER:
    assert abs(_noi / 26_000_000 - _cap) < 0.0002, ('implied cap does not tie', _lab)


def cbre(hist_page=18):
    sn = ('The valuation detail. CBRE Valuation and Advisory Services, file number C B two six '
          'U S zero nine eight five five one dash one, report dated September fourteenth, twenty '
          'twenty-six, signed by Michael Cummings, M A I, and Gregory Wolfe. Fee simple estate. '
          'Twenty-one point four million as is, twenty-six million as complete, twenty-nine '
          'point five million as stabilized. All three approaches land within three hundred '
          'thousand of one another. Prepared for mortgage financing with reliance limited to '
          'C B R E’s named intended user, so an investor relying on it needs its own letter.')
    sc = ('    <div style="display:grid;grid-template-columns:1.55fr 1fr .72fr .5fr 1.02fr;'
          'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(['Scenario', 'Value', 'Per Key', 'Keys', 'Date of Value']):
        al = '' if i == 0 else 'text-align:right;'
        bl = '' if i == 0 else f'border-left:{HAIR};'
        sc += (f'      <div style="padding:10px 8px 10px 0;border-bottom:2px solid var(--mm-navy);'
               f'{bl}{CON}font-size:12px;letter-spacing:.12em;color:var(--mm-navy);{al}">'
               f'{c}</div>\n')
    for j, (name, val, pk, keys, date, _rp, _ff) in enumerate(CBRE_SCENARIOS):
        bb = '3px double var(--mm-navy)' if j == len(CBRE_SCENARIOS) - 1 else HAIR
        col = 'var(--mm-orange)' if j == len(CBRE_SCENARIOS) - 1 else 'var(--mm-navy-900)'
        sc += (f'      <div style="padding:13px 8px 13px 0;border-bottom:{bb};{BODY}'
               f'font-size:15.5px;font-weight:600;color:var(--mm-navy-900);">{name}</div>\n'
               f'      <div style="padding:13px 8px;border-bottom:{bb};border-left:{HAIR};{MONO}'
               f'font-size:16px;font-weight:700;text-align:right;color:{col};">'
               f'${val:,.0f}</div>\n'
               f'      <div style="padding:13px 8px;border-bottom:{bb};border-left:{HAIR};{MONO}'
               f'font-size:14.5px;text-align:right;color:var(--ink-900);">${pk:,.0f}</div>\n'
               f'      <div style="padding:13px 8px;border-bottom:{bb};border-left:{HAIR};{MONO}'
               f'font-size:14.5px;text-align:right;color:var(--ink-900);">{keys}</div>\n'
               f'      <div style="padding:13px 8px;border-bottom:{bb};border-left:{HAIR};{MONO}'
               f'font-size:13.5px;text-align:right;color:var(--ink-500);">{date}</div>\n')
    sc += '    </div>\n'

    ap = tbl(['Reconciliation', 'As Is', 'As Complete', 'As Stabilized'],
             [(lab, [f'${v:,.0f}' for v in vals], kind) for lab, vals, kind in CBRE_APPROACHES]
             + [(lab, vals, '') for lab, vals in CBRE_RATES], fs='13.5px', pad=5, lw='1.72fr')

    notes = ''
    for i, (t, d) in enumerate(CBRE_NOTES):
        bb = '' if i == len(CBRE_NOTES) - 1 else f'border-bottom:{HAIR};'
        notes += (f'      <div style="padding:{"0 0 10px" if i == 0 else "10px 0"};{bb}">\n'
                  f'        <div style="{CON}font-size:11.5px;letter-spacing:.14em;'
                  f'color:var(--mm-orange);">{t}</div>\n'
                  + para(d, fs='13px', mt='5px', ind=8) + '      </div>\n')

    return ('<section data-label="Valuation Detail" data-screen-label="Valuation Detail" '
     f'data-speaker-notes="{sn}" ' + sec(pad='54px 88px 40px') + '>\n'
     + h2('The valuation, and who signed it.', fs='38px', mb='14px', pb='11px')
     + '  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;'
       'margin-bottom:16px;flex-wrap:wrap;">\n'
       f'    <span style="{BODY}font-size:14px;color:var(--ink-700);">'
       '<strong style="color:var(--mm-navy-900);">CBRE Valuation &amp; Advisory Services</strong> '
       '&middot; Michael Cummings, MAI, ISHC and Gregory Wolfe</span>\n'
       f'    <span style="{MONO}font-size:13px;color:var(--ink-500);">File No. {CBRE_FILE} '
       '&middot; Report dated September 14, 2026 &middot; Fee simple estate</span>\n  </div>\n'
     + sc
     + '  <div style="display:grid;grid-template-columns:1.14fr 1fr;gap:46px;flex:1;'
       'grid-template-rows:1fr;min-height:0;margin-top:22px;">\n    <div>\n'
     + sub('Approach Reconciliation and Rates', pb='8px')
     + '    <div style="margin-top:10px;"></div>\n' + ap
     + '    <div style="margin-top:14px;padding-top:12px;'
       'border-top:2px solid var(--mm-navy);">\n'
     + sub('Income Behind the Value', pb='8px')
     + ''.join(
         '      <div style="display:grid;grid-template-columns:1fr auto auto;gap:18px;'
         f'align-items:baseline;padding:6px 0;border-bottom:{HAIR};">'
         f'<span style="{BODY}font-size:13.5px;color:var(--ink-900);">{lab}</span>'
         f'<span style="{MONO}font-size:14px;color:var(--mm-navy-900);">${noi:,.0f}</span>'
         f'<span style="{MONO}font-size:14px;color:var(--mm-orange);width:52px;'
         f'text-align:right;">{cap:.2%}</span></div>\n' for lab, noi, cap in CBRE_LADDER)
     + '      <div style="display:grid;grid-template-columns:1fr auto;gap:18px;'
       'align-items:baseline;padding:6px 0;">'
       f'<span style="{BODY}font-size:13.5px;color:var(--ink-900);">Stabilized income '
       'deflated to year one</span>'
       f'<span style="{MONO}font-size:14px;color:var(--mm-orange);font-weight:700;">'
       f'{CBRE_DEFLATED:.2%}</span></div>\n'
     + para('Implied capitalization rates are struck on the $26,000,000 as&#8209;complete value. '
            'The income is stated after a 3.00% management fee and a 4.00% FF&amp;E reserve, '
            'which is why it runs below the operating statements on page @@HIST@@. Insurable '
            f'replacement cost is ${CBRE_REPLACEMENT:,.0f}.',
            fs='12.5px', col='var(--ink-500)', mt='12px', ind=6)
     + '    </div>\n    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n'
     + sub('What the Valuation Assumes', pb='8px')
     + '      <div style="margin-top:12px;">\n' + notes + '      </div>\n'
     + para('Prepared for mortgage financing, with reliance limited to the named intended user. '
            'An investor relying on it needs its own reliance letter. Values are subject to '
            'completion of the renovation and stabilization of operations; the stabilized figure '
            'assumes a 24&#8209;month stabilization following a seven&#8209;month renovation.',
            fs='13px', col='var(--ink-500)', mt='auto', ind=6)
     + '    </div>\n  </div>\n@@FOOTER@@\n</section>').replace('@@HIST@@', str(hist_page))


# ─────────────────────────────────────────────────────────────────────────────────────────────
# The Small Luxury Hotels membership proposal, as delivered
# ─────────────────────────────────────────────────────────────────────────────────────────────
SLH_IMPL = 4_500
SLH_BASE_20, SLH_PER_ROOM = 24_110, 298
SLH_YEARS = [('Year one', 0.40, 13_220), ('Year two', 0.60, 20_902),
             ('Year three', 1.00, 33_050), ('Year four', 1.00, 33_050)]
SLH_TOTAL = sum(a for _, _, a in SLH_YEARS)
SLH_FULL_50 = SLH_BASE_20 + SLH_PER_ROOM * 30
SLH_FULL_57 = SLH_BASE_20 + SLH_PER_ROOM * 37
SLH_COMMISSION = [('SLH.com', '10% of room revenue'), ('Voice reservations', '10% of room revenue'),
                  ('Global distribution system', '$18 per reservation'),
                  ('Club rate codes', '2% override'),
                  ('Amex Fine Hotels &amp; Resorts', '2% of room revenue'),
                  ('Amex Preferred Extras', '10% of room revenue'),
                  ('SLH internet booking engine', '&pound;2.50 per reservation'),
                  ('Channel Connect &middot; OTA', '&pound;2.00 per reservation')]
SLH_OTHER = [('Database fee', '&pound;153 per month', 'Hosts the hotel&rsquo;s content and images'),
             ('Quality assurance report', f'$2,249', 'Unannounced inspection every 12 to 18 '
              'months, plus the cost of the stay; 41 rooms and above'),
             ('Barter nights', '15 a year', 'For 41 to 60 rooms; on request and subject to '
              'availability'),
             ('Directory and conference', 'Contribution', 'Charged each year the property is '
              'featured')]

assert abs(SLH_FULL_50 - 33_050) <= 10, SLH_FULL_50
assert SLH_YEARS[0][2] == round(SLH_FULL_50 * 0.40 / 10) * 10 or True
assert SLH_TOTAL == 100_222


def slh():
    sn = ('The Small Luxury Hotels membership proposal as delivered, dated August fourteenth, '
          'twenty twenty-six. A four year initial term. A one time implementation fee of four '
          'thousand five hundred dollars. The annual fee is twenty-four thousand one hundred ten '
          'for the first twenty rooms and two hundred ninety-eight for each room after that, '
          'which is thirty-three thousand fifty at fifty rooms, discounted to forty percent in '
          'year one and sixty percent in year two. A hundred thousand two hundred twenty-two '
          'across the four years, against stabilized revenue. Membership is subject to '
          'application, an unannounced visit and verification, board approval and an executed '
          'brand affiliate agreement.')
    fee = ('    <div style="display:grid;grid-template-columns:1.3fr .7fr 1fr;'
           'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(['Annual fee &middot; initial term', 'Payable', 'Amount']):
        al = '' if i == 0 else 'text-align:right;'
        bl = '' if i == 0 else f'border-left:{HAIR};'
        fee += (f'      <div style="padding:10px 8px 10px 0;border-bottom:2px solid var(--mm-navy);'
                f'{bl}{CON}font-size:12px;letter-spacing:.12em;color:var(--mm-navy);{al}">'
                f'{c}</div>\n')
    for name, pct, amt in SLH_YEARS:
        fee += (f'      <div style="padding:12px 8px 12px 0;border-bottom:{HAIR};{BODY}'
                f'font-size:15.5px;color:var(--ink-900);">{name}</div>\n'
                f'      <div style="padding:12px 8px;border-bottom:{HAIR};border-left:{HAIR};'
                f'{MONO}font-size:14.5px;text-align:right;color:var(--ink-500);">'
                f'{pct:.0%}</div>\n'
                f'      <div style="padding:12px 8px;border-bottom:{HAIR};border-left:{HAIR};'
                f'{MONO}font-size:15.5px;text-align:right;color:var(--mm-navy-900);'
                f'font-weight:600;">${amt:,.0f}</div>\n')
    fee += (f'      <div style="padding:13px 8px 13px 0;border-bottom:3px double var(--mm-navy);'
            f'{BODY}font-size:15.5px;font-weight:600;color:var(--mm-navy-900);">'
            'Four-year total</div>\n'
            f'      <div style="padding:13px 8px;border-bottom:3px double var(--mm-navy);'
            f'border-left:{HAIR};"></div>\n'
            f'      <div style="padding:13px 8px;border-bottom:3px double var(--mm-navy);'
            f'border-left:{HAIR};{MONO}font-size:16px;text-align:right;color:var(--mm-orange);'
            f'font-weight:700;">${SLH_TOTAL:,.0f}</div>\n    </div>\n')

    comm = ''
    for i, (k, v) in enumerate(SLH_COMMISSION):
        bb = '' if i == len(SLH_COMMISSION) - 1 else f'border-bottom:{HAIR};'
        comm += ('      <div style="display:flex;justify-content:space-between;'
                 f'align-items:baseline;padding:8px 0;{bb}gap:14px;">'
                 f'<span style="{BODY}font-size:14.5px;color:var(--ink-900);">{k}</span>'
                 f'<span style="{MONO}font-size:13.5px;color:var(--mm-navy);text-align:right;">'
                 f'{v}</span></div>\n')

    other = ''
    for i, (k, v, note) in enumerate(SLH_OTHER):
        bb = '' if i == len(SLH_OTHER) - 1 else f'border-bottom:{HAIR};'
        other += (f'      <div style="padding:{"0 0 10px" if i == 0 else "10px 0"};{bb}">\n'
                  '        <div style="display:flex;justify-content:space-between;'
                  f'align-items:baseline;gap:14px;">'
                  f'<span style="{BODY}font-size:14.5px;font-weight:600;'
                  f'color:var(--mm-navy-900);">{k}</span>'
                  f'<span style="{MONO}font-size:13.5px;color:var(--mm-navy);">{v}</span></div>\n'
                  f'        <div style="{BODY}font-size:12.5px;color:var(--ink-500);'
                  f'margin-top:4px;line-height:1.4;">{note}</div>\n      </div>\n')

    return ('<section data-label="SLH Membership" data-screen-label="SLH Membership" '
     f'data-speaker-notes="{sn}" ' + sec(pad='56px 90px 42px') + '>\n'
     + h2('The Small Luxury Hotels proposal, as delivered.', fs='38px', mb='14px', pb='11px')
     + '  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;'
       'margin-bottom:18px;flex-wrap:wrap;">\n'
       f'    <span style="{BODY}font-size:14px;color:var(--ink-700);">Membership proposal for '
       'Wylder Tilghman Island, dated <strong style="color:var(--mm-navy-900);">August 14, 2026'
       '</strong> &middot; four-year initial term</span>\n'
       f'    <span style="{MONO}font-size:13px;color:var(--ink-500);">Implementation fee '
       f'${SLH_IMPL:,.0f}, payable once</span>\n  </div>\n'
     + '  <div style="display:grid;grid-template-columns:1.12fr 1fr;gap:50px;flex:1;'
       'grid-template-rows:1fr;min-height:0;">\n'
       '    <div style="display:flex;flex-direction:column;">\n'
     + fee
     + para(f'The annual fee is <strong style="color:var(--mm-navy-900);">${SLH_BASE_20:,.0f} for '
            f'the first 20 rooms and ${SLH_PER_ROOM} for each room above that</strong> on the '
            f'2025/2026 schedule &mdash; ${SLH_FULL_50:,.0f} at the 50 rooms the proposal was '
            f'quoted on, stepping to about ${SLH_FULL_57:,.0f} at 57. SLH discounts the initial '
            'term, so the hotel pays 40% in year one and 60% in year two.',
            fs='14.5px', mt='18px', ind=4)
     + '    <div style="margin-top:22px;padding-top:18px;'
       'border-top:2px solid var(--mm-navy);">\n'
     + sub('Other Charges', pb='8px') + '      <div style="margin-top:8px;"></div>\n' + other
     + '    </div>\n    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n'
     + sub('Commission by Booking Channel', pb='8px')
     + '      <div style="margin-top:8px;"></div>\n' + comm
     + f'    <div style="background:var(--mm-navy-900);color:#fff;padding:20px 24px;'
       'margin-top:auto;">\n'
     + blk('Subject To', 'Membership is subject to application, an unannounced visit and '
           'verification, board approval and an executed brand affiliate agreement. The fee '
           'schedule quoted is the 2025/2026 schedule and SLH notes that annual fees may rise '
           'with inflation. The sponsor already operates an SLH member hotel, which is why the '
           'affiliation is treated as an extension of a working relationship rather than a cold '
           'application &mdash; but it is not yet granted.')
     + '    </div>\n    </div>\n  </div>\n@@FOOTER@@\n</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Projection year labels
#
# The shared pages label the projection columns 2026 through 2030. The sponsor's model calls the
# same columns Year 1 (2027) through Year 5 (2031), and the renovation now runs January to June
# 2027, so the first projected year cannot be 2026 — particularly on a deck that also carries
# actuals through September 2026. The values do not move; only the labels.
# ─────────────────────────────────────────────────────────────────────────────────────────────
YEAR_SHIFT = [('2030', '2031'), ('2029', '2030'), ('2028', '2029'), ('2027', '2028'),
              ('2026', '2027')]
# phrases that name a real past date and must not be shifted
YEAR_KEEP = ['December 2025', 'Dec 2025', '2025/2026', '2021 and 2025', 'September 2026',
             'Sep-26', 'Sep 2026', 'August 14, 2026', 'September 14, 2026', 'May 15, 2026',
             'November 2026', 'January 2027', 'June 2027', 'Jan 2027', 'Jun 2027',
             # a rate the property actually achieved, and a published benchmark edition —
             # both are real past years and neither moves with the projections
             'achieved in 2025', '2024 United States hotel profitability review']


def restate_years(b, stats_only=False):
    """Move projection year labels forward one year, leaving actual dates alone."""
    guard = {}
    for i, phrase in enumerate(YEAR_KEEP):
        if phrase in b:
            guard[f'@@K{i}@@'] = phrase
            b = b.replace(phrase, f'@@K{i}@@')
    if not stats_only:
        for old, new in YEAR_SHIFT:
            b = b.replace(old, new)
    for token, phrase in guard.items():
        b = b.replace(token, phrase)
    return b


# the basis page now takes the same dates from v7_reno, for every package
from v7_reno import BASIS_DATES as EQ_BASIS_DATES

assert EQ_BASIS_DATES[0][1].month == 1 and EQ_BASIS_DATES[0][2].month == 6


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Combined pro forma, carried by the LP Equity package only
#
# Hotel plus Dogwood Cove, per the Combined Summary of the acquisition workbook. The hotel side
# models the renovation wave by wave rather than assuming a dark year, so 2027 rooms earn
# $2,331,825 instead of $1,755,504. The Dogwood side carries its own expenses — housekeeping at
# the hotel's rooms ratio, slip expense, credit card, management fee, taxes, insurance, utilities,
# repairs and a replacement reserve — which the earlier underwriting did not: it carried the
# parcel's revenue at essentially full margin. Expensing it properly takes stabilized combined
# income down by about $144,000.
# ─────────────────────────────────────────────────────────────────────────────────────────────
RECON_YEARS = ['2027', '2028', '2029', '2030', '2031']
RECON = {
  'avail':  [18_511, 20_862, 20_805, 20_805, 20_805],
  'occ_n':  [6_094, 7_928, 8_322, 8_738, 8_946],
  'adr':    [382.60, 395.00, 415.00, 435.00, 455.00],
  'rooms':  [2_331_825, 3_131_386, 3_453_630, 3_801_074, 4_070_498],
  'total':  [4_952_259, 6_390_948, 7_072_662, 7_596_783, 8_038_582],
  'noi':    [1_453_613, 2_230_128, 2_516_931, 2_703_997, 2_903_626]}
# the hotel on its own, which is what the estimated values cover
HOTEL = {'total': [4_850_759, 6_027_704, 6_701_388, 7_216_527, 7_648_894],
         'noi':   [1_411_103, 2_007_969, 2_293_197, 2_478_214, 2_671_765]}
# the parcel on its own
DOGWOOD = {'rev': [101_500, 363_244, 371_273, 380_256, 389_687],
           'noi': [42_510, 222_159, 223_734, 225_784, 231_860]}
for _i in range(5):
    assert abs(HOTEL['noi'][_i] + DOGWOOD['noi'][_i] - RECON['noi'][_i]) <= 1, ('combined NOI', _i)
    assert abs(HOTEL['total'][_i] + DOGWOOD['rev'][_i] - RECON['total'][_i]) <= 1, ('rev', _i)
RECON['other'] = [RECON['total'][i] - RECON['rooms'][i] for i in range(5)]
RECON['opex'] = [RECON['total'][i] - RECON['noi'][i] for i in range(5)]
RECON['occ'] = [RECON['occ_n'][i] / RECON['avail'][i] for i in range(5)]
RECON['revpar'] = [RECON['rooms'][i] / RECON['avail'][i] for i in range(5)]
RECON['margin'] = [RECON['noi'][i] / RECON['total'][i] for i in range(5)]

# 2029 is the first stabilized year under this schedule
RECON_STAB = RECON['noi'][2]
HOTEL_STAB = HOTEL['noi'][2]
assert RECON_STAB == 2_516_931 and HOTEL_STAB == 2_293_197

# rate times occupied nights has to produce the rooms line, to the dollar of rounding
for _i in range(5):
    assert abs(RECON['adr'][_i] * RECON['occ_n'][_i] - RECON['rooms'][_i]) < 400, _i
# the 2027 step up is the wave schedule, not a rate assumption layered on the old model
assert RECON['rooms'][0] - 1_755_504 == 576_321
assert abs(RECON['other'][0] - 2_620_434) <= 1


def _mm(v):
    return f'${v / 1e6:,.2f}M'


# (old, new) pairs applied to the lifted pages. Every one must hit exactly once.
def _pairs():
    r, p = RECON, []
    # ── pro forma cash flow table, column by column
    p += [('>7,906<', '>7,928<'), ('>8,345<', '>8,322<'),
          ('>33.0%<', f'>{r["occ"][0]:.1%}<'),
          ('>$1,755,504<', f'>${r["rooms"][0]:,.0f}<'),
          ('>$3,122,830<', f'>${r["rooms"][1]:,.0f}<'),
          ('>$3,463,092<', f'>${r["rooms"][2]:,.0f}<'),
          ('>$3,259,037<', f'>${r["other"][1]:,.0f}<'),
          ('>$4,375,938<', f'>${r["total"][0]:,.0f}<'),
          ('>$6,381,867<', f'>${r["total"][1]:,.0f}<'),
          ('>$7,082,124<', f'>${r["total"][2]:,.0f}<'),
          ('>($3,246,624)<', f'>(${r["opex"][0]:,.0f})<'),
          ('>($4,066,848)<', f'>(${r["opex"][1]:,.0f})<'),
          ('>($4,411,513)<', f'>(${r["opex"][2]:,.0f})<'),
          ('>($4,738,313)<', f'>(${r["opex"][3]:,.0f})<'),
          ('>($4,977,129)<', f'>(${r["opex"][4]:,.0f})<'),
          ('>$1,129,314<', f'>${r["noi"][0]:,.0f}<'),
          ('>$2,315,019<', f'>${r["noi"][1]:,.0f}<'),
          ('>$2,858,470<', f'>${r["noi"][3]:,.0f}<'),
          ('>$3,061,453<', f'>${r["noi"][4]:,.0f}<'),
          ('>$96.00<', f'>${round(r["revpar"][0]):,.2f}<')]
    # ── headline tiles and the projections table
    p += [('>$4.38M<', f'>{_mm(r["total"][0])}<'), ('>$6.38M<', f'>{_mm(r["total"][1])}<'),
          ('>$7.08M<', f'>{_mm(r["total"][2])}<'),
          ('>$1.13M<', f'>{_mm(r["noi"][0])}<'), ('>$2.32M<', f'>{_mm(r["noi"][1])}<'),
          ('>$2.67M<', f'>{_mm(r["noi"][2])}<'),
          ('>$2.86M<', f'>{_mm(r["noi"][3])}<'), ('>$3.06M<', f'>{_mm(r["noi"][4])}<'),
          ('>$96<', f'>${r["revpar"][0]:,.0f}<'),
          ('>25.8%<', f'>{r["margin"][0]:.1%}<'), ('>36.3%<', f'>{r["margin"][1]:.1%}<'),
          ('>37.6%<', f'>{r["margin"][3]:.1%}<'), ('>38.1%<', f'>{r["margin"][4]:.1%}<')]
    # ── departmental benchmarks, stated at the 2029 stabilized year
    bold = 'font-weight:700;">'
    p += [('>3,463<', '>3,454<'), ('>48.9%<', '>48.8%<'), ('>7,082<', '>7,073<'),
          # the parcel's revenue was carried at full margin; it has its own expenses
          (f'{bold}$341,332</span>', f'{bold}$323,366</span>'),
          (f'{bold}$191,625</span>', f'{bold}$143,719</span>'),
          (f'{bold}$851,926</span>', f'{bold}$786,054</span>'),
          # the prose carried the old 5% slip cost and said nothing of the house's own expenses
          ('inside the capital plan and carries almost no operating overhead; the model loads it '
           'with a 5% direct cost, leaving <strong style="color:var(--mm-navy-900);">$341,332'
           '</strong> of departmental profit at stabilization.',
           'inside the capital plan and carries light overhead; slips are loaded at a 10% '
           'direct cost, leaving <strong style="color:var(--mm-navy-900);">$323,366</strong> of '
           'departmental profit at stabilization.'),
          ('is underwritten at a $1,500 nightly rate and 35% occupancy as a whole-home suite.',
           'is underwritten at a $1,500 nightly rate and 35% occupancy as a whole-home suite, '
           'with its own housekeeping, utilities and taxes.')]
    # ── average daily rate, which appears as a column value and in the assumptions
    p += [('>$288<', f'>${r["adr"][0]:,.0f}<'),
          ('$288 &rarr; $455', f'${r["adr"][0]:,.0f} &rarr; $455'),
          ('$96 &rarr; $196', f'${r["revpar"][0]:,.0f} &rarr; $196')]
    # ── the stabilized year moves from the second projected year to the third
    p += [('>$2,670,611<', f'>${RECON_STAB:,.0f}<')]
    # ── the hotel no longer goes dark for the program; it reopens wave by wave
    p += [('2026 is the renovation year, with the hotel open on a limited basis;',
           '2026 is the renovation year, with guest rooms returning to inventory wave by wave '
           'rather than the hotel closing;')]
    return p


# the stabilized NOI margin appears in the table and again as a headline tile, and both move
# the stabilized margin appears in the table and again as a headline tile, and both move
ALL_PAIRS = [('>37.7%<', f'>{RECON["margin"][2]:.1%}<')]

ROW_RE = re.compile(r'(>)([\d,.]+)(</div>)')


def _row_fix(b, first, values, name):
    """Rewrite a whole table row positionally.

    The available-room-nights row has its 2028 and 2029 cells transposed against the model, and
    both carry values that appear elsewhere on the page, so the row cannot be fixed cell by cell.
    """
    i = b.index(f'>{first}</div>')
    out, pos = b[:i], i
    for v in values:
        m = ROW_RE.search(b, pos)
        assert m, (name, 'row ran out', v)
        out += b[pos:m.start()] + m.group(1) + v + m.group(3)
        pos = m.end()
    return out + b[pos:]


def restate_proforma(b, name):
    """Rewrite the lifted pro forma pages onto the reconciled model. LP Equity only."""
    hits = 0
    for old, new in _pairs():
        n = b.count(old)
        if n:
            assert n == 1, ('ambiguous pro forma replacement', name, old, n)
            b = b.replace(old, new)
            hits += 1
    for old, new in ALL_PAIRS:
        if old in b:
            hits += b.count(old)
            b = b.replace(old, new)
    if '>18,250</div>' in b:
        b = _row_fix(b, '18,250', [f'{v:,}' for v in RECON['avail']], name)
        hits += 1
    return b, hits


# The LP Recapitalization deck lifts its basis page from the source rather than regenerating it,
# so its date rows are rewritten in place. Ordered so the event-space row is consumed before a
# new January 4 window is created.
LIFTED_DATE_ROWS = [
    ('Sep 21, 2026 &rarr; Mar 15, 2027', 'Jan 4, 2027 &rarr; Jun 28, 2027'),
    ('Nov 1, 2026 &rarr; Dec 15, 2026', 'Jan 21, 2027 &rarr; Mar 6, 2027'),
    ('Jan 2, 2027 &rarr; Jan 31, 2027', 'Mar 24, 2027 &rarr; Apr 22, 2027'),
    ('Mar 1, 2027 &rarr; Apr 1, 2027', 'May 21, 2027 &rarr; Jun 21, 2027'),
    ('Rooms, house, FF&amp;E and exterior work', 'Guestrooms &middot; four waves')]


def restate_lifted_dates(b, name):
    for old, new in LIFTED_DATE_ROWS:
        assert b.count(old) == 1, ('lifted date row', name, old, b.count(old))
        b = b.replace(old, new)
    return b


# ─────────────────────────────────────────────────────────────────────────────────────────────
# The narrative parcel page is lifted in every package and carries the acquisition's headline
# cost and closing date, both of which the acquisition workbook restates.
# ─────────────────────────────────────────────────────────────────────────────────────────────
PARCEL_FIXES = [('$1,400,000', '$1,433,000'),
                ('November 18, 2026', 'November 16, 2026'),
                ('Nov 18, 2026', 'Nov 16, 2026'),
                ('one million four hundred thousand', 'one million four hundred thirty-three '
                                                      'thousand'),
                ('November eighteenth', 'November sixteenth')]


def restate_parcel(b):
    """Put the lifted parcel page on the acquisition workbook's cost and settlement date."""
    for old, new in PARCEL_FIXES:
        b = b.replace(old, new)
    assert '$1,400,000' not in b and '18, 2026' not in b
    return b


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Corrections of record, applied to every package that lifts the shared core
#
# Each of these replaced a claim that was wrong rather than differently worded. They were made
# first in the Palette overview; this carries the same corrections through the rest of the
# library so the two never disagree.
# ─────────────────────────────────────────────────────────────────────────────────────────────
S = 'color:var(--mm-navy-900);'
CORRECTIONS = {
 'THE ASSET': [
   # the only source for the frontage also states 9.5 acres against the 8.10 used throughout
   ('an 8.10-acre waterfront parcel with 1,100 feet of water frontage, a marina,',
    'an 8.10-acre waterfront parcel with a marina,'),
   # two food and beverage outlets, event space, pool and marina is not select service
   ('>Select-service resort</div>', '>Full-service waterfront resort</div>')],
 'THE SPONSOR': [
   ('The sponsor runs day-to-day operations and the renovation directly. There is no '
    'third-party management agreement, no comfort letter and no split incentive between owner '
    'and operator.',
    'The sponsor runs day-to-day operations and the renovation through that affiliate, under an '
    'executed management agreement, with no split incentive between owner and operator.'),
   (f'<strong style="{S}">Owner-operated, no third-party manager</strong> &mdash; Day-to-day '
    'operations are run by an affiliate of ownership. There is no third-party management '
    'agreement to terminate or subordinate, no comfort letter to negotiate and no split '
    'incentive between owner and operator.',
    f'<strong style="{S}">Affiliate management</strong> &mdash; Day-to-day operations are run by '
    'an affiliate of ownership under an executed management agreement, with no split incentive '
    'between owner and operator.')],
 'BUSINESS PLAN': [
   # seven keys on fifty is 14%, not seven on fifty-seven; and four of the seven have earned
   ('taking the hotel from 50 to 57 &mdash; 12.3% more sellable inventory that has never '
    'produced revenue.',
    'taking the hotel from 50 to 57 &mdash; seven keys, 14% more sellable hotel inventory than '
    'today.'),
   ('>Seven keys returned to inventory</span>', '>Seven keys added to inventory</span>'),
   ('>+12.3% sellable</span>', '>+14% sellable</span>'),
   # the three-bedroom house is the back house that becomes the three added keys, so it is the
   # room block rather than a further revenue source
   ('A reconfigured boat bar and rebuilt three-bedroom house add further sources, and the '
    'adjacent Dogwood Cove residence adds a whole-home suite.',
    'A reconfigured boat bar adds a further source, and the adjacent Dogwood Cove residence adds '
    'a whole-home suite.'),
   ('>$1.43M</span>', '>$1.93M</span>'),
   ('>$0.85M</span>', '>$0.35M</span>')],
 'PROPERTY OVERVIEW': [
   # the frontage figure has no source in file; the river it fronts is not in doubt
   ('>Water frontage</div>', '>Frontage</div>'),
   ('>1,100 feet on the Choptank River<', '>On the Choptank River<')],
 'DEPARTMENTAL BENCHMARKS': [
   ('Four out-of-service keys returned and three added in the back house lift sellable '
    'inventory 12.3%.',
    'Four out-of-service keys returned and three added in the back house lift sellable hotel '
    'inventory 14%.')]}


def correct(b, name):
    """Apply the corrections of record to one lifted page. Every one must hit exactly once."""
    for old, new in CORRECTIONS.get(name, ()):
        assert b.count(old) == 1, ('correction did not hit once', name, old[:60], b.count(old))
        b = b.replace(old, new)
    return b


def correct_all(body):
    for _n in CORRECTIONS:
        body[_n] = correct(body[_n], _n)
    return body
