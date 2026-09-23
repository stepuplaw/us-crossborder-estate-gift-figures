"""Fallback: fetch Rev. Rul. PDFs from irs.gov/pub/irs-drop/ and extract text with
PyMuPDF (from the caselaw venv). Saves cache/irsdrop/<name>.pdf and .txt."""
import os
import sys
import urllib.request

sys.path.append('/home/zvi/.venvs/caselaw/lib/python3.13/site-packages')
import pymupdf  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'cache', 'irsdrop')
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (research dataset; local use)'}

for name in sys.argv[1:]:
    url = f'https://www.irs.gov/pub/irs-drop/{name}.pdf'
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    except Exception as e:
        print(name, 'ERR', e)
        continue
    open(os.path.join(OUT, name + '.pdf'), 'wb').write(data)
    doc = pymupdf.open(stream=data, filetype='pdf')
    text = '\n'.join(p.get_text() for p in doc)
    open(os.path.join(OUT, name + '.txt'), 'w').write(text)
    first = ' '.join(text.split())[:160]
    print(name, len(data), '|', first)
