"""Turn the extracted Rev. Proc. paragraphs into figure rows.

Reads cache/revproc_summary.json (written by extract_revprocs.py) and writes
cache/revproc_rows.json. Every amount is parsed from the paragraph text; nothing
is typed in by hand except the official first page of each Rev. Proc., which comes
from the IRB finding lists (see FIRST_PAGE)."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Official first page, from the cumulative finding lists in later IRB issues
# (e.g. "2025-32, 2025-45 I.R.B. 695" in IRB 2025-48).
FIRST_PAGE = {
    '2014-61': ('2014-47', 860), '2015-53': ('2015-44', 615), '2016-55': ('2016-45', 707),
    '2017-58': ('2017-45', 489), '2018-18': ('2018-10', 392), '2018-57': ('2018-49', 827),
    '2019-44': ('2019-47', 1093), '2020-45': ('2020-46', 1016), '2021-45': ('2021-48', 764),
    '2022-38': ('2022-45', 445), '2023-34': ('2023-48', 1287), '2024-40': ('2024-45', 1100),
    '2025-32': ('2025-45', 695),
}

# figure_id -> (paragraph key, amount regex)
PARSE = {
    'gift_annual_exclusion': ('gift_annual_exclusion', r'first \$([\d,]+) of gifts to any person'),
    'gift_noncitizen_spouse': ('gift_annual_exclusion',
                               r'first \$([\d,]+)(?: \(instead of .*?\))? of gifts to a spouse who is not a citizen'),
    'basic_exclusion': ('basic_exclusion', r'basic exclusion amount is \$([\d,]+)'),
    'basic_exclusion ': ('basic_exclusion_statutory', r'basic exclusion amount to \$([\d,]+) for calendar year'),
    'gst_exemption': ('basic_exclusion_statutory', r'2631\(c\) is equal to \$([\d,]+)'),
    'section_2032a_cap': ('section_2032a_cap', r'(?:cannot|may not) exceed \$([\d,]+)'),
    'section_6166_2pct_amount': ('section_6166_2pct_amount', r'6166 is \$([\d,]+)'),
    'form3520_foreign_gift_corp_partnership': ('form3520_foreign_gift_corp_partnership',
                                               r'exceeds \$([\d,]+)'),
    'expatriation_avg_tax_liability': ('expatriation_avg_tax_liability', r'is more than \$([\d,]+)'),
    'expatriation_877a_exclusion': ('expatriation_877a_exclusion', r'\(but not below zero\) by \$([\d,]+)'),
}

YEAR_IN_TEXT = r'(?:calendar year|taxable years beginning in|dying in calendar year|dying during calendar year) (\d{4})'


def main():
    summary = json.load(open(os.path.join(ROOT, 'cache', 'revproc_summary.json')))
    rows = []
    for fid, (key, rx) in PARSE.items():
        for s in summary:
            if s.get('key') != key or 'text' not in s:
                continue
            text = s['text']
            m = re.search(rx, text)
            if not m:
                rows.append({'figure_id': fid, 'year': s['year'], 'error': 'no amount', 'text': text})
                continue
            ym = set(re.findall(YEAR_IN_TEXT, text))
            if ym != {str(s['year'])} and key != 'basic_exclusion_statutory':
                rows.append({'figure_id': fid, 'year': s['year'], 'error': f'year mismatch {ym}'})
            issue, first = FIRST_PAGE[s['revproc']]
            pin = f", {s['page']}" if s.get('page') and s['page'] != first else ''
            rows.append({
                'figure_id': fid.strip(), 'year': s['year'], 'amount': int(m.group(1).replace(',', '')),
                'revproc': s['revproc'], 'section': s['section'],
                'authority': f"Rev. Proc. {s['revproc']}, sec. {s['section']}, {issue} I.R.B. {first}{pin}",
                'authority_url': f"https://www.irs.gov/pub/irs-irbs/irb{issue[2:]}.pdf",
                'source_file': f"data/sources/revproc-{s['revproc']}-excerpts.txt",
                'quote': text,
            })
    json.dump(rows, open(os.path.join(ROOT, 'cache', 'revproc_rows.json'), 'w'), indent=1)
    for r in sorted(rows, key=lambda r: (r['figure_id'], r['year'])):
        print(r['figure_id'], r['year'], r.get('amount'), r.get('authority') or r.get('error'))


if __name__ == '__main__':
    main()
