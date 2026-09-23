# REPORT: US Cross-Border Estate, Gift and Reporting Figures, 2015 to 2026

Prepared for Kevin D. Klagge, StepUp Law. Built September 23, 2026 from primary sources only: the annual inflation Revenue Procedures, the monthly AFR revenue rulings, the statutes, Notice 97-34, and the Federal Register. Data are in `data/figures.csv`, `data/figures.json` and `data/section7520_rates.csv`; see `README.md` for columns and method.

## Status

- All 13 requested figures are filled for every year from 2015 to 2026: 145 rows, with one row for the unindexed nonresident alien credit. `section_6039f_penalty_note` is left out because no indexed amount exists: the IRC 6039F(c) penalty is a percentage (5% a month, capped at 25%).
- The 7520 rate is filled for all 142 months from January 2015 to October 2026. Checked against the Evans 7520 chart, all 142 months agree.
- Every amount cites the Rev. Proc. section and IRB page, statute, or Federal Register document it came from. The cited text is saved in `data/sources/`.
- Not done by the local corpus alone: the corpus has no FinCEN Federal Register rules and ends at IRB 2026-37. So the FBAR adjustments come from federalregister.gov metadata plus GovInfo text, and the October 2026 7520 rate comes from the irs.gov irs-drop PDF of Rev. Rul. 2026-19. That ruling has no IRB page yet.
- Nothing was published, pushed, emailed or submitted.

## The table (figures down, years across; whole dollars)

{{PIVOT}}

Notes on reading the table:

- **2018** mixes two Rev. Procs. Rev. Proc. 2018-18 (after the Tax Cuts and Jobs Act) superseded three items of Rev. Proc. 2017-58: the basic exclusion ($5,600,000 became $11,180,000), the 877A exclusion ($713,000 became $711,000) and the 6039F threshold ($16,111 became $16,076). The other 2018 items stand under 2017-58.
- **2026 basic exclusion and GST exemption** ($15,000,000) are set by statute (Pub. L. 119-21 sec. 70106), not by inflation adjustment. Rev. Proc. 2025-32 restates them in sec. 2.14.
- **GST exemption for 2015 to 2025** equals the basic exclusion under IRC 2631(c). No Rev. Proc. before 2025-32 prints it.
- **FBAR** rows are keyed to the year the adjustment took effect. Penalties follow the assessment date, and 2026 carries over the 2025 amounts (see finding 3).
- **Form 3520, individuals**, and the **nonresident alien credit** are fixed amounts that are not indexed. They are shown in every column for convenience.

### IRC 7520 rate by month (percent)

{{PIVOT7520}}

Source: Table 5 of each monthly AFR revenue ruling (Rev. Rul. 2015-1 for January 2015 through Rev. Rul. 2026-19 for October 2026). The ruling and IRB page for each month are in `data/section7520_rates.csv`.

## Conflicts with widely quoted pages

Four pages were compared, as required: the IRS expatriation tax page, Greenback's Form 3520 page, the Evans Estate Law Resources estate and gift table, and ElderLawAnswers' 2026 exemptions article. Two more were checked for context: the IRS "Gifts from Foreign Person" page and the Evans 7520 chart. Each page's text as retrieved on September 23, 2026 is saved as `data/sources/US-popular-<name>.txt`.

### 1. IRS, "Expatriation Tax" (irs.gov/individuals/international-taxpayers/expatriation-tax), "Page Last Reviewed or Updated: 03-Oct-2025"

`US-popular-irs-expatriation-tax.txt`

| Item | Page says | Primary source | Verdict |
|---|---|---|---|
| Covered expatriate tax test, 2017 to 2025 | $162,000; $165,000; $168,000; $171,000; $172,000; $178,000; $190,000; $201,000; $206,000 | Same, Rev. Procs 2016-55 to 2024-40 | Agrees |
| Covered expatriate tax test, 2026 | Not given; the list stops at 2025 | $211,000, Rev. Proc. 2025-32, sec. 4.37 | **Missing (stale)** |
| Covered expatriate tax test, 2015 and 2016 | Not given | $160,000 (Rev. Proc. 2014-61, sec. 3.30); $161,000 (Rev. Proc. 2015-53, sec. 3.30) | Missing (the list starts at 2017) |
| 877A exclusion | Gives only "For calendar year 2025, the exclusion amount is $890,000" and sends the reader to the Form 8854 instructions for other years | 2025: $890,000 (Rev. Proc. 2024-40, sec. 2.38). 2026: $910,000 (Rev. Proc. 2025-32, sec. 4.38) | 2025 agrees; **2026 missing** |

