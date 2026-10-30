# Handoff: Wylder Hotel Tilghman Island — Three Capitalization Packages

## Overview
Three 28-slide institutional packages marketing a **$17,404,044 recapitalization** of Wylder Hotel
Tilghman Island (Talbot County, MD) — one package per capital tranche, each disclosing only its own
economics. Built on the **10.28.26 financial model**.

| Tranche | Amount | Share | Terms | Base case ($30.0M exit, 3-yr hold) |
|---|---|---|---|---|
| Senior loan · 1st trust deed | $10,000,000 | 57.46% | 12.00% all-in (SOFR 3.79% + 8.21%), IO, 3 yr, 5.00% exit participation | 1.48x · 15.6% IRR |
| Preferred equity | $3,904,044 | 22.43% | 17.00% accrued, no current pay, cash sweep, 10.00% exit participation | 1.97x · 31.5% IRR |
| Common equity · LP | $3,500,000 | 20.11% | 15.00% cumulative pref, capital, then 50/50 residual | 2.33x · 32.6% IRR |
| **Total capitalization** | **$17,404,044** | | All funded at close | |

Alongside the LP, the GP (John Flannigan / Wylder Hotels) has **$2,000,000 of its own cash** in the
deal on identical pari passu terms — a $5,500,000 partnership in which the LP holds 63.64% of the
capital. **The GP holds a 51% ownership interest** but receives **41.9% of partnership cash** at the
base case, and takes no distribution until the LP has been paid its 15.00% preferred return and its
capital back in full. Its 50% of the residual on 36.36% of the capital is the whole of its promote.

**Total cost basis $19,247,882 — $331,860 per key on 58 keys.** Estimated values: as-is $21,400,000,
upon completion $26,000,000, upon stabilization $29,500,000.

### Economic isolation between the packages
Each package carries only its own economics. **No package discloses another tranche's rate, fees,
participation, promote, splits or returns.** What every recipient does see: the three tranche
**amounts** and their share of the stack, position in the stack, LTV / loan-to-cost /
debt-and-preferred-to-value, total basis, estimated values, the operating projections, and senior
debt service in dollars where the property cash flow requires it. In the common equity package the
senior and preferred deduction in the waterfall is a **single aggregated amount** ($4,751,666 at the
base case), never itemized.

Enforced by an audit in `scripts/build/v7_build.py` and verified against the PDFs by
`scripts/crosscheck.py` (19 checks).

### No exit level showing a loss
The returns page in each package (page 22, marked "not for distribution") spans $18M–$36M for the
senior and preferred, both of which profit at every level, and **$21M–$36M for the common equity**,
because the LP's $18M column is a loss (0.77x, −8.2%). The partnership breakeven and the GP's $18M
figures are omitted from the common package entirely.

Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

## About the Design Files
The files in `deck/` are a **design reference built in HTML** — a working prototype of the intended look,
content and slide flow, not production code to ship as-is. If the goal is a distributable presentation, the
HTML itself is already the deliverable and exports to PDF one slide per page.

The deck is a single self-contained Design Component (`.dc.html`) rendered through a lightweight slide-shell
web component (`deck-stage.js`) and a runtime (`support.js`). All styling is **inline** on each element; the
only shared stylesheet is the design system's `colors_and_type.css` (design tokens + `@font-face`).

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, copy and figures. Capital-structure,
waterfall and return figures reconcile to the **10.28.26 financial model**; every figure used is
asserted in `scripts/build/figs_v7.py`, which foots the stack, the uses, the preferred roll-forward,
the exit waterfall at all seven exit values, each tranche's basis / cash / profit / multiple, and the
partnership tiers. Operating figures reconcile to the same model's pro forma. Do not alter numbers
without an updated model.

## How to Run the Reference
Serve `deck/` over a local static server (relative paths to `_ds/`, `assets/`, `deck-stage.js`,
`support.js` must resolve — `file://` fails CORS) and open one of:

- `Wylder Tilghman Island - Senior Debt.dc.html`
- `Wylder Tilghman Island - Preferred Equity.dc.html`
- `Wylder Tilghman Island - Common Equity.dc.html`

Arrow keys / on-screen nav move between slides; the shell handles scaling, a thumbnail rail, speaker
notes and print-to-PDF.

