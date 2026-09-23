"""Save the statute text behind each figure to data/sources/statute-*.txt, from
the local USC corpus (2024 edition), the CFR corpus (2025) and the enacted
public-law corpus (Pub. L. 119-21, the OBBBA)."""
import os
import re
import sys

sys.argv = ['x', 'none']
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'irb.py')).read())
SRC = os.path.join(os.path.dirname(HERE), 'data', 'sources')

WANT = [
    ('usc', '26', '2503'), ('usc', '26', '2523'), ('usc', '26', '2010'), ('usc', '26', '2631'),
    ('usc', '26', '2032A'), ('usc', '26', '6166'), ('usc', '26', '6601'), ('usc', '26', '6039F'),
    ('usc', '26', '877'), ('usc', '26', '877A'), ('usc', '26', '2102'), ('usc', '26', '7520'),
    ('usc', '26', '6048'), ('usc', '26', '6677'),
    ('usc', '31', '5321'), ('cfr', '31', '1010.821'),
    ('plaw', '119-21', 'PL 119-21 sec. 70106'),
]


def main():
    for corpus, title, cite in WANT:
        rows = con.execute(
            "SELECT * FROM sections WHERE corpus=? AND title=? AND cite=?",
            (corpus, title, cite)).fetchall()
        if not rows:
            print('MISSING', corpus, title, cite)
            continue
        r = rows[0]
        body = text(r)
        name = re.sub(r'[^A-Za-z0-9.]+', '-', f'{corpus}-{title}-{cite}').strip('-')
        path = os.path.join(SRC, f'statute-{name}.txt')
        with open(path, 'w') as f:
            f.write(f"{corpus.upper()} {title} {cite}: {r['heading']}\n"
                    f"Edition: {r['edition']}. Source URL: {r['url']}\n"
                    f"Text from the local law corpus (us-law.db).\n\n{body}\n")
        print(path, r['edition'], len(body))


if __name__ == '__main__':
    main()
