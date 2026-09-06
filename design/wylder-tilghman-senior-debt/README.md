# Handoff: Wylder Hotel Tilghman Island — Senior Debt Financing Deck

## Overview
A 24-slide institutional financing package supporting a **$12,600,000 senior loan** (first mortgage) from **New Day Commercial Capital** on the Wylder Hotel Tilghman Island (Talbot County, MD). The loan refinances the existing $10,714,782 loan, funds closing and origination costs, and returns $843,046 of cash to the sponsor. Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

The deck carries **no equity offering of any kind** — the capitalization is the single first mortgage.

## About the Design Files
The files in `deck/` are a **design reference built in HTML** — a working prototype of the intended look, content, and slide flow, not production code to ship as-is. The task is to **recreate this deck in the target environment** using its established patterns. If the goal is a web app, rebuild the slides as components in the codebase's framework (React/Vue/etc.). If the goal is a distributable presentation, the HTML itself is already the deliverable and can be exported to PDF/PPTX from the design tool.

The deck is a single self-contained Design Component (`.dc.html`) rendered through a lightweight slide-shell web component (`deck-stage.js`) and a runtime (`support.js`). All styling is **inline** on each element; the only shared stylesheet is the design system's `colors_and_type.css` (design tokens + `@font-face`).

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, copy, and figures. Recreate pixel-for-pixel using the exact tokens below. Every figure reconciles to the financial model `Wylder Tighman Island_ Financials_ New Day L 9.4.26.xlsx`; do not alter numbers without an updated model.

## How to Run the Reference
Open `deck/Wylder Tilghman Island - Senior Debt Financing.dc.html` through a local static server (relative paths to `_ds/`, `assets/`, `deck-stage.js`, `support.js` must resolve). Arrow keys / on-screen nav move between slides; the shell handles scaling, a thumbnail rail, speaker notes, and print-to-PDF (one page per slide).

Canvas is **1920×1080** per slide (16:9).

## Design Tokens
Sourced from `deck/_ds/.../colors_and_type.css`. Use these exact values.

**Color**
- `--mm-navy-900` `#001A3D` — deepest navy; dark-slide backgrounds, headline ink on cream
- `--mm-navy` `#002F6C` — primary brand navy (PMS 295); rules, totals
- `--mm-navy-700` `#1A4280`, `--mm-navy-300` / `--mm-navy-100` — lighter navy tints for secondary text on dark
- `--mm-orange` `#E87722` — accent; eyebrows, key figures, the senior loan bar
- `--mm-orange-700` `#C0631C`, `--mm-orange-100` `#FBE3CF`
- `--paper` `#FAF8F4` — warm cream; default light-slide surface
- `--ink-900` `#0E1116`, `--ink-700` `#2A2F37`, `--ink-500` `#5A6068`, `--ink-400` — body text on cream
- `--hairline` `rgba(0,26,61,.12)` — 1px structural dividers
- Capital-stack tier colors used literally: senior loan `#032D67`, accent `#E87722`, value-above-loan blue-gray `#456EAB`, brass `#957551`

**Typography** — Microsoft **Aptos** family, loaded from the design system `fonts/` via `@font-face` (no CDN).
- `--font-display` "Aptos Display" — H1/H2 headlines (700), italic taglines
- `--font-body` "Aptos" — body copy, ledes, captions
- `--font-condensed` "Aptos Narrow" — eyebrows, ALL-CAPS labels, table headers (700, letter-spacing .14–.30em, uppercase)
- `--font-mono` "Aptos Mono" — all currency, percentages, dates, phone (tabular-nums)
- `--font-serif` "Aptos Serif" — used only for the "wylder" wordmark on the title slide

**Type sizes in use (px, at 1920×1080):** title H1 104; section H2 50–56; big stat/hero figures 96–104; stat-grid values 54; table body 17–22; eyebrow 17; labels 13–15.

**Running footer:** every interior slide (2–14) carries a footer rule — `Wylder Hotel Tilghman Island · Senior Debt Financing` left, `MMCC · The TRANCHE Group` right — in `--font-condensed` 14px/700, `.2em` tracking, uppercase, `--ink-400` on light slides and `rgba(255,255,255,.38)` on dark. The title and contact slides carry their own footers instead.

