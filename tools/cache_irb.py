"""Dump IRB issues 2014 to 2026 from the local corpus to cache/irb/<cite>.txt."""
import os
import sys
sys.argv = ['x', 'none']
exec(open(os.path.join(os.path.dirname(__file__), 'irb.py')).read())

out = os.path.join(os.path.dirname(__file__), '..', 'cache', 'irb')
os.makedirs(out, exist_ok=True)
rows = con.execute(
    "SELECT cite, url, block_id, idx FROM sections WHERE corpus='irb' "
    "AND CAST(edition AS INTEGER) >= 2014 ORDER BY cite").fetchall()
for r in rows:
    with open(os.path.join(out, r['cite'] + '.txt'), 'w') as f:
        f.write(text(r))
with open(os.path.join(out, 'index.tsv'), 'w') as f:
    for r in rows:
        f.write(f"{r['cite']}\t{r['url']}\n")
print(len(rows))
