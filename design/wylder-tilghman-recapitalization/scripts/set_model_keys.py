# -*- coding: utf-8 -*-
"""Set the model's key count to 58 by editing the Inputs sheet XML only.

B49 (Keys post PIP) is a hardcoded input referenced by exactly one formula, B51
(=$B$18/$B$49). Both the input and B51's cached value are rewritten; every other
part of the archive is copied byte for byte, so formulas, formatting and all other
cached values survive untouched.
"""
import zipfile, re, sys

SRC, OUT, NEW_KEYS = sys.argv[1], sys.argv[2], 58
zin = zipfile.ZipFile(SRC)

# locate the Inputs sheet part
wbx = zin.read('xl/workbook.xml').decode('utf-8')
rels = zin.read('xl/_rels/workbook.xml.rels').decode('utf-8')
rid = re.search(r'<sheet[^>]*name="Inputs"[^>]*r:id="([^"]+)"', wbx).group(1)
target = 'xl/' + re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1).lstrip('/')
xml = zin.read(target).decode('utf-8')

def cell(ref):
    m = re.search(rf'<c r="{ref}"[^>]*>.*?</c>|<c r="{ref}"[^>]*/>', xml, re.S)
    return m

b49, b51 = cell('B49'), cell('B51')
assert b49 and b51, 'B49/B51 not found'
print('before:')
print('  B49', b49.group(0))
print('  B51', b51.group(0))
assert '<v>57</v>' in b49.group(0), 'B49 is not 57'
assert re.search(r'<f>\$?B\$?18/\$?B\$?49</f>', b51.group(0)), 'B51 is not the per-key formula'

b18 = cell('B18')
gross = float(re.search(r'<v>([^<]+)</v>', b18.group(0)).group(1))
print(f'  B18 (LP equity gross) = {gross:,.6f}')
new_per_key = gross / NEW_KEYS
out49 = b49.group(0).replace('<v>57</v>', f'<v>{NEW_KEYS}</v>')
out51 = re.sub(r'<v>[^<]*</v>', f'<v>{new_per_key!r}</v>', b51.group(0))
xml2 = xml.replace(b49.group(0), out49).replace(b51.group(0), out51)
assert xml2 != xml

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == target:
            data = xml2.encode('utf-8')
        zout.writestr(item, data)
print(f'\nafter:  B49 -> {NEW_KEYS}   B51 -> {new_per_key:,.2f}   (sheet part: {target})')