### Rebuilding
```
python3 scripts/build/v7_build.py      # regenerates all three .dc.html from the shared core, with the leak audit
python3 dist/build-dist.py             # optimizes assets into dist/_dist-deck (25.3 MB -> 2.3 MB)
python3 scripts/crosscheck.py          # verifies the three exported PDFs
```
`v7_build.py` lifts the fifteen shared core pages from
`deck/Wylder Tilghman Island - Recapitalization.dc.html` (the superseded single-package deck, kept as
the source of those pages), patches the two that carried tranche economics, and writes the three
packages. Print the optimized decks to PDF at 1920×1080 into `package/`.

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

**Running footer:** every interior slide (2–27) carries a footer rule — `Wylder Hotel Tilghman Island · <Senior Debt | Preferred Equity | Common Equity>` left, `MMCC · The TRANCHE Group` right, then the page number after a hairline divider — in `--font-condensed` 14px/700, `.2em` tracking, uppercase, `--ink-400` on light slides and `rgba(255,255,255,.38)` on dark. The cover (01) and contact (28) slides carry the page number in the header bar beside the confidentiality label (`Confidential · <tranche> Placement`).

**Rules & borders:** section headers sit above a `1px solid var(--mm-navy)` rule; tables use 2px navy
top/bottom borders with 1px `--hairline` interior lines. Corners 0–2px (printed feel, not app-like). No
gradients except the photo-overlay scrims on dark hero slides.

**A design-system CSS rule caps `<p>` width at ~479px.** Every paragraph needs an explicit `max-width:none`
(or a `ch` value) or it wraps narrow.

**Motif:** a strata bar on the title and contact slides, split 60/40 between `#F0720E` and the recipient's tranche color — senior `#032D67`, preferred `#957551`, common `#456EAB`. The same three colors carry the stacked capital bar on page 18, where the recipient's tranche is at full opacity with an orange left mark and the other two are at 42%.

## Screens / Views (28 slides, identical structure in all three)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text.
Interior slides open with a 64×3px `--mm-orange` rule in place of a text eyebrow, followed by a plain
descriptive H2.

**01 Title** — tranche-specific. Eyebrow `<TRANCHE> · $<amount>`, H1 property name, a factual tagline
carrying that tranche's terms and projected return, dated October 30, 2026.

**02 Summary** — tranche-specific lede plus an 8-tile grid of that tranche's own measures, ending in
its projected multiple and IRR.

**03–17 Shared core** — identical in all three except where noted:
3. A 58-key waterfront resort on 8.10 acres, with an adjacent parcel under contract.
4. What the asset comprises — four columns, each with a photograph and a fact card. 50 rooms in
   service, 4 out of service to be restored, 3 from the rebuilt three-bedroom house = 57 hotel keys,
   58 with Dogwood Cove. Marina 23 slips today · 24 with the acquisition · 47 on completion.
5. Adjacent acquisition — 21441 Dogwood Cove. $1,100,000 purchase funded from the capitalization at
   closing with no acquisition debt, fee simple, $15,000 deposit, closing November 18, 2026,
   $300,000 renovation.
6. Ownership and operating structure — the sponsor.
7. Operator background and brand portfolio.
8. Business plan and capital improvement program — the $3.3M / $56,948-per-key program.
9. The renovation is designed, priced and scheduled — Gantt, November 1, 2026 to April 30, 2027.
   The axis and bars are computed from real dates in `scripts/build/v7_reno.py`, which also
   feeds the start/completion rows on page 24 — change the dates there, not in the markup.
10. Small Luxury Hotels affiliation and distribution.
11. Estimated values and underwritten projections.
12. Pro forma cash flow and underwriting assumptions.
13. Stabilized cash flow carried forward, 2030 through 2041 — what a **buyer** underwrites at exit.
    *Tranche-aware:* the senior package states the rate on the debt-service line; the other two see
    the dollar debt service only.
14. Departmental revenue and margins against industry benchmarks — 2028 stabilized year.
15. Historical operations and competitive benchmarking.
16. The competitive market, supply and demand.
17. Drive-to demand, visitation and new supply.

**18 Capital structure** — a proportional stacked bar of the $17,404,044 stack with the recipient's
tranche at full opacity and an orange left mark, the other two at 42%. Capital Measures (all three
amounts, the GP co-investment, LTV, loan-to-cost, debt-and-preferred to value, total per key).
**Your Terms** carries the recipient's economics only.

