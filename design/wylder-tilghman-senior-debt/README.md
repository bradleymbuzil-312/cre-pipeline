# Handoff: Wylder Hotel Tilghman Island — Senior Debt & Preferred Equity Deck

## Overview
A 28-slide institutional financing package supporting a **$17,970,734 capitalization** of the Wylder Hotel Tilghman
Island (Talbot County, MD):

| Tranche | Amount | Share | Terms |
|---|---|---|---|
| Senior loan (first mortgage) | $12,840,000 | 71.45% | 8.79% floating (30-day SOFR 3.79% + 5.00%), 3-yr term, full-term interest-only, ADS $1,128,636 |
| Acquisition loan — 21441 Dogwood Cove | $770,000 | 4.28% | 8.79%, 30-yr amortization, $72,955 annual P&I, 70% of purchase price |
| Preferred equity | $4,360,734 | 24.27% | 17.0% total — 10% current pay / 7% accrued PIK, 3-yr hold |
| **Total** | **$17,970,734** | **100%** | **No common equity at close** |

Proceeds retire the existing $10,714,782 loan, buy the adjacent parcel at 21441 Dogwood Cove ($1,100,000), fund
$3,303,000 of capital improvements, and establish $2,137,664 of reserves and working capital. Financing costs are
$715,288 (3.98% of total capitalization). Nothing is distributed to the sponsor.

Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

## About the Design Files
The files in `deck/` are a **design reference built in HTML** — a working prototype of the intended look, content and
slide flow, not production code to ship as-is. The task is to **recreate this deck in the target environment** using
its established patterns. If the goal is a distributable presentation, the HTML itself is already the deliverable and
exports to PDF one slide per page.

The deck is a single self-contained Design Component (`.dc.html`) rendered through a lightweight slide-shell web
component (`deck-stage.js`) and a runtime (`support.js`). All styling is **inline** on each element; the only shared
stylesheet is the design system's `colors_and_type.css` (design tokens + `@font-face`).

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, copy and figures. Every figure reconciles to the
sponsor's financial model dated **October 6, 2026** (`Wylder Tilghman Island - Financials - 10.6.26 w Acq pref.xlsx`);
do not alter numbers without an updated model.

## How to Run the Reference
Serve `deck/` over a local static server (relative paths to `_ds/`, `assets/`, `deck-stage.js`, `support.js` must
resolve — `file://` fails CORS) and open
`Wylder Tilghman Island - Senior Debt Financing.dc.html`. Arrow keys / on-screen nav move between slides; the shell
handles scaling, a thumbnail rail, speaker notes and print-to-PDF.

Canvas is **1920×1080** per slide (16:9).

## Design Tokens
Sourced from `deck/_ds/.../colors_and_type.css`. Use these exact values.

**Color**
- `--mm-navy-900` `#001A3D` — deepest navy; dark-slide backgrounds, headline ink on cream
- `--mm-navy` `#002F6C` — primary brand navy (PMS 295); rules, totals
- `--mm-navy-700` `#1A4280`, `--mm-navy-300` / `--mm-navy-100` — lighter navy tints for secondary text on dark
- `--mm-orange` `#E87722` — accent; eyebrows, key figures
- `--mm-orange-700` `#C0631C`, `--mm-orange-100` `#FBE3CF`
- `--paper` `#FAF8F4` — warm cream; default light-slide surface
- `--ink-900` `#0E1116`, `--ink-700` `#2A2F37`, `--ink-500` `#5A6068`, `--ink-400` — body text on cream
- `--hairline` `rgba(0,26,61,.12)` — 1px structural dividers
- Capital-stack tier colors used literally: senior loan `#032D67`, accent `#E87722`, preferred equity `#456EAB`,
  acquisition loan brass `#957551`

**Typography** — Microsoft **Aptos** family, loaded from the design system `fonts/` via `@font-face` (no CDN).
- `--font-display` "Aptos Display" — H1/H2 headlines (700), italic taglines
- `--font-body` "Aptos" — body copy, ledes, captions
- `--font-condensed` "Aptos Narrow" — eyebrows, ALL-CAPS labels, table headers (700, letter-spacing .14–.30em)
- `--font-mono` "Aptos Mono" — all currency, percentages, dates, phone (tabular-nums)
- `--font-serif` "Aptos Serif" — used only for the "wylder" wordmark on the title slide

**Type sizes in use (px, at 1920×1080):** title H1 104; section H2 41–52; big stat/hero figures 92–104; stat-grid
values 46–54; table body 13–22; eyebrow 17; labels 12–15.

