# -*- coding: utf-8 -*-
"""Total basis (shared) and the tranche-specific pages for each of the three packages."""
from v7_lib import *
from figs_v7 import *
from v7_reno import BASIS_DATES, fmt as _rfmt

# ═════════════════════════════════════════════ TOTAL BASIS (shared)
ACQ = [('Acquisition and capital expenses', 10_714_782),
       ('Land and house acquisition &middot; 21441 Dogwood Cove', 1_100_000),
       ('Sponsor cash equity outside loan proceeds', 2_000_000)]
PIP = [('Room renovation', 1_425_000), ('Marina replacement and expansion', 250_000),
       ('Replace three-bedroom house', 500_000), ('Interior public space and FF&amp;E', 50_000),
       ('Convert boat bar', 50_000), ('Exterior and interior improvements', 300_000),
       ('Contingency', 258_000), ('Professional fees', 170_000),
       ('Dogwood Cove house renovation', 300_000)]
# other costs: the senior fee lines are itemized only in the senior package
OTH_BY = {
 'senior': [('Interest and carry reserve &middot; 12 months', 1_200_000),
            ('Working capital', 500_000), ('Senior origination fee', 200_000),
            ('Closing, legal and mortgage tax', 120_000), ('Broker fee &middot; MMCC', 100_000),
            ('Processing and third-party fees', 10_100)],
 'other':  [('Interest and carry reserve', 1_200_000), ('Working capital', 500_000),
            ('Financing fees', 300_000), ('Closing, legal and mortgage tax', 120_000),
            ('Processing and third-party fees', 10_100)]}
OTH = OTH_BY['senior']
T_ACQ, T_PIP, T_OTH = 13_814_782, 3_303_000, 2_130_100
assert sum(v for _, v in ACQ) == T_ACQ and sum(v for _, v in PIP) == T_PIP
assert all(sum(v for _, v in o) == T_OTH for o in OTH_BY.values())
assert T_ACQ + T_PIP + T_OTH == COST_BASIS

def total_basis(t='senior'):
    OTH = OTH_BY['senior'] if t in ('senior', 'hm') else OTH_BY['other']
    def grp(title, lines, tl, tot):
        s = sub(title, fs='13.5px')
        for k, v in lines:
            s += row(k, f'${v:,.0f}', pad=5, fs='15px')
        return s + row(tl, f'${tot:,.0f}', pad=5, fs='15px', kind='sub')
    GAP = '      <div style="height:12px;"></div>\n'
    left = (grp('Acquisition', ACQ, 'Total acquisition', T_ACQ) + GAP
     + grp('Other Costs', OTH, 'Total other costs', T_OTH)
     + '      <div style="height:14px;"></div>\n'
     + row('Total cost basis', f'${COST_BASIS:,.0f}', pad=9, fs='19px', kind='tot')
     + row('Cost basis per key &middot; 58 keys', f'${COST_BASIS_KEY:,.0f}', pad=7, fs='16px', kind='sub')
     + para('The basis includes <strong style="color:var(--mm-navy-900);">$2,000,000 of sponsor cash '
            'already invested</strong> outside loan proceeds &mdash; the same capital that stands as the '
            f'GP&rsquo;s pari passu interest in the partnership. The capitalization on page 18 funds '
            f'${TOTAL:,.0f} of this basis; a further $642,693 was invested in the hotel between 2021 and '
            '2025, outside the plan at right.', fs='14.5px', auto=True))
    right = grp('Renovation Program', PIP, 'Total renovation program', T_PIP)
    right += ('      <div style="height:14px;"></div>\n'
     f'      <div style="display:grid;grid-template-columns:repeat(4,1fr);align-items:start;'
     f'border-top:{NAVY2};">\n'
     + stat('Cost basis / key', f'${COST_BASIS_KEY:,.0f}', '58 keys', pad='14px 14px 0 0')
     + stat('Capitalization / key', f'${TOTAL/KEYS:,.0f}', 'Funded at close', pad='14px 14px 0 14px',
            vc='var(--mm-orange)')
     + stat('As-complete / key', f'${VAL["complete"]/KEYS:,.0f}', 'April 2027', pad='14px 14px 0 14px')
     + stat('Stabilized / key', f'${VAL["stab"]/KEYS:,.0f}', 'April 2029', br=False, pad='14px 0 0 14px')
     + '      </div>\n'
     + '      <div style="height:14px;"></div>\n' + sub('Start and Completion Dates', fs='13.5px')
     + ''.join(row(lab, f'{_rfmt(a)} &rarr; {_rfmt(b)}', pad=5, fs='15px',
                   kind=('sub' if lab.startswith('Punch') else ''))
               for lab, a, b in BASIS_DATES)
     + para('The renovation program is funded at close from the capitalization. The schedule by trade is '
            'on page 9. Per-key figures are stated on 58 keys &mdash; the 57 hotel keys post-renovation '
            'plus the Dogwood Cove residence. The estimated values are for the hotel and exclude the '
            'adjacent parcel.', fs='14.5px', auto=True))
    return ('<section data-label="Total Basis" data-screen-label="Total Basis" '
     'data-speaker-notes="Total cost basis of nineteen million two hundred forty-seven thousand eight '
     'hundred eighty-two dollars, three hundred thirty-one thousand eight hundred sixty per key on '
     'fifty-eight keys. Acquisition and payoff of thirteen million eight hundred fourteen thousand seven '
     'hundred eighty-two includes two million of sponsor cash already invested outside loan proceeds, which '
     'is the same capital standing as the general partner pari passu interest. The renovation program is '
     'three million three hundred three thousand, itemized at right and funded at close. Other costs are '
     'two million one hundred thirty thousand one hundred, including a twelve-month interest and carry '
     'reserve and five hundred thousand of working capital." '
     + sec(pad='48px 88px 38px') + '>\n'
     + h2('Total cost basis and the renovation program.', fs='41px', mb='17px', pb='14px')
     + '  <div style="display:grid;grid-template-columns:1.02fr 1fr;gap:50px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + left + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + right + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')

