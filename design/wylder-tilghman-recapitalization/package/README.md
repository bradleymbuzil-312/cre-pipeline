# Wylder Hotel Tilghman Island — capitalization packages and the marina valuation

Built on the 10.28.26 model. The capitalization is **$17,404,044** in three tranches, all funded
at close: a $10,000,000 senior loan (first trust deed), $3,904,044 of preferred equity and
$3,500,000 of common equity from a new LP, alongside $2,000,000 of sponsor cash already invested.

| File | For | Request | Pages |
|---|---|---|---|
| `Wylder Tilghman Island - Senior Debt.pdf` | A lender taking a 5.00% equity kicker | $10,000,000 | 30 |
| `Wylder Tilghman Island - Senior Debt - 8M Request.pdf` | **Lender-facing** — no kicker, no return shown | $8,000,000 | 29 |
| `Wylder Tilghman Island - Senior Debt - 10M Request.pdf` | **Lender-facing** — no kicker, no return shown | $10,000,000 | 29 |
| `Wylder Tilghman Island - Senior Debt - 11M Request.pdf` | **Lender-facing** — no kicker, no return shown | $11,000,000 | 29 |
| `Wylder Tilghman Island - Senior Debt - 12.5M Request.pdf` | **Lender-facing** — no kicker, no return shown | $12,500,000 | 29 |
| `Wylder Tilghman Island - Senior Debt Model - 12.5M.xlsx` | **The live debt model** for that request | $12,500,000 | 7 tabs |
| `Wylder Tilghman Island - LP Recapitalization.pdf` | **A prospective LP** — request only, terms open | — | 29 |
| `Wylder Tilghman Island - Preferred Equity.pdf` | The preferred investor | — | 29 |
| `Wylder Tilghman Island - Common Equity.pdf` | The LP | — | 29 |
| `Wylder Tilghman Island - Marina Valuation.pdf` | **Standalone** — the marina analysis on its own | — | 9 |

**The three "Request" packages are the lender-facing set.** Same loan, same 12.00% all-in rate,
same 3-year interest-only term, same 2.00% origination — sized at three requests. They quote no
exit participation, project no lender return, carry no returns page (27 pages), and use no
partnership, GP or LP vocabulary anywhere. Send one. Never send two requests to the same lender.

`Senior Debt.pdf` is the one package that quotes a 5.00% kicker and carries a lender returns page.
It exists only at $10,000,000, because the model's exit waterfall is solved only there.

### What moves with the request

| | $8,000,000 | $10,000,000 | $11,000,000 | $12,500,000 |
|---|---|---|---|---|
| Annual debt service · IO | $960,000 | $1,200,000 | $1,320,000 | $1,500,000 |
| Interest and carry reserve · 12 mo | $960,000 | $1,200,000 | $1,320,000 | $1,500,000 |
| Origination 2.00% / broker 1.00% | $160,000 / $80,000 | $200,000 / $100,000 | $220,000 / $110,000 | $250,000 / $125,000 |
| Net proceeds at close | $6,880,000 | $8,600,000 | $9,460,000 | $10,750,000 |
| LTV as-is / stabilized | 37.38% / 27.12% | 46.73% / 33.90% | 51.40% / 37.29% | 58.41% / 42.37% |
| Loan to cost | 46.58% | 57.46% | 62.79% | 70.66% |
| DSCR 2026 / 2027 / 2028 | 1.18x / 2.41x / 2.78x | 0.94x / 1.93x / 2.23x | 0.86x / 1.75x / 2.02x | 0.75x / 1.54x / 1.78x |
| Debt yield 2027 / 2028 | 28.94% / 33.38% | 23.15% / 26.71% | 21.05% / 24.28% | 18.52% / 21.36% |
| **Preferred equity (the plug)** | **$5,674,878** | **$3,904,044** | **$3,018,628** | **$1,690,502** |
| Preferred fees · 2.00% each side | $113,498 / $113,498 | $78,081 / $78,081 | $60,373 / $60,373 | $33,810 / $33,810 |
| Common equity · LP | $3,500,000 | $3,500,000 | $3,500,000 | $3,500,000 |
| Capitalization | $17,174,878 | $17,404,044 | $17,518,628 | $17,690,502 |
| Debt and preferred to as-is | 63.90% | 64.97% | 65.51% | 66.31% |
| Total cost basis / key | $18,947,882 / $326,688 | $19,247,882 / $331,860 | $19,397,882 / $334,446 | $19,622,882 / $338,326 |

The uses are the same deal at every request: the payoff, the renovation, the acquisition and
working capital do not move, while the reserve, the origination fee and the broker fee all scale
with the loan. **The LP commitment is held at $3,500,000 and the preferred is the balancing item** —
it fills whatever the senior does not. Because the preferred carries two fees of 2.00% of itself,
it solves against itself; at $10,000,000 that reproduces the model's own $3,904,044 exactly, which
is what confirms the convention.

Note the consequence at the top of the range: **a larger loan request shrinks the preferred raise,
not the LP.** At $11,000,000 the preferred is $3,018,628, down from the model's $3,904,044.

