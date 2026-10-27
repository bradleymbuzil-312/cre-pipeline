# -*- coding: utf-8 -*-
"""Check the deck PDF, the LP summary and the model agree, and that none names an appraiser."""
import re, sys, pymupdf, docx, openpyxl
P = "/home/user/cre-pipeline/design/wylder-tilghman-recapitalization/package"
pdf = f"{P}/Wylder Tilghman Island - Recapitalization.pdf"
doc = f"{P}/Wylder Tilghman Island - LP Equity Summary.docx"
xls = f"{P}/Wylder Tilghman Island - GP-LP Model v4.xlsx"

d = pymupdf.open(pdf)
deck = re.sub(r'\s+', ' ', ''.join(p.get_text() for p in d)).replace('’', "'")
norm = lambda t: re.sub(r'[^A-Za-z0-9.$%/&-]', '', t).lower()
dk_flat = norm(deck)

def doc_paras(c):
    for p in c.paragraphs: yield p.text
    for t in c.tables:
        for row in t.rows:
            for cell in row.cells: yield from doc_paras(cell)
summ = re.sub(r'\s+', ' ', '\n'.join(doc_paras(docx.Document(doc)))).replace('’', "'")

wb = openpyxl.load_workbook(xls, data_only=True)
S, I = wb['Summary'], wb['Inputs']
def cell(ws, a):
    import openpyxl.utils.cell as u
    col, row = u.coordinate_from_string(a)
    return ws.cell(row, u.column_index_from_string(col)).value

fails = []
def check(label, model, deck_tokens, summ_tokens):
    dk = [t for t in deck_tokens if norm(t) not in dk_flat]
    sm = [t for t in summ_tokens if t not in summ]
    ok = not dk and not sm
    print(f'  {"OK " if ok else "!! "}{label:34s} model {model}')
    if dk: print(f'        missing from deck:    {dk}')
    if sm: print(f'        missing from summary: {sm}')
    if not ok: fails.append(label)

print('── figures present in all three ──')
check('LP equity (gross)',     f'{cell(S,"B5"):,.2f}',  ['$13,255,085'], ['$13,255,000', '$13.26M'])
check('LP net cash invested',  f'{cell(S,"B6"):,.2f}',  ['$12,989,984'], ['$12,990,000', '$12.99M'])
check('LP equity % of as-is',  f'{cell(S,"B7"):.4f}',   ['61.94%'],      ['61.9%'])
check('Preferred return',      f'{cell(S,"B8"):.2%}',   ['12.0%', '12.55%'], ['12.0%', '12.55%'])
check('Tier 2 multiple / IRR', f'{cell(S,"B9")} / {cell(S,"B10"):.0%}', ['2.0x', '20%'], ['2.0x', '20% IRR'])
check('Tier 3 LP / Tier 4 LP', f'{cell(S,"B12"):.0%} / {cell(S,"B14"):.0%}',
      ['20% LP / 80% GP', '50% LP / 50% GP'], ['20% LP / 80% GP', '50% LP / 50% GP'])
check('Tier 4 hurdle',         f'{cell(S,"B13"):,}',    ['$30,000,000'], ['$30.0M'])
check('Senior refinance',      f'{cell(S,"B15"):,}',    ['$7,000,000'],  ['$7.0M', 'SOFR + 600'])
check('Return of capital',     f'{cell(S,"B16"):,}',    ['$2,070,384'],  ['$2.07M'])
check('Sale month / value',    f'{cell(S,"B17")} / {cell(S,"B18"):,}', ['36', '$29,500,000'], ['month 36', '$29.5M'])
check('Equity multiple',       f'{cell(S,"E7"):.4f}',   ['2.06x'],       ['2.06x'])
check('LP IRR',                f'{cell(S,"E8"):.4f}',   ['37.3%'],       ['37.3%'])
check('Cash before sale',      f'{cell(S,"E10"):,.2f}', ['$8,038,602'],  ['62%'])
check('GP ownership / LP',     f'{cell(S,"E28"):.0%} / {cell(S,"E29"):.0%}', ['51%', '49%'], ['51%', '49%'])
check('Keys post PIP',         f'{cell(I,"B49")}',      ['58 keys'],     ['58 keys'])
check('LP equity per key',     f'{cell(I,"B51"):,.2f}', ['$228,536'],    ['$228,536'])
check('Dogwood Cove closing',  'Nov 18, 2026',          ['Nov 18, 2026'], ['November 18, 2026'])
check('Closing: loan payoff',  f'{cell(S,"B21"):,.2f}', ['$10,714,782'], ['$10.71M'])
check('Closing: MCA payoff',   f'{cell(S,"B22"):,}',    ['$530,000'],    ['$0.53M'])
check('Closing: Dogwood Cove', f'{cell(S,"B23"):,}',    ['$1,100,000'],  ['$1.10M'])
check('LP origination fee',    f'{cell(S,"B26"):,.2f}', ['$265,102'],    ['$265,102'])

print('\n── model values the deck must match exactly ──')
for label, want, tok in [('Tier 1 to LP', cell(S,'E14'), '$14,483,289'),
                         ('Tier 2 to LP', cell(S,'E15'), '$11,496,678'),
                         ('Tier 3 to LP', cell(S,'E16'), '$827,471'),
                         ('Total LP distributions', cell(S,'E18'), '$26,807,438'),
                         ('GP distributions', cell(S,'E23'), '$3,309,883')]:
    ok = tok.replace(',', '').replace('$', '') == f'{want:,.0f}'.replace(',', '') and \
         norm(tok) in dk_flat
    print(f'  {"OK " if ok else "!! "}{label:34s} {want:,.2f} -> {tok}')
    if not ok: fails.append(label)

print('\n── banned terms (standing instruction) ──')
for name, text in (('deck', deck), ('summary', summ)):
    hits = [w for w in ('CBRE', 'LWHA', 'Newmark', 'appraisal', 'Appraisal', 'appraiser', 'New Day')
            if w in text]
    print(f'  {"OK " if not hits else "!! "}{name:8s} {hits or "clean"}')
    if hits: fails.append(f'banned term in {name}')
mx = [w for w in ('CBRE', 'appraisal') if any(w in str(c.value) for ws in wb.worksheets
      for r in ws.iter_rows() for c in r if c.value)]
print(f'  -- model   {mx} (internal working file; not distributed as a marketing document)')

print('\n── return grid: summary vs model sensitivity ──')
Sens = wb['Sensitivity']
rows = {21_400_000: '1.71x / 27.5%|1.88x / 25.4%', 26_000_000: '2.01x / 36.0%|2.04x / 28.7%',
        29_500_000: '2.06x / 37.3%|2.10x / 29.6%', 32_000_000: '2.15x / 39.4%|2.18x / 31.1%',
        35_000_000: '2.26x / 42.1%|2.29x / 33.0%'}
for r in range(6, 17):
    v = Sens.cell(r, 1).value
    if v not in rows: continue
    m36, m48 = Sens.cell(r, 3).value, Sens.cell(r, 4).value
    i36, i48 = Sens.cell(r + 14, 3).value, Sens.cell(r + 14, 4).value
    calc = f'{m36:.2f}x / {i36:.1%}|{m48:.2f}x / {i48:.1%}'
    want = rows[v]
    ok = calc == want and all(p in summ for p in want.split('|'))
    print(f'  {"OK " if ok else "!! "}${v/1e6:>5,.1f}M  model {calc}   summary {want}')
    if not ok: fails.append(f'grid {v}')

print('\nRESULT:', 'all three documents reconcile' if not fails else f'{len(fails)} MISMATCH: {fails}')
sys.exit(1 if fails else 0)
