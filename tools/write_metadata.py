#!/usr/bin/env python3
"""Write data/schema.json, data/datapackage.json and kaggle/dataset-metadata.json.

The column definitions live here once, so the three files cannot disagree.

    python3 tools/write_metadata.py
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIGURE_IDS = sorted({r["figure_id"] for r in csv.DictReader(open(ROOT / "data" / "figures.csv"))})

FIGURES = [
    {"name": "figure_id", "type": "string", "description": "Stable identifier for the figure, e.g. gift_noncitizen_spouse", "constraints": {"required": True, "enum": FIGURE_IDS}},
    {"name": "figure_name", "type": "string", "description": "Plain-English name with the Code section"},
    {"name": "year", "type": "integer", "description": "Year the amount applies to: calendar year of the gift, death or expatriation, or the taxable year for the Form 3520 thresholds. For FBAR penalties, the year the adjustment took effect (penalties follow the assessment date; see note). Blank for nra_estate_credit, which is one row for all years"},
    {"name": "amount", "type": "integer", "description": "Amount in whole US dollars", "constraints": {"required": True, "minimum": 0}},
    {"name": "unit", "type": "string", "description": "Always USD", "constraints": {"enum": ["USD"]}},
    {"name": "authority", "type": "string", "description": "Source of the amount: Rev. Proc. number, section, IRB issue and first page, then the pin page where known; or a statute; or a Federal Register citation"},
    {"name": "authority_url", "type": "string", "format": "uri", "description": "IRS Internal Revenue Bulletin PDF, federalregister.gov document, or GovInfo statute page"},
    {"name": "note", "type": "string", "description": "Scope, caveats, superseded amounts, and how carried-over or derived rows were determined"},
]
RATES = [
    {"name": "year", "type": "integer", "description": "Year the rate applies to"},
    {"name": "month", "type": "integer", "description": "Month the rate applies to (1 to 12)", "constraints": {"minimum": 1, "maximum": 12}},
    {"name": "rate_percent", "type": "number", "description": "IRC 7520 rate in percent, e.g. 5.6"},
    {"name": "revenue_ruling", "type": "string", "description": "The monthly applicable federal rate revenue ruling that announced the rate"},
    {"name": "irb_cite", "type": "string", "description": "Internal Revenue Bulletin issue and first page of the ruling, or a statement that it is not yet in a bulletin"},
    {"name": "table", "type": "string", "description": "The table in the ruling (always Table 5)"},
    {"name": "authority_url", "type": "string", "format": "uri", "description": "IRB PDF, or the irs.gov irs-drop PDF for October 2026"},
    {"name": "note", "type": "string", "description": "Set only for September 2018, where the IRB table caption misprints the ruling number"},
]
TITLE = "US Cross-Border Estate, Gift and Reporting Figures, 2015 to 2026"
PAGE = "https://stepuplaw.com/data/us-crossborder-estate-gift-figures/"
REPO = "https://github.com/stepuplaw/us-crossborder-estate-gift-figures"

schema = {
    "figures.csv": {"fields": FIGURES, "primaryKey": ["figure_id", "year"]},
    "section7520_rates.csv": {"fields": RATES, "primaryKey": ["year", "month"]},
}
(ROOT / "data" / "schema.json").write_text(json.dumps(schema, indent=2) + "\n")

pkg = {
    "name": "us-crossborder-estate-gift-figures",
    "title": TITLE,
    "version": "2026.09.23",
    "licenses": [{"name": "CC-BY-4.0", "path": "https://creativecommons.org/licenses/by/4.0/"}],
    "homepage": PAGE,
    "contributors": [{"title": "Kevin D. Klagge", "role": "author", "organization": "Klagge Law, PLLC (StepUpLaw)"}],
    "resources": [
        {"name": "figures", "path": "figures.csv", "format": "csv", "mediatype": "text/csv", "schema": schema["figures.csv"]},
        {"name": "section7520_rates", "path": "section7520_rates.csv", "format": "csv", "mediatype": "text/csv", "schema": schema["section7520_rates.csv"]},
    ],
}
(ROOT / "data" / "datapackage.json").write_text(json.dumps(pkg, indent=2) + "\n")

strip = lambda fs: [{k: f[k] for k in ("name", "description", "type")} for f in fs]
kaggle = {
    "title": "US Cross-Border Estate and Gift Figures 2015-2026",
    "subtitle": "Annual IRS amounts for foreign spouses, gifts, expatriation and FBAR",
    "id": "stepuplaw/us-crossborder-estate-gift-figures",
    "licenses": [{"name": "CC-BY-4.0"}],
    "keywords": ["law", "government", "finance", "united states", "tax"],
    "description": (
        "A year-by-year table, 2015 to 2026, of the US estate, gift, expatriation and foreign-reporting figures that cross-border planners quote: "
        "the gift tax annual exclusion, the annual exclusion for gifts to a spouse who is not a US citizen, the estate and gift basic exclusion amount, "
        "the GST exemption, the special use valuation cap, the section 6166 2-percent amount, both Form 3520 foreign gift thresholds, the covered expatriate "
        "tax test, the section 877A exclusion, the FBAR civil penalty maximums, and the $13,000 nonresident alien estate credit. A second table gives the "
        "IRC 7520 rate for every month from January 2015 to October 2026.\n\n"
        "Every amount cites the annual inflation Revenue Procedure by section and Internal Revenue Bulletin page, the statute, or the Federal Register "
        "document it came from. The 2026 basic exclusion of $15,000,000 is set by statute (Pub. L. 119-21 sec. 70106), not by inflation adjustment. "
        "The FBAR maximums did not rise in 2026. Column definitions are in schema.json.\n\n"
        f"Canonical page and citation: {PAGE}\n"
        f"Source repository with the saved text of every source: {REPO}\n"
        "Author: Kevin D. Klagge, Klagge Law, PLLC, ORCID https://orcid.org/0009-0002-1385-8498\n\n"
        "This is reference data, not legal advice. Check the current Revenue Procedure before relying on a figure."
    ),
    "resources": [
        {"path": "figures.csv", "description": "145 rows: 13 figures, one row per figure and year, 2015 to 2026, plus one row for the unindexed nonresident alien estate credit", "schema": {"fields": strip(FIGURES)}},
        {"path": "section7520_rates.csv", "description": "142 rows: the IRC 7520 rate for each month, January 2015 to October 2026", "schema": {"fields": strip(RATES)}},
    ],
}
assert len(kaggle["title"]) <= 50, len(kaggle["title"])
(ROOT / "kaggle" / "dataset-metadata.json").write_text(json.dumps(kaggle, indent=2) + "\n")
print("wrote schema.json, datapackage.json, kaggle/dataset-metadata.json")