The page has no wrong numbers, only missing years. A reader who expatriates in 2026 and relies on it would apply the 2025 amounts: $206,000 instead of $211,000, and $890,000 instead of $910,000.

### 2. Greenback Expat Tax Services, "Form 3520" (greenbacktaxservices.com/knowledge-center/form-3520/), "Updated on March 25, 2026"

`US-popular-greenback-form-3520.txt`

| Item | Page says | Primary source | Verdict |
|---|---|---|---|
| Threshold for gifts from foreign corporations or partnerships | "more than $20,116 (2025)"; table headed "Reporting Threshold (2025)": "More than $20,116 total" | 2025: $20,116 (Rev. Proc. 2024-40, sec. 2.48). 2026: $20,573 (Rev. Proc. 2025-32, sec. 4.47, published November 2025) | 2025 figure correct and labeled 2025; **2026 figure absent** from a page updated four months after it was published |
| Threshold for gifts from foreign individuals or estates | "more than $100,000"; "Each gift over $5,000 must be separately identified" | Notice 97-34, sec. VI.B.1: "exceeds $100,000"; "each gift in excess of $5,000" | Agrees |
| Penalty for unreported foreign gifts | "5% of gift value per month, up to 25% maximum" | IRC 6039F(c)(1)(B): 5% per month, not to exceed 25% | Agrees |

The brief framed this as the page giving $20,116 "instead of" $20,573. The saved text is narrower than that: the page labels $20,116 as the 2025 figure, which is right for 2025 returns filed in 2026. The real problem is that it gives no 2026 figure at all. A reader asking about a gift received in 2026 has only the 2025 number to go on.

### 3. Evans Estate Law Resources, "Federal Estate and Gift Tax Rates and Exclusions" (resources.evans-legal.com/?p=3627)

`US-popular-evans-legal-rates-exclusions.txt`

| Item | Page says, 2015 to 2026 | Primary source | Verdict |
|---|---|---|---|
| Estate tax exclusion | $5,430,000; $5,450,000; $5,490,000; $11,180,000; $11,400,000; $11,580,000; $11,700,000; $12,060,000; $12,920,000; $13,610,000; $13,990,000; $15,000,000 | Same (2018 per Rev. Proc. 2018-18; 2026 per Pub. L. 119-21 sec. 70106) | Agrees, all 12 years |
| Gift annual exclusion | $14,000 (2015 to 2017); $15,000 (2018 to 2021); $16,000; $17,000; $18,000; $19,000; $19,000 | Same | Agrees, all 12 years |
| Cross-border items (2523(i), 6039F, 877, 877A, 2032A, 6166, FBAR) | Not covered | See table above | Not a conflict; outside the page's scope |

No numeric conflicts. The page confirms that Evans has the domestic figures but none of the cross-border ones. The Evans 7520 chart (`US-popular-evans-legal-7520-rates.txt`, "Current through October 2026") also agrees with all 142 months in `section7520_rates.csv`.

### 4. ElderLawAnswers, "Annual Gift Tax and Estate Tax Exemptions for 2026" (elderlawanswers.com, WealthCounsel), widely syndicated on law firm sites

`US-popular-elderlawanswers-2026-exemptions.txt`

