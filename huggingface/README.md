---
license: cc-by-4.0
language:
  - en
pretty_name: US Cross-Border Estate, Gift and Reporting Figures, 2015 to 2026
tags:
  - legal
  - law
  - tax
  - estate-tax
  - gift-tax
  - international-tax
  - fbar
  - expatriation
  - united-states
  - reference
size_categories:
  - n<1K
configs:
  - config_name: figures
    data_files: figures.csv
    default: true
  - config_name: section7520_rates
    data_files: section7520_rates.csv
---

# US Cross-Border Estate, Gift and Reporting Figures, 2015 to 2026

This Hugging Face copy holds `figures.csv`, `figures.json`, `section7520_rates.csv`, `schema.json` and `datapackage.json`. The saved text of every source and the build tools are in the [GitHub repository](https://github.com/stepuplaw/us-crossborder-estate-gift-figures).

A year-by-year table of the US estate, gift, expatriation and foreign-reporting figures that cross-border planners quote. These are the numbers that matter to a person married to someone who is not a US citizen, a US person who receives a gift or inheritance from abroad, someone giving up US citizenship or a long-held green card, and anyone with a foreign bank account. Every amount is tied to the primary source it came from, which is the annual inflation Revenue Procedure (by section and Internal Revenue Bulletin page), the statute, or the Federal Register. The dataset also has a monthly IRC 7520 rate table running from January 2015 to October 2026.

Compiled by [Kevin D. Klagge, Esq.](https://stepuplaw.com/about), a Florida estate planning attorney whose practice includes international and cross-border clients (Klagge Law, PLLC). Built and checked on September 23, 2026.

- Canonical page with the tables and the citation: <https://stepuplaw.com/data/us-crossborder-estate-gift-figures/>
- Source repository: <https://github.com/stepuplaw/us-crossborder-estate-gift-figures>

[FINDINGS.md](https://github.com/stepuplaw/us-crossborder-estate-gift-figures/blob/main/FINDINGS.md) has the pivoted table, the conflicts found on widely quoted web pages, and the ten findings most likely to surprise a reader.

## Files

| Path | What it is |
|---|---|
| `data/figures.csv`, `data/figures.json` | 145 rows: 13 figures, one row per (figure, year) for 2015 to 2026, plus one row for the unindexed nonresident alien estate credit |
| `data/section7520_rates.csv` | 142 rows: the IRC 7520 rate for each month from January 2015 to October 2026 |
| `data/sources/revproc-*-excerpts.txt` | The relevant paragraphs of each annual inflation Rev. Proc. (2014-61 through 2025-32, plus 2018-18), with section and IRB page |
| `data/sources/notice-97-34-sec-VI-excerpt.txt` | Notice 97-34, section VI (source of the $100,000 Form 3520 threshold for gifts from individuals) |
| `data/sources/statute-*.txt` | Statute text: 26 U.S.C. 877, 877A, 2010, 2032A, 2102, 2503, 2523, 2631, 6039F, 6048, 6166, 6601, 6677, 7520; 31 U.S.C. 5321; 31 CFR 1010.821; Pub. L. 119-21 sec. 70106 |
| `data/sources/fr-*-excerpt.txt` | Federal Register FBAR penalty adjustment rows (2016 to 2025) and the 2026 cancellation notice |
| `data/sources/section7520-revrul-excerpts.txt` | The "Rate Under Section 7520" table from each monthly revenue ruling |
| `data/sources/US-popular-*.txt` | Widely quoted web pages compared in `FINDINGS.md` (text as retrieved September 23, 2026) |
| `data/schema.json` | Data dictionary for both CSV files as Frictionless Table Schemas |
| `data/datapackage.json` | Frictionless Data Package descriptor for both CSV files |
| `tools/` | The code that built everything from the sources (see Method), plus `write_metadata.py` for the schema and package files |
| `notebooks/crossborder-figures-overview.ipynb` | A short notebook that loads the CSV files and prints the pivoted table and the 7520 range |
| `FINDINGS.md` | The pivoted table, conflicts with widely quoted pages, and findings |
| `progress.log` | One line per figure family as it was completed |

## Columns: `figures.csv` / `figures.json`

| Column | Meaning |
|---|---|
| `figure_id` | Stable identifier, e.g. `gift_noncitizen_spouse` |
| `figure_name` | Plain-English name with the Code section |
| `year` | The year the amount applies to: calendar year of the gift, death or expatriation, or the taxable year (Form 3520 thresholds). For FBAR penalties, the year the adjustment took effect (penalties are keyed to the assessment date; see `note`). Blank for `nra_estate_credit`, which is one row for all years |
| `amount` | Whole US dollars |
| `unit` | Always `USD` |
| `authority` | Where the amount comes from: Rev. Proc. number, section, IRB issue and first page, then the pin page where known (for example `Rev. Proc. 2025-32, sec. 4.42, 2025-45 I.R.B. 695, 704`); or a statute; or a Federal Register cite |
| `authority_url` | IRS IRB PDF, federalregister.gov document link, or GovInfo statute page |
| `note` | Scope, caveats, superseded amounts, and how carried-over or derived rows were determined |

JSON has the same fields. `year` is `null` for the single `nra_estate_credit` row.

### Figures

| figure_id | Source type |
|---|---|
| `gift_annual_exclusion` | Rev. Proc., each year |
| `gift_noncitizen_spouse` | Rev. Proc., each year |
| `basic_exclusion` | Rev. Proc., each year; 2026 set by statute (Pub. L. 119-21 sec. 70106) and restated in Rev. Proc. 2025-32 sec. 2.14 |
| `gst_exemption` | IRC 2631(c) makes it equal to the basic exclusion amount; only Rev. Proc. 2025-32 (2026) states it directly |
| `section_2032a_cap` | Rev. Proc., each year |
| `section_6166_2pct_amount` | Rev. Proc., each year (the indexed form of the $1,000,000 in IRC 6601(j)(2)) |
| `form3520_foreign_gift_corp_partnership` | Rev. Proc., each year (IRC 6039F(d) indexing of the $10,000 in 6039F(a)) |
| `form3520_foreign_gift_individual` | Notice 97-34, sec. VI.B.1; $100,000, not indexed |
| `expatriation_avg_tax_liability` | Rev. Proc., each year |
| `expatriation_877a_exclusion` | Rev. Proc., each year |
| `fbar_penalty_nonwillful_max` | 31 U.S.C. 5321(a)(5)(B)(i) for 2015; FinCEN/Treasury Federal Register adjustments 2016 to 2025; 2025 amount carried to 2026 (adjustment cancelled) |
| `fbar_penalty_willful_max_floor` | Same, for the dollar amount in 5321(a)(5)(C)(i)(I). The willful maximum is the greater of this amount or 50% of the balance |
| `nra_estate_credit` | IRC 2102(b)(1); $13,000, not indexed, one row |

`section_6039f_penalty_note` is left out on purpose. It would belong only if an indexed amount existed, and none does: the IRC 6039F(c) penalty is 5% of the gift per month, capped at 25%, with no dollar figure to index (statute text in `data/sources/statute-usc-26-6039F.txt`).

## Columns: `section7520_rates.csv`

| Column | Meaning |
|---|---|
| `year`, `month` | The month the rate applies to |
| `rate_percent` | The 7520 rate, in percent (e.g. `5.6`) |
| `revenue_ruling` | The monthly AFR revenue ruling that announced it |
| `irb_cite` | IRB issue and first page of the ruling. October 2026 (Rev. Rul. 2026-19) is not yet in a bulletin issue; it comes from the irs.gov irs-drop release |
| `table` | The table in the ruling (always Table 5) |
| `authority_url` | IRB PDF, or the irs-drop PDF for October 2026 |
| `note` | Set only for September 2018, where the IRB table caption misprints the ruling number |

## Method

1. **Revenue Procedures.** The Internal Revenue Bulletin issues for 2014 to 2026 were read from the local IRB corpus (`us-law.db`, corpus `irb`) using `lawcorpus.section_text()` (`tools/cache_irb.py`). `tools/extract_revprocs.py` finds each Rev. Proc. in its issue and splits it into its numbered items. It then keeps the paragraphs that contain a dollar amount for each figure, skipping table-of-contents lines. `tools/revproc_figures.py` parses the amount with a regex specific to each figure. It also checks that the paragraph names the expected year and fails on any unmatched paragraph. No amount was typed by hand.
2. **IRB pages.** Each Rev. Proc.'s first page comes from the IRB cumulative finding lists (e.g. "2025-32, 2025-45 I.R.B. 695"). Pin pages come from the page markers in the extracted text. Older bulletins print these markers at the foot of each page and newer ones at the head, so for each issue the script uses whichever reading reproduces the official first page.
3. **2018.** Rev. Proc. 2017-58 set the 2018 amounts. After Pub. L. 115-97, Rev. Proc. 2018-18 superseded some of them. The table uses 2018-18 for the three items it changed (basic exclusion, 877A exclusion, 6039F threshold) and 2017-58 for the rest. The notes give the superseded amounts.
4. **Statutes** come from the local USC corpus (2024 edition), plus the enacted text of Pub. L. 119-21 sec. 70106 for the 2026 basic exclusion (`tools/save_statutes.py`).
5. **FBAR penalties.** The local Federal Register corpus holds IRS rules only. So the FinCEN and Treasury civil penalty adjustment rules were found through the federalregister.gov API and read from GovInfo's copy of each Federal Register issue (`tools/fr_fetch.py`). `tools/fbar_figures.py` then parses the 31 U.S.C. 5321(a)(5) rows. For 2026, no FinCEN adjustment appears in the Federal Register through September 23, 2026. Notices from other agencies (for example PBGC, 91 FR 25936) report that OMB memorandum M-26-11 of April 17, 2026 cancelled the 2026 adjustment, so the 2025 amounts carry over.
6. **7520 rates.** `tools/rates7520.py` reads Table 5 of every monthly AFR revenue ruling in the corpus. It takes the ruling number from the ruling's own header, not the table caption. October 2026 is not in the corpus yet, so it comes from the irs.gov irs-drop PDF of Rev. Rul. 2026-19 (`tools/irs_drop.py`, text extracted with PyMuPDF). As a check on the extraction, all 142 months were compared with the Evans Estate Law Resources 7520 chart (`tools/compare_7520.py`). Every month matched.
7. **Build.** `tools/build_dataset.py` assembles `figures.csv` and `figures.json`, checks that each (figure, year) pair has exactly one source row, and checks for dash characters. `tools/make_report.py` renders the report from `tools/report_template.md`, published here as `FINDINGS.md`.

To rebuild: run `cache_irb.py`, `extract_revprocs.py`, `revproc_figures.py`, `save_statutes.py`, `fbar_figures.py` (after `fr_fetch.py text ...`), `rates7520.py`, `build_dataset.py`, then `make_report.py` (which renders the findings report from `tools/report_template.md`). The rebuild needs the local IRB and USC corpora, which are not part of this repository; the saved excerpts in `data/sources/` are what each figure rests on. The scripts use system `python3`, with the caselaw venv's site-packages appended for `zstandard` and `pymupdf`.

## Conventions and caveats

- Source excerpts keep the source wording, except that ligatures are expanded, soft hyphens are dropped, and em and en dashes are converted to hyphens to match house style.
- The GST exemption for 2015 to 2025 is not stated in any Rev. Proc. It is derived from IRC 2631(c), which sets it equal to the basic exclusion amount. The `authority` field says so.
- FBAR adjustments apply to penalties *assessed* after the adjustment's effective date, for violations after November 2, 2015. In 2016, 2018 and 2019 the adjustment took effect partway through the year (August 1, March 19 and October 10), so earlier assessments that year used the prior amounts.

## Not legal advice

This is reference data, not legal advice, and using it creates no attorney-client relationship. Check the current Revenue Procedure, statute or Federal Register notice before relying on a figure.

## License

The data is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may use it commercially, modify it and build products on it with credit. The statute text and government excerpts in `data/sources/` are US government works.

## Citation

Klagge, Kevin D. *US Cross-Border Estate, Gift and Reporting Figures, 2015 to 2026*. StepUpLaw, 2026. https://stepuplaw.com/data/us-crossborder-estate-gift-figures/

`CITATION.cff` holds the same citation in machine-readable form. Corrections are welcome at office@stepuplaw.com.
