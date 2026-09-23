"""Fetch FinCEN civil monetary penalty inflation adjustment documents from the
Federal Register API and save their raw text under cache/fr/."""
import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'cache', 'fr')
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'crossborder-figures research dataset (local, non-commercial)'}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=90).read()


def search(term, agency='financial-crimes-enforcement-network'):
    q = {'conditions[term]': term, 'per_page': '100', 'order': 'oldest',
         'fields[]': ['title', 'document_number', 'citation', 'publication_date', 'type',
                      'raw_text_url', 'effective_on', 'agencies', 'html_url']}
    if agency:
        q['conditions[agencies][]'] = agency
    url = 'https://www.federalregister.gov/api/v1/documents.json?' + urllib.parse.urlencode(q, doseq=True)
    return json.loads(get(url))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'search':
        agency = sys.argv[3] if len(sys.argv) > 3 else 'financial-crimes-enforcement-network'
        d = search(sys.argv[2], None if agency == 'none' else agency)
        json.dump(d, open(os.path.join(OUT, 'search-last.json'), 'w'), indent=1)
        print(d.get('count'))
        for r in d.get('results', []):
            print(r['publication_date'], r['citation'], r['document_number'], r['type'],
                  r['effective_on'], '|', r['title'][:90])
    elif cmd == 'text':
        for docnum in sys.argv[2:]:
            meta = json.loads(get(f'https://www.federalregister.gov/api/v1/documents/{docnum}.json'))
            # federalregister.gov serves an access check to scripts; GovInfo has the same text.
            d = meta['publication_date']
            gi = f'https://www.govinfo.gov/content/pkg/FR-{d}/html/{docnum}.htm'
            meta['govinfo_url'] = gi
            raw = get(gi).decode('utf-8', 'replace')
            if 'Request Access' in raw[:2000]:
                raise SystemExit(f'{docnum}: blocked')
            with open(os.path.join(OUT, f'{docnum}.txt'), 'w') as f:
                f.write(raw)
            with open(os.path.join(OUT, f'{docnum}.meta.json'), 'w') as f:
                json.dump(meta, f, indent=1)
            print(docnum, meta['citation'], meta['publication_date'], len(raw), meta['title'][:80])
