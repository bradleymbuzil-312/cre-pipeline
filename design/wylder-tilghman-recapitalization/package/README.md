# Send-together package — Wylder Hotel Tilghman Island recapitalization

Three documents, reconciled against each other. Send as a set.

| File | What it is | For |
|---|---|---|
| `Wylder Tilghman Island - Recapitalization.pdf` | The 30-page marketing deck | The read |
| `Wylder Tilghman Island - LP Equity Summary.docx` | Two-page term summary | The cover note |
| `Wylder Tilghman Island - GP-LP Model v4.xlsx` | Monthly waterfall and sensitivities | The diligence file |

## What reconciles

Every figure below is identical in all three, checked by `scripts/crosscheck.py` (30 assertions,
all passing). The model is the source; the deck and summary quote it.

| | |
|---|---|
| LP equity (gross / net cash invested) | $13,255,085 / $12,989,984 |
| Basis | 61.94% of the $21.4M estimated as-is value · $228,536 per key on 58 keys |
| Equity ownership | GP 51% / LP 49% — distributions follow the waterfall, not the percentages |
| Preferred return | 12.0% cumulative, compounded quarterly (12.55% effective) |
| Waterfall | 100% LP to pref and capital → 100% LP to 2.0x and a 20% IRR → 20/80 to $30.0M → 50/50 above |
| Senior refinance | $7,000,000 at month 3 · SOFR + 600 · interest-only · returns $2,070,384 |
| Base case (month 36 at $29.5M) | 2.06x / 37.3% IRR · $26,807,438 to the LP · $3,309,883 to the GP |
| Cash before the sale | $8,038,602 — 62% of net cash invested |
| LP reaches 2.0x at | $25,278,210 · full capital returned at $12,023,125 |

## Conventions applied across all three

- **No appraiser, appraisal firm or valuation document is named in any of the three.** Values are
  "estimated as is / upon completion / upon stabilization," stated for underwriting purposes and
  subject to completion and stabilization. The LP summary and the model's own labels were revised
  to match the deck on this point; the model's figures, formulas and cached values are untouched
  (only `xl/sharedStrings.xml` was rewritten — 7 labels, 0 of 2,575 numeric cells and 0 of 2,182
  formulas changed).
- **Per-key figures are on 58 keys** — the 57 hotel keys post-renovation plus the Dogwood Cove residence,
  which is the 58th key and is operated as a whole-home suite. The model's own key input was set to 58 to
  match (`Inputs!B49`; only that cell and the per-key cell it feeds changed, 2 of 2,575 numeric cells).
- **The Dogwood Cove parcel closes November 18, 2026**, shortly after the recapitalization.
- **The estimated values are for the hotel and exclude the adjacent parcel.** Stated in both the deck
  (pages 5, 11, 18, 24, 25, 26, 27) and the LP summary. Page 5 values the parcel separately: ~$300,000 of
  EBITDA at a 7.0% cap is ~$4.3M against a $1.4M all-in cost, roughly $2.9M above cost — none of it in any
  value, coverage or return figure elsewhere in the package.
- **The renovation program is $3,303,000** — $3,003,000 for the hotel plan plus $300,000 for the
  Dogwood Cove residence, both held back by the senior lender and drawn against the work.
- **The marina is 23 slips today and 47 on completion**; the 24 slips that come with the Dogwood
  Cove acquisition are the expansion.

## Known differences, left as drafted

- **Title on the summary footer** reads "Senior Director, Capital Markets"; the deck's footer and
  contact page read "Senior Director · The TRANCHE Group." Both are in use — not changed without
  instruction. The CA DRE license from the summary has been added to the deck's contact page.
- **The model retains its internal working notes** (the GP's $5.0M target and the shortfall against
  it, the v2/v3 promote history, the "80% GP share is aggressive" flag). These are deliberately not
  in the deck or the summary. Decide whether to send the model as-is or strip the Notes tab before
  it goes to an investor.