| Item | Page says | Primary source | Verdict |
|---|---|---|---|
| 2026 estate exemption | $15 million; up from $13.99 million in 2025 | $15,000,000 (Pub. L. 119-21 sec. 70106; Rev. Proc. 2025-32, sec. 2.14); $13,990,000 (Rev. Proc. 2024-40, sec. 2.41) | Agrees |
| 2026 annual exclusion | $19,000 | Rev. Proc. 2025-32, sec. 4.42(1) | Agrees |
| Non-citizen spouse | $194,000 in 2026, up from $190,000 in 2025 | Rev. Proc. 2025-32, sec. 4.42(2); Rev. Proc. 2024-40, sec. 2.43 | Agrees |
| Why the 2026 numbers changed | "These exclusion amounts are adjusted annually to account for changes in the cost of living" | The $15,000,000 is a statutory reset, not a cost-of-living adjustment; Rev. Proc. 2025-32 sec. 2.14 says indexing resumes for 2027 | **Conflict in explanation** (the amount is right; the stated reason is wrong for the exemption) |

### Context check: IRS, "Gifts from Foreign Person" (irs.gov/businesses/gifts-from-foreign-person), "Page Last Reviewed or Updated: 17-Apr-2026"

`US-popular-irs-gifts-from-foreign-person.txt`. This page gives "$20,116 for 2025, and $20,573 for 2026" and the $100,000 individual threshold. Both match the primary sources. So the IRS's own foreign-gift page is current for 2026 while its expatriation page is not.

### Conflicts found inside the primary sources

- **IRB 2018-36, Table 5 caption.** The September 2018 7520 table is captioned "REV. RUL. 2018-21 TABLE 5", but it belongs to Rev. Rul. 2018-23 (header at 2018-36 I.R.B. 405). Rev. Rul. 2018-21 is a different ruling at 2018-32 I.R.B. 282. The dataset cites 2018-23 and flags the misprint.
- **31 CFR 1010.821 history note** (local CFR corpus, 2025 edition) cites "86 FR 7349, Jan. 28, 2020". The Federal Register API dates that document (FR Doc. 2021-01919) to January 28, 2021. The CFR note's year is a typo. Its other page numbers (e.g. 83 FR 11881 for a rule that starts at 11876) are pin cites to the amendatory text, not errors.

## Ten findings most likely to surprise a reader

1. **In 2018 two inflation figures went down during the year.** Rev. Proc. 2018-18 (March 2018) recomputed 2018 amounts with the chained CPI adopted by Pub. L. 115-97. The Form 3520 threshold for gifts from foreign corporations fell from $16,111 to $16,076, and the 877A mark-to-market exclusion fell from $713,000 to $711,000. Tables that copied Rev. Proc. 2017-58 in late 2017 still show the higher, superseded numbers.

2. **The 2026 $15,000,000 exemption is not an inflation adjustment and is not in the Rev. Proc.'s list of adjusted items.** It was written into IRC 2010(c)(3)(A) by Pub. L. 119-21 sec. 70106. Rev. Proc. 2025-32 mentions it only in section 2 ("Changes"). That same paragraph is the first time since at least 2015 that an annual Rev. Proc. states the GST exemption directly. Indexing starts again for 2027.

3. **FBAR penalty maximums did not rise in 2026.** OMB memorandum M-26-11 (April 17, 2026) cancelled the 2026 civil penalty inflation adjustment government-wide, according to agency notices in the Federal Register (e.g. PBGC, 91 FR 25936; FCC, 91 FR 39613; SEC, 91 FR 41722). FinCEN has published nothing for 2026. So the 2025 figures, $16,536 non-willful and $165,353 willful (90 FR 5629), remain the latest, and this is the first year without an increase since the 2016 catch-up.

4. **The $100,000 Form 3520 threshold for gifts from foreign individuals is not in the Internal Revenue Code and has not changed since 1997.** IRC 6039F(a) sets a single $10,000 threshold, indexed under 6039F(d). The separate $100,000 threshold for nonresident alien individuals and foreign estates comes from Notice 97-34, sec. VI.B.1 (1997-25 I.R.B. 22, 30), and the notice provides no indexing. Meanwhile the corporate/partnership threshold has doubled from its $10,000 base to $20,573.

