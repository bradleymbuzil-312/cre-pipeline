# Handoff: Wylder Hotel Tilghman Island — GP/LP Recapitalization Deck

## Overview
A 30-slide institutional equity package marketing a **$13,255,085 limited partner recapitalization** of the
equity in Wylder Hotel Tilghman Island (Talbot County, MD). The LP funds the entire closing; a senior
refinance follows in month three.

**Equity ownership is GP 51% / LP 49%** — and ownership is deliberately not the same thing as capital. The
LP contributes 100% of the equity and holds 49% of it; the GP holds 51% and contributes none. The waterfall
sits ahead of the ownership split, so the GP's majority interest is fully subordinated and has no effect
until the LP has been made whole. In the base case the GP receives **11.0% of total equity cash
($3,309,883 of $30,117,321)** against its 51% interest, and it receives nothing at all below a $25,278,210
sale value.

| | Amount | Note |
|---|---|---|
| LP equity (gross) | $13,255,085 | 61.94% of as-is value · $228,536 per key on 58 keys |
| LP net cash invested | $12,989,984 | After the 2.00% origination fee retained at funding |
| Senior loan (month 3) | $7,000,000 | SOFR + 600, interest-only, 2.00% origination, balance held flat |
| **Total capital** | **$20,255,085** | Less $2,070,384 returned to the LP at the refinance |
| **Net capital in the asset** | **$18,184,701** | $313,529 per key |

**The waterfall.** Tier 1 — operating cash flow 100% to the LP until the accrued preferred return is
current; capital events 100% to the LP until the preferred return **and** all invested capital are repaid.
Tier 2 — 100% to the LP until it has received 2.0x net cash invested *and* earned at least a 20% IRR; the GP
receives nothing before that. Tier 3 — 20% LP / 80% GP on proceeds up to a $30,000,000 gross sale value (the promote, above the GP's 51%
pro rata). Tier 4 — 50/50 above $30,000,000 (marginally below it). Preferred return 12.0% compounded quarterly (12.55% effective annual),
cumulative, on the gross capital account. **No GP capital account, no minimum multiple, no GP guaranty.**

**Base case** — a month-36 sale at the $29,500,000 stabilized value: **2.06x / 37.3% IRR**, $26,807,438 of
total LP distributions, $13,817,455 of net profit, of which $8,038,602 (62% of net cash invested) is
returned before the sale month. GP distributions $3,309,883.

GP = Wylder Hotels (John Flannigan), operator, sponsor and managing member, holding 51% of the equity.
LP = recapitalization equity investor, holding 49% and contributing all of the capital.
Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

## About the Design Files
The files in `deck/` are a **design reference built in HTML** — a working prototype of the intended look,
content and slide flow, not production code to ship as-is. If the goal is a distributable presentation, the
HTML itself is already the deliverable and exports to PDF one slide per page.

The deck is a single self-contained Design Component (`.dc.html`) rendered through a lightweight slide-shell
web component (`deck-stage.js`) and a runtime (`support.js`). All styling is **inline** on each element; the
only shared stylesheet is the design system's `colors_and_type.css` (design tokens + `@font-face`).

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, copy and figures. Capital-structure, waterfall
and return figures reconcile to **`Wylder Tilghman Recapitalization GP/LP Model v4`, dated 27 October 2026**
(Summary, Inputs, Waterfall, Operating CF, Sensitivity). Operating figures reconcile to the **10.6.26
financial model** — the Operating CF tab of the v4 model is that pro forma's NOI after the asset management
fee, tied out month by month. Do not alter numbers without an updated model.

## How to Run the Reference
Serve `deck/` over a local static server (relative paths to `_ds/`, `assets/`, `deck-stage.js`, `support.js`
must resolve — `file://` fails CORS) and open `Wylder Tilghman Island - Recapitalization.dc.html`. Arrow keys
/ on-screen nav move between slides; the shell handles scaling, a thumbnail rail, speaker notes and
print-to-PDF.

Canvas is **1920×1080** per slide (16:9).

## Design Tokens
Sourced from `deck/_ds/.../colors_and_type.css`. Use these exact values.