**19 Sources and uses of funds at closing** — three sources with share and per-key, eleven uses,
closing detail $130,100, sources less uses $0. The recipient's own fee lines are itemized; the other
tranches' fees are rolled into one generic line. The Net Funding block is the recipient's own.

**20–23 Tranche pages** — the only four pages that differ in substance:

| | Senior Debt | Preferred Equity | Common Equity |
|---|---|---|---|
| 20 | Terms of the senior loan *(dark)* | Terms of the preferred equity *(dark)* | Terms of the partnership *(dark)* |
| 21 | Coverage, debt yield and leverage | The cash sweep and the preferred balance | How sale proceeds reach the partnership |
| 22 | **Senior loan return across exit values** | **Preferred equity return across exit values** | **Limited partner return across exit values** |
| 23 | Credit considerations and downside coverage *(dark)* | Position in the stack and downside coverage *(dark)* | Sponsor alignment and the GP position *(dark)* |

**24 Total basis and the renovation program** — the $19,247,882 basis in three groups, the renovation
plan itemized, four per-key tiles and the exact start/completion dates. The senior package itemizes
the senior fee lines; the other two show one generic financing-fees line.

**25 Estimated value positioned against market evidence** — per-key positioning against both
comparable sets, with the recipient's own attachment point: the senior at $172,414 per key, the
preferred last dollar at $239,725, the full capitalization at $300,070.

**26 Comparable hotel sales, resort and local.**

**27 Recent transaction evidence and local market activity.**

**28 Contact and next steps** — tranche-specific. Stat strip carries the recipient's own three
headline terms.

### The estimated values exclude the acquisition
The estimated as-is, as-complete and stabilized values are **for the hotel**. They do not include the
adjacent Dogwood Cove parcel, and every basis, coverage and return figure in the package is measured against
them — so the parcel's value is upside the numbers do not carry. This is stated on pages 5, 11, 24 and 25 of each package. Page 5 sizes it: capitalizing the **~$300,000 of EBITDA the parcel itself
produces** (marina and room revenue) at **7.0%** implies **~$4.3M of value** against a **$1.4M all-in
cost** — roughly **$2.9M above cost**, 3.1x on cost. The $300,000 is conservative against the model's own
components (the Dogwood Cove house carries $191,625 of revenue at stabilization and the marina $341,332 of
departmental profit, of which 24 of 47 slips are attributable to the parcel).

### Valuation language
No appraiser, appraisal firm or third-party valuation conclusion is named anywhere in the package, and the
word *appraisal* does not appear. The value points are an **estimated as-is value of $21,400,000**, **upon
completion of $26,000,000** and **upon stabilization of $29,500,000**, labeled: "Values are stated for
underwriting purposes and are subject to completion of the renovation and stabilization of operations."

### Key count convention
The **hotel** is 50 keys today and 57 on completion of the renovation; the Dogwood Cove residence is the
**58th key**, operated as a whole-home suite at a $1,500 nightly rate and 35% occupancy ($191,625 a year from
stabilization, in the projections). **All per-key figures in every package are stated on 58 keys** — cost basis
$331,860 per key, total capitalization $300,070 per key. The marina is
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

## The packages

`package/` holds the three PDFs, one per tranche, with a manifest (`package/README.md`) stating the
isolation rule, the page map and the conventions applied across all three. **Send one package per
recipient; never cross-send.** `scripts/crosscheck.py` asserts, against the exported PDFs, that each
carries its own economics, carries none of the other two tranches', names no source document, uses
US spelling, states per-key figures on 58 keys, and — for the common equity package — shows no exit
level at which the recipient loses money.

```
python3 scripts/crosscheck.py     # 19 checks; exits non-zero on a failure
```

The v4 single-package set (`Wylder Tilghman Island - Recapitalization.pdf`, the LP Equity Summary
and the GP-LP Model v4) is superseded and kept for reference only. It does not reconcile with these
three and would disclose cross-tranche economics if sent alongside them.
`scripts/crosscheck-v4-superseded.py` checks that older set.

