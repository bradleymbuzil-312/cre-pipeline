# Handoff: Wylder Hotel Tilghman Island — Preferred Equity Investment Deck

## Overview
A 15-slide institutional investor presentation soliciting a **$7,276,056 preferred equity investment** in the recapitalization and renovation of the Wylder Hotel Tilghman Island (Talbot County, MD). The audience is a prospective preferred-equity investor. Advisor: Bradley M. Buzil, The TRANCHE Group at Marcus & Millichap Capital Corporation (MMCC).

## About the Design Files
The files in `deck/` are a **design reference built in HTML** — a working prototype of the intended look, content, and slide flow, not production code to ship as-is. The task is to **recreate this deck in the target environment** using its established patterns. If the goal is a web app, rebuild the slides as components in the codebase's framework (React/Vue/etc.). If the goal is a distributable presentation, the HTML itself is already the deliverable and can be exported to PDF/PPTX from the design tool.

The deck is a single self-contained Design Component (`.dc.html`) rendered through a lightweight slide-shell web component (`deck-stage.js`) and a runtime (`support.js`). All styling is **inline** on each element; the only shared stylesheet is the design system's `colors_and_type.css` (design tokens + `@font-face`).

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, copy, and figures. Recreate pixel-for-pixel using the exact tokens below. Every dollar figure is reconciled to the source financial model and the term sheet dated 8/24/26; do not alter numbers.

## How to Run the Reference
Open `deck/Wylder Tilghman Island - Preferred Equity Investment.dc.html` through a local static server (relative paths to `_ds/`, `assets/`, `deck-stage.js`, `support.js` must resolve). Arrow keys / on-screen nav move between slides; the shell handles scaling, a thumbnail rail, speaker notes, and print-to-PDF (one page per slide).

Canvas is **1920×1080** per slide (16:9).

## Design Tokens
Sourced from `deck/_ds/.../colors_and_type.css`. Use these exact values.

**Color**
- `--mm-navy-900` `#001A3D` — deepest navy; dark-slide backgrounds, headline ink on cream
- `--mm-navy` `#002F6C` — primary brand navy (PMS 295); rules, totals
- `--mm-navy-700` `#1A4280`, `--mm-navy-300` / `--mm-navy-100` — lighter navy tints for secondary text on dark
- `--mm-orange` `#E87722` — accent; eyebrows, key figures, the preferred tranche
- `--mm-orange-700` `#C0631C`, `--mm-orange-100` `#FBE3CF`
- `--paper` `#FAF8F4` — warm cream; default light-slide surface
- `--ink-900` `#0E1116`, `--ink-700` `#2A2F37`, `--ink-500` `#5A6068`, `--ink-400` — body text on cream
- `--hairline` `rgba(0,26,61,.12)` — 1px structural dividers
- Capital-stack tier colors used literally: senior `#032D67`, preferred `#E87722` (accent), common/blue-gray `#456EAB`, brass `#957551`

**Typography** — Microsoft **Aptos** family, loaded from the design system `fonts/` via `@font-face` (no CDN).
- `--font-display` "Aptos Display" — H1/H2 headlines (700), italic taglines
- `--font-body` "Aptos" — body copy, ledes, captions
- `--font-condensed` "Aptos Narrow" — eyebrows, ALL-CAPS labels, table headers (700, letter-spacing .14–.30em, uppercase)
- `--font-mono` "Aptos Mono" — all currency, percentages, dates, phone (tabular-nums)
- `--font-serif` "Aptos Serif" — used only for the "wylder" wordmark on the title slide

**Type sizes in use (px, at 1920×1080):** title H1 104; section H2 50–56; big stat/hero figures 96–104; stat-grid values 54; table body 17–22; eyebrow 17; labels 13–15.

**Running footer:** every interior slide (2–14) carries a footer rule — `Wylder Hotel Tilghman Island · Preferred Equity Investment` left, `MMCC · The TRANCHE Group` right — in `--font-condensed` 14px/700, `.2em` tracking, uppercase, `--ink-400` on light slides and `rgba(255,255,255,.38)` on dark. The title and contact slides carry their own footers instead.

**Rules & borders:** section headers sit above a `1px solid var(--mm-navy)` rule; tables use 2px navy top/bottom borders with 1px `--hairline` interior lines. Corners 0–2px (printed feel, not app-like). No gradients except the photo-overlay scrims on dark hero slides. No shadows except soft photo scrims.

