"""Query helper for the local IRB corpus (us-law.db, corpus 'irb')."""
import os
import sys
os.environ.setdefault('CL_LAW_DB', os.path.expanduser('~/cl-data/us-law.db'))
sys.path.insert(0, '/home/zvi/caselaw')
sys.path.append('/home/zvi/.venvs/caselaw/lib/python3.13/site-packages')
import lawcorpus

con = lawcorpus.connect()


def find(pattern, corpus='irb', limit=50):
    return con.execute(
        "SELECT id, cite, heading, edition, url, block_id, idx, nchars FROM sections "
        "WHERE corpus=? AND (cite LIKE ? OR heading LIKE ?) ORDER BY cite LIMIT ?",
        (corpus, pattern, pattern, limit)).fetchall()


def text(row):
    return lawcorpus.section_text(con, row['block_id'], row['idx'])


def get(cite, corpus='irb'):
    rows = con.execute(
        "SELECT id, cite, heading, edition, url, block_id, idx, nchars FROM sections "
        "WHERE corpus=? AND cite=?", (corpus, cite)).fetchall()
    return rows


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'stats':
        for s in lawcorpus.stats(con):
            print(s)
    elif cmd == 'find':
        for r in find(sys.argv[2], *(sys.argv[3:4] or ['irb'])):
            print(dict(r))
    elif cmd == 'text':
        for r in get(sys.argv[2], *(sys.argv[3:4] or ['irb'])):
            print(dict(r))
            print(text(r))