## Files
- `deck/Wylder Tilghman Island - Senior Debt.dc.html` — the senior debt package (28 slides)
- `deck/Wylder Tilghman Island - Preferred Equity.dc.html` — the preferred equity package
- `deck/Wylder Tilghman Island - Common Equity.dc.html` — the common equity package
- `deck/Wylder Tilghman Island - Recapitalization.dc.html` — the superseded v4 deck, kept as the
  source of the fifteen shared core pages that `v7_build.py` lifts
- `deck/deck-stage.js` — slide-shell web component (scaling, nav, print)
- `deck/support.js` — Design Component runtime
- `deck/_ds/tranche-group-design-system-.../colors_and_type.css` — design tokens + Aptos `@font-face`
- `dist/build-dist.py` — asset-optimizing distribution build for all three decks (see `dist/README.md`)
- `package/` — the three PDFs plus the manifest and the superseded v4 set
- `scripts/build/` — the package generator: `figs_v7.py` (model figures, all asserted), `v7_lib.py`
  (markup helpers and the shared-core extractor), `v7_common.py` (capital structure, sources and
  uses), `v7_pages.py` (total basis, returns grid), `v7_patch.py` (per-package edits to the two
  shared pages that carried tranche economics), `v7_tranche.py` (covers, terms, mechanics, returns,
  position, contacts), `v7_num.py` (renumbering), `v7_build.py` (assembly and leak audit)
- `scripts/crosscheck.py` — PDF verification; `scripts/scrub_model.py` — label scrub

> **Data note.** Capital, waterfall and return figures reconcile to the **10.28.26 financial
> model**; `scripts/build/figs_v7.py` asserts every one of them and foots the stack, the uses, the
> preferred roll-forward, the exit waterfall at all seven exit values, each tranche's
> basis / cash / profit / multiple, and the partnership tiers. Sources and uses balance to $0. Do
> not change numbers without an updated model.
>
> **Open items in the 10.28.26 model — resolve before distribution:**
>
> 1. **Loan Analysis rows 53–73 are stale.** They show preferred at $7,404,044 and common at $0 — the
>    pre-common-equity case. Sources and Uses is authoritative and is what the packages use. Fix or
>    delete those rows before the model goes to anyone.
> 2. **"Indicative pricing: SOFR + 500 bps" contradicts the model's own rate.** The spread is 821 bps
>    (3.79% + 8.21% = 12.00% all-in). The packages use 821.
> 3. **The kicker base is labeled "Net Proceeds less Senior and Pref"** but the arithmetic deducts only
>    the senior principal; the preferred balance comes out after the participations. The packages follow
>    the arithmetic, which foots at all seven exit values. Definitive documents must define "equity
>    value at exit" precisely, because the two readings differ by roughly $290,000 of participation at
>    the base case.
> 4. **Selling costs are 4.0%**, up from 2.0% in v4, and exclude Maryland transfer and recordation
>    taxes, which require local verification.
> 5. **Maryland mortgage recording tax and stub interest on the existing loan are budgeted at zero**
>    in sources and uses. Confirm at closing; both would come out of the $130,100 closing line.
> 6. **Year-one coverage is 0.94x** and is carried entirely by the twelve-month interest and carry
>    reserve. If the renovation runs past the twelve months the reserve funds, coverage has no other
>    source. The schedule runs November 1, 2026 to April 30, 2027 — six months against a twelve-month
>    reserve, so roughly six months of slack. Confirm that is acceptable to the senior lender.
> 7. **The LP loses money below roughly $21,000,000** and the partnership receives nothing below
>    $12,783,904. Neither figure appears in the common equity package, by instruction. The sponsor and
>    counsel should be aware of both; a subscription document will have to disclose the downside even
>    though the marketing package does not show those columns.
> 8. **The GP's 51% interest carries control, not just economics.** An LP contributing 63.64% of
>    partnership capital while holding a 49% interest needs the operating agreement to carry its
>    protections — major-decision consents, removal rights on a GP default, and the subordination
>    itself. The packages present the economics; counsel must paper the governance, including the tax
>    allocation of a 50% residual share on 36.36% of the capital.
> 9. **Three separate investors will eventually see each other's terms** at closing, in the
>    intercreditor and the operating agreement. The isolation here is a marketing-stage measure, not a
>    confidentiality undertaking — it keeps each party from negotiating against another's pricing
>    during the raise.
