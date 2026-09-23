#!/usr/bin/env python3
"""Generate crossborder-figures-overview.ipynb.

The notebook is generated rather than hand-edited, so the prose and the code
live in one reviewable file. Rebuild and run it with

    python3 notebooks/build_overview_notebook.py
    python3 -m nbconvert --execute --inplace notebooks/crossborder-figures-overview.ipynb
"""
import pathlib
import nbformat as nbf

HERE = pathlib.Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

cells = [
    md("# US cross-border estate, gift and reporting figures, 2015 to 2026\n\n"
       "This notebook loads `data/figures.csv` and `data/section7520_rates.csv` and reproduces the tables in the README. "
       "Each row of `figures.csv` is one figure for one year, with the Revenue Procedure, statute or Federal Register "
       "document the amount came from."),
    code("import pandas as pd\n\n"
         "fig = pd.read_csv('../data/figures.csv')\n"
         "rates = pd.read_csv('../data/section7520_rates.csv')\n"
         "len(fig), len(rates)"),
    md("## Figures down, years across\n\n"
       "The nonresident alien estate credit is one row with no year, because IRC 2102(b)(1) fixes it at $13,000."),
    code("pivot = fig.dropna(subset=['year']).astype({'year': int}).pivot(index='figure_id', columns='year', values='amount')\n"
         "pivot"),
    md("## Growth from 2015 to 2026\n\n"
       "The FBAR maximums grew faster than the IRS-indexed amounts because of the one-time 2016 catch-up adjustment."),
    code("growth = (pivot[2026] / pivot[2015] - 1).mul(100).round(1).sort_values(ascending=False)\n"
         "growth.rename('percent change 2015 to 2026')"),
    md("## The 2018 double Revenue Procedure\n\n"
       "Rev. Proc. 2018-18 superseded three 2018 amounts from Rev. Proc. 2017-58 after the Tax Cuts and Jobs Act."),
    code("fig[(fig['year'] == 2018) & fig['authority'].str.contains('2018-18')][['figure_id', 'amount', 'note']]"),
    md("## IRC 7520 rate by month"),
    code("rates.pivot(index='year', columns='month', values='rate_percent')"),
    code("rates.loc[[rates['rate_percent'].idxmin(), rates['rate_percent'].idxmax()], ['year', 'month', 'rate_percent', 'revenue_ruling']]"),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, HERE / "crossborder-figures-overview.ipynb")
print("wrote", HERE / "crossborder-figures-overview.ipynb")