## Send one package per recipient. Never cross-send.

Each package carries **only its own economics**. No package discloses another tranche's rate,
fees, participation, promote, splits or returns. Verified by `scripts/crosscheck.py`
(87 checks, all passing).

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

The three lender-facing packages have **no returns page** — page 22 is removed and the deck is
27 pages, with the closing pages at 23–27.

| | Basis | Base case ($30.0M exit, 3-year hold) | Exit values shown |
|---|---|---|---|
| Senior loan (with kicker) | $9,800,000 net funded | 1.48x · 15.6% IRR · $14,540,000 received | $18M – $36M |
| Senior loan (lender-facing, any request) | — | *no return shown* | — |
| Preferred equity | $3,825,963 net funded | 1.97x · 31.5% IRR · $7,526,610 received | $18M – $36M |
| Common equity · LP | $3,500,000 committed | 2.33x · 32.6% IRR · $8,164,823 received | **$21M – $36M** |

The common equity package starts at $21M because the LP's $18M column is a loss (0.77x, −8.2%).
No exit level at which the recipient loses money appears in any package; the partnership
breakeven and the GP's $18M figures are omitted from the common package entirely.

## Page map (identical structure in all three)

| | |
|---|---|
| 01–02 | Cover and summary — tranche-specific |
| 06 | **Dogwood Cove acquisition in detail** — the PSA, what the $1,400,000 buys, what it earns |
| 03–18 | Shared core: asset, property, adjacent acquisition, **acquisition detail**, sponsor, brand, business plan, renovation schedule, affiliation, projections, cash flow, extended cash flow, departmental benchmarks, historical operations, competitive market, market and demand |
| 18–19 | Capital structure and sources and uses — recipient's tranche highlighted, recipient's terms and net funding only |
| 20–23 | Tranche pages: terms, mechanics (coverage / cash sweep / waterfall), **returns**, position |
| 24–27 | Total basis, value positioning, sale comparables, recent transactions |
| 28 | Contact — tranche-specific |

The lender-facing packages drop the returns page, so their tranche block is 20–22 (terms,
coverage, credit considerations), the closing pages shift to 23–26 and contact is 27.

Page 25 states each recipient's own attachment point: the senior at $172,414 per key, the
preferred last dollar at $239,725, the full capitalization at $300,070.

## The Dogwood Cove acquisition

Page 5 makes the strategic case; **page 6 carries the deal.** The purchase and sale agreement
($1,100,000, a $15,000 deposit, a 45-day closing period, contemplated closing November 18, 2026,
bought by 21551 Tilghman Investors LLC in fee simple), what the $1,400,000 all-in buys (the
four-bedroom residence as the 58th key, roughly three acres, 24 slips usable day one, $300,000 of
renovation), and what it earns ($1,500 ADR at 35% occupancy, $191,625 at stabilization, taking the
marina to 47 slips).

The parcel was part of the hotel historically and was separated and sold to a third party in
bankruptcy about ten years ago, which is why it is available to buy back.

**Note the tension on timing:** the PSA contemplates a 45-day closing period, and the closing date
carried throughout the package is November 18, 2026. Both are stated on page 6. If the PSA period
runs from a later execution date those two do not agree, and the date should be confirmed before
the package goes out.

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

## The marina valuation

Every debt package carries a **Marina Valuation** page, directly after the hotel value positioning.
The standalone deck is the same analysis in full, Wylder-branded on the TRANCHE Group kit.

| | Low · $25K | Recommended · $30K | High · $40K |
|---|---|---|---|
| Wylder · 23 slips | $575,000 | $690,000 | $920,000 |
| Dogwood Cove · 24 slips, upon approval | $600,000 | $720,000 | $960,000 |
| **Combined · 47 slips** | **$1,175,000** | **$1,410,000** | **$1,880,000** |

Until the Dogwood Cove slips are approved for commercial use they carry about **$280,000** — the
$1,100,000 contract price less the parcel's $820,833 residential assessment. That approval is the
difference between $280,000 and $720,000.

The recommendation is the adjusted median of three deed-verified sales that are mostly slips, within
about an hour of Tilghman: $26,800 to $48,019 per slip after a 3%-a-year time adjustment, median
$30,837. Four further local trades carrying a full-service boatyard or hotel and restaurant
operations run $94,025 to $184,091 per slip; they are shown as context, not as slip prices. An
income cross-check on market seasonal rents supports $27,000 per slip, 10% below.

**None of this value is in the estimated hotel values** — it is incremental collateral. The sponsor
model's 2028 slip revenue would imply $2.75M to $3.50M for the combined marina, but that is upside
to be proven with a trailing marina P&L, not collateral value today.

Two things were deliberately left out of every package: the third-party per-slip benchmark, which
names no closed sales, and the internal note on the model's 2028 slip expense line. Both are
underwriting notes rather than lender material.

## The LP Recapitalization deck

