# Four capitalization packages — Wylder Hotel Tilghman Island

Built on the 10.28.26 model. The capitalization is **$17,404,044** in three tranches, all funded
at close: a $10,000,000 senior loan (first trust deed), $3,904,044 of preferred equity and
$3,500,000 of common equity from a new LP, alongside $2,000,000 of sponsor cash already invested.

| File | For | Pages |
|---|---|---|
| `Wylder Tilghman Island - Senior Debt.pdf` | A lender taking a 5.00% equity kicker | 28 |
| `Wylder Tilghman Island - Senior Debt (Hard Money).pdf` | **Hard money lenders** — same loan, no kicker | 27 |
| `Wylder Tilghman Island - Preferred Equity.pdf` | The preferred investor | 28 |
| `Wylder Tilghman Island - Common Equity.pdf` | The LP | 28 |

The two debt packages are the **same $10,000,000 loan** at the same rate, term and fee. They differ
only in the exit participation: the first quotes a 5.00% kicker and carries a lender returns page;
the hard money version quotes no participation, projects no lender return, and has no returns page
(27 pages instead of 28). Send one or the other, not both.

## Send one package per recipient. Never cross-send.

Each package carries **only its own economics**. No package discloses another tranche's rate,
fees, participation, promote, splits or returns. Verified by `scripts/crosscheck.py`
(26 checks, all passing).

| Shown to everyone | Shown to that recipient only |
|---|---|
| The three tranche **amounts** and their share of the stack | Its rate or preferred return |
| Position in the stack and what stands ahead of / beneath it | Its origination, broker and placement fees |
| LTV, loan to cost, debt-and-preferred to value, per-key basis | Its participation in equity value at exit |
| Total cost basis, estimated values, the operating projections | Its IRR, equity multiple, cash and profit |
| Senior debt service in dollars, where property cash flow requires it | Its own waterfall or roll-forward |

In the common equity package the senior and preferred deduction in the waterfall is shown as a
**single aggregated amount** ($4,751,666 at the base case), never itemized.

## Returns pages (page 22 in every package, marked "not for distribution")

The hard money package has **no returns page** — page 22 is removed and the deck is 27 pages.

| | Basis | Base case ($30.0M exit, 3-year hold) | Exit values shown |
|---|---|---|---|
| Senior loan (with kicker) | $9,800,000 net funded | 1.48x · 15.6% IRR · $14,540,000 received | $18M – $36M |
| Senior loan (hard money) | — | *no return shown* | — |
| Preferred equity | $3,825,963 net funded | 1.97x · 31.5% IRR · $7,526,610 received | $18M – $36M |
| Common equity · LP | $3,500,000 committed | 2.33x · 32.6% IRR · $8,164,823 received | **$21M – $36M** |

The common equity package starts at $21M because the LP's $18M column is a loss (0.77x, −8.2%).
No exit level at which the recipient loses money appears in any package; the partnership
breakeven and the GP's $18M figures are omitted from the common package entirely.

## Page map (identical structure in all three)

| | |
|---|---|
| 01–02 | Cover and summary — tranche-specific |
| 03–17 | Shared core: asset, property, adjacent acquisition, sponsor, brand, business plan, renovation schedule, affiliation, projections, cash flow, extended cash flow, departmental benchmarks, historical operations, competitive market, market and demand |
| 18–19 | Capital structure and sources and uses — recipient's tranche highlighted, recipient's terms and net funding only |
| 20–23 | Tranche pages: terms, mechanics (coverage / cash sweep / waterfall), **returns**, position |
| 24–27 | Total basis, value positioning, sale comparables, recent transactions |
| 28 | Contact — tranche-specific |

The hard money package drops the returns page, so its tranche block is 20–22 (terms, coverage,
credit considerations), the closing pages shift to 23–26 and contact is 27.

Page 25 states each recipient's own attachment point: the senior at $172,414 per key, the
preferred last dollar at $239,725, the full capitalization at $300,070.

## Conventions applied across all three

- **No appraiser, appraisal firm or valuation document is named anywhere.** Values are "estimated
  as is / upon completion / upon stabilization," stated for underwriting purposes and subject to
  completion and stabilization.
- **Per-key figures are on 58 keys** — the 57 hotel keys post-renovation plus the Dogwood Cove
  residence, operated as a whole-home suite.
- **The Dogwood Cove parcel closes November 18, 2026.**
- **The estimated values are for the hotel and exclude the adjacent parcel.** Page 5 values the
  parcel separately: ~$300,000 of EBITDA at a 7.0% cap is ~$4.3M against a $1.4M all-in cost,
  roughly $2.9M above cost — none of it in any value, coverage or return figure elsewhere.
- **The renovation program is $3,303,000** — $3,003,000 for the hotel plan plus $300,000 for the
  Dogwood Cove residence, funded from the capitalization at close.
- **The marina is 23 slips today and 47 on completion**; the 24 slips that come with the Dogwood
  Cove acquisition are the expansion.
- **US spelling throughout.**

## Superseded — do not send with these packages

| File | Why |
|---|---|
| `Wylder Tilghman Island - Recapitalization.pdf` | The single-package GP/LP deck on the v4 model |
| `Wylder Tilghman Island - LP Equity Summary.docx` | Written to the v4 structure ($13,255,085 LP equity, 12.0% pref, no senior or preferred tranche) |
| `Wylder Tilghman Island - GP-LP Model v4.xlsx` | The v4 model, superseded by 10.28.26 |

These three reconcile with each other and are kept for reference. They do **not** reconcile with
the three packages above and would disclose cross-tranche economics if sent alongside them.
`scripts/crosscheck-v4-superseded.py` checks that older set.

## If the kicker is dropped

The 10.28.26 model gives the senior a 5.00% participation in equity value at exit — $940,000 at the
base case, and the whole of the difference between the senior's 1.42x at an $18M sale and 1.51x at
$36M. Removing it has two consequences the model does not yet reflect:

1. **A hard money lender will want that value back in rate or points.** The hard money package
   quotes the same 12.00% all-in and 2.00% origination as the kicker version. If the market prices
   the lost participation into the coupon, the senior's rate and the DSCR and debt-yield figures on
   page 21 move with it.
2. **The 5.00% falls to the equity unless repriced.** In the model's waterfall that participation
   comes out of the kicker base before the residual, so dropping it adds $940,000 to the partnership
   residual at the base case and raises the LP and GP returns. The preferred and common packages as
   built still assume the senior takes its 5.00%. Re-run them if the hard money quote is the one
   that closes.

## Open items in the 10.28.26 model

- **Loan Analysis rows 53–73 are stale** — they show preferred at $7,404,044 and common at $0,
  the pre-common-equity case. Sources and Uses is authoritative and is what the packages use.
- **"Indicative pricing: SOFR + 500 bps"** contradicts the actual 821 bps spread (3.79% + 8.21%
  = 12.00% all-in). The packages use 821.
- **The kicker base label** reads "Net Proceeds less Senior and Pref," but the arithmetic deducts
  only the senior principal; the preferred balance comes out after the participations. The
  packages follow the arithmetic, which foots at all seven exit values.
- **Selling costs are 4.0%** in this model, up from 2.0% in v4.
