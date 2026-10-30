# -*- coding: utf-8 -*-
"""Shared pages, built per tranche so no package discloses another tranche's economics.

Isolation rule applied throughout:
  SHOWN to everyone  — capital AMOUNTS, position in the stack, term, leverage ratios.
  SHOWN to the recipient only — its own rate, fees, participation, returns and splits.
  NEVER shown — any other tranche's rate, fee, participation, promote or return.
"""
from v7_lib import *
from figs_v7 import *

TRANCHE_COLOR = {'senior': '#032D67', 'pref': '#957551', 'common': '#456EAB'}
TNAME = {'senior': 'the senior loan', 'pref': 'the preferred equity',
         'common': 'the common equity'}

# ───────────────────────────────────────────────── capital structure
def capital_structure(t):
    rows_ = [('Common equity &middot; LP', COMMON, 'common'),
             ('Preferred equity', PREF, 'pref'),
             ('Senior loan &middot; 1st trust deed', SENIOR, 'senior')]
    bar = '    <div style="display:flex;flex-direction:column;flex:1;min-height:0;">\n'
    for lab, amt, key in rows_:
        pc = amt / TOTAL
        on = (key == t)
        dim = '' if on else 'opacity:.42;'
        mark = ('<div style="position:absolute;left:0;top:0;bottom:0;width:7px;'
                'background:var(--mm-orange);"></div>') if on else ''
        bar += (f'      <div style="position:relative;flex:0 0 {pc*100:.2f}%;'
                f'background:{TRANCHE_COLOR[key]};{dim}'
                'box-sizing:border-box;padding:22px 30px;display:flex;flex-direction:column;'
                'justify-content:flex-end;min-height:0;overflow:hidden;">\n'
                f'        {mark}\n'
                f'        <div style="{DISP}font-weight:700;font-size:23px;color:#fff;">{lab}</div>\n'
                '        <div style="display:flex;justify-content:space-between;align-items:baseline;'
                'margin-top:5px;gap:14px;">'
                f'<span style="{CON}font-size:13px;letter-spacing:.16em;color:rgba(255,255,255,.82);">'
                f'${amt:,.0f}</span>'
                f'<span style="{MONO}font-size:19px;font-weight:700;color:#fff;">{pc:.2%}</span></div>\n'
                '      </div>\n')
    bar += ('    </div>\n'
            '    <div style="display:flex;justify-content:space-between;align-items:baseline;'
            f'margin-top:14px;padding-top:12px;border-top:{NAVY2};">'
            f'<span style="{CON}font-size:13px;letter-spacing:.18em;color:var(--mm-navy);">'
            'Total Capitalization</span>'
            f'<span style="{MONO}font-size:28px;font-weight:700;color:var(--mm-navy-900);">'
            f'${TOTAL:,.0f}</span></div>\n')

    meas = (sub('Capital Measures', pb='7px')
     + row('Senior loan &middot; 1st trust deed', f'${SENIOR:,.0f}', pad=4,
           kind=('hi' if t == 'senior' else ''))
     + row('Preferred equity', f'${PREF:,.0f}', pad=4, kind=('hi' if t == 'pref' else ''))
     + row('Common equity &middot; LP', f'${COMMON:,.0f}', pad=4, kind=('hi' if t == 'common' else ''))
     + row('Total capitalization', f'${TOTAL:,.0f}', kind='sub', pad=4)
     + row('GP co-investment &middot; sponsor cash', f'${GP_CASH:,.0f}', pad=4,
           note='John Flannigan, invested outside loan proceeds and remaining in the deal')
     + row('Senior LTV &middot; as-is', f'{LTV["is"]:.2%}', pad=4)
     + row('Senior LTV &middot; as-stabilized', f'{LTV["stab"]:.2%}', pad=4)
     + row('Senior loan to cost', f'{LTC:.2%}', pad=4)
     + row('Debt and preferred to as-is value', f'{(SENIOR+PREF)/VAL["is"]:.2%}', pad=4)
     + row('Total capitalization per key &middot; 58', f'${TOTAL/KEYS:,.0f}', kind='sub', pad=4))

    # ── terms: the recipient's own economics only
    if t == 'senior':
        terms = (row('Amount', f'${SENIOR:,.0f}', pad=4, vfs='15px')
         + row('Rate', f'{ALLIN:.2%} floating', pad=4, vfs='15px',
               note=f'SOFR {SOFR:.2%} plus a {SPREAD:.2%} spread, resetting monthly')
         + row('Term and amortization', f'{SR_TERM} years &middot; interest-only', pad=4, vfs='15px')
         + row('Exit participation', f'{SR_KICKER:.2%} of equity value at exit', pad=4, vfs='15px')
         + row('Origination fee', '2.00%', pad=4, vfs='15px', kind='sub'))
        note = ('The senior loan is a single advance funded in full at close, with no future funding '
                'obligation. The balance of the requirement is funded by subordinate capital, all of '
                'which closes concurrently.')
    elif t == 'pref':
        terms = (row('Commitment', f'${PREF:,.0f}', pad=4, vfs='15px')
         + row('Accrual rate', f'{PF_RATE_PIK:.2%}', pad=4, vfs='15px',
               note='Compounding on the outstanding balance')
         + row('Current pay', 'None &middot; fully accrued', pad=4, vfs='15px')
         + row('Cash sweep', 'Applied against the balance', pad=4, vfs='15px')
         + row('Exit participation', f'{PF_KICKER:.2%} of equity value at exit', pad=4, vfs='15px')
         + row('Origination fee', '2.00%', pad=4, vfs='15px', kind='sub'))
        note = ('The preferred equity funds in full at close, behind the senior loan and ahead of all '
                'common capital. There is no current-pay obligation; available cash flow sweeps against '
                'the balance.')
    else:
        terms = (row('LP commitment', f'${COMMON:,.0f}', pad=4, vfs='15px')
         + row('GP co-investment', f'${GP_CASH:,.0f}', pad=4, vfs='15px',
               note='Sponsor cash already invested, pari passu with the LP on the same terms')
         + row('Partnership capital', f'${PARTNERSHIP:,.0f}', pad=4, vfs='15px', kind='sub')
         + row('Preferred return', f'{CE_PREF:.2%} cumulative', pad=4, vfs='15px')
         + row('Residual split', '50 / 50 LP and GP', pad=4, vfs='15px')
         + row('Ownership interest', 'GP 51% &middot; LP 49%', pad=4, vfs='15px', kind='sub'))
        note = ('The LP and the GP fund a single partnership tranche on identical pari passu terms. '
                'The GP holds a 51% ownership interest and has contributed '
                f'${GP_CASH:,.0f} of its own cash, but takes no distribution until the LP has received '
                f'its {CE_PREF:.0%} preferred return and its capital back in full.')
    terms = ('      <div style="height:10px;"></div>\n'
             + sub('Your Terms', pb='7px') + terms + para(note, fs='15px', auto=True))

    sn = {'senior': ('This page is shown from the senior lender&rsquo;s perspective. The senior loan is '
                     'ten million dollars, forty-six point seven percent of as-is value and fifty-seven '
                     'point five percent of cost, at twelve percent floating and interest-only for three '
                     'years, with a five percent participation in equity value at exit. Seven million four '
                     'hundred four thousand of subordinate capital closes beneath it, all funded at close, '
                     'plus two million of sponsor cash already in the deal.'),
          'pref': ('This page is shown from the preferred investor&rsquo;s perspective. The preferred '
                   'commitment is three million nine hundred four thousand dollars, accruing at seventeen '
                   'percent with no current pay and a ten percent participation in equity value at exit. '
                   'Ten million of senior debt sits ahead of it and three million five hundred thousand of '
                   'common equity closes beneath it, plus two million of sponsor cash already in the deal. '
                   'Debt and preferred together are sixty-five percent of as-is value.'),
          'common': ('This page is shown from the common equity investor&rsquo;s perspective. The LP '
                     'commitment is three million five hundred thousand dollars alongside two million of '
                     'sponsor cash on identical pari passu terms, a five million five hundred thousand '
                     'dollar partnership. The LP earns a fifteen percent cumulative preferred return and '
                     'its capital back before any residual is split fifty-fifty. Thirteen million nine '
                     'hundred four thousand of senior and preferred capital sits ahead of the '
                     'partnership.')}[t]

    return ('<section data-label="Capital Structure" data-screen-label="Capital Structure" '
     f'data-speaker-notes="The capitalization is seventeen million four hundred four thousand dollars in '
     f'three tranches, all funded at close. {sn}" '
     + sec(pad='60px 96px 44px') + '>\n'
     + h2(f'A ${TOTAL:,.0f} capitalization in three tranches.', fs='44px', mb='15px', pb='13px')
     + '  <div style="display:grid;grid-template-columns:1.02fr 1fr;gap:50px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;min-height:0;">\n' + bar + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + meas + terms + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')


# ───────────────────────────────────────────────── sources and uses
BASE_USES = [('Existing loan payoff', 10_714_782),
             ('PIP / renovation', 3_003_000),
             ('@@RESERVE@@', SR_RESERVE),
             ('Land and house acquisition &middot; 21441 Dogwood Cove', 1_100_000),
             ('Working capital', 500_000),
             ('Dogwood Cove house renovation', 300_000)]
FEE_USES = {
    'senior': [('Senior origination fee &middot; 2.0%', SR_ORIG),
               ('Closing, legal and other', 130_100),
               ('Broker fee &middot; MMCC senior debt &middot; 1.0%', SR_BROKER),
               ('Other capitalization costs and fees', PF_ORIG + PF_MMCC)],
    'pref':   [('Preferred origination fee &middot; 2.0%', PF_ORIG),
               ('Preferred equity placement fee &middot; 2.0%', PF_MMCC),
               ('Closing, legal and other', 130_100),
               ('Other capitalization costs and fees', SR_ORIG + SR_BROKER)],
    'common': [('Closing, legal and other', 130_100),
               ('Capitalization costs and fees', SR_ORIG + SR_BROKER + PF_ORIG + PF_MMCC)]}
for _k, _v in FEE_USES.items():
    assert sum(a for _, a in BASE_USES) + sum(a for _, a in _v) == TOTAL, _k

NET_FUNDING = {
    'senior': ('Net Funding &middot; Senior Loan',
               [('Senior gross loan amount', f'${SENIOR:,.0f}', ''),
                ('Less origination fee &middot; 2.0%', f'(${SR_ORIG:,.0f})', ''),
                ('Less interest and carry reserve', f'(${SR_RESERVE:,.0f})', ''),
                ('Net senior proceeds at close', f'${SR_NET:,.0f}', 'sub')]),
    'pref':   ('Net Funding &middot; Preferred Equity',
               [('Preferred commitment', f'${PREF:,.0f}', ''),
                ('Less origination fee &middot; 2.0%', f'(${PF_ORIG:,.0f})', ''),
                ('Net preferred funded at close', f'${PF_NET:,.0f}', 'sub')]),
    'common': ('Net Funding &middot; Partnership',
               [('LP commitment', f'${COMMON:,.0f}', ''),
                ('GP co-investment &middot; sponsor cash', f'${GP_CASH:,.0f}', ''),
                ('Total partnership capital', f'${PARTNERSHIP:,.0f}', 'sub'),
                ('LP share of partnership capital', f'{COMMON/PARTNERSHIP:.2%}', '')])}


def sources_and_uses(t):
    src = sub('Sources')
    for lab, amt in SOURCES:
        src += row(lab, f'${amt:,.0f}', pad=15, fs='18px',
                   note=f'{amt/TOTAL:.2%} of total &middot; ${amt/KEYS:,.0f} per key')
    src += row('Total sources', f'${TOTAL:,.0f}', pad=15, fs='18px', kind='sub')
    src += ('      <div style="height:18px;"></div>\n' + sub('Closing, Legal and Other Detail')
     + ''.join(row(k, f'${v:,.0f}', pad=10) for k, v in CLOSING)
     + row('Total closing, legal and other', '$130,100', pad=10, kind='sub')
     + para('Maryland mortgage recording tax and stub interest on the existing loan are budgeted at zero '
            'and should be confirmed at closing.', fs='15px', auto=True))

    reserve = ('Interest and carry reserve &middot; 12 months' if t == 'senior'
               else 'Interest and carry reserve')
    uses = sub('Uses')
    for lab, amt in BASE_USES + FEE_USES[t]:
        uses += row(lab.replace('@@RESERVE@@', reserve), f'${amt:,.0f}', pad=9, fs='16.5px')
    uses += row('Total uses', f'${TOTAL:,.0f}', pad=9, fs='16.5px', kind='sub')
    uses += row('Sources less uses', '$0', pad=9, fs='16.5px', kind='hi')

    title, lines = NET_FUNDING[t]
    uses += ('      <div style="margin-top:auto;padding-top:18px;">\n' + sub(title, ind=8)
     + ''.join(row(k, v, pad=8, ind=8, kind=kd) for k, v, kd in lines) + '      </div>\n')

    sn = {'senior': 'Net senior proceeds at close are eight million six hundred thousand after the '
                    'origination fee and the carry reserve.',
          'pref': 'Net preferred funded at close is three million eight hundred twenty-five thousand nine '
                  'hundred sixty-three after the two percent origination fee.',
          'common': 'Total partnership capital is five million five hundred thousand &mdash; three million '
                    'five hundred thousand from the LP and two million of sponsor cash on the same terms. '
                    'The LP holds sixty-three point six four percent of partnership capital.'}[t]
    return ('<section data-label="Sources &amp; Uses" data-screen-label="Sources &amp; Uses" '
     'data-speaker-notes="Sources and uses at closing. Ten million of senior debt, three million nine '
     'hundred four thousand of preferred equity and three million five hundred thousand of common equity, '
     'seventeen million four hundred four thousand in total. The uses retire the ten million seven hundred '
     'fourteen thousand seven hundred eighty-two dollar existing loan, fund the three million three '
     'thousand dollar renovation program and the one million one hundred thousand dollar Dogwood Cove '
     'acquisition with three hundred thousand of renovation, and establish an interest and carry reserve '
     'of one million two hundred thousand plus five hundred thousand of working capital. Sources equal '
     f'uses to the dollar. {sn}" '
     + sec(pad='60px 96px 42px') + '>\n'
     + h2('Sources and uses of funds at closing.', fs='44px', mb='20px', pb='16px')
     + '  <div style="display:grid;grid-template-columns:1fr 1.06fr;gap:50px;flex:1;'
       'font-variant-numeric:tabular-nums;">\n'
       '    <div style="display:flex;flex-direction:column;">\n' + src + '    </div>\n'
       '    <div style="display:flex;flex-direction:column;">\n' + uses + '    </div>\n'
       '  </div>\n@@FOOTER@@\n</section>')

if __name__ == '__main__':
    for t in ('senior', 'pref', 'common'):
        a, b = capital_structure(t), sources_and_uses(t)
        bad = []
        FORBID = {'senior': ['17.00%', '15.00% cumulative', '10.00% of equity', '50 / 50',
                             f'${PF_ORIG:,.0f}', f'${PF_NET:,.0f}', f'${PARTNERSHIP:,.0f}'],
                  'pref': ['12.00%', 'SOFR', '5.00% of equity', '15.00% cumulative', '50 / 50',
                           f'${SR_NET:,.0f}', f'${PARTNERSHIP:,.0f}'],
                  'common': ['12.00%', 'SOFR', '17.00%', '5.00% of equity', '10.00% of equity',
                             f'${SR_NET:,.0f}', f'${PF_NET:,.0f}']}[t]
        for f in FORBID:
            if f in a or f in b:
                bad.append(f)
        print(f'{t:7s} capital_structure+sources_and_uses — leaks: {bad or "none"}')