**Color**
- `--mm-navy-900` `#001A3D` — deepest navy; dark-slide backgrounds, headline ink on cream
- `--mm-navy` `#002F6C` — primary brand navy (PMS 295); rules, totals
- `--mm-navy-700` `#1A4280`, `--mm-navy-300` / `--mm-navy-100` — lighter navy tints for secondary text on dark
- `--mm-orange` `#E87722` — accent; eyebrows, key figures, the GP share of each tier bar
- `--mm-orange-700` `#C0631C`, `--mm-orange-100` `#FBE3CF`
- `--paper` `#FAF8F4` — warm cream; default light-slide surface
- `--ink-900` `#0E1116`, `--ink-700` `#2A2F37`, `--ink-500` `#5A6068`, `--ink-400` — body text on cream
- `--hairline` `rgba(0,26,61,.12)` — 1px structural dividers
- Capital tier colors used literally: **LP equity `#456EAB`**, **senior loan `#032D67`**, GP share of a tier
  bar `#957551`, strata-bar orange `#F0720E`

**Typography** — Microsoft **Aptos** family, loaded from the design system `fonts/` via `@font-face` (no CDN).
- `--font-display` "Aptos Display" — H1/H2 headlines (700), italic taglines
- `--font-body` "Aptos" — body copy, ledes, captions
- `--font-condensed` "Aptos Narrow" — eyebrows, ALL-CAPS labels, table headers (700, letter-spacing .14–.30em)
- `--font-mono` "Aptos Mono" — all currency, percentages, multiples, dates, phone (tabular-nums)
- `--font-serif` "Aptos Serif" — used only for the "wylder" wordmark on the title slide

**Type sizes in use (px, at 1920×1080):** title H1 104; section H2 40–48; big stat/hero figures 92–104;
stat-grid values 44–46; table body 13–22; eyebrow 17; labels 10–15.

**Running footer:** every interior slide (2–29) carries a footer rule —
`Wylder Hotel Tilghman Island · Recapitalization` left, `MMCC · The TRANCHE Group` right, then the page
number after a hairline divider — in `--font-condensed` 14px/700, `.2em` tracking, uppercase, `--ink-400` on
light slides and `rgba(255,255,255,.38)` on dark. The cover (01) and contact (30) slides carry the page
number in the header bar beside the confidentiality label (`Confidential · Equity Recapitalization`).

**Rules & borders:** section headers sit above a `1px solid var(--mm-navy)` rule; tables use 2px navy
top/bottom borders with 1px `--hairline` interior lines. Corners 0–2px (printed feel, not app-like). No
gradients except the photo-overlay scrims on dark hero slides.

**A design-system CSS rule caps `<p>` width at ~479px.** Every paragraph needs an explicit `max-width:none`
(or a `ch` value) or it wraps narrow.

**Motif:** a strata bar (stacked segments in the LP and senior colors) on the title, investor-returns and
contact slides — the capital-stack metaphor, split 65.44% / 34.56% to match LP equity and the senior loan.

## Screens / Views (30 slides)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text. Interior
slides open with a 64×3px `--mm-orange` rule in place of a text eyebrow, followed by a plain descriptive H2.

1. **Title** — eyebrow "RECAPITALIZATION · $13,255,085 LP EQUITY", H1 property name, factual tagline, dated
   October 27, 2026.
2. **Summary of the recapitalization** — lede plus an 8-tile grid: LP equity $13.26M, GP/LP equity 51%/49%,
   preferred return 12.0%, equity multiple 2.06x, projected IRR 37.3%, GP share of cash 11.0%, debt at
   closing $0, cash before the sale $8.04M.
3. **A 58-key waterfront resort on 8.10 acres, with an adjacent parcel under contract** — photo split, lede,
   2×2 facts, two thumbnails.
4. **What the asset comprises** — four columns (Location, Accommodations, Food/Beverage/Events, Amenities),
   each with a photograph and a fact card. Key bridge: 50 rooms in service, 4 out of service to be restored,
   3 from the rebuilt three-bedroom house = 57 hotel keys, 58 with Dogwood Cove. Marina 23 slips today · 24
   with the acquisition · 47 on completion.
5. **Adjacent acquisition — 21441 Dogwood Cove** — full-width aerial, then Transaction ($1,100,000 purchase
   funded by LP equity at closing with no acquisition debt, fee simple, $15,000 deposit, closing
   November 18, 2026,
   $300,000 renovation held back by the senior lender), What It Adds, and Why It Matters.
6. **Ownership and operating structure** — the GP. Ownership narrative, 2×2 facts and four Structure and
   Alignment points.
