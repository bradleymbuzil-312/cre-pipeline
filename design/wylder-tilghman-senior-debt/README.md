# Handoff: Wylder Hotel Tilghman Island — Senior Debt Financing Deck

## Overview
A 15-slide institutional financing package supporting a **$12,600,000 senior loan** (first mortgage) from **New Day Commercial Capital** on the Wylder Hotel Tilghman Island (Talbot County, MD). The loan refinances the existing $10,714,782 loan, funds closing and origination costs, and returns $843,046 of cash to the sponsor. Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

The deck carries **no equity offering of any kind** — the capitalisation is the single first mortgage.

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

## Screens / Views (15 slides)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text. Each slide is
1920×1080, `box-sizing:border-box`, ~76–96px padding. Slides 2–14 carry the running footer.

1. **Title** (dark, full-bleed `wt-aerial-spring.jpg` + navy scrim). Eyebrow "SENIOR DEBT FINANCING · $12,600,000";
   H1 "Wylder Hotel Tilghman Island."; italic tagline. Top bar = MMCC white logo + "CONFIDENTIAL · FINANCING
   PROPOSAL". Footer = Bradley Buzil / date / "wylder" serif wordmark. Right-edge strata bar.
2. **The Financing** (light). H2 "One fixed-rate first mortgage, fully amortizing." 8-tile stat grid (4×2):
   Loan Amount $12.60M (100% of capitalisation · $221,053/key); All-In Rate 10.29% (4.54% UST + 5.75% spread);
   Term & Amortization 30 yrs; Annual Debt Service $1.36M; LTV at Close 60.0%; Stabilized DSCR 1.47x;
   Stabilized Debt Yield 15.9%; Sponsor Cost Basis $18.68M.
3. **The Asset** (light, split). Left 44% photo `wt-pier.jpg`. Right = H2, lede, 2×2 facts (Keys 50→57;
   Site 8.10 ac; Positioning Upper Upscale; Location Tilghman, MD) and two thumbnails.
4. **The Sponsor** (light, split). Ownership narrative (21551 Tilghman Investors LLC / John Flannigan /
   Wylder Hotels / Wylder Eastern Shore Mgmt.), 2×2 facts, and four numbered **Sponsor Commitments to the Lender**
   (completion & cost-overrun guaranty; full carry guaranty; recourse carve-out & environmental indemnity;
   $10M net-worth covenant), closing on the $2,000,000 of sponsor cash equity outside the project basis.
5. **Wylder Hotels & Track Record** (light). Brand blurb, three-property portfolio, John Flannigan bio and
   career timeline, Recognition line.
6. **Business Plan** (light). Three numbered value-creation levers ($1.43M / $0.85M / SLH Yr 2) against a
   $3,003,000 · $52,684-per-key programme. Right = RevPAR index 41.5% → ~70%, thesis, NOI and value stats.
7. **Historical & Proforma Financials** (light). Actual 2023/2024/2025 vs Proforma 2027/2028/2029.
   Occupancy 27/32/33 → 33/38/40%; ADR $312/291/265 → $330/395/415; RevPAR $83/92/87 → $109/150/166;
   Revenue $3.48/3.81/3.79M → $4.51/6.02/6.71M; NOI $0.49/0.92/0.66M → $1.26/2.00/2.30M;
   margin 14.0/24.0/17.6% → 28.0/33.3/34.3%.
8. **Capital Structure** (light). H2 "One first mortgage. Nothing beside it." Two proportional bars against the
   $21.0M Year-1 value: Value Above the Loan (blue, $8,400,000 / 40.0%) and Senior Loan (navy, $12,600,000 /
   60.0%). Right = narrative + LTV-by-basis table (Newmark as-is 61.8%; Yr1 60.0%; Yr2 49.4%; Yr3 44.2%).
9. **Senior Loan Terms** (dark). Three big-number columns: 10.29% (index 4.54% / spread 5.75% / fixed);
   30 yrs (debt service $1,359,403 / constant 10.789% / no IO); 60.0% max LTV (loan $12,600,000 / min DSCR 1.20x /
   prepay 1 yr: 5%). Bottom strip: lender, origination 4.00% + 1.00%, MMCC 1.00%, processing $10,100.
   Bottom strata bar.
10. **Debt Service Coverage** (light). 2027/2028/2029 table — NOI, debt service, net cash flow, DSCR, debt yield.
    Right = stabilized DSCR 1.47x and debt yield 15.9%, plus the Year-1 coverage note ($99,668 shortfall).
11. **Credit Protections** (dark). LTV-by-basis table plus a highlighted callout ($6.08M of cost above the loan),
    and three blocks: Basis, Amortization, Sponsor Support.
12. **Cost Basis & Sponsor Equity** (light). Total cost basis $18,679,659 (acquisition $12,714,782 /
    PIP $3,003,000 / other $2,961,877), basis per key $327,713 vs loan per key $221,053. Right = the eight-line
    $2,000,000 sponsor cash equity outside basis, plus 2021–2025 CapEx of $642,693.
13. **Valuation & Comps** (light). Newmark appraisal (as-is $20.40M / $377,778 per key on 54 keys;
    as-stabilized $27.80M / $487,719 per key on 57 keys) and the underwritten proforma values. Right = six
    East Coast waterfront sale comps plus weighted average ($396K/key) and median ($397K/key) of 11 sales.
14. **Sources & Uses** (light). Sources ($12,600,000 senior loan, $0 sponsor equity) and closing-cost detail;
    Uses (payoff $10,714,782; origination $504,000 + $126,000; closing $276,072; MMCC $126,000; processing
    $10,100; cash-out to sponsor $843,046), balanced to $0, plus the net-funding memo ($11,844,000 net proceeds,
    $1,119,118 to the borrower).
15. **Next Steps / Contact** (dark, full-bleed `wt-aerial.jpg` + scrim). Stat strip: Loan Amount $12,600,000 /
    All-In Rate 10.29% / Amortization 30 Years. Footer = Bradley headshot, name, "Senior Director · The TRANCHE
    Group", cell `310.909.5473`, email `bradley.buzil@marcusmillichap.com`. Top strata bar.

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
> Open items carried from the model: Year-1 (2027) DSCR is 0.93x against a 1.20x minimum, a $99,668 shortfall,
> and no interest reserve is funded in the sources and uses; the $12,600,000 loan is 60.0% of the $21.0M Year-1
> proforma value but 61.8% of the $20.4M Newmark as-is appraisal, above the 60% maximum LTV per the LOI; and the
> Newmark appraisal date and appraiser are not carried in the model, so slide 13 cites neither.
