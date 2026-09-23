"""Pull the estate, gift and expatriation paragraphs out of each annual inflation
Rev. Proc. in the cached IRB text, with the IRB page each paragraph sits on.

Writes data/sources/revproc-<number>-excerpts.txt and cache/revproc_summary.json."""
import json
import os
import re

from revproc_figures import FIRST_PAGE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, 'cache', 'irb')
SRC = os.path.join(ROOT, 'data', 'sources')
os.makedirs(SRC, exist_ok=True)

# tax year -> (Rev. Proc., IRB issue)
REVPROCS = [
    (2015, '2014-61', '14-47'),
    (2016, '2015-53', '15-44'),
    (2017, '2016-55', '16-45'),
    (2018, '2017-58', '17-45'),
    (2018, '2018-18', '18-10'),
    (2019, '2018-57', '18-49'),
    (2020, '2019-44', '19-47'),
    (2021, '2020-45', '20-46'),
    (2022, '2021-45', '21-48'),
    (2023, '2022-38', '22-45'),
    (2024, '2023-34', '23-48'),
    (2025, '2024-40', '24-45'),
    (2026, '2025-32', '25-45'),
]

TOPICS = {
    'basic_exclusion': r'Unified Credit Against Estate Tax',
    'section_2032a_cap': r'Qualified Real Property',
    'gift_annual_exclusion': r'Annual Exclusion for Gifts',
    'form3520_foreign_gift_corp_partnership': r'Notice of Large Gifts',
    'expatriation_avg_tax_liability': r'Expatriation to Avoid Tax',
    'expatriation_877a_exclusion': r'Tax Responsibilities of Expatriation',
    'section_6166_2pct_amount': r'Estate Tax Payable in Installments',
    # Rev. Proc. 2025-32 sec. 2.14 restates the OBBBA $15,000,000 amount instead
    # of listing an inflation-adjusted basic exclusion item in section 4.
    'basic_exclusion_statutory': r'amends § 2010\(c\)',
}

ITEM_START = re.compile(r'^\.(\d{2}) ')
SECTION = re.compile(r'^(?:SECTION|Section|SEC\.) (\d+)\.')
PAGE_NUM = re.compile(r'^\d{1,4}$')
DATE = re.compile(r'^(January|February|March|April|May|June|July|August|September|'
                  r'October|November|December) \d{1,2}, \d{4}$')


def norm(s):
    s = re.sub(r'[\x00-\x08\x0b-\x1f]', '', s)
    return (s.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬀ', 'ff')
            .replace('–', '-').replace('—', '-').replace('’', "'")
            .replace('“', '"').replace('”', '"').replace('\x07', '')
            .replace(' ', ' '))


def load(issue):
    with open(os.path.join(CACHE, issue + '.txt')) as f:
        return [norm(l) for l in f.read().split('\n')]


def triplets(lines):
    """(line index of page number, page number) for every page-marker triplet."""
    out = []
    for i, l in enumerate(lines):
        if PAGE_NUM.match(l.strip()):
            near = lines[max(0, i - 2):i + 3]
            if any('Bulletin No.' in x for x in near) and any(DATE.match(x.strip()) for x in near):
                out.append((i, int(l.strip())))
    # A code-section number in a table of contents can sit next to a page
    # marker and pass the test above; real page numbers run in sequence.
    keep = []
    for k, (i, p) in enumerate(out):
        nb = [q for _, q in out[max(0, k - 2):k] + out[k + 1:k + 3]]
        if any(0 < abs(p - q) <= 2 for q in nb):
            keep.append((i, p))
    return keep


def page_mode(lines, trips):
    """'header' if the marker opens each page (IRBs from about 2019 on), else 'footer'."""
    return 'header' if trips and trips[0][0] < 10 else 'footer'


def page_of(i, trips, mode):
    if mode == 'header':
        prev = [p for j, p in trips if j <= i]
        return prev[-1] if prev else None
    nxt = [p for j, p in trips if j >= i]
    return nxt[0] if nxt else None


def is_marker(lines, j):
    s = lines[j].strip()
    return 'Bulletin No.' in s or DATE.match(s) or (PAGE_NUM.match(s) and any(
        'Bulletin No.' in x for x in lines[max(0, j - 2):j + 3]))


