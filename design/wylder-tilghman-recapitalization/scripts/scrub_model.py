# -*- coding: utf-8 -*-
"""Scrub the appraiser's name from the model's labels by rewriting sharedStrings only.

Formulas, formatting, conditional formatting and cached values are untouched: the only
part of the archive that changes is xl/sharedStrings.xml, and no formula references the
replaced literals.
"""
import zipfile, shutil, re, sys, html
SRC = sys.argv[1]
OUT = sys.argv[2]
REPL = [
 ('LP equity as % of CBRE as is', 'LP equity as % of estimated as is'),
 ('CBRE stabilized value (4/1/29). Assumption, not a market quote',
  'Estimated stabilized value (4/1/29). Assumption, not a market quote'),
 ('CBRE as is value (9/11/26)', 'Estimated as is value (9/11/26)'),
 ('CBRE as complete value (4/1/27)', 'Estimated as complete value (4/1/27)'),
 ('CBRE stabilized value (4/1/29)', 'Estimated stabilized value (4/1/29)'),
 ('Sale values reference CBRE appraisals (as is 9/11/26, as complete 4/1/27, stabilized 4/1/29). '
  'Sale timing is an assumption.',
  'Sale values are stated for underwriting purposes and are subject to completion of the renovation '
  'and stabilization of operations (as is 9/11/26, as complete 4/1/27, stabilized 4/1/29). Sale timing '
  'is an assumption.'),
]
zin = zipfile.ZipFile(SRC)
ss = zin.read('xl/sharedStrings.xml').decode('utf-8')
before = ss
for old, new in REPL:
    o, n = html.escape(old, quote=False), html.escape(new, quote=False)
    if o in ss:
        ss = ss.replace(o, n)
    elif old in ss:
        ss = ss.replace(old, new)
assert ss != before, 'no substitutions made'
left = [t for t in re.findall(r'<t[^>]*>(.*?)</t>', ss, re.S) if 'CBRE' in t or 'ppraisal' in t]
assert not left, f'still present: {left}'

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'xl/sharedStrings.xml':
            data = ss.encode('utf-8')
        zout.writestr(item, data)
print(f'rewrote xl/sharedStrings.xml; every other part copied byte for byte')