**Rules & borders:** section headers sit above a `1px solid var(--mm-navy)` rule; tables use 2px navy top/bottom borders with 1px `--hairline` interior lines. Corners 0–2px (printed feel, not app-like). No gradients except the photo-overlay scrims on dark hero slides. No shadows except soft photo scrims.

**Motif:** a vertical/horizontal "strata" bar (stacked orange `#F0720E` + blue `#456EAB` segments) on the title, asset, sponsor, terms and contact slides — the capital-stack metaphor. Every instance is split **60% orange / 40% blue**, matching the loan / value-above-loan share of the Year-1 value.

## Screens / Views (24 slides)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text. Each slide is
1920×1080, `box-sizing:border-box`, ~48–96px padding.

**Headings.** Interior slides open with a 64×3px `--mm-orange` rule in place of a text eyebrow, followed by a plain
descriptive H2 (Aptos Display 700, 44–48px). Headlines are declarative statements of fact, not marketing lines — the
package is read by a lender and by the appraiser on the deal.

**Page numbers.** All 24 pages are numbered. Interior slides carry the number at the right end of the running footer,
after a hairline divider; the cover and closing slides carry it in the header bar beside the confidentiality label.

1. **Title** — eyebrow "SENIOR DEBT FINANCING · $12,600,000", H1 property name, factual tagline.
2. **Summary of the financing request** — 8-tile grid: loan $12.60M, all-in rate 10.29%, 30-yr term, debt service
   $1.36M, LTV 60.0%, projected stabilized DSCR 1.47x, debt yield 15.9%, cost basis $18.68M.
3. **A 57-key waterfront resort on 8.10 acres in Talbot County, Maryland** — photo split, lede, 2×2 facts,
   two thumbnails.
4. **Ownership, operator and credit support** — ownership narrative, 2×2 facts, four Sponsor Commitments to the
   Lender, closing note on the $2,000,000 of sponsor cash equity funded outside loan proceeds.
5. **Operator background and brand portfolio** — brand blurb, three-property portfolio, principal's career record.
6. **Business plan and capital improvement program** — three numbered items against the $3,003,000 /
   $52,684-per-key program, funded by the sponsor outside this financing. Item 01 quantifies the seven added keys
   (four returned from out-of-service, three in the back house — 12.3% more sellable inventory); item 02 quantifies
   the 25-slip marina at $250,000 of cost against roughly $146,000 a year of departmental profit.
7. **Small Luxury Hotels affiliation and distribution** — Hilton.com / Hilton app / Hilton Honors distribution, the
   existing relationship through Wylder Windham, and the American Express Fine Hotels & Resorts designation. Right
   column carries membership economics ($100,222 over the four-year term, 0.49% of stabilized revenue).
8. **Estimated values and underwritten projections** — three-value band across the top: estimated as-is $21,000,000
   ($368,421/key), upon completion $25,500,000 ($447,368/key), upon stabilization $28,500,000 ($500,000/key),
   disclaimed immediately beneath. Below, projected 2027/2028/2029 operations and a stabilized-NOI takeaway.
9. **Pro forma cash flow and underwriting assumptions** — available and occupied room nights, occupancy, ADR,
   RevPAR, rooms and other revenue, operating expenses and NOI for 2027–2029 at left; the assumption set at right.
10. **Extended cash flow, fiscal 2030 through fiscal 2040** — an eleven-year projection on a *more conservative*
    basis than the sponsor model: occupancy flat at 43.0%, 3.0% rate growth, no market growth, and a 3.0%
    management fee and 4.0% replacement reserve deducted as separate lines. Full departmental build to NOI, then
    debt service, DSCR (1.43x → 2.00x) and debt yield (15.4% → 21.6%). The ~15% shortfall against the sponsor case
    at the common point is stated on the page rather than left to be discovered.
11. **Departmental revenue and margins against industry benchmarks** — revenue by department at stabilization vs the
    resort segment; F&B against outlet comparables (per seat, per SF, per occupied room); the marina and the seven
    added keys shown as $580,000 of revenue and $444,000 of departmental profit *not present in any historical
    period*; margins and departmental cost ratios against the resort and independent segments.
