# -*- coding: utf-8 -*-
"""Renumber slide comments, running footers and cover/closing header stamps for any deck file."""
import io, re

def footer(page, label, dark=False, auto=False):
    col = 'rgba(255,255,255,.38)' if dark else 'var(--ink-400)'
    div = 'rgba(255,255,255,.28)' if dark else 'var(--hairline)'
    mt = 'auto' if auto else '24px'
    return (f'  <div style="margin-top:{mt};display:flex;justify-content:space-between;align-items:center;'
            'font-family:var(--font-condensed);font-size:14px;font-weight:700;letter-spacing:.2em;'
            f'text-transform:uppercase;color:{col};">\n'
            f'    <span>Wylder Hotel Tilghman Island · {label}</span>\n'
            '    <span style="display:flex;align-items:center;gap:20px;"><span>MMCC · The TRANCHE Group</span>'
            '<span style="font-family:var(--font-mono);letter-spacing:.08em;padding-left:20px;'
            f'border-left:1px solid {div};">{page:02d}</span></span>\n  </div>\n')

FOOT_RE = re.compile(
    r'  <div style="margin-top:(auto|24px);display:flex;justify-content:space-between;align-items:center;'
    r'font-family:var\(--font-condensed\);font-size:14px;font-weight:700;letter-spacing:\.2em;'
    r'text-transform:uppercase;color:[^"]*;">\s*<span>Wylder Hotel Tilghman Island · [^<]*</span>\s*'
    r'<span[^>]*>.*?</span>\s*</div>\n?', re.S)
HDR_RE = re.compile(
    r'(<span style="font-family:var\(--font-mono\);font-size:15px;font-weight:700;letter-spacing:\.08em;'
    r'color:rgba\(255,255,255,\.62\);padding-left:20px;border-left:1px solid rgba\(255,255,255,\.32\);">)\d\d(</span>)')


def renumber(deck, label, dark=frozenset(), quiet=False):
    s = io.open(deck, encoding='utf-8').read()
    parts = re.split(r'(<!-- ═+ \d+\w* · [^═]*?═+ -->)', s)
    names = [re.search(r'· ([^═]*?)\s*═', parts[i]).group(1) for i in range(1, len(parts), 2)]
    for k, name in enumerate(names):
        page = k + 1; i = 1 + 2 * k
        parts[i] = f'<!-- ═══════════ {page:02d} · {name} ═══════════ -->'
        b = parts[i + 1]
        if '@@FOOTER@@' in b:
            b = b.replace('@@FOOTER@@\n', footer(page, label, dark=(name in dark)))
        else:
            m = FOOT_RE.search(b)
            if m:
                b = (b[:m.start()] + footer(page, label, dark=(name in dark), auto=(m.group(1) == 'auto'))
                     + b[m.end():])
            else:
                b = HDR_RE.sub(lambda mm: f'{mm.group(1)}{page:02d}{mm.group(2)}', b)
        parts[i + 1] = b
    out = ''.join(parts)
    io.open(deck, 'w', encoding='utf-8').write(out)
    ok = True
    parts = re.split(r'(<!-- ═+ \d+ · [^═]*?═+ -->)', out)
    for k in range(1, len(parts), 2):
        m = re.search(r'(\d+) · ([^═]*?)\s*═', parts[k]); b = parts[k + 1]
        pg = re.search(r'border-left:1px solid [^"]*;">\s*(\d\d)</span>', b)
        p = pg.group(1) if pg else 'MISSING'
        if p != m.group(1):
            ok = False; print(f'  !! {m.group(1)} {m.group(2)} -> {p}')
    if not quiet:
        print(f'  {len(names)} slides · numbering ok: {ok} · leftover placeholders: {out.count("@@FOOTER@@")}')
    assert ok and out.count('@@FOOTER@@') == 0
    return len(names)
