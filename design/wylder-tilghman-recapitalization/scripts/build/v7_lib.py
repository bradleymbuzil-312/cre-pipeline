# -*- coding: utf-8 -*-
"""Markup helpers and the shared-core extractor for the three capitalization packages."""
import io, re
DECKDIR = "/home/user/cre-pipeline/design/wylder-tilghman-recapitalization/deck"
SRC = f"{DECKDIR}/Wylder Tilghman Island - Recapitalization.dc.html"
CON  = 'font-family:var(--font-condensed);font-weight:700;text-transform:uppercase;'
MONO = 'font-family:var(--font-mono);'
BODY = 'font-family:var(--font-body);'
DISP = 'font-family:var(--font-display);'
HAIR = '1px solid var(--hairline)'
NAVY2 = '2px solid var(--mm-navy)'
DHAIR = '1px solid rgba(255,255,255,.14)'
DRULE = '1px solid rgba(255,255,255,.35)'

def sec(dark=False, pad='72px 96px', extra=''):
    bg = 'var(--mm-navy-900);color:#fff' if dark else 'var(--paper);color:var(--ink-900)'
    return (f'style="width:100%;height:100%;box-sizing:border-box;background:{bg};padding:{pad};'
            f'display:flex;flex-direction:column;font-family:var(--font-body);{extra}"')

def h2(t, dark=False, fs='46px', mb='24px', pb='18px'):
    col = '#fff' if dark else 'var(--mm-navy-900)'
    bd = 'rgba(255,255,255,.22)' if dark else 'var(--mm-navy)'
    return ('  <div style="width:64px;height:3px;background:var(--mm-orange);margin:0 0 20px;"></div>\n'
            f'  <h2 style="{DISP}font-weight:700;font-size:{fs};line-height:1.05;letter-spacing:-0.01em;'
            f'color:{col};margin:0 0 {mb};border-bottom:1px solid {bd};padding-bottom:{pb};">{t}</h2>\n')

def sub(t, dark=False, fs='14px', pb='9px', ind=6):
    c = '#fff' if dark else 'var(--mm-navy)'
    bd = DRULE if dark else '1px solid var(--mm-navy)'
    return (f'{" "*ind}<div style="{CON}font-size:{fs};letter-spacing:.18em;color:{c};'
            f'border-bottom:{bd};padding-bottom:{pb};">{t}</div>\n')

def row(k, v, kind='', fs='17px', pad=11, dark=False, note=None, ind=6, vfs=None):
    vfs = vfs or fs
    if dark:
        bb = DRULE if kind in ('sub', 'tot') else DHAIR
        lc = '#fff;'
        vc = {'': '#fff', 'sub': '#fff', 'tot': 'var(--mm-orange)', 'hi': 'var(--mm-orange)'}[kind]
    else:
        bb = {'': HAIR, 'sub': NAVY2, 'tot': '3px double var(--mm-navy)', 'hi': HAIR}[kind]
        lc = 'var(--ink-900);font-weight:600;' if kind in ('sub', 'tot') else 'var(--ink-700);'
        vc = {'': 'var(--ink-900)', 'sub': 'var(--mm-navy)', 'tot': 'var(--mm-orange)',
              'hi': 'var(--mm-orange)'}[kind]
    fw = 'font-weight:700;' if kind in ('sub', 'tot', 'hi') else ''
    bg = ('background:rgba(232,119,34,.06);' if (kind == 'hi' and not dark)
          else ('background:rgba(255,255,255,.06);' if kind == 'hi' else ''))
    s = (f'{" "*ind}<div style="display:flex;justify-content:space-between;align-items:baseline;'
         f'padding:{pad}px 2px;border-bottom:{bb};{bg}gap:16px;">'
         f'<span style="{BODY}font-size:{fs};color:{lc}">{k}</span>'
         f'<span style="{MONO}font-size:{vfs};color:{vc};{fw}text-align:right;">{v}</span></div>\n')
    if note:
        nc = 'var(--mm-navy-100)' if dark else 'var(--ink-500)'
        s += f'{" "*ind}<div style="padding:0 2px 8px;{BODY}font-size:13px;color:{nc};">{note}</div>\n'
    return s