12. **Historical operations and competitive benchmarking** — actual 2023/2024/2025 at left; STR benchmarking
    (YTD December 2025) at right against the four-property, 364-room competitive set. 2026 is a transition year and
    is not presented.
13. **The competitive market, supply and demand** — the five-property, 404-room market set with 2025 occupancy, ADR
    and RevPAR and the subject's 44% RevPAR index; penetration against the market for 2024 and 2025 (RevPAR index
    48% → 44%, with the rate-driven cause stated); the supply/demand/ADR/RevPAR series 2019–2025 with CAGRs and TTM
    March 2026; and market seasonality by peak/shoulder/trough. Notes explicitly that this set and the STR set on
    page 12 are differently constituted.

    CAGRs run 2019–2025, not 2015–2025: the 2015 panel carried only 98 rooms, which produced a 15.2% "supply CAGR"
    that contradicted the flat-supply narrative on the same page.
14. **Drive-to demand, visitation and new supply** — metropolitan areas within a half-day drive (36.9M people within
    3.5 hours), Talbot County visitation and visitor spending, and the submarket new-supply pipeline.
15. **A single first mortgage at 60.0% of estimated as-is value** — two proportional bars against the $21,000,000
    estimated as-is value: implied equity $8,400,000 (40.0%) and senior loan $12,600,000 (60.0%).
16. **Summary of senior loan terms** (dark) — 10.29% (index 4.54% / spread 5.75% / fixed); 30 yrs (debt service
    $1,359,403 / constant 10.789% / no IO); 60.0% max LTV (min DSCR 1.20x / prepay 1 year · 5%). Fee strip.
17. **Projected debt service coverage, 2027 through 2029** — NOI, debt service, DSCR and debt yield. Net cash flow
    after debt service is deliberately not shown.
18. **Loan measured against cost basis, value and sponsor support** (dark) — loan coverage measures, a callout
    separating cost incurred to date from cost remaining to be funded, and three supporting blocks.
19. **Cost Basis and Sponsor Equity** — total project cost basis $18,679,659 split into $12,714,782 incurred to date
    and $5,964,877 remaining to be funded; cost basis per key $327,713 vs loan per key $221,053.
20. **Estimated value positioned against market evidence** — per-key positioning table placing the senior loan
    ($221,053/key), total project cost basis ($327,713/key), the three estimated values and **both** comparable
    sets — the East Coast waterfront sales and the recent resort trades — on one scale, so the two sets reconcile
    on the page rather than implying two different positions.
21. **Comparable hotel sales, resort and local** — eight East Coast waterfront resort trades plus the weighted
    average and median of eleven sales at left; eight local Eastern Shore transactions at right, with a note
    distinguishing them so the lower local pricing is addressed rather than left to be discovered.
22. **Recent transaction evidence and local market activity** — eight independent resort and waterfront trades
    closed January 2025 to March 2026 averaging 44 keys (weighted average $463K/key, median $332K/key); at right,
    the Tilghman Island Inn under contract at $260K/key, the Robert Morris Inn closed and relisted, and the
    Tidewater Inn coming to market, all distinguished on product tier and income base.
23. **Sources and uses of funds at closing** — sources ($12,600,000, $0 sponsor equity) and closing-cost detail;
    uses balanced to $0, plus the net-funding memo.
24. **Contact and next steps** — stat strip, contact block, page number in the header bar.

### Valuation language
No appraiser, appraisal firm or third-party valuation conclusion is named anywhere in the package. The value points
are an **estimated as-is value of $21,000,000**, **upon completion of $25,500,000** and **upon stabilization of
$28,500,000**, carried on slides 8, 15 and 20 and labeled with: "Estimated values are management's estimates
prepared for underwriting purposes only. They are not appraisals, and no third-party valuation conclusion is
represented." This is deliberate — the package is distributed to the appraiser engaged on the transaction, and must
not anchor that appraiser to a prior conclusion.