7. **Operator background and brand portfolio.**
8. **Business plan and capital improvement program** — three numbered items against the $3.3M /
   $56,948-per-key program; RevPAR index, drivers list and two stat tiles at right.
9. **The renovation is designed, priced and scheduled** — Gantt across September 21, 2026 to April 1, 2027
   with exact dates, alongside the completed model room.
10. **Small Luxury Hotels affiliation and distribution.**
11. **Estimated values and underwritten projections** — as-is $21,400,000 ($368,966/key), upon completion
    $26,000,000 ($448,276/key), upon stabilization $29,500,000 ($508,621/key); 2026–2030 operations.
12. **Pro forma cash flow and underwriting assumptions** — 2026–2030 at left, the assumption set at right.
13. **Stabilized cash flow carried forward, 2030 through 2041** — 2030 is the first full year after the
    projected October 2029 sale, so this page is what a **buyer** underwrites at exit. Debt service is the
    $7,000,000 senior loan held flat and interest-only.
14. **Departmental revenue and margins against industry benchmarks** — 2028 stabilized year.
15. **Historical operations and competitive benchmarking** — actual 2023/2024/2025 plus STR benchmarking.
16. **The competitive market, supply and demand.**
17. **Drive-to demand, visitation and new supply.**
18. **A $13,255,085 LP recapitalization of the equity** — a proportional bar of total capital (LP 65.44% /
    senior 34.56%), an Equity Ownership block (GP 51% / LP 49%, with the capital-versus-ownership
    distinction stated), Capital Measures, and The Parties.
19. **Sources and uses of funds at closing** — LP equity is the only source; seven uses to $13,255,085;
    closing detail $130,100. Sources less uses = $0.
20. **A $7,000,000 senior refinance in month three** — terms at left, allocation of proceeds at right, with
    the $2,070,384 return of capital highlighted.
21. **The GP holds 51% of the equity and is paid last** (dark) — four tiers with LP/GP split bars and
    base-case dollars per tier, over a lede stating that the ownership split has no effect until the LP is
    made whole. Bottom strip: GP equity interest 51%, GP share of base-case cash 11.0%, preferred return
    12.0%/12.55%, and the $25.3M sale value below which the GP receives nothing.
22. **Projected investor returns** (dark) — 2.06x / 37.3% / 36 months, with supporting rows and a bottom
    strip (cash returned before the sale, from the refinance, from operations, unpaid capital after sale).
23. **LP distributions across the hold period** — by calendar year 2026–2029 plus a Total column (operating
    cash flow, capital events, pref accrued, tiers 1–3, total), the LP capital account trajectory, and the
    LP/GP equity cash split at five sale values (100.0%/0.0% at $21.4M through 82.7%/17.3% at $35.0M).
24. **Sensitivity to sale value and sale month** — multiple and IRR grids across 11 sale values × 4 sale
    months, plus the gross sale value needed for LP 1.00x and 2.00x at each hold.
25. **The downside and what protects it** (dark) — twelve downside measures (including the GP's 51% interest
    against its 11.0% share of base-case cash) and five structural protections, among them "A Majority
    Interest, Paid Last", which also carries the LP's major-decision approval rights.
26. **Total basis and the renovation plan** — the $18,184,701 net capital in four groups, the capital plan
    itemized, four per-key tiles and the exact start/completion dates.
27. **Estimated value positioned against market evidence** — per-key positioning placing LP equity, net
    capital, the three estimated values and **both** comparable sets on one scale.
28. **Comparable hotel sales, resort and local.**
29. **Recent transaction evidence and local market activity.**
30. **Contact and next steps** — stat strip (LP equity, preferred return, equity multiple), contact block.

### Valuation language
No appraiser, appraisal firm or third-party valuation conclusion is named anywhere in the package, and the
word *appraisal* does not appear. The value points are an **estimated as-is value of $21,400,000**, **upon
completion of $26,000,000** and **upon stabilization of $29,500,000**, labeled: "Values are stated for
underwriting purposes and are subject to completion of the renovation and stabilization of operations."

### Key count convention
The **hotel** is 50 keys today and 57 on completion of the renovation; the Dogwood Cove residence is the
**58th key**, operated as a whole-home suite at a $1,500 nightly rate and 35% occupancy ($191,625 a year from
stabilization, in the projections). **All per-key figures in this package are stated on 58 keys** — the deck,
the LP summary and the model agree (`Inputs!B49` = 58, `LP equity per key` = $228,536). The marina is
**23 slips today and 47 on completion** — the 24 slips that come with the Dogwood Cove acquisition are the
expansion, which closes **November 18, 2026**.