**Running footer:** every interior slide (2–27) carries a footer rule —
`Wylder Hotel Tilghman Island · Senior Debt & Preferred Equity` left, `MMCC · The TRANCHE Group` right, then the page
number after a hairline divider — in `--font-condensed` 14px/700, `.2em` tracking, uppercase, `--ink-400` on light
slides and `rgba(255,255,255,.38)` on dark. The cover (01) and contact (28) slides carry the page number in the
header bar beside the confidentiality label instead.

**Rules & borders:** section headers sit above a `1px solid var(--mm-navy)` rule; tables use 2px navy top/bottom
borders with 1px `--hairline` interior lines. Corners 0–2px (printed feel, not app-like). No gradients except the
photo-overlay scrims on dark hero slides. No shadows except soft photo scrims.

**A design-system CSS rule caps `<p>` width at ~479px.** Every paragraph needs an explicit `max-width:none` (or a
`ch` value) or it wraps narrow.

**Motif:** a strata bar (stacked segments in the tranche colors) on the title, loan-terms and contact slides — the
capital-stack metaphor. On the loan-terms slide it is split 71.45% / 4.28% / 24.27%, matching the three tranches.

## Screens / Views (28 slides)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text. Each slide is
1920×1080, `box-sizing:border-box`, ~44–96px padding. Interior slides open with a 64×3px `--mm-orange` rule in place
of a text eyebrow, followed by a plain descriptive H2. Headlines are declarative statements of fact, not marketing
lines.

1. **Title** — eyebrow "SENIOR DEBT & PREFERRED EQUITY · $17,970,734", H1 property name, factual tagline, dated
   October 7, 2026.
2. **Summary of the capitalization** — lede plus an 8-tile grid: total capitalization $17.97M, senior loan $12.84M
   ($221,379/key on 58 keys), all-in rate 8.79% floating, 3-yr full-term IO, LTV at close 60.0%, stabilized DSCR
   2.37x, stabilized debt yield 20.8%, preferred equity $4.36M.
3. **A 57-key waterfront resort on 8.10 acres, with an adjacent parcel under contract** — photo split, lede, 2×2
   facts (50 → 58 keys, 8.10 ac expanding to ~11, Upper Upscale, Tilghman MD), two thumbnails.
4. **What the asset comprises** — four columns (Location, Accommodations, Food/Beverage/Events, Amenities), each
   with a photograph and a six-row fact card. Reconciles the key bridge explicitly: 50 rooms in service, 4 out of
   service to be restored, 3 from the rebuilt three-bedroom house = 57 hotel keys, 58 with Dogwood Cove. Marina
   reads 23 slips today · 25 added under the capital plan · 24 at Dogwood Cove.
5. **Adjacent acquisition — 21441 Dogwood Cove** — full-width aerial of the hotel and the parcel, then three
   columns: Transaction ($1,100,000 purchase, fee simple, $15,000 deposit, 45-day close, $300,000 renovation,
   $1,400,000 all in), What It Adds (24 slips, ±3 acres, 4-bedroom residence, 1 key, ±11.1 acres and 72 slips on
   completion) and Why It Matters (it was part of the hotel until a bankruptcy sale roughly ten years ago; the
   $770,000 acquisition loan at 70% LTV funds it; $976,214 of stabilized revenue exists in no historical period).
6. **Ownership and operating structure** — ownership narrative, 2×2 facts, and four Structure and Alignment points.
   The single-asset-entity point now reads that 21551 Tilghman Investors LLC will also hold the Dogwood Cove parcel.
7. **Operator background and brand portfolio** — brand blurb, the two-property portfolio, a Proof Case block on
   Wylder Windham, recognition, and the principal's career record.
8. **Business plan and capital improvement program** — three numbered items against the $3.3M / $56,948-per-key
   program; at right the RevPAR index (41.4% → 79% at stabilization), a "What Drives the Plan" list and two stat
   tiles (NOI 2026→2030 2.7x; RevPAR 2025→2030 $87→$196).
9. **The renovation is designed, priced and scheduled** — a Gantt of the seven renovation items across September 21,
   2026 to April 1, 2027 with exact start and completion dates, alongside a full-height photograph of the completed
   model room.
10. **Small Luxury Hotels affiliation and distribution** — Hilton distribution, the existing Windham relationship,
    the Amex Fine Hotels & Resorts designation and membership economics.
11. **Estimated values and underwritten projections** — three-value band: as-is $21,400,000 ($368,966/key), upon
    completion $26,000,000 ($448,276/key), upon stabilization $29,500,000 ($508,621/key). Below, 2026–2030
    operations and a stabilized-NOI takeaway (2028: $2,670,611 at a 37.7% margin).
12. **Pro forma cash flow and underwriting assumptions** — room nights, occupancy, ADR, RevPAR, rooms/other revenue,
    operating expenses and NOI for 2026–2030 at left; the assumption set at right.
