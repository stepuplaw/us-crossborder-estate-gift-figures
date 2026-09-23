"""Render REPORT.md from scripts/report_template.md, filling {{PIVOT}} and
{{PIVOT7520}} from data/figures.csv and data/section7520_rates.csv, and
normalize dash characters in data/sources/ to hyphens (house style)."""
import csv
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEARS = list(range(2015, 2027))
SHORT = {
    'gift_annual_exclusion': 'Gift annual exclusion (2503(b))',
    'gift_noncitizen_spouse': 'Non-citizen spouse annual exclusion (2523(i))',
    'basic_exclusion': 'Basic exclusion amount (2010(c))',
    'gst_exemption': 'GST exemption (2631(c))',
    'section_2032a_cap': 'Special use valuation cap (2032A)',
    'section_6166_2pct_amount': '6166 2-percent portion amount (6601(j))',
    'form3520_foreign_gift_corp_partnership': 'Form 3520: gifts from foreign corps/partnerships (6039F)',
    'form3520_foreign_gift_individual': 'Form 3520: gifts from foreign individuals/estates (Notice 97-34)',
    'expatriation_avg_tax_liability': 'Covered expatriate tax test (877(a)(2)(A))',
    'expatriation_877a_exclusion': 'Mark-to-market exclusion (877A(a)(3))',
    'fbar_penalty_nonwillful_max': 'FBAR non-willful maximum (5321(a)(5)(B))',
    'fbar_penalty_willful_max_floor': 'FBAR willful: dollar amount in max (5321(a)(5)(C))',
    'nra_estate_credit': 'Nonresident alien estate credit (2102(b)(1))',
}
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def pivot():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'figures.csv'))))
    by = {}
    for r in rows:
        by[(r['figure_id'], r['year'])] = int(r['amount'])
    out = ['| Figure | ' + ' | '.join(map(str, YEARS)) + ' |',
           '|---|' + '---:|' * len(YEARS)]
    for fid, label in SHORT.items():
        cells = []
        for y in YEARS:
            v = by.get((fid, str(y)), by.get((fid, '')))
            cells.append(f'{v:,}' if v is not None else '')
        out.append(f'| {label} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


def pivot7520():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'section7520_rates.csv'))))
    by = {(int(r['year']), int(r['month'])): r['rate_percent'] for r in rows}
    out = ['| Year | ' + ' | '.join(MONTHS) + ' |', '|---|' + '---:|' * 12]
    for y in YEARS:
        out.append(f'| {y} | ' + ' | '.join(by.get((y, m), '') for m in range(1, 13)) + ' |')
    return '\n'.join(out)


def normalize_sources():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'data', 'sources', '*.txt')):
        t = open(p).read()
        u = t.replace('—', '--').replace('–', '-')
        if u != t:
            open(p, 'w').write(u)
            n += 1
    return n


def main():
    tpl = open(os.path.join(ROOT, 'scripts', 'report_template.md')).read()
    out = tpl.replace('{{PIVOT}}', pivot()).replace('{{PIVOT7520}}', pivot7520())
    open(os.path.join(ROOT, 'REPORT.md'), 'w').write(out)
    print('sources normalized:', normalize_sources())
    for p in [os.path.join(ROOT, f) for f in ('REPORT.md', 'README.md', 'data/figures.csv',
                                              'data/figures.json', 'data/section7520_rates.csv')]:
        if os.path.exists(p):
            bad = re.findall('[–—]', open(p).read())
            print(os.path.basename(p), 'dashes:', len(bad))


if __name__ == '__main__':
    main()