A request for investment, **not an offer of terms**, and on a **different capital plan from the
packages above**. Here the limited partner funds the entire closing and no debt sits ahead of it; a
$7,000,000 senior refinance in month three funds the renovation and returns capital. This is the
plan the original recapitalization deck was built on, and it is the only one in which a
**$13,255,085** LP raise reconciles.

| At closing | |
|---|---|
| LP equity · gross | $13,255,085 |
| Less origination fee · 2.00% | ($265,102) |
| **Net cash invested** | **$12,989,984** |
| Senior debt at closing | $0 |
| LP equity to as-is value | 61.94% · $228,536 per key |

| After the month-three refinance | |
|---|---|
| Senior refinance | $7,000,000 |
| Total capital | $20,255,085 |
| Returned to the LP | ($2,070,384) — 15.9% of net cash invested, inside 90 days |
| **Net capital in the asset** | **$18,184,701** — $313,529 per key |

Uses at closing retire the $10,714,782 existing loan and the $530,000 merchant cash advance in
full, buy the adjacent parcel for $1,100,000 and fund $250,000 of working capital. The renovation
is funded from the refinance, not from closing equity.

| Carried | Left out |
|---|---|
| The $13,255,085 sought and what it clears | Any preferred return, split, hurdle or promote |
| The refinance **allocation** — what the proceeds do | The refinance's rate, spread, fees and reserve terms |
| Cash flow after debt service, and coverage | Debt yield, and the debt request pages |
| The waterfall **mechanics**, tier by tier | Every rate and split in them |
| The $2,070,384 returned in month three | Ownership percentages and the promote |

Page 20 separates what is fixed from what is open. Page 21 shows what the refinance funds. Page 22
sets out the four tiers — preferred return, return of capital, residual split, promote — each
marked to be determined, beside what will set them.

**This deck does not reconcile with the capitalization packages above** and is not part of that
set. They solve a $10,000,000 senior request with preferred and common equity beneath it; this one
has the LP funding the close alone. Send one plan or the other, not both. The operating
projections, the renovation program, the basis detail and the market pages are common to both.

Dated **November 11, 2026**; the capitalization packages keep their October 30 date.

## The debt model

`Wylder Tilghman Island - Senior Debt Model - 12.5M.xlsx` is a live workbook, not a printout. The
loan amount in **Loan Request!B5** drives everything: debt service, the reserve, both fees, net
funding, every leverage and coverage measure, the three sizing tests and the sensitivity grid.
225 formulas, no hardcoded outputs.

| Tab | What it does |
|---|---|
| Loan Request | The request, pricing, net funding at close, leverage against each estimated value, coverage |
| Loan Sizing | Maximum loan by LTV, DSCR interest-only, DSCR 30-year amortizing and debt yield, with the binding constraint on both the stabilizing year and the first full year |
| Sources & Uses | Uses at closing; subordinate capital is the plug, so sources equal uses at any loan amount |
| Operations | 2026–2028 projections, debt service, coverage, debt yield and the permanent takeout test |
| Extended Cash Flow | 2030–2041 carried forward, with coverage and cash flow after debt service |
| Sensitivity | DSCR and debt yield across five loan amounts and five NOI scenarios |
| Total Basis | The basis build, with the loan-driven lines moving with the loan |

It carries **no equity economics** — no preferred rate, no waterfall, no promote, no partner
returns — for the same reason the debt packages do not. The preferred and common amounts appear
only as a single "subordinate capital" plug, with the split stated at the requested loan amount.

Rebuild at another size with `WT_SENIOR_LOAN=11000000 python3 scripts/build/v7_model.py`.

## Lender-facing vocabulary

The debt packages carry **no partnership, GP or LP language at all.** The capital stack names the
tranche "Common equity," the sponsor line reads "Sponsor cash equity," the basis note describes
capital that "stays in the asset behind the loan," and the adjacent parcel comes into "the
borrowing entity." The equity packages keep the partnership vocabulary, which is correct for them.

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

## Corrected on page 13

The extended cash flow page was lifted from an earlier deck and its senior debt service block was
fixed to a loan that is not the one being requested. The debt service row, both coverage rows, the
debt yield row and the four summary measures beneath the table are now **re-derived from the
request** in every package. The debt yield row in particular was materially wrong: at $10,000,000
it read 23.8% rising to 33.0%, against a correct 30.6% rising to 42.4%. It understated the loan,
but a lender recomputing it would have found the error.

## Open items in the 10.28.26 model

- **Loan Analysis rows 53–73 are stale** — they show preferred at $7,404,044 and common at $0,
  the pre-common-equity case. Sources and Uses is authoritative and is what the packages use.
- **"Indicative pricing: SOFR + 500 bps"** contradicts the actual 821 bps spread (3.79% + 8.21%
  = 12.00% all-in). The packages use 821.
- **The kicker base label** reads "Net Proceeds less Senior and Pref," but the arithmetic deducts
  only the senior principal; the preferred balance comes out after the participations. The
  packages follow the arithmetic, which foots at all seven exit values.
- **Selling costs are 4.0%** in this model, up from 2.0% in v4.