13. **Stabilized cash flow carried forward, 2030 through 2041** — 2030 is the last year of the pro forma, shown as a
    highlighted anchor column; every year after continues the same line (occupancy 43.0%, rate +3.0%/yr, margin
    38.1%). Debt service is the **permanent takeout basis** ($973,890 + $72,955), since the senior loan carries a
    three-year term. Minimum coverage 2.92x; $28.9M of aggregate cash flow after debt service 2031–2041.
14. **Departmental revenue and margins against industry benchmarks** — revenue by department at the 2028 stabilized
    year; F&B against outlet comparables; the marina, seven added keys and Dogwood Cove house shown as $976,214 of
    revenue and $851,926 of departmental profit *not present in any historical period*; margins and departmental
    cost ratios against the resort and independent segments.
15. **Historical operations and competitive benchmarking** — actual 2023/2024/2025 at left; STR benchmarking (YTD
    December 2025) at right against the four-property, 364-room set.
16. **The competitive market, supply and demand** — the five-property, 404-room market set; penetration (RevPAR
    index 48% → 44%, target 83%); the supply/demand series 2019–2025 with CAGRs and TTM March 2026; seasonality.
17. **Drive-to demand, visitation and new supply.**
18. **A three-tranche capitalization of $17,970,734** — a proportional stacked bar (senior 71.45%, acquisition
    4.28%, preferred 24.27%), a Capital Measures table and a Tranche Terms table.
19. **Preferred equity terms and position** (dark) — instrument, position in the stack, equity beneath the
    preferred at each value point, and a three-year roll-forward (beginning balance, 7% PIK accrual, ending
    balance, 10% current pay, combined obligations, NOI, coverage 0.69x → 1.39x → 1.57x).
20. **Summary of senior loan terms** (dark) — 8.79% all-in (SOFR 3.79% + 5.00%, floating); 3 yrs full-term IO (ADS
    $1,128,636, constant 8.790%); 60.0% LTV at close ($12,840,000, $221,379/key, 58 keys). Bottom strip carries the
    acquisition loan and the fee schedule (2.00% origination, 1.00% MMCC, $10,100 processing).
21. **Projected debt service coverage, 2026 through 2030** — NOI, senior debt service, acquisition P&I, total debt
    service, DSCR senior (1.00x → 2.71x), DSCR all debt (0.94x → 2.55x) and senior debt yield (8.80% → 23.84%), with
    the renovation-year coverage and permanent-takeout blocks at right.
22. **The capitalization measured against cost basis and value** (dark) — ten coverage measures, a callout breaking
    the $17,970,734 into its four uses groups, and four supporting blocks (cost basis, interest-only structure,
    preferred equity, sponsor support).
23. **Total project cost basis and the renovation plan** — the full $17,970,734 basis in four groups (acquisition
    and payoff $11,814,782, capital improvements $3,303,000, reserves and working capital $2,137,664, financing
    costs $715,288) at left; the hotel capital plan itemized to $3,003,000 plus the $300,000 Dogwood Cove
    renovation, four per-key tiles and the exact start/completion dates at right.
24. **Estimated value positioned against market evidence** — per-key positioning table placing the senior loan
    ($221,379/key), cost basis ($309,840/key), the three estimated values and **both** comparable sets on one scale.
25. **Comparable hotel sales, resort and local.**
26. **Recent transaction evidence and local market activity.**
27. **Sources and uses of funds at closing** — three sources plus $0 common equity, twelve uses, closing detail
    ($155,658) and the proceeds narrative. Sources less uses = $0.
28. **Contact and next steps** — stat strip (total capitalization, senior all-in rate, preferred equity), contact
    block, page number in the header bar.

### Valuation language
No appraiser, appraisal firm or third-party valuation conclusion is named anywhere in the package. The value points
are an **estimated as-is value of $21,400,000**, **upon completion of $26,000,000** and **upon stabilization of
$29,500,000**, carried on slides 11, 18, 19, 22 and 24 and labeled: "Values are stated for underwriting purposes and
are subject to completion of the renovation and stabilization of operations." The word *appraisal* does not appear
anywhere in the deck. This is deliberate — the package is distributed to the appraiser engaged on the transaction and
must not anchor that appraiser to a prior conclusion.

### One projection, carried forward
The deck carries a single operating projection. Slides 11–12 are the sponsor model 2026–2030; slide 13 continues that
same line to 2041 rather than restarting from a differently constituted forecast. Slide 14 is benchmarked on the same
2028 stabilized year, so the departmental mix and margins reconcile to slides 11–13.

