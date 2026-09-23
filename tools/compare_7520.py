"""Compare data/section7520_rates.csv with the Evans 7520 chart (a secondary
cross-check of the extraction, not a source)."""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = [l.strip() for l in open(os.path.join(ROOT, 'data', 'sources',
                                              'US-popular-evans-legal-7520-rates.txt'))]
cells = [l.lstrip('| ').strip() for l in lines if l.startswith('|')]
evans = {}
i = 0
while i < len(cells):
    if re.fullmatch(r'(19|20)\d\d', cells[i]):
        y = int(cells[i])
        vals = cells[i + 1:i + 13]
        for m, v in enumerate(vals, 1):
            mm = re.match(r'(\d*\.\d)%', v)
            if mm:
                evans[(y, m)] = float(mm.group(1))
        i += 13
    else:
        i += 1
ours = {(int(r['year']), int(r['month'])): float(r['rate_percent'])
        for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'section7520_rates.csv')))}
diff = [(k, ours[k], evans.get(k)) for k in sorted(ours) if evans.get(k) != ours[k]]
print(f'compared {sum(1 for k in ours if k in evans)} of {len(ours)} months; differences: {diff}')