### The two projections
The deck carries **two** operating projections and says so on the page. Slides 8–9 are the sponsor model
(calendar 2027–2029). Slide 10 is an independent, more conservative eleven-year view on fiscal years ending
April 30, which deducts a management fee and a replacement reserve as separate lines and lands roughly 15% below
the sponsor case at the common stabilized point. Both are shown because the loan covers in both; presenting only
the higher one would invite exactly the question the second projection answers.

### Figures
Every per-key figure runs on 57 keys and every column total was re-derived from its components during review. The
$000s table on slide 10 carries an explicit "columns may not foot due to rounding" note because 5 of its 11 columns
differ by $1K from the sum of the rounded components.

### Market data
Comparable sales, competitive-set composition, market supply and demand, drive-to demand, visitation, departmental
comparables and industry benchmarks are presented as market facts. Talbot County visitation is attributed to Talbot
County Economic Development and Tourism; competitive set performance is attributed to STR. No brokerage, appraisal
or valuation document is cited or reproduced anywhere in the package.

## Interactions & Behavior
- Slide navigation via `deck-stage`: arrow keys, click nav, thumbnail rail, print-to-PDF (one page/slide). No per-element interactivity — this is a linear presentation.
- Entrance/transition animations are the shell's; for a static/print build they are frozen to final frame.
- No forms, data fetching, or app state.

## State Management
None. Static content deck. If rebuilt as app components, the only "state" is the current slide index (owned by the slide shell).

## Assets (in `deck/assets/`)
- `wt-aerial-spring.png` — hero aerial (title slide)
- `wt-aerial.png` — aerial (contact slide)
- `wt-pier.png` — waterfront at dusk (asset slide, left)
- `wt-suite.jpg` — renovated guest room (asset thumbnail)
- `wt-pool.png` — waterfront pool (asset thumbnail)
- `wt-lobby.png` — renovated interior/lobby (The Sponsor slide photo panel)
- `flannigan.png` — John Flannigan headshot, square-cropped for circular display (Track Record slide)
- `mmcc-2018-white.png` — Marcus & Millichap Capital Corporation logo, white
- `buzil.jpg` — Bradley M. Buzil headshot (contact slide)
All are real property/brand photography. If rebuilding in a codebase with its own brand system, reuse the MMCC brand assets there.

## Files
- `deck/Wylder Tilghman Island - Senior Debt Financing.dc.html` — the deck (all 15 slides, inline-styled)
- `deck/deck-stage.js` — slide-shell web component (scaling, nav, print)
- `deck/support.js` — Design Component runtime
- `deck/_ds/tranche-group-design-system-.../colors_and_type.css` — design tokens + Aptos `@font-face`
- `deck/_ds/.../fonts/` — Aptos font files
- `deck/assets/` — imagery and logo

> Data note: every figure reconciles to `Wylder Tighman Island_ Financials_ New Day L 9.4.26.xlsx`
> (Loan Analysis, Sources and Uses, Pro Forma, Total Cost Basis, Borrower Equity, Sales Comps, STR Summary).
> Sources and uses balance to $0.00. Do not change numbers without an updated model.
>
> **Open items requiring sponsor or lender input before distribution:**
>
> 1. **The $3,003,000 capital improvement program is funded by the sponsor outside this financing** and is not
>    drawn from loan proceeds. Stated on slides 6, 8, 14, 15 and 18 so the absence of a PIP line in the sources and
>    uses is explained where it is visible. Confirmed by the sponsor 6 September 2026.
> 2. **Projected Year-1 (2027) DSCR is 0.93x against a 1.20x minimum.** Max loan by DSCR in Year 1 is $9,730,166,
>    some $2,869,834 below the $12,600,000 request, and no interest reserve is funded in the sources and uses. The
>    deck discloses the sub-minimum coverage and attributes any shortfall to the sponsor carry guaranty.
> 3. **The $21,000,000 estimated as-is value is management's, not an appraisal.** It equals the Year-1 proforma
>    value in the model (NOI capitalized at 5.999%). It is disclaimed as such wherever it appears.
> 4. **Key count.** The model's Pro Forma tab is headed "54 rooms" while Loan Analysis uses 50 current / 57 at
>    stabilization. The package uses 50→57 throughout, and all per-key figures are computed on 57 keys.
