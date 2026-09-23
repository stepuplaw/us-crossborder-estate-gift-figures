"""FBAR civil penalty maximums by year, parsed from the saved Federal Register
rules (cache/fr/*.txt, from GovInfo). Writes cache/fbar_rows.json and saves an
excerpt of each rule to data/sources/fr-<doc>-excerpt.txt."""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FR = os.path.join(ROOT, 'cache', 'fr')
SRC = os.path.join(ROOT, 'data', 'sources')

# tax year -> FinCEN (or Treasury-wide) annual adjustment document in effect that year
ADJ = [
    (2016, '2016-15653'), (2017, '2017-01637'), (2018, '2018-05550'), (2019, '2019-22094'),
    (2020, '2020-02526'), (2021, '2021-01919'), (2022, '2022-01284'), (2023, '2023-00943'),
    (2024, '2024-01420'), (2025, '2025-01374'),
]
# Notice showing OMB M-26-11 cancelled the 2026 adjustment government-wide.
CANCEL_DOC = '2026-09334'


def clean(doc):
    t = open(os.path.join(FR, doc + '.txt')).read()
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    return re.sub(r'[ \t]+', ' ', t)


def meta(doc):
    return json.load(open(os.path.join(FR, doc + '.meta.json')))


def amounts(t):
    """Last dollar column of the 5321(a)(5)(B)(i) and 5321(a)(5)(C) table rows."""
    flat = re.sub(r'\s+', ' ', t)
    out = {}
    for key, pat in (('nonwillful', r'5321\(a\)\(5\)\(B\)\(i\)'), ('willful', r'5321\(a\)\(5\)\(C\)')):
        # Tables wrap differently each year; take the row text from the cite up to the
        # next '31 U.S.C.' and read the numbers after the statutory amount.
        base = '10,000' if key == 'nonwillful' else '100,000'
        for m in re.finditer(pat, flat):
            seg = flat[m.start():m.start() + 300].split('31 U.S.C.')[0]
            nums = re.findall(r'\b\d{1,3}(?:,\d{3})+\b', seg)
            if base in nums and nums.index(base) + 1 < len(nums):
                # columns: statutory amount, [prior adjusted amount,] new amount
                after = nums[nums.index(base) + 1:]
                out[key] = (int(after[-1].replace(',', '')) if len(after) <= 2 else None, seg)
                break
        if key not in out:
            # 2022 layout: 'Foreign Financial Agency 10,000 14,489 5321(a)(5)(B)(i)'
            m = re.search(r'Foreign Financial Agency ' + re.escape(base) + r' ([\d,]+) ' + pat, flat)
            if m:
                out[key] = (int(m.group(1).replace(',', '')), flat[m.start():m.start() + 200])
    return out


def dates_line(t):
    m = re.search(r'DATES:(.*?)(?:\n\s*\n|FOR FURTHER)', t, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def main():
    rows, log = [], []
    fin = 'https://www.federalregister.gov/d/'
    # 2015: no adjustment yet; statutory amounts.
    usc = 'https://www.govinfo.gov/content/pkg/USCODE-2024-title31/html/USCODE-2024-title31-subtitleIV-chap53-subchapII-sec5321.htm'
    rows.append(dict(fid='fbar_penalty_nonwillful_max', year=2015, amount=10000,
                     authority='31 U.S.C. 5321(a)(5)(B)(i)', url=usc,
                     note='Statutory amount; the first inflation adjustment took effect August 1, 2016.'))
    rows.append(dict(fid='fbar_penalty_willful_max_floor', year=2015, amount=100000,
                     authority='31 U.S.C. 5321(a)(5)(C)(i)(I)', url=usc,
                     note='Statutory amount; maximum is the greater of this amount or 50% of the '
                          'account balance at the time of the violation (5321(a)(5)(C)(i)(II), (D)).'))
    for year, doc in ADJ:
        t, m = clean(doc), meta(doc)
        a = amounts(t)
        assert 'nonwillful' in a and 'willful' in a and a['nonwillful'][0] and a['willful'][0], (doc, a)
        dl = dates_line(t)
        cite = f"{m['citation']} ({m['publication_date']}), amending 31 CFR 1010.821, Table 1"
        with open(os.path.join(SRC, f'fr-{doc}-excerpt.txt'), 'w') as f:
            f.write(f"{m['citation']}, {m['publication_date']}: {m['title']}\n"
                    f"FR Doc. {doc}. Text from GovInfo: {m.get('govinfo_url')}\n"
                    f"DATES: {dl}\n\nTable rows for 31 U.S.C. 5321(a)(5):\n"
                    f"{a['nonwillful'][1]}\n{a['willful'][1]}\n")
        eff = m.get('effective_on') or ''
        common = (f'Adjustment effective {eff}; applies to penalties assessed after that date for '
                  f'violations after November 2, 2015. ')
        if doc == '2018-05550':
            common += ('Treasury-wide rule covering FinCEN; 84 FR 51973 (Oct. 1, 2019) later corrected '
                       'its table dates, not its amounts. ')
        rows.append(dict(fid='fbar_penalty_nonwillful_max', year=year, amount=a['nonwillful'][0],
                         authority=cite, url=fin + doc, note=common.strip()))
        rows.append(dict(fid='fbar_penalty_willful_max_floor', year=year, amount=a['willful'][0],
                         authority=cite, url=fin + doc,
                         note=(common + 'Maximum is the greater of this amount or 50% of the balance '
                               '(31 U.S.C. 5321(a)(5)(C), (D)).')))
        log.append((year, doc, a['nonwillful'][0], a['willful'][0], dl))
    # 2026: OMB cancelled the adjustment; FinCEN published no 2026 table.
    c = meta(CANCEL_DOC)
    last = {r['fid']: r for r in rows if r['year'] == 2025}
    for fid in ('fbar_penalty_nonwillful_max', 'fbar_penalty_willful_max_floor'):
        rows.append(dict(fid=fid, year=2026, amount=last[fid]['amount'],
                         authority=last[fid]['authority'] + '; 2026 adjustment cancelled by OMB M-26-11 '
                                   f"(Apr. 17, 2026), as reported at {c['citation']} ({c['publication_date']})",
                         url=last[fid]['url'],
                         note=('No 2026 adjustment. OMB memorandum M-26-11 (Apr. 17, 2026) cancelled the '
                               '2026 civil penalty inflation adjustment and told agencies to keep 2025 levels; '
                               'FinCEN published no 2026 adjustment in the Federal Register (searched through '
                               '2026-09-23), so the 2025 amount carries over.')))
    out = [dict(fid=r['fid'], year=r['year'], amount=r['amount'], authority=r['authority'],
                url=r['url'], note=r['note']) for r in rows]
    json.dump([{'fid': r['fid'], **{k: v for k, v in r.items() if k != 'fid'}} for r in out],
              open(os.path.join(ROOT, 'cache', 'fbar_rows.json'), 'w'), indent=1)
    t = clean(CANCEL_DOC)
    i = t.find('On April 17, 2026')
    with open(os.path.join(SRC, f'fr-{CANCEL_DOC}-excerpt.txt'), 'w') as f:
        f.write(f"{c['citation']}, {c['publication_date']}: {c['title']} (Pension Benefit Guaranty Corporation)\n"
                f"FR Doc. {CANCEL_DOC}. Text from GovInfo: {c.get('govinfo_url')}\n\n"
                + re.sub(r'\s+', ' ', t[i:i + 700]) + '\n')
    for l in log:
        print(l)


if __name__ == '__main__':
    main()