### Market data
Comparable sales, competitive-set composition, market supply and demand, drive-to demand, visitation,
departmental comparables and industry benchmarks are presented as market facts. Talbot County visitation is
attributed to Talbot County Economic Development and Tourism; competitive-set performance is attributed to
STR. No brokerage, appraisal or valuation document is cited or reproduced, and no lender is named.

## Assets (in `deck/assets/`)
`wt-aerial-spring.png` (title), `wt-aerial.png` (contact), `wt-pier.png` (asset slide + thumbnail),
`wt-suite.jpg` (model guest room, slides 3/4/9), `wt-pool.png`, `wt-fb-signs.jpg`,
`wt-dogwood-aerial.jpg` (slide 5), `wt-lobby.png` (sponsor), `flannigan.png`, `buzil.jpg`,
`mmcc-2018-white.png` (the only asset with real transparency).

## The send-together package

`package/` holds the three documents that go to an investor as a set — the deck PDF, the LP equity
summary and the GP/LP model — with its own manifest and the list of conventions applied across all
three. `scripts/crosscheck.py` asserts that every shared figure reconciles and that no appraiser or
appraisal is named in any of them; run it after any change to the deck, the summary or the model.

```
python3 -I scripts/crosscheck.py     # 30 assertions; exits non-zero on a mismatch
```

## Files
- `deck/Wylder Tilghman Island - Recapitalization.dc.html` — the deck (all 30 slides, inline-styled)
- `deck/deck-stage.js` — slide-shell web component (scaling, nav, print)
- `deck/support.js` — Design Component runtime
- `deck/_ds/tranche-group-design-system-.../colors_and_type.css` — design tokens + Aptos `@font-face`
- `dist/build-dist.py` — asset-optimizing distribution build (see `dist/README.md`)
- `package/` — the three send-together documents plus their manifest
- `scripts/crosscheck.py` — cross-document reconciliation; `scripts/scrub_model.py` — label scrub

> **Data note.** Capital, waterfall and return figures reconcile to the GP/LP model v4 dated 27 October 2026;
> operating figures reconcile to the 10.6.26 financial model. Sources and uses balance to $0. Do not change
> numbers without an updated model.
>
> **Open items requiring sponsor or counsel input before distribution:**
>
> 1. **2.0x is a projection, not a minimum.** At month 36 the LP is below 2.0x if the sale is under
>    $25,278,210. Capital is returned in full at $12,023,125, 43.8% below the as-is value. Both are on
>    pages 24 and 25.
> 2. **The GP falls short of its $5.0M target in the base case** at $3,309,883. The model's own sensitivity
>    puts $5.0M at roughly $32.6M at month 36 or $29.4M at month 48. The deck does not present the GP target;
>    expect it in negotiation. Note the tension with the 51% ownership: a majority holder taking 11.0% of the
>    cash is the point of the subordination, but it is also why the $5.0M target is not met here.
> 3. **The GP's 51% interest carries control, not just economics.** An LP funding 100% of the capital while
>    holding a 49% minority interest needs the operating agreement to carry its protections — major-decision
>    consents, removal rights on a GP default, and the subordination itself. The deck presents the economics;
>    counsel must paper the governance. Tax allocations of a 51% interest with no capital account also need
>    to be set by counsel.
> 4. **The 80% GP share in tier 3 is aggressive** relative to institutional feedback (the model's own note).
>    The deck presents it as drafted.
> 5. **The $30.0M tier 4 hurdle is a gross sale value test.** Definitive documents should define it (gross
>    versus net of costs) because the definition shifts the split.
> 6. **Working capital appears twice.** $250,000 is a closing use funded by LP equity and $500,000 is held
>    back at the refinance, so the deck shows $750,000 of total working capital on page 26. The model's input
>    label reads "funded $250K, held back $250K" while its arithmetic subtracts the full $500,000 from refinance
>    proceeds. Confirm which is intended.
> 7. **Sale costs are modeled at 2.0% of value** and exclude Maryland transfer and recordation taxes, which
>    require local verification.
> 8. **Legal ownership, control and tax allocation of the promote** are to be set by counsel.