def find_start(lines, rp):
    pat = re.compile(r'^Rev\. Proc\. ' + re.escape(rp) + r'\s*$')
    hits = [i for i, l in enumerate(lines) if pat.match(l.strip())]
    return hits[0] if hits else None


def find_end(lines, start):
    pat = re.compile(r'^(Rev\. Proc\.|Rev\. Rul\.|Notice|T\.D\.) \d{4}-\d+\s*$')
    for i in range(start + 1, len(lines)):
        if pat.match(lines[i].strip()):
            return i
    return len(lines)


def flatten(parts):
    s = ' '.join(p.strip() for p in parts if p.strip())
    s = re.sub(r'­\s*', '', s)
    return re.sub(r'\s+', ' ', s)


def items(lines, start, end):
    """Every '.NN Title. body' paragraph in the Rev. Proc., skipping TOC lines."""
    out = []
    section = None
    cur = None
    for i in range(start, end):
        l = lines[i]
        m = SECTION.match(l.strip())
        if m:
            section = m.group(1)
            if cur:
                out.append(cur)
                cur = None
            continue
        m = ITEM_START.match(l)
        if m:
            if cur:
                out.append(cur)
            cur = {'line': i, 'section': section, 'item': m.group(1), 'parts': [l]}
            continue
        if cur and not is_marker(lines, i):
            cur['parts'].append(l)
    if cur:
        out.append(cur)
    for it in out:
        it['text'] = flatten(it['parts'])
    return [it for it in out if '. . .' not in it['text'] and '$' in it['text']]


def main():
    summary = []
    for year, rp, issue in REVPROCS:
        lines = load(issue)
        trips = triplets(lines)
        mode = page_mode(lines, trips)
        start = find_start(lines, rp)
        if start is None:
            summary.append({'year': year, 'revproc': rp, 'error': 'start not found'})
            continue
        end = find_end(lines, start)
        # Pick the page-marker layout that reproduces the official first page
        # from the finding lists; with neither, give no pin pages.
        issue_full, official = FIRST_PAGE[rp]
        modes = [m for m in ('footer', 'header') if page_of(start, trips, m) == official]
        mode = modes[0] if modes else None
        first_page = official
        its = items(lines, start, end)
        doc = [f'Rev. Proc. {rp}, 20{issue} I.R.B. {first_page}',
               f'Text from the local IRB corpus, issue 20{issue} '
               f'(https://www.irs.gov/pub/irs-irbs/irb{issue}.pdf).',
               f'First page {first_page} is from the IRB cumulative finding lists. Pin pages '
               f'(after the first page) come from the page markers in the extracted text, '
               f'read in the {mode} layout that reproduces the first page.',
               '']
        for key, title in TOPICS.items():
            hits = [it for it in its if re.search(title, it['text'][:160])]
            if not hits:
                summary.append({'year': year, 'revproc': rp, 'key': key, 'error': 'not found'})
                continue
            for it in hits:
                pg = page_of(it['line'], trips, mode) if mode else None
                cite = f"Rev. Proc. {rp}, sec. {it['section']}.{it['item']}, 20{issue} I.R.B. {first_page}" + (
                    f", {pg}" if pg else '')
                doc.append(f'--- {key}: {cite} ---')
                doc.append(it['text'])
                doc.append('')
                summary.append({'year': year, 'revproc': rp, 'issue': issue, 'key': key,
                                'section': f"{it['section']}.{it['item']}",
                                'first_page': first_page, 'page': pg, 'cite': cite,
                                'text': it['text']})
        with open(os.path.join(SRC, f'revproc-{rp}-excerpts.txt'), 'w') as f:
            f.write('\n'.join(doc) + '\n')
    with open(os.path.join(ROOT, 'cache', 'revproc_summary.json'), 'w') as f:
        json.dump(summary, f, indent=1)
    for s in summary:
        print(s.get('year'), s.get('key'), s.get('cite') or s.get('error'), '|',
              (s.get('text') or '')[:300])


if __name__ == '__main__':
    main()