5. **The annual exclusion held at $19,000 for 2026, but the non-citizen spouse exclusion rose $4,000, to $194,000.** Both are indexed. IRC 2503(b)(2) rounds the $10,000-based amount down to a multiple of $1,000, and 2523(i)(2) applies the same rule to a $100,000 base. A small rise in the index can therefore leave the annual exclusion flat while the spouse amount moves. Over 2015 to 2026 the spouse amount went from 10.5 times the annual exclusion to 10.2 times.

6. **FBAR maximums rose about twice as fast as the IRS figures.** From 2015 to 2026 the non-willful maximum grew 65% ($10,000 to $16,536). The IRS-indexed figures grew about 32% (e.g. the covered expatriate test went from $160,000 to $211,000, the 877A exclusion from $690,000 to $910,000, the 6166 amount from $1,470,000 to $1,940,000). Most of the gap is the one-time 2016 catch-up to $12,459, which measured inflation from 2004, the last statutory change.

7. **Some FBAR "annual" adjustments arrived late in the year.** The 2016, 2018 and 2019 adjustments took effect August 1, 2016, March 19, 2018 and October 10, 2019. For a penalty assessed in, say, June 2019, the applicable maximum was still the 2018 amount ($12,921). The amount follows the assessment date, not the year of the unfiled FBAR, and applies only to violations after November 2, 2015.

8. **The nonresident alien estate credit has been $13,000 since 1988.** IRC 2102(b)(1) is not indexed. Pub. L. 100-647 raised it from $3,600 in 1988, and it has not changed since. Over the same 2015 to 2026 period, the citizen/resident basic exclusion nearly tripled, from $5,430,000 to $15,000,000.

9. **The 7520 rate ranged from 0.4% to 5.8% in this period.** It was 0.4% from August to November 2020 and peaked at 5.8% in December 2023. It is 5.6% for October 2026 (Rev. Rul. 2026-19). A remainder or annuity valued in late 2020 can differ sharply from the same one valued in 2023, which matters for GRATs, CRTs and QPRTs.

10. **The 2026 Rev. Proc. is the first to print the IRC 2801 exception for gifts from covered expatriates.** Rev. Proc. 2025-32 sec. 4.42(3) says the 2801 tax on covered gifts and bequests from a covered expatriate applies only to the extent they exceed $19,000 in 2026, the same as the annual exclusion. None of the Rev. Procs for 2015 to 2025 mention section 2801. This matters for US heirs of people who expatriate with the 2026 figures ($211,000 tax test, $910,000 exclusion), which the IRS expatriation page does not yet show.

## Sources used (primary)

- Rev. Proc. 2014-61, 2014-47 I.R.B. 860; 2015-53, 2015-44 I.R.B. 615; 2016-55, 2016-45 I.R.B. 707; 2017-58, 2017-45 I.R.B. 489; 2018-18, 2018-10 I.R.B. 392; 2018-57, 2018-49 I.R.B. 827; 2019-44, 2019-47 I.R.B. 1093; 2020-45, 2020-46 I.R.B. 1016; 2021-45, 2021-48 I.R.B. 764; 2022-38, 2022-45 I.R.B. 445; 2023-34, 2023-48 I.R.B. 1287; 2024-40, 2024-45 I.R.B. 1100; 2025-32, 2025-45 I.R.B. 695.
- Notice 97-34, 1997-25 I.R.B. 22.
- Monthly AFR revenue rulings, Rev. Rul. 2015-1 through Rev. Rul. 2026-19 (list in `data/section7520_rates.csv`).
- 26 U.S.C. 877, 877A, 2010, 2032A, 2102, 2503, 2523, 2631, 6039F, 6166, 6601(j), 7520; 31 U.S.C. 5321; 31 CFR 1010.821; Pub. L. 119-21 sec. 70106.
- Federal Register: 81 FR 42503 (2016); 82 FR 10434 (2017); 83 FR 11876 (2018), corrected by 84 FR 51973 and 84 FR 53053 (dates only); 84 FR 54495 (2019); 85 FR 9370 (2020); 86 FR 7348 (2021); 87 FR 3433 (2022); 88 FR 3311 (2023); 89 FR 4820 (2024); 90 FR 5629 (2025); 91 FR 25936 (2026 cancellation, as reported by PBGC).
