"""Section 7520 rates, January 2015 to October 2026, from the monthly AFR revenue
rulings in the cached IRB text. Writes data/section7520_rates.csv and
data/sources/section7520-revrul-excerpts.txt."""
import csv
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, 'cache', 'irb')
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']

import sys
sys.path.insert(0, HERE)
from extract_revprocs import norm, triplets, page_of  # noqa: E402

TABLE = re.compile(r'Rate Under Section 7520 for (' + '|'.join(MONTHS) + r') (\d{4})')
RULING = re.compile(r'REV\.? ?RUL\.? (\d{4})[-–](\d+)', re.I)
PCT = re.compile(r'^(\d{0,2}\.\d{1,2}) ?%$')  # rates under 1% print as '.8%'


def scan(pattern=os.path.join(CACHE, '*.txt')):
    found = {}
    for path in sorted(glob.glob(pattern)):
        issue = os.path.basename(path)[:-4]
        lines = [norm(l).strip() for l in open(path).read().split('\n')]
        lines = [l for l in lines if l] if 'irsdrop' in path else lines
        for i, l in enumerate(lines):
            m = TABLE.search(l)
            if not m:
                continue
            month, year = MONTHS.index(m.group(1)) + 1, int(m.group(2))
            # the rate is the first bare percentage within the next few lines
            rate = None
            for j in range(i + 1, min(len(lines), i + 12)):
                p = PCT.match(lines[j].strip())
                if p:
                    rate = p.group(1)
                    break
            # the ruling number is on the table caption line or just above
            rr = None
            for j in range(i, max(0, i - 4), -1):
                r = RULING.search(lines[j])
                if r:
                    rr = f'{r.group(1)}-{int(r.group(2))}'
                    break
            if rate is None or rr is None:
                continue
            # Trust the ruling's own header over the table caption (IRB 2018-36
            # captions Rev. Rul. 2018-23's tables as '2018-21').
            head = None
            for j in range(i, max(0, i - 400), -1):
                h = re.match(r'^Rev\. Rul\. (\d{4})-(\d+)\s*$', lines[j].strip())
                if h:
                    head = f'{h.group(1)}-{int(h.group(2))}'
                    break
            found.setdefault((year, month), []).append(
                {'issue': issue, 'line': i, 'rate': rate, 'revrul': head or rr,
                 'caption': rr, 'lines': lines})
    return found


def ruling_start_page(lines, rr):
    """IRB page where the ruling starts, from 'See Rev. Rul. YYYY-N, page P' cross-references."""
    y, n = rr.split('-')
    m = re.search(r'Rev\. Rul\. ' + y + r'[-–]0?' + n + r',? page (\d+)', '\n'.join(lines), re.I)
    return int(m.group(1)) if m else None


def main():
    found = scan()
    # Fallback for months not yet in the corpus: rulings fetched by irs_drop.py.
    for k, v in scan(os.path.join(ROOT, 'cache', 'irsdrop', '*.txt')).items():
        found.setdefault(k, v)
    rows, excerpts, problems = [], [], []
    for year in range(2015, 2027):
        for month in range(1, 13):
            if (year, month) > (2026, 10):
                break
            c = found.get((year, month), [])
            rates = {x['rate'] for x in c}
            if not c:
                problems.append(f'{year}-{month:02d}: not found')
                continue
            if len(rates) > 1:
                problems.append(f'{year}-{month:02d}: conflicting {[(x["issue"], x["rate"]) for x in c]}')
            x = c[0]
            if x['caption'] != x['revrul']:
                problems.append(f"{year}-{month:02d}: table caption says Rev. Rul. {x['caption']}, "
                                f"ruling header says Rev. Rul. {x['revrul']} (using header)")
            rate = float(x['rate'])
            assert abs(round(rate, 1) - rate) < 1e-9, x['rate']
            if x['issue'].startswith('rr-'):
                cite = 'not yet in an I.R.B. issue (irs-drop release)'
                url = f"https://www.irs.gov/pub/irs-drop/{x['issue']}.pdf"
                page = None
            else:
                page = ruling_start_page(x['lines'], x['revrul'])
                issue_full = '20' + x['issue']
                cite = f"{issue_full} I.R.B. {page}" if page else f"{issue_full} I.R.B."
                url = f"https://www.irs.gov/pub/irs-irbs/irb{x['issue']}.pdf"
            rows.append({
                'year': year, 'month': month, 'rate_percent': f'{rate:.1f}',
                'revenue_ruling': f"Rev. Rul. {x['revrul']}",
                'irb_cite': cite,
                'table': f"Table 5, Rate Under Section 7520 for {MONTHS[month - 1]} {year}",
                'authority_url': url,
                'note': (f"IRB table caption misprints the ruling as Rev. Rul. {x['caption']}"
                         if x['caption'] != x['revrul'] else ''),
            })
            lo, hi = max(0, x['line'] - 2), x['line'] + 6
            excerpts.append(f"--- {year}-{month:02d}: Rev. Rul. {x['revrul']}, {cite} ---\n"
                            + '\n'.join(x['lines'][lo:hi]))
    with open(os.path.join(ROOT, 'data', 'section7520_rates.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(ROOT, 'data', 'sources', 'section7520-revrul-excerpts.txt'), 'w') as f:
        f.write('Section 7520 rate tables from the monthly AFR revenue rulings, local IRB corpus.\n\n'
                + '\n\n'.join(excerpts) + '\n')
    print(len(rows), 'rows')
    print('\n'.join(problems) or 'no problems')


if __name__ == '__main__':
    main()
