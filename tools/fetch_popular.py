"""Save the text of a widely quoted web page as data/sources/US-popular-<name>.txt.

usage: fetch_popular.py <name> <url>"""
import datetime
import html
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'data', 'sources')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/126.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9'}


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', raw)
    raw = re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h\d|td|th|table|section)>', '\n', raw)
    raw = re.sub(r'(?i)<(td|th)[^>]*>', ' | ', raw)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    t = re.sub(r'[ \t ]+', ' ', t)
    return re.sub(r'\n\s*\n+', '\n', t).strip()


def main():
    name, url = sys.argv[1], sys.argv[2]
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    raw = raw.decode('utf-8', 'replace')
    t = text_of(raw)
    stamp = datetime.date.today().isoformat()
    path = os.path.join(SRC, f'US-popular-{name}.txt')
    with open(path, 'w') as f:
        f.write(f'Source: {url}\nRetrieved: {stamp}\n\n{t}\n')
    print(path, len(t))


if __name__ == '__main__':
    main()
