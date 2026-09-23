"""Assemble data/figures.csv and data/figures.json from the parsed source rows.

Inputs (all produced by other scripts from saved primary text):
  cache/revproc_rows.json   extract_revprocs.py + revproc_figures.py
  cache/fbar_rows.json      fbar_figures.py (optional until that family is done)
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
YEARS = range(2015, 2027)
COLUMNS = ['figure_id', 'figure_name', 'year', 'amount', 'unit', 'authority', 'authority_url', 'note']

NAMES = {
    'gift_annual_exclusion': 'Gift tax annual exclusion per donee (IRC 2503(b))',
    'gift_noncitizen_spouse': 'Annual exclusion for gifts to a non-citizen spouse (IRC 2523(i)(2))',
    'basic_exclusion': 'Estate and gift tax basic exclusion amount (IRC 2010(c)(3))',
    'gst_exemption': 'Generation-skipping transfer tax exemption (IRC 2631(c))',
    'section_2032a_cap': 'Special use valuation: maximum decrease in value of qualified real property (IRC 2032A(a)(3))',
    'section_6166_2pct_amount': 'Estate tax deferral: dollar amount used to figure the 2-percent portion (IRC 6601(j), 6166)',
    'form3520_foreign_gift_corp_partnership': 'Form 3520 reporting threshold: gifts from foreign corporations and partnerships (IRC 6039F(a), (d))',
    'form3520_foreign_gift_individual': 'Form 3520 reporting threshold: gifts and bequests from nonresident alien individuals and foreign estates',
    'expatriation_avg_tax_liability': 'Covered expatriate tax liability test: average annual net income tax (IRC 877(a)(2)(A))',
    'expatriation_877a_exclusion': 'Expatriation mark-to-market exclusion amount (IRC 877A(a)(3))',
    'fbar_penalty_nonwillful_max': 'FBAR civil penalty, non-willful violation, maximum (31 U.S.C. 5321(a)(5)(B)(i))',
    'fbar_penalty_willful_max_floor': 'FBAR civil penalty, willful violation: the dollar amount in the maximum (greater of this amount or 50% of the balance) (31 U.S.C. 5321(a)(5)(C)(i))',
    'nra_estate_credit': 'Estate tax unified credit for nonresident non-citizen decedents (IRC 2102(b)(1))',
}
ORDER = list(NAMES)

IRB = 'https://www.irs.gov/pub/irs-irbs/'
USC = 'https://www.govinfo.gov/content/pkg/USCODE-2024-title26/html/'

NOTES = {
    'gift_annual_exclusion': 'Per donee, present interests only.',
    'gift_noncitizen_spouse': 'Replaces the unlimited marital deduction for gifts to a spouse who is not a US citizen; present interests only.',
    'section_2032a_cap': 'Cap on the total reduction from fair market value when the executor elects special use valuation.',
    'section_6166_2pct_amount': 'This is the indexed form of the $1,000,000 in IRC 6601(j)(2)(A). The 2-percent portion is the lesser of the tentative tax on this amount plus the applicable exclusion amount, less the applicable credit, or the deferred tax; interest on the rest runs at 45% of the underpayment rate (IRC 6601(j)(1)(B)).',
    'form3520_foreign_gift_corp_partnership': 'Report on Form 3520 when aggregate purported gifts from foreign corporations and foreign partnerships in the taxable year exceed this amount (indexed form of the $10,000 in IRC 6039F(a)).',
    'expatriation_avg_tax_liability': 'Average annual net income tax for the 5 taxable years ending before the expatriation date; exceeding it makes the person a covered expatriate unless an 877A(g)(1)(B) exception applies. Keyed to the calendar year of expatriation.',
    'expatriation_877a_exclusion': 'Reduces the mark-to-market gain of a covered expatriate (but not below zero). Keyed to the year of the expatriation date.',
}

# Rev. Proc. 2018-18 superseded these 2018 items of Rev. Proc. 2017-58 after Pub. L. 115-97.
SUPERSEDED_2018 = {
    'basic_exclusion': ('3.35', 5600000),
    'expatriation_877a_exclusion': ('3.33', 713000),
    'form3520_foreign_gift_corp_partnership': ('3.42', 16111),
}


def money(n):
    return f'${n:,}'


def row(fid, year, amount, authority, url, note, unit='USD'):
    return {'figure_id': fid, 'figure_name': NAMES[fid], 'year': year, 'amount': amount,
            'unit': unit, 'authority': authority, 'authority_url': url, 'note': note}


def revproc_family():
    src = json.load(open(os.path.join(ROOT, 'cache', 'revproc_rows.json')))
    errs = [r for r in src if 'error' in r and not (
        r['figure_id'].strip() in ('basic_exclusion', 'gst_exemption') and r['year'] == 2026
        and 'mismatch' in r['error'])]
    if errs:
        raise SystemExit(f'unresolved parse errors: {errs}')
    src = [r for r in src if 'amount' in r]
    by = {}
    for r in src:
        by.setdefault((r['figure_id'], r['year']), []).append(r)
    out = []
    for fid in ['gift_annual_exclusion', 'gift_noncitizen_spouse', 'basic_exclusion',
                'section_2032a_cap', 'section_6166_2pct_amount',
                'form3520_foreign_gift_corp_partnership', 'expatriation_avg_tax_liability',
                'expatriation_877a_exclusion']:
        for y in YEARS:
            cands = by.get((fid, y), [])
            if y == 2018 and len(cands) > 1:
                cands = [c for c in cands if c['revproc'] == '2018-18']
            if len(cands) != 1:
                raise SystemExit(f'{fid} {y}: {len(cands)} candidates')
            c = cands[0]
            notes = [NOTES.get(fid, '')]
            if y == 2018 and fid in SUPERSEDED_2018:
                sec, old = SUPERSEDED_2018[fid]
                prior = [p for p in by[(fid, 2018)] if p['revproc'] == '2017-58']
                assert prior and prior[0]['amount'] == old, (fid, prior)
                notes.append(f'Rev. Proc. 2018-18 superseded the {money(old)} in Rev. Proc. 2017-58, '
                             f'sec. {sec}, 2017-45 I.R.B. 489, after Pub. L. 115-97 (TCJA).')
            elif y == 2018:
                notes.append('Rev. Proc. 2017-58 amount; not among the items Rev. Proc. 2018-18 modified.')
            authority = c['authority']
            if fid == 'basic_exclusion' and y == 2026:
                authority = ('IRC 2010(c)(3)(A) as amended by Pub. L. 119-21, sec. 70106; restated in '
                             + authority)
                notes.append('Set by statute for 2026 (not an inflation adjustment); indexed again from 2027. '
                             'Rev. Proc. 2025-32 states it in sec. 2.14 (Changes), not in the sec. 4 list.')
            elif fid == 'basic_exclusion' and 2018 <= y <= 2025:
                notes.append('Includes the Pub. L. 115-97 doubling (base $10,000,000) that ran 2018 to 2025.')
            if fid == 'gift_annual_exclusion' and y == 2026:
                notes.append('Sec. 4.42(3) also sets the IRC 2801 annual exception for covered gifts '
                             'and bequests from a covered expatriate at $19,000.')
            out.append(row(fid, y, c['amount'], authority, c['authority_url'],
                           ' '.join(n for n in notes if n)))
    # GST exemption equals the basic exclusion amount under IRC 2631(c).
    be = {r['year']: r for r in out if r['figure_id'] == 'basic_exclusion'}
    for y in YEARS:
        b = be[y]
        if y == 2026:
            c = [r for r in src if r['figure_id'] == 'gst_exemption' and r['year'] == 2026][0]
            assert c['amount'] == b['amount']
            out.append(row('gst_exemption', y, c['amount'], c['authority'], c['authority_url'],
                           'Rev. Proc. 2025-32 sec. 2.14 states the 2026 GST exemption directly: '
                           'equal to the $15,000,000 basic exclusion amount under IRC 2631(c).'))
        else:
            out.append(row('gst_exemption', y, b['amount'],
                           'IRC 2631(c) (GST exemption equals the basic exclusion amount); amount from '
                           + b['authority'], b['authority_url'],
                           'The Rev. Proc. does not list the GST exemption separately for this year; '
                           'IRC 2631(c) sets it equal to the basic exclusion amount.'))
    return out


def statutory_family():
    out = []
    n97 = IRB + 'irb97-25.pdf'
    for y in YEARS:
        out.append(row('form3520_foreign_gift_individual', y, 100000,
                       'Notice 97-34, sec. VI.B.1, 1997-25 I.R.B. 22, 30', n97,
                       'Not indexed. The $100,000 threshold is administrative (Notice 97-34), not in '
                       'IRC 6039F, which indexes only the $10,000 amount; count gifts from related '
                       'foreign persons together (sec. VI.B.3).'))
    out.append(row('nra_estate_credit', None, 13000, 'IRC 2102(b)(1)',
                   USC + 'USCODE-2024-title26-subtitleB-chap11-subchapB-sec2102.htm',
                   'One row for all years: not indexed, and the same $13,000 applies to every year '
                   '2015 to 2026 (substituted for $3,600 by Pub. L. 100-647 in 1988). Treaties can change '
                   'the credit (IRC 2102(b)(3)(A)). Year is left blank on purpose.'))
    return out


def fbar_family():
    p = os.path.join(ROOT, 'cache', 'fbar_rows.json')
    if not os.path.exists(p):
        return []
    return [row(**r) for r in json.load(open(p))]


def main():
    rows = revproc_family() + statutory_family() + fbar_family()
    rows.sort(key=lambda r: (ORDER.index(r['figure_id']), r['year'] or 0))
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data', 'figures.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: ('' if r[k] is None else r[k]) for k in COLUMNS})
    with open(os.path.join(ROOT, 'data', 'figures.json'), 'w') as f:
        json.dump(rows, f, indent=1, ensure_ascii=False)
    for bad in ('–', '—'):
        for r in rows:
            assert bad not in json.dumps(r, ensure_ascii=False), r
    counts = {}
    for r in rows:
        counts[r['figure_id']] = counts.get(r['figure_id'], 0) + 1
    print(len(rows), counts)


if __name__ == '__main__':
    main()