**Motif:** a vertical/horizontal "strata" bar (stacked orange `#F0720E` + blue `#456EAB` segments) on the title, asset, sponsor, terms and contact slides — the capital-stack metaphor. Every instance is split **44.7% orange / 55.3% blue**, matching the preferred/senior share of total capitalisation.

## Screens / Views (15 slides)
Light slides = `--paper` background, navy ink. Dark slides = `--mm-navy-900` background, white text. Each slide is 1920×1080, `box-sizing:border-box`, ~76–96px padding.

1. **Title** (dark, full-bleed photo `wt-aerial-spring.png` + navy gradient scrim). Eyebrow "PREFERRED EQUITY INVESTMENT · $7,276,056"; H1 "Wylder Hotel Tilghman Island."; italic tagline. Top bar = MMCC white logo + "CONFIDENTIAL · INVESTMENT PROPOSAL". Footer = Bradley Buzil / date / "wylder" serif wordmark. Right-edge strata bar.
2. **The Opportunity** (light). H2 "A 17% preferred return, behind one senior loan." 8-tile stat grid (4×2), bordered: Preferred Investment $7.28M (44.7% of cap · $127,650/key); Preferred Return 17.00% (10% current / 7% accrued); Minimum Multiple 1.20x (floor $8.73M); Profit Participation 10.0% (no hurdle); Projected Multiple 1.55x (before participation); Term 3 yrs (coterminous + two 12-mo ext.); Senior Loan Ahead $9.00M (42.9% LTV); Last-Dollar Basis 77.5% (of $21.0M as-is).
3. **The Asset** (light, split). Left 44% = full-height photo `wt-pier.png` with strata edge. Right = H2 "A waterfront resort on the Chesapeake.", lede, 2×2 facts (Keys 50→57; Site 8.10 ac / 352,759 SF; Positioning Upper Upscale select-service; Location Tilghman, MD), and two thumbnails (`wt-suite.jpg`, `wt-pool.png`).
4. **The Sponsor** (light, split). Left content = H2 "A hands-on owner-operator, fully aligned.", ownership narrative (21551 Tilghman Investors LLC / John Flannigan / Wylder Hotels / Wylder Eastern Shore Mgmt.), 2×2 facts, and four numbered "Sponsor Commitments to the Preferred" (completion & cost-overrun guaranty; full carry guaranty; recourse carve-out & environmental indemnity; $10M net-worth covenant), closing on "overruns dilute common equity, not the preferred." Right = full-height photo panel `wt-lobby.png` with strata edge.
5. **Wylder Hotels & Track Record** (light). H2 "A proven operator, and the brand he built." Left = `wylder Hotels` wordmark, brand blurb, three-property portfolio (Tilghman Island MD 50→57 keys Est. 2017; Hope Valley CA 30 cabins Est. 2019; Windham NY 110 keys ~$27M Est. 2022) + Recognition line (T+L #1 NY resort 2023; MICHELIN/SLH; Condé Nast 2018). Right = John Flannigan circular headshot (`flannigan.png`) + name/title + "3 decades", career timeline (Wylder Founder&CEO / Proper COO / JRK President / Ace NY Opening GM / earlier) + education line.
6. **Business Plan** (light). H2 "Closing a RevPAR gap the market has already proven." Left = three numbered value-creation levers (01 Reset the product $1.43M; 02 Add revenue streams $0.85M; 03 Lift demand through brand — SLH Yr 2); $3.0M / $52,684-per-key program. Right = RevPAR index 41.5% → ~70%, thesis, and two stats (NOI 2026→2028 = 2.2×; Value as-is→stab. $21→$28.5M).
7. **Historical & Proforma Financials** (light). H2 "Three years of history, three years of upside." Full-width table grouped Actual (2023/2024/2025) vs Proforma (2026/2027/2028), 2px navy divider before 2026; rows Occupancy 27/32/33 → 33/38/40%, ADR $312/291/265 → $288/395/415, RevPAR $83/92/87 → $96/150/166, Total revenue $3.48/3.81/3.79M → $4.27/6.02/6.71M, NOI $0.49/0.92/0.66M → $1.03/2.00/2.30M, NOI margin 14.0/24.0/17.6% → 24.0/33.3/34.3%. Takeaway strip: Historical NOI band $0.5M–$0.9M · Stabilized NOI $2.30M · RevPAR $87→$166.
8. **Capital Stack** (light). H2 "One senior loan ahead. Nothing beside it." Left = stacked bars top→bottom: Common Equity (blue #456EAB, "value cushion 22.5%"), Preferred Equity (orange, $7,276,056 / 44.7%), Senior Loan (navy #032D67, $9,000,000 / 55.3%), total $16,276,056. Right = narrative + attachment table (Senior last-$ $9.00M @ 42.9% LTV; Preferred last-$ $16.28M @ 77.5%; value cushion $4.72M / 22.5%).
9. **Preferred Terms** (dark). H2 "Three economics define the position." Three big-number columns: 17.00% (current 10% / accrued 7% / reserve $727,606); 1.20x (min dollars $8,731,268 / redemption any time / 2.00% origination); 10.0% (trigger sale / no hurdle / senior to common). Bottom strip: Term 3 yrs + 2×12-mo; Ranking senior to common; Default bump +5.00%; Break-up fee $25,000. Bottom strata bar.
10. **Return Profile** (light). H2 "A 1.55x base-case multiple, before participation." Left = pref accrual table (Year 1/2/3): beginning $7.28/7.79/8.33M, accrued 7% PIK $509/545/583K, ending $7.79/8.33/8.91M, current pay $728/779/833K. Right = Projected Multiple 1.55x, Hold 3 yrs, cumulative current pay $2,339,179, accrued balance at exit $8,913,482, total distributions $11,252,661, disclaimer.
11. **Downside Protection** (dark). H2 "Protected by value, cash, and control." Left = LTV table (As-is $21.0M: Sr 42.9% / Pref last-$ 77.5%; Completion $25.5M: 35.3% / 63.8%; Stabilization $28.5M: 31.6% / 57.1%) + highlighted callout "22.5% of as-is value" cushion. Right = three blocks: Cash ($727,606 pref reserve + $823,769 senior reserve), Control (approval rights, remove managing member, force sale, recognition agreement), Sponsor Alignment (completion/carry guaranties, $10M min net worth).
12. **Waterfall & Governance** (light). H2 "Paid before the sponsor, at every level." Left = Operating Cash Flow Waterfall (5 steps, pref current pay + accrued highlighted) and Capital Event Waterfall (5 steps, pref return / capital + min multiple / profit participation highlighted). Right = Approval Rights, Remedies on Default, Recognition Agreement paragraphs.
13. **Valuation & Comps** (light). H2 "Value supported by appraisal and market." Left = LWHA appraisal (As-is $21.0M/$420K; Completion $25.5M/$447K; Stabilization $28.5M/$500K; Job 26-NY-290, Michael Cline MAI, dated 5/15/26 eff 5/5/26). Right = per-key waterfront sale comps (Tilghman unrenov. $378K; Tilghman renovated $488K highlighted; St Michaels $1.00M; Montauk $577K; Fernandina Beach $410K).
14. **Sources & Uses** (light). H2 "Every dollar accounted for at close." Left = Sources (Senior at close $6.5M; future funding $2.5M; Preferred $7,276,056 highlighted; total $16,276,056) + Renovation detail ($52,684/key, itemized to $3,003,000). Right = Uses (payoff $10.25M; PIP $3.003M; senior reserve $823,769; pref reserve $727,606 highlighted; working capital $500K; closing/legal $438,400; senior orig 2.50% $225,000; MMCC broker $162,761; pref orig 2.00% $145,521 highlighted; total $16,276,056; balanced $0) + required-equity note.
15. **Next Steps / Contact** (dark, full-bleed `wt-aerial.png` + scrim). H2 "Available for review." Paragraph (acceptance by Sep 11, close on/before Sep 21, 2026). Stat strip: Preferred Investment $7,276,056 / Preferred Return 17.00% / Target Close Sep 21, 2026. Footer = Bradley headshot (`buzil.jpg`, 104×104, 2px radius, 1px white border) + name + "Senior Director · The TRANCHE Group" + cell `310.909.5473` + email `bradley.buzil@marcusmillichap.com`. Top strata bar.

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
- `deck/Wylder Tilghman Island - Preferred Equity Investment.dc.html` — the deck (all 15 slides, inline-styled)
- `deck/deck-stage.js` — slide-shell web component (scaling, nav, print)
- `deck/support.js` — Design Component runtime
- `deck/_ds/tranche-group-design-system-.../colors_and_type.css` — design tokens + Aptos `@font-face`
- `deck/_ds/.../fonts/` — Aptos font files
- `deck/assets/` — imagery and logo

> Data note: figures reconcile to the LCP/Preferred financial model and the term sheet dated 8/24/26. Return and hold-period figures are the model's base case and exclude the 10% sale profit participation (incremental upside). Do not change numbers without an updated model.
