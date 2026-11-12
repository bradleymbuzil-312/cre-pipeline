# -*- coding: utf-8 -*-
"""The lender-facing debt model for a senior loan request.

A live workbook: the loan amount on 'Loan Request' drives the debt service, the reserve, the fees,
net funding, every coverage and leverage measure, the three sizing tests and the sensitivity grid.
It carries no equity economics — no preferred rate, no waterfall, no promote, no partner returns —
for the same reason the debt packages do not.

    WT_SENIOR_LOAN=12500000 python3 v7_model.py
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from figs_v7 import (SENIOR, PREF, COMMON, TOTAL, SOFR, SPREAD, ALLIN, SR_ORIG_PC, SR_BROKER_PC,
                     SR_TERM, PERM_RATE, KEYS, VAL, PRO, COST_BASIS, CLOSING)

NAVY, ORANGE, INK, PAPER = '002F6C', 'E87722', '0E1116', 'FAF8F4'
HAIR = Side(style='thin', color='C9CDD4')
RULE = Side(style='medium', color=NAVY)
F = 'Aptos'

MONEY, MONEY0, PCT, PCT1, MULT = '$#,##0', '$#,##0', '0.00%', '0.0%', '0.00"x"'
NUM = '#,##0'


def sheet(wb, name, widths, title, subtitle=''):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    last = get_column_letter(len(widths))
    ws.merge_cells(f'A1:{last}1')
    c = ws['A1']
    c.value = f'WYLDER HOTEL TILGHMAN ISLAND   ·   {title}'
    c.font = Font(name=F, size=13, bold=True, color='FFFFFF')
    c.fill = PatternFill('solid', fgColor=NAVY)
    c.alignment = Alignment(vertical='center', indent=1)
    ws.row_dimensions[1].height = 26
    if subtitle:
        ws.merge_cells(f'A2:{last}2')
        c = ws['A2']
        c.value = subtitle
        c.font = Font(name=F, size=10, italic=True, color='5A6068')
        c.alignment = Alignment(vertical='center', indent=1)
    ws.row_dimensions[2].height = 18
    return ws


def head(ws, row, text, cols=1):
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name=F, size=10, bold=True, color=NAVY)
    c.alignment = Alignment(indent=1)
    for i in range(1, cols + 1):
        ws.cell(row=row, column=i).border = Border(bottom=RULE)
    ws.row_dimensions[row].height = 20


def line(ws, row, label, value, fmt=MONEY, bold=False, accent=False, note='', col=2,
         indent=1, rule=False):
    c = ws.cell(row=row, column=1, value=label)
    c.font = Font(name=F, size=10, bold=bold, color=INK)
    c.alignment = Alignment(indent=indent)
    v = ws.cell(row=row, column=col, value=value)
    v.font = Font(name=F, size=10, bold=bold or accent,
                  color=(ORANGE if accent else (NAVY if bold else INK)))
    v.number_format = fmt
    v.alignment = Alignment(horizontal='right')
    b = Border(bottom=RULE if rule else HAIR)
    c.border = b
    v.border = b
    if note:
        n = ws.cell(row=row, column=col + 1, value=note)
        n.font = Font(name=F, size=9, italic=True, color='5A6068')
        n.alignment = Alignment(indent=1)
    return row + 1


def grid_head(ws, row, labels, start=2):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=t)
        c.font = Font(name=F, size=10, bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=NAVY)
        c.alignment = Alignment(horizontal='right', indent=1)
    ws.row_dimensions[row].height = 18
    return row + 1


def grid_row(ws, row, label, values, fmt=MONEY, bold=False, accent=False, start=2, rule=False):
    c = ws.cell(row=row, column=1, value=label)
    c.font = Font(name=F, size=10, bold=bold, color=INK)
    c.alignment = Alignment(indent=1)
    c.border = Border(bottom=RULE if rule else HAIR)
    for i, v in enumerate(values):
        x = ws.cell(row=row, column=start + i, value=v)
        x.font = Font(name=F, size=10, bold=bold or accent,
                      color=(ORANGE if accent else (NAVY if bold else INK)))
        x.number_format = fmt
        x.alignment = Alignment(horizontal='right')
        x.border = Border(bottom=RULE if rule else HAIR)
    return row + 1


# ─────────────────────────────────────────────────────────────── the extended series
EXT_YEARS = list(range(2030, 2042))
EXT = {
 'Occupancy':        [0.43] * 12,
 'Average daily rate': [455, 469, 483, 497, 512, 527, 543, 560, 576, 594, 611, 630],
 'RevPAR':           [196, 202, 208, 214, 220, 227, 234, 241, 248, 255, 263, 271],
 'Rooms revenue':    [4070, 4193, 4318, 4448, 4581, 4719, 4860, 5006, 5156, 5311, 5470, 5635],
 'Other operated departments':
                     [3968, 4087, 4210, 4336, 4466, 4600, 4738, 4880, 5027, 5177, 5333, 5493],
 'Total revenue':    [8039, 8280, 8528, 8784, 9047, 9319, 9598, 9886, 10183, 10489, 10803, 11127],
 'Operating expenses':
                     [-4977, -5126, -5280, -5439, -5602, -5770, -5943, -6121, -6305, -6494,
                      -6689, -6890],
 'Net operating income':
                     [3061, 3153, 3248, 3345, 3446, 3549, 3656, 3765, 3878, 3995, 4114, 4238],
 'Net cash flow at a 4.0% reserve':
                     [3046, 3137, 3231, 3328, 3428, 3531, 3637, 3746, 3858, 3974, 4093, 4216],
}
for _k, _v in EXT.items():
    assert len(_v) == 12, _k
# rounded to thousands, so revenue less expenses can differ from NOI by a dollar
for _i in range(12):
    assert abs(EXT['Total revenue'][_i] + EXT['Operating expenses'][_i]
               - EXT['Net operating income'][_i]) <= 2, _i

USES_FIXED = [('Existing loan payoff', 10_714_782), ('PIP / renovation', 3_003_000),
              ('Land and house acquisition &middot; 21441 Dogwood Cove'.replace('&middot;', '·'),
               1_100_000),
              ('Working capital', 500_000), ('Dogwood Cove house renovation', 300_000),
              ('Closing, legal and other', 130_100)]
BASIS_ACQ = [('Acquisition and capital expenses', 10_714_782),
             ('Land and house acquisition · 21441 Dogwood Cove', 1_100_000),
             ('Sponsor cash equity outside loan proceeds', 2_000_000)]
BASIS_PIP = [('Room renovation', 1_425_000), ('Marina replacement and expansion', 250_000),
             ('Replace three-bedroom house', 500_000), ('Interior public space and FF&E', 50_000),
             ('Convert boat bar', 50_000), ('Exterior and interior improvements', 300_000),
             ('Contingency', 258_000), ('Professional fees', 170_000),
             ('Dogwood Cove house renovation', 300_000)]
BASIS_OTH_FIXED = [('Working capital', 500_000), ('Closing, legal and mortgage tax', 120_000),
                   ('Processing and third-party fees', 10_100)]
SUBORDINATE_COSTS = round(PREF * 0.04)      # shown as one amount, never as a rate


C = get_column_letter


def build():
    wb = Workbook()
    wb.remove(wb.active)


    # ════════════════════════════════════════════ 1 · Loan Request
    ws = sheet(wb, 'Loan Request', [46, 18, 44], 'SENIOR LOAN REQUEST',
               'The loan amount in B5 drives every figure in this workbook.')
    R = {}
    r = 4
    head(ws, r, 'The Request', 3); r += 1
    R['loan'] = f'B{r}'
    r = line(ws, r, 'Senior loan amount — first trust deed', SENIOR, bold=True, accent=True,
             note='← the input that drives the workbook')
    R['keys'] = f'B{r}'
    r = line(ws, r, 'Keys', KEYS, fmt=NUM)
    r = line(ws, r, 'Loan per key', f'={R["loan"]}/{R["keys"]}')
    r = line(ws, r, 'Term, years', SR_TERM, fmt='0')
    r = line(ws, r, 'Amortization', 'Interest-only', fmt='@', rule=True)
    r += 1

    head(ws, r, 'Pricing', 3); r += 1
    R['sofr'] = f'B{r}'; r = line(ws, r, 'Index — SOFR', SOFR, fmt=PCT)
    R['spread'] = f'B{r}'; r = line(ws, r, 'Spread', SPREAD, fmt=PCT)
    R['allin'] = f'B{r}'
    r = line(ws, r, 'All-in rate', f'={R["sofr"]}+{R["spread"]}', fmt=PCT, bold=True)
    R['ads'] = f'B{r}'
    r = line(ws, r, 'Annual debt service — interest-only', f'={R["loan"]}*{R["allin"]}', bold=True)
    R['orig_pc'] = f'B{r}'; r = line(ws, r, 'Origination fee', SR_ORIG_PC, fmt=PCT)
    R['brk_pc'] = f'B{r}'; r = line(ws, r, 'Broker fee — MMCC', SR_BROKER_PC, fmt=PCT)
    R['res_mo'] = f'B{r}'
    r = line(ws, r, 'Interest and carry reserve, months', 12, fmt='0', rule=True)
    R['reserve'] = f'({R["ads"]}*{R["res_mo"]}/12)'
    R['orig'] = f'({R["loan"]}*{R["orig_pc"]})'
    R['brk'] = f'({R["loan"]}*{R["brk_pc"]})'
    r += 1

    head(ws, r, 'Net Funding at Close', 3); r += 1
    a = r
    r = line(ws, r, 'Gross loan amount', f'={R["loan"]}')
    r = line(ws, r, 'Less origination fee', f'=-{R["orig"]}')
    r = line(ws, r, 'Less interest and carry reserve', f'=-{R["reserve"]}')
    R['net'] = f'B{r}'
    r = line(ws, r, 'Net senior proceeds at close', f'=SUM(B{a}:B{r - 1})', bold=True,
             accent=True, rule=True)
    r += 1

    head(ws, r, 'Leverage Against Estimated Value', 3); r += 1
    r = grid_head(ws, r, ['Value', 'Per key', 'Senior LTV'])
    vals = [('As-is — today', VAL['is']), ('Upon completion — April 2027', VAL['complete']),
            ('Upon stabilization — April 2029', VAL['stab'])]
    v0 = r
    for i, (lab, v) in enumerate(vals):
        last = (i == len(vals) - 1)
        grid_row(ws, r, lab, [v, f'=B{r}/{R["keys"]}', f'={R["loan"]}/B{r}'], bold=last,
                 rule=last)
        ws.cell(row=r, column=3).number_format = MONEY
        ws.cell(row=r, column=4).number_format = PCT
        r += 1
    R['val_is'] = f'B{v0}'
    R['val_stab'] = f'B{v0 + 2}'
    r += 1

    head(ws, r, 'Coverage and Debt Yield', 3); r += 1
    r = grid_head(ws, r, [str(y) for y, *_ in PRO])
    noi = r
    r = grid_row(ws, r, 'Net operating income', [n for *_, n in PRO], bold=True)
    r = grid_row(ws, r, 'Senior debt service', [f'=-{R["ads"]}'] * 3)
    r = grid_row(ws, r, 'Cash flow after debt service',
                 [f'={C(2 + i)}{noi}+{C(2 + i)}{noi + 1}' for i in range(3)])
    r = grid_row(ws, r, 'Debt service coverage',
                 [f'={C(2 + i)}{noi}/{R["ads"]}' for i in range(3)], fmt=MULT, bold=True)
    r = grid_row(ws, r, 'Debt yield', [f'={C(2 + i)}{noi}/{R["loan"]}' for i in range(3)],
                 fmt=PCT, accent=True, rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='2026 is the renovation year; the interest and carry reserve funded at '
                      'close pays twelve months of debt service in full.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    R['noi_row'] = noi
    return wb, R


def add_sources_uses(wb, R):
    ws = sheet(wb, 'Sources & Uses', [46, 18, 44], 'SOURCES AND USES AT CLOSING',
               'Subordinate capital is the plug, so sources equal uses at any loan amount.')
    L = "'Loan Request'!"
    loan, ads, res, orig, brk = (L + R['loan'], L + R['ads'], None, None, None)
    reserve = f"({L}{R['ads']}*{L}{R['res_mo']}/12)"
    origf = f"({L}{R['loan']}*{L}{R['orig_pc']})"
    brkf = f"({L}{R['loan']}*{L}{R['brk_pc']})"
    r = 4
    head(ws, r, 'Uses', 3); r += 1
    u0 = r
    for lab, v in USES_FIXED:
        r = line(ws, r, lab, v)
    r = line(ws, r, 'Interest and carry reserve — 12 months', f'={reserve}')
    r = line(ws, r, f'Senior origination fee — {SR_ORIG_PC:.2%}', f'={origf}')
    r = line(ws, r, f'Broker fee — MMCC senior debt — {SR_BROKER_PC:.2%}', f'={brkf}')
    r = line(ws, r, 'Subordinate capital costs and fees', SUBORDINATE_COSTS,
             note='At the requested loan amount')
    u1 = r - 1
    r = line(ws, r, 'Total uses', f'=SUM(B{u0}:B{u1})', bold=True, rule=True)
    uses = f'B{r - 1}'
    r += 1

    head(ws, r, 'Sources', 3); r += 1
    s0 = r
    r = line(ws, r, 'Senior loan — first trust deed', f'={loan}')
    r = line(ws, r, 'Subordinate capital — preferred and common equity',
             f'={uses}-{loan}', accent=True, note='The plug: total uses less the senior loan')
    sub = f'B{r - 1}'
    r = line(ws, r, 'Total sources', f'=SUM(B{s0}:B{r - 1})', bold=True)
    tot = f'B{r - 1}'
    r = line(ws, r, 'Sources less uses', f'={tot}-{uses}', bold=True, rule=True)
    r += 1

    head(ws, r, 'Capitalization at the Requested Loan Amount', 3); r += 1
    r = line(ws, r, 'Senior loan — first trust deed', f'={loan}')
    r = line(ws, r, 'Preferred equity', PREF, note='Amount only; its terms are not shown here')
    r = line(ws, r, 'Common equity — LP', COMMON)
    r = line(ws, r, 'Total capitalization', f'=SUM(B{r - 3}:B{r - 1})', bold=True)
    cap = f'B{r - 1}'
    r = line(ws, r, 'Senior loan to total capitalization', f'={loan}/{cap}', fmt=PCT, bold=True)
    r = line(ws, r, 'Senior and preferred to as-is value',
             f"=({loan}+B{r - 4})/{L}{R['val_is']}", fmt=PCT)
    r = line(ws, r, 'Capital beneath the loan', f'={cap}-{loan}+2000000',
             note='Subordinate capital plus $2,000,000 of sponsor cash already invested',
             rule=True)
    r += 1

    head(ws, r, 'Closing, Legal and Other Detail', 3); r += 1
    c0 = r
    for lab, v in CLOSING:
        r = line(ws, r, lab.replace('&mdash;', '—'), v)
    r = line(ws, r, 'Total closing, legal and other', f'=SUM(B{c0}:B{r - 1})', bold=True,
             rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='The split of subordinate capital between preferred and common equity is '
                      'stated at the requested loan amount. Flexing the loan moves the subordinate '
                      'capital line, not the uses of funds.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    return ws


def add_sizing(wb, R):
    ws = sheet(wb, 'Loan Sizing', [46, 18, 18, 18, 30], 'LOAN SIZING — THE THREE TESTS',
               'What each standard test supports, against the amount requested.')
    L = "'Loan Request'!"
    r = 4
    head(ws, r, 'Test Assumptions', 5); r += 1
    R['t_ltv'] = f'B{r}'; r = line(ws, r, 'Target LTV — stabilized value', 0.65, fmt=PCT)
    R['t_dscr'] = f'B{r}'; r = line(ws, r, 'Target DSCR', 1.25, fmt=MULT)
    R['t_dy'] = f'B{r}'; r = line(ws, r, 'Target debt yield', 0.12, fmt=PCT)
    R['perm'] = f'B{r}'; r = line(ws, r, 'Permanent rate — amortizing test', PERM_RATE, fmt=PCT)
    R['amort'] = f'B{r}'; r = line(ws, r, 'Amortization, years', 30, fmt='0')
    n0 = r
    for y, *_, n in PRO:
        r = line(ws, r, f'Net operating income — {y}', n,
                 note=('Renovation year' if y == 2026 else
                       'First full year after reopening' if y == 2027 else 'Stabilizing year'))
    R['noi_2027'] = f'B{n0 + 1}'
    R['t_noi'] = f'B{r}'
    r = line(ws, r, 'NOI used in the tests below', f'=B{n0 + 2}', bold=True, accent=True,
             note='Editable — point it at any year above', rule=True)
    r += 1

    head(ws, r, 'Maximum Loan by Test', 5); r += 1
    r = grid_head(ws, r, ['Maximum loan', 'vs request', '', ''])
    m0 = r
    r = grid_row(ws, r, 'Loan to value — stabilized',
                 [f"={L}{R['val_stab']}*{R['t_ltv']}",
                  f'=B{r}-{L}{R["loan"]}', '', ''])
    r = grid_row(ws, r, 'Debt service coverage — interest-only',
                 [f"={R['t_noi']}/({R['t_dscr']}*{L}{R['allin']})",
                  f'=B{r}-{L}{R["loan"]}', '', ''])
    r = grid_row(ws, r, 'Debt service coverage — 30-year amortizing',
                 [f"={R['t_noi']}/({R['t_dscr']}*12*(-PMT({R['perm']}/12,{R['amort']}*12,1)))",
                  f'=B{r}-{L}{R["loan"]}', '', ''])
    r = grid_row(ws, r, 'Debt yield', [f"={R['t_noi']}/{R['t_dy']}", f'=B{r}-{L}{R["loan"]}',
                                       '', ''])
    m1 = r - 1
    r = grid_row(ws, r, 'Binding constraint — lowest of the four',
                 [f'=MIN(B{m0}:B{m1})', f'=B{r}-{L}{R["loan"]}', '', ''], bold=True, accent=True)
    r = grid_row(ws, r, 'Binding constraint on 2027 NOI — first full year',
                 [f"=MIN({L}{R['val_stab']}*{R['t_ltv']},"
                  f"{R['noi_2027']}/({R['t_dscr']}*{L}{R['allin']}),"
                  f"{R['noi_2027']}/({R['t_dscr']}*12*(-PMT({R['perm']}/12,{R['amort']}*12,1))),"
                  f"{R['noi_2027']}/{R['t_dy']})",
                  f'=B{r}-{L}{R["loan"]}', '', ''])
    r = grid_row(ws, r, 'Amount requested', [f'={L}{R["loan"]}', '', '', ''], bold=True, rule=True)
    for rr in range(m0, r):
        ws.cell(row=rr, column=3).number_format = MONEY
    r += 1

    head(ws, r, 'What the Request Implies', 5); r += 1
    r = line(ws, r, 'LTV on the stabilized estimate', f"={L}{R['loan']}/{L}{R['val_stab']}",
             fmt=PCT)
    r = line(ws, r, 'DSCR on 2028 NOI — interest-only',
             f"={R['t_noi']}/({L}{R['loan']}*{L}{R['allin']})", fmt=MULT)
    r = line(ws, r, 'DSCR on 2028 NOI — 30-year amortizing at the permanent rate',
             f"={R['t_noi']}/({L}{R['loan']}*12*(-PMT({R['perm']}/12,{R['amort']}*12,1)))",
             fmt=MULT)
    r = line(ws, r, 'Debt yield on 2028 NOI', f"={R['t_noi']}/{L}{R['loan']}", fmt=PCT,
             accent=True, rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='Targets and the NOI are editable. The tests above run on the stabilizing '
                      'year, which is a takeout view; the row beneath the binding constraint runs '
                      'the same four tests on the first full year after reopening. Neither sizes '
                      'on 2026, when the asset is down for the renovation and the interest and '
                      'carry reserve funded at close pays debt service in full.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    return ws


def add_operations(wb, R):
    ws = sheet(wb, 'Operations', [46, 16, 16, 16, 30], 'OPERATIONS AND COVERAGE, 2026 – 2028',
               'Underwritten projections, with coverage driven by the loan amount.')
    L = "'Loan Request'!"
    r = 4
    head(ws, r, 'Operating Projections', 5); r += 1
    r = grid_head(ws, r, [str(y) for y, *_ in PRO])
    r = grid_row(ws, r, 'Occupancy', [p[1] for p in PRO], fmt=PCT1)
    r = grid_row(ws, r, 'Average daily rate', [p[2] for p in PRO])
    r = grid_row(ws, r, 'RevPAR', [p[3] for p in PRO])
    r = grid_row(ws, r, 'Total revenue', [p[4] for p in PRO])
    noi = r
    r = grid_row(ws, r, 'Net operating income', [p[5] for p in PRO], bold=True, rule=True)
    r += 1

    head(ws, r, 'Senior Debt Service', 5); r += 1
    r = grid_head(ws, r, [str(y) for y, *_ in PRO])
    r = grid_row(ws, r, 'Debt service — interest-only', [f"=-{L}{R['ads']}"] * 3)
    ds = r - 1
    r = grid_row(ws, r, 'Cash flow after debt service',
                 [f'={C(2 + i)}{noi}+{C(2 + i)}{ds}' for i in range(3)])
    r = grid_row(ws, r, 'Debt service coverage',
                 [f"={C(2 + i)}{noi}/{L}{R['ads']}" for i in range(3)], fmt=MULT, bold=True)
    r = grid_row(ws, r, 'Debt yield', [f"={C(2 + i)}{noi}/{L}{R['loan']}" for i in range(3)],
                 fmt=PCT, accent=True, rule=True)
    r += 1

    head(ws, r, 'Permanent Takeout Test', 5); r += 1
    r = grid_head(ws, r, [str(y) for y, *_ in PRO])
    r = grid_row(ws, r, 'Indicative permanent rate', [f"='Loan Sizing'!{R['perm']}"] * 3, fmt=PCT)
    r = grid_row(ws, r, 'Annual debt service — 30-year amortizing',
                 [f"={L}{R['loan']}*12*(-PMT('Loan Sizing'!{R['perm']}/12,"
                  f"'Loan Sizing'!{R['amort']}*12,1))"] * 3)
    pa = r - 1
    r = grid_row(ws, r, 'Coverage on the permanent loan',
                 [f'={C(2 + i)}{noi}/{C(2 + i)}{pa}' for i in range(3)], fmt=MULT, bold=True,
                 rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='Net operating income is after a 4.0% management fee and a replacement '
                      'reserve. Estimated values are for the hotel and exclude the adjacent '
                      'Dogwood Cove parcel.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    return ws


def add_extended(wb, R):
    ws = sheet(wb, 'Extended Cash Flow', [40] + [11] * 12,
               'STABILIZED CASH FLOW CARRIED FORWARD, 2030 – 2041',
               'Dollars in thousands. 2030 is the first full year after a sale at the end of '
               'year three, so it is what a buyer underwrites.')
    L = "'Loan Request'!"
    r = 4
    r = grid_head(ws, r, [str(y) for y in EXT_YEARS])
    r = grid_row(ws, r, 'Occupancy', EXT['Occupancy'], fmt=PCT1)
    r = grid_row(ws, r, 'Average daily rate', EXT['Average daily rate'], fmt='$#,##0')
    r = grid_row(ws, r, 'RevPAR', EXT['RevPAR'], fmt='$#,##0')
    r = grid_row(ws, r, 'Rooms revenue', EXT['Rooms revenue'], fmt=NUM)
    r = grid_row(ws, r, 'Other operated departments', EXT['Other operated departments'], fmt=NUM)
    rev = r
    r = grid_row(ws, r, 'Total revenue', EXT['Total revenue'], fmt=NUM, bold=True)
    r = grid_row(ws, r, 'Operating expenses', EXT['Operating expenses'], fmt=NUM)
    noi = r
    r = grid_row(ws, r, 'Net operating income', EXT['Net operating income'], fmt=NUM, bold=True)
    r = grid_row(ws, r, 'NOI margin', [f'={C(2 + i)}{noi}/{C(2 + i)}{rev}' for i in range(12)],
                 fmt=PCT1)
    ncf = r
    r = grid_row(ws, r, 'Net cash flow at a 4.0% reserve',
                 EXT['Net cash flow at a 4.0% reserve'], fmt=NUM, rule=True)
    r += 1
    ds = r
    r = grid_row(ws, r, 'Senior debt service', [f"=-{L}{R['ads']}/1000"] * 12, fmt=NUM)
    r = grid_row(ws, r, 'Coverage on net operating income',
                 [f'={C(2 + i)}{noi}/-{C(2 + i)}{ds}' for i in range(12)], fmt=MULT, bold=True)
    r = grid_row(ws, r, 'Coverage at a 4.0% reserve',
                 [f'={C(2 + i)}{ncf}/-{C(2 + i)}{ds}' for i in range(12)], fmt=MULT)
    r = grid_row(ws, r, 'Cash flow after debt service',
                 [f'={C(2 + i)}{noi}+{C(2 + i)}{ds}' for i in range(12)], fmt=NUM, accent=True,
                 rule=True)
    cfads = r - 1
    r += 1
    r = line(ws, r, 'Minimum coverage over the period, in 2030', f'=B{ds + 1}', fmt=MULT,
             bold=True)
    r = line(ws, r, 'Aggregate cash flow after debt service, 2031 to 2041',
             f'=SUM(C{cfads}:M{cfads})*1000', bold=True, accent=True)
    r = line(ws, r, 'Net operating income in 2041 against 2030', f'=M{noi}/B{noi}', fmt=MULT,
             rule=True)
    return ws


SENS_LOANS = [8_000_000, 10_000_000, 11_000_000, 12_500_000, 14_000_000]
SENS_NOI = [0.85, 0.925, 1.00, 1.075, 1.15]


def add_sensitivity(wb, R):
    ws = sheet(wb, 'Sensitivity', [40] + [15] * 5 + [26],
               'COVERAGE AND DEBT YIELD ACROSS LOAN AMOUNTS',
               'On the 2028 stabilizing-year net operating income, at the all-in rate.')
    L = "'Loan Request'!"
    r = 4
    head(ws, r, 'Debt Service Coverage — interest-only, 2028 NOI', 6); r += 1
    r = grid_head(ws, r, [f'${v / 1e6:g}M' for v in SENS_LOANS])
    for f in SENS_NOI:
        grid_row(ws, r, f'NOI at {f:.0%} of underwritten',
                 [f"=({PRO[2][5]}*{f})/({v}*{L}{R['allin']})" for v in SENS_LOANS], fmt=MULT,
                 bold=(f == 1.00), rule=(f == SENS_NOI[-1]))
        r += 1
    r += 1

    head(ws, r, 'Debt Yield — 2028 NOI', 6); r += 1
    r = grid_head(ws, r, [f'${v / 1e6:g}M' for v in SENS_LOANS])
    for f in SENS_NOI:
        grid_row(ws, r, f'NOI at {f:.0%} of underwritten',
                 [f'=({PRO[2][5]}*{f})/{v}' for v in SENS_LOANS], fmt=PCT,
                 bold=(f == 1.00), rule=(f == SENS_NOI[-1]))
        r += 1
    r += 1

    head(ws, r, 'Leverage and Net Funding by Loan Amount', 6); r += 1
    r = grid_head(ws, r, [f'${v / 1e6:g}M' for v in SENS_LOANS])
    r = grid_row(ws, r, 'LTV — as-is', [f"={v}/{L}{R['val_is']}" for v in SENS_LOANS], fmt=PCT)
    r = grid_row(ws, r, 'LTV — stabilized',
                 [f"={v}/{L}{R['val_stab']}" for v in SENS_LOANS], fmt=PCT)
    r = grid_row(ws, r, 'Annual debt service',
                 [f"={v}*{L}{R['allin']}" for v in SENS_LOANS])
    r = grid_row(ws, r, 'Interest and carry reserve — 12 months',
                 [f"={v}*{L}{R['allin']}" for v in SENS_LOANS])
    r = grid_row(ws, r, 'Net proceeds at close',
                 [f"={v}-{v}*{L}{R['orig_pc']}-{v}*{L}{R['allin']}" for v in SENS_LOANS],
                 bold=True, accent=True, rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='The bold row is the underwritten case. Net proceeds are the gross loan '
                      'less the origination fee and the twelve-month interest and carry reserve.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    return ws


def add_basis(wb, R):
    ws = sheet(wb, 'Total Basis', [52, 18, 40], 'TOTAL COST BASIS',
               'The loan-driven lines move with the loan amount.')
    L = "'Loan Request'!"
    reserve = f"({L}{R['ads']}*{L}{R['res_mo']}/12)"
    r = 4
    head(ws, r, 'Acquisition', 3); r += 1
    a0 = r
    for lab, v in BASIS_ACQ:
        r = line(ws, r, lab, v)
    r = line(ws, r, 'Total acquisition', f'=SUM(B{a0}:B{r - 1})', bold=True, rule=True)
    t_acq = f'B{r - 1}'; r += 1

    head(ws, r, 'Renovation Program', 3); r += 1
    p0 = r
    for lab, v in BASIS_PIP:
        r = line(ws, r, lab, v)
    r = line(ws, r, 'Total renovation program', f'=SUM(B{p0}:B{r - 1})', bold=True, rule=True)
    t_pip = f'B{r - 1}'; r += 1

    head(ws, r, 'Other Costs', 3); r += 1
    o0 = r
    r = line(ws, r, 'Interest and carry reserve — 12 months', f'={reserve}')
    for lab, v in BASIS_OTH_FIXED:
        r = line(ws, r, lab, v)
    r = line(ws, r, 'Senior origination fee', f"={L}{R['loan']}*{L}{R['orig_pc']}")
    r = line(ws, r, 'Broker fee — MMCC', f"={L}{R['loan']}*{L}{R['brk_pc']}")
    r = line(ws, r, 'Total other costs', f'=SUM(B{o0}:B{r - 1})', bold=True, rule=True)
    t_oth = f'B{r - 1}'; r += 1

    r = line(ws, r, 'Total cost basis', f'={t_acq}+{t_pip}+{t_oth}', bold=True, accent=True)
    basis = f'B{r - 1}'
    r = line(ws, r, 'Cost basis per key — 58 keys', f"={basis}/{L}{R['keys']}", bold=True)
    r = line(ws, r, 'Senior loan to total cost basis', f"={L}{R['loan']}/{basis}", fmt=PCT,
             rule=True)
    c = ws.cell(row=r + 1, column=1,
                value='The basis includes $2,000,000 of sponsor cash already invested outside '
                      'loan proceeds. A further $642,693 was invested in the hotel between 2021 '
                      'and 2025, outside the plan above.')
    c.font = Font(name=F, size=9, italic=True, color='5A6068')
    return ws


def main():
    wb, R = build()
    add_sizing(wb, R)
    add_sources_uses(wb, R)
    add_operations(wb, R)
    add_extended(wb, R)
    add_sensitivity(wb, R)
    add_basis(wb, R)
    wb._sheets = [wb['Loan Request'], wb['Loan Sizing'], wb['Sources & Uses'], wb['Operations'],
                  wb['Extended Cash Flow'], wb['Sensitivity'], wb['Total Basis']]
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, os.pardir, os.pardir, 'package',
                       f'Wylder Tilghman Island - Senior Debt Model - '
                       f'{SENIOR / 1_000_000:g}M.xlsx')
    wb.save(out)
    print(f'  {os.path.basename(out)} — {len(wb.sheetnames)} tabs: '
          f'{", ".join(wb.sheetnames)}')
    return os.path.abspath(out)


if __name__ == '__main__':
    main()