def para(t, fs='17px', dark=False, auto=False, mt='14px', ind=6, col=None):
    c = col or ('var(--mm-navy-100)' if dark else 'var(--ink-700)')
    m = 'auto 0 0' if auto else f'{mt} 0 0'
    pt = 'padding-top:14px;' if auto else ''
    return (f'{" "*ind}<p style="{BODY}max-width:none;font-size:{fs};line-height:1.5;color:{c};'
            f'margin:{m};{pt}">{t}</p>\n')

def stat(lab, val, note='', dark=False, pad='16px 20px 0 0', br=True, vc=None, vfs='26px', ind=8):
    b = ('border-right:1px solid ' + ('rgba(255,255,255,.22)' if dark else 'var(--hairline)') + ';') if br else ''
    lc = 'var(--mm-navy-300)' if dark else 'var(--ink-500)'
    nc = 'var(--mm-navy-100)' if dark else 'var(--ink-500)'
    vc = vc or ('#fff' if dark else 'var(--mm-navy)')
    n = (f'<div style="{DISP}font-style:italic;font-size:15px;color:{nc};margin-top:4px;">{note}</div>'
         if note else '')
    return (f'{" "*ind}<div style="padding:{pad};{b}">'
            f'<div style="{CON}font-size:12px;letter-spacing:.14em;color:{lc};">{lab}</div>'
            f'<div style="{MONO}font-size:{vfs};line-height:1.15;font-weight:700;color:{vc};'
            f'margin-top:6px;">{val}</div>{n}</div>\n')

def tiles(items, cols=4, pad='34px 28px 34px 0'):
    out = ''
    for i, (lab, val, note, acc) in enumerate(items):
        br = '' if i % cols == cols - 1 else f'border-right:{HAIR};'
        bb = f'border-bottom:{HAIR};' if i < cols else ''
        col = 'var(--mm-orange)' if acc else 'var(--mm-navy-900)'
        out += (f'    <div style="padding:{pad};{br}{bb}display:flex;flex-direction:column;'
                'justify-content:center;">'
                f'<div style="{CON}font-size:13px;letter-spacing:.16em;color:var(--ink-500);">{lab}</div>'
                f'<div style="{DISP}font-weight:700;font-size:44px;line-height:1.05;color:{col};'
                f'margin-top:9px;">{val}</div>'
                f'<div style="{BODY}font-size:15.5px;color:var(--ink-500);margin-top:9px;'
                f'line-height:1.4;">{note}</div></div>\n')
    return out

# ───────────────────────────────── shared core, lifted from the working deck
SHARED = ['THE ASSET', 'PROPERTY OVERVIEW', 'ADJACENT ACQUISITION', 'THE SPONSOR',
          'WYLDER BRAND & RESUME', 'BUSINESS PLAN', 'RENOVATION SCHEDULE', 'BRAND AFFILIATION',
          'PROJECTIONS', 'CASH FLOW AND ASSUMPTIONS', 'EXTENDED CASH FLOW',
          'DEPARTMENTAL BENCHMARKS', 'HISTORICAL OPERATIONS', 'COMPETITIVE MARKET',
          'MARKET AND DEMAND', 'VALUE POSITIONING', 'SALE COMPARABLES', 'RECENT TRANSACTIONS']

def load_sections(path=SRC):
    s = io.open(path, encoding='utf-8').read()
    parts = re.split(r'(<!-- ═+ \d+ · [^═]*?═+ -->)', s)
    head = parts[0]
    body = {}
    for i in range(1, len(parts), 2):
        name = re.search(r'· ([^═]*?)\s*═', parts[i]).group(1)
        body[name] = parts[i + 1].rstrip('\n')
    return head, body

def write_deck(path, head, order, body, footer_label):
    out = head
    for n in order:
        out += f'<!-- ═══════════ 00 · {n} ═══════════ -->' + body[n] + '\n\n'
    out = out.rstrip('\n') + '\n'
    # every interior footer and both header stamps carry this package's label
    out = re.sub(r'Wylder Hotel Tilghman Island · [^<]*', f'Wylder Hotel Tilghman Island · {footer_label}', out)
    io.open(path, 'w', encoding='utf-8').write(out)
    return len(order)