# ═════════════════════════════════════════════ returns grid (per tranche, exclusive)
def returns_grid(label, idx, mult, irr, cash, profit, extra_rows=(), note=''):
    """idx = indices into EXITS this package may show (loss levels already excluded)."""
    n = len(idx)
    cols = f'1.55fr repeat({n},1fr)'
    def hd(t, first=False, accent=False):
        if first:
            return (f'      <div style="padding:10px 4px 10px 0;border-bottom:{NAVY2};{CON}font-size:14px;'
                    f'letter-spacing:.12em;color:var(--ink-500);">{t}</div>\n')
        c = 'var(--mm-orange)' if accent else 'var(--mm-navy)'
        return (f'      <div style="padding:10px 6px;border-bottom:{NAVY2};border-left:{HAIR};{CON}'
                f'font-size:14px;color:{c};text-align:right;">{t}</div>\n')
    def tr(lab, vals, pad=13, bold=False, last=False, accent=False):
        bb = NAVY2 if last else HAIR
        lw = 'font-weight:600;color:var(--ink-900);' if bold else 'color:var(--ink-700);'
        s = (f'      <div style="padding:{pad}px 4px {pad}px 0;border-bottom:{bb};{BODY}font-size:16.5px;'
             f'{lw}">{lab}</div>\n')
        for j, v in enumerate(vals):
            hi = (idx[j] == B)
            c = ('var(--mm-orange-700)' if accent else 'var(--mm-navy-900)') if hi else 'var(--ink-900)'
            fw = 'font-weight:700;' if (hi or bold) else ''
            bg = 'background:rgba(232,119,34,.07);' if hi else ''
            s += (f'      <div style="padding:{pad}px 6px;border-bottom:{bb};border-left:{HAIR};{bg}{MONO}'
                  f'font-size:16px;text-align:right;color:{c};{fw}">{v}</div>\n')
        return s
    g = (f'    <div style="display:grid;grid-template-columns:{cols};flex:1;'
         'font-variant-numeric:tabular-nums;align-content:start;">\n')
    g += hd('Gross exit value', first=True)
    for i in idx:
        g += hd(f'${EXITS[i]/1e6:,.0f}M', accent=(i == B))
    g += tr('Implied cap rate on year 3 NOI', [f'{IMPLIED_CAP[i]:.2%}' for i in idx])
    g += tr('Implied value per key', [f'${EXITS[i]/KEYS:,.0f}' for i in idx])
    for lab, vals in extra_rows:
        g += tr(lab, [vals[i] for i in idx])
    g += tr(f'{label} &mdash; total cash received', [f'${cash[i]:,.0f}' for i in idx])
    g += tr(f'{label} &mdash; profit', [f'${profit[i]:,.0f}' for i in idx], bold=True)
    g += tr('Equity multiple', [f'{mult[i]:.2f}x' for i in idx], bold=True, accent=True)
    g += tr('IRR', [f'{irr[i]:.1%}' for i in idx], bold=True, accent=True, last=True)
    return g + '    </div>\n'

# ═════════════════════════════════════════════ small helpers used by the tranche builders
def dkv(k, v, accent=False, last=False, pad=26, ind=8):
    bb = '' if last else f'border-bottom:{DHAIR};'
    c = 'var(--mm-orange)' if accent else '#fff'
    return (f'{" "*ind}<div style="display:flex;justify-content:space-between;align-items:baseline;'
            f'padding:{pad}px 0;{bb}gap:14px;">'
            f'<span style="{BODY}font-size:18px;color:var(--mm-navy-100);">{k}</span>'
            f'<span style="{MONO}font-size:20px;color:{c};font-weight:700;">{v}</span></div>\n')

def bigcol(lab, big, ital, rows_, pos, fs='88px'):
    br = '' if pos == 'last' else f'border-right:{DRULE};'
    p = {'first': '0 44px 0 0', 'mid': '0 44px', 'last': '0 0 0 44px'}[pos]
    return (f'    <div style="padding:{p};{br}display:flex;flex-direction:column;">\n'
            f'      <div style="{CON}font-size:15px;letter-spacing:.2em;color:var(--mm-navy-300);">'
            f'{lab}</div>\n'
            f'      <div style="{DISP}font-weight:700;font-size:{fs};line-height:1;letter-spacing:-0.02em;'
            f'color:#fff;margin:12px 0 6px;">{big}</div>\n'
            f'      <div style="{DISP}font-style:italic;font-size:22px;color:var(--mm-orange-100);">'
            f'{ital}</div>\n'
            f'      <div style="margin-top:auto;padding-top:22px;border-top:{DRULE};">\n{rows_}'
            '      </div>\n    </div>\n')

def blk(title, body, ind=6):
    return (f'{" "*ind}<div>\n'
            f'{" "*(ind+2)}<div style="{CON}font-size:13px;letter-spacing:.18em;color:var(--mm-orange);'
            f'margin-bottom:8px;">{title}</div>\n'
            f'{" "*(ind+2)}<p style="{BODY}max-width:none;font-size:16px;line-height:1.45;color:#fff;'
            f'margin:0;">{body}</p>\n{" "*ind}</div>\n')