### Key count convention
The **hotel** is 50 keys today and 57 on completion of the renovation. The **financing basis** is **58 keys** — the
57 hotel keys plus the Dogwood Cove residence, which the model carries as one key at a $1,500 nightly rate and 35%
occupancy. Every per-key figure in the package is computed on 58; where the comparables are discussed, the subject is
compared on its 57 hotel keys. Both conventions are stated wherever they appear.

### Market data
Comparable sales, competitive-set composition, market supply and demand, drive-to demand, visitation, departmental
comparables and industry benchmarks are presented as market facts. Talbot County visitation is attributed to Talbot
County Economic Development and Tourism; competitive-set performance is attributed to STR. No brokerage, appraisal or
valuation document is cited or reproduced anywhere in the package, and no lender is named.

## Interactions & Behavior
Slide navigation via `deck-stage`: arrow keys, click nav, thumbnail rail, print-to-PDF (one page/slide). No
per-element interactivity, no forms, no data fetching. If rebuilt as app components the only "state" is the current
slide index.

## Assets (in `deck/assets/`)
- `wt-aerial-spring.png` — hero aerial (title slide)
- `wt-aerial.png` — aerial (contact slide)
- `wt-pier.png` — waterfront at dusk (asset slide, left; thumbnail on slide 04)
- `wt-suite.jpg` — completed model guest room (slides 03, 04 and the renovation slide)
- `wt-pool.png` — waterfront pool (thumbnails on slides 03 and 04)
- `wt-fb-signs.jpg` — property signage naming Tickler's Crab Shack and Bar Mumbo (slide 04)
- `wt-dogwood-aerial.jpg` — aerial of the hotel and the adjacent Dogwood Cove parcel (slide 05)
- `wt-lobby.png` — renovated interior/lobby (sponsor slide)
- `flannigan.png` — John Flannigan headshot
- `mmcc-2018-white.png` — MMCC logo, white (the only asset with real transparency)
- `buzil.jpg` — Bradley M. Buzil headshot

## Files
- `deck/Wylder Tilghman Island - Senior Debt Financing.dc.html` — the deck (all 28 slides, inline-styled)
- `deck/deck-stage.js` — slide-shell web component (scaling, nav, print)
- `deck/support.js` — Design Component runtime
- `deck/_ds/tranche-group-design-system-.../colors_and_type.css` — design tokens + Aptos `@font-face`
- `deck/assets/` — imagery and logo
- `dist/build-dist.py` — asset-optimizing distribution build (see `dist/README.md`)
- `dist/Wylder-Tilghman-Senior-Debt-Financing.pdf` — the 28-page export

> **Data note.** Every figure reconciles to the sponsor's financial model dated October 6, 2026 (Loan Analysis,
> Sources and Uses, Pro Forma, Total Cost Basis (Hotel), Acquisition & CapEx, Borrower Equity, 5-Yr CapEx History,
> Sales Comps, STR Summary). Sources and uses balance to $0. Do not change numbers without an updated model.
>
> **Open items requiring sponsor or lender input before distribution:**
>
> 1. **2026 combined coverage is 0.69x.** The renovation year does not cover its obligations. The capitalization
>    funds a 12-month interest and carry reserve of $1,201,591 and a 12-month preferred current-pay reserve of
>    $436,073 to carry that period; coverage clears 1.00x in 2027 and reaches 1.57x in 2028. Disclosed on slides 19
>    and 21.
> 2. **Zero common equity at close.** The preferred is sized cash-neutral. The sponsor's residual equity is
>    $3,429,266 at the as-is value and $11,529,266 at the stabilized value.
> 3. **The RevPAR index target moved materially.** The plan now reaches 83% of the five-property market set's RevPAR
>    at stabilization (79% of the four-property STR set), against 70% in the prior model. The entire gain is still
>    attributed to the renovation, the added keys, the expanded marina, the adjacent parcel and the brand
>    affiliation, with no assumed growth in the underlying market.
> 4. **Slip counts are inconsistent between sources.** The capital plan line reads "Marina · 25 new slips"; the Pro
>    Forma revenue line reads "Slips Revenue (incl. 20 add'l slips)"; the Dogwood Cove PSA adds 24. The package uses
>    25 for the capital plan and 24 for Dogwood Cove, for 72 on completion, and does not restate a count alongside
>    the revenue line. Confirm with the sponsor.
> 5. **Three undistributed expense lines run below segment** and are flagged rather than smoothed: administrative
>    and general 6.2%, sales and marketing 4.3%, property operation and maintenance 2.4% of revenue at
>    stabilization.
> 6. **Sponsor support on slide 22** (completion and cost-overrun guaranty, carry guaranty, recourse carve-outs,
>    environmental indemnity, $10,000,000 minimum net-worth covenant) carries over from the prior lender LOI, which
>    is no longer in the package. Confirm it still reflects the intended terms.
