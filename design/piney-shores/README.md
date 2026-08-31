# Piney Shores Resorts — Debt Offering Memorandum

A 23-slide lender package for **Piney Shores Resorts**, 8350 Piney Shores Drive,
Conroe, TX 77304 — a 70-unit lakefront multifamily asset on Lake Conroe. The
deck presents a **$10,085,769 bridge loan request** at 75% loan-to-cost to
prospective capital sources on behalf of Brookside Equities Inc., arranged by
The TRANCHE Group at Marcus & Millichap Capital Corporation.

This is a standalone presentation artifact. It has no build step, no npm
dependencies, and no relationship to the `cre-pipeline` React app it lives
beside — it is a self-contained deck that runs from this directory.

## Viewing it

```bash
cd design/piney-shores
python3 -m http.server 8099
# open http://127.0.0.1:8099/deck.html
```

Opening `deck.html` directly off the filesystem also works, with one
degradation: browsers block `cssRules` access on `file://` stylesheets, so the
thumbnail rail renders its slide clones without the deck's typography. Serve it
over HTTP and the rail is correct.

| Key | Action |
|---|---|
| `←` `→` · `PgUp` `PgDn` · `Space` | Advance and reverse |
| `Home` `End` | First and last slide |
| number keys | Jump to slide |
| `R` | Reset to slide 1 |
| `Ctrl`/`Cmd` + `P` | Print — one landscape page per slide |

The thumbnail rail down the left edge takes a click to jump, a drag to reorder,
and a right-click for skip / move / duplicate / delete. Drag its right edge to
resize; the width persists to `localStorage`. Speaker notes ride on each
`<section data-speaker-notes>`, so a note stays with its slide through a
reorder.

`deck.html#7` opens directly on slide 7.

## Exporting to PDF

`Ctrl`/`Cmd` + `P` → *Save as PDF*, landscape, margins none, background
graphics on. The component injects `@page { size: 1920px 1080px; margin: 0 }`,
so each slide becomes exactly one 20″ × 11.25″ page with no scaling artifacts.

Headless, from this directory with the server running:

```bash
chromium --headless --no-pdf-header-footer \
  --print-to-pdf=Piney_Shores_Debt_Package.pdf \
  --virtual-time-budget=15000 \
  http://127.0.0.1:8099/deck.html
```

Verified output: 23 pages, uniform 1440 × 810 pt MediaBox, ~1.4 MB.

## Files

```
design/piney-shores/
├── deck.html        the deck — 23 slides, all layout and copy
├── tokens.css       design tokens; every var(--*) in the deck resolves here
├── deck-stage.js    slide shell: scaling, nav, rail, notes, print
├── assets/          photography and brand marks
├── fonts/           drop the Aptos TTFs here (see fonts/README.md)
└── tools/
    └── generate-placeholder-assets.py   regenerates everything in assets/
```

### `deck.html`

The 23 `<section>` elements are lifted **verbatim** from the handoff's
`Piney Shores Debt Package.dc.html`. Copy is client-approved capital-markets
language and every figure is reconciled against the source financial model, so
nothing here was re-typeset, re-coloured, or re-worded.

What changed is only the shell. The original was a Claude Design document
depending on a runtime (`support.js`, `<x-dc>`, `<helmet>`, `<x-import>`) that
was not part of the handoff. That wrapper is replaced by a plain
`<deck-stage width="1920" height="1080">` mount and two `<script>`/`<link>`
tags — so the deck now runs anywhere, with nothing to install.

### `deck-stage.js`

Extracted **verbatim** from the handoff's `_ds_bundle.js`
(`slides/deck-stage.js`, sourceHash `d8d952171670`). Only the design-system
IIFE wrapper and its error-reporting `try`/`catch` were stripped; the component
source is unmodified. It turned out to be fully self-contained — no
design-system globals, no runtime — so reusing it gives exact behavioural
fidelity for scaling, navigation, the rail, notes, and print, rather than an
approximation of them.

### `tokens.css`

A **reconstruction**. The authoritative `colors_and_type.css` was not in the
handoff bundle. Token *names* are taken verbatim from the design system's
adherence config (`_adherence.oxlintrc.json` → `x-omelette.tokens`); token
*values* are the literals documented in the handoff README and the design-system
README. Every `var(--*)` the deck references resolves.

Three values needed a judgement call, all internally consistent with the
documented system:

- **`--tier-*`** — the design-system README describes the tier ramp as
  navy → blue-gray → warm brass → orange, senior to equity. The Cover and
  Contact strata bands run top-down `#F0720E` → `#957551` → `#456EAB` →
  `#032D67` → `#001D4A`, which is that ramp inverted (equity on top). The
  tokens are assigned to match.
- **`--mm-orange-700`** is `#C0631C`, the "Best Comp" tag text — the darkest
  orange in the deck, which is what a `700` step should be. The handoff's
  "Orange Deep" `#F0720E` is the topmost strata band and lives at
  `--tier-equity`, where it is actually used.
- **`--mm-navy`** stays the `#002F6C` anchor (PMS 295) with the ramp running
  `900` dark → `050` light around it, so `--mm-navy-900` is Navy Deep
  `#001A3D` and `--mm-navy-050` is Wash `#EEF2F8`.

If the real `colors_and_type.css` is recovered, drop it in place of this file —
the token names are the contract.

## Assets

Two different things live in `assets/`, and the difference matters.

**Recreated.** `mmcc-white.png` and `mmcc-blue.png` reproduce the Marcus &
Millichap Capital Corporation lockup — "Marcus & Millichap" over a rule with
"Capital Corporation" beneath, the wordmark-rule motif the whole system is
built on. The mark is typographic, so it reproduces faithfully from type. It is
still Marcus & Millichap property: **in production, source it from the MMCC
brand package** rather than from this directory.

**Stand-ins.** The client photography was not included in the handoff. Every
other file in `assets/` is a generated placeholder at the exact pixel
dimensions its layout expects, carrying an on-image marker naming the file it
replaces — nothing silently passes for real asset photography. No likeness is
synthesized for either headshot; both are initials tiles.

| File | Slide | Status |
|---|---|---|
| `mmcc-white.png` | Cover, Contact | Recreated from type |
| `mmcc-blue.png` | *(unreferenced; kept for light-surface use)* | Recreated from type |
| `aerial-lake.jpg` | Cover, Site Context | Stand-in |
| `presidential-building.jpg` | Property & Amenities | Stand-in |
| `pool-aerial.jpg`, `pool-ground.jpg` | Property & Amenities | Stand-in |
| `registration.jpg` | Property & Amenities | Stand-in |
| `michael-bastan.png` | Sponsorship | Stand-in |
| `bradley-buzil.jpg` | Contact | Stand-in |

**To swap in the real images:** drop each file into `assets/` under the same
name. Nothing in `deck.html` needs editing. Regenerate the stand-ins any time
with `python3 tools/generate-placeholder-assets.py` (Chromium required; Pillow
optional, for real JPEG encoding).

## Fonts

The deck is a single-family system on **Aptos**. The TTFs are Microsoft
property and are not redistributed here, so `tokens.css` declares each face as
`local()` first and `url("fonts/…")` second:

- On any machine with **Microsoft 365 installed, the deck already renders in
  real Aptos** — `local()` finds it, no files needed.
- Otherwise, drop the TTFs into `fonts/` (names in `fonts/README.md`).
- Failing both, the deck falls back to a humanist sans with close metrics. It
  reads correctly; the figures just aren't in Aptos Mono.

## Open items carried over from the handoff

Flagged rather than resolved, because both are deal-team decisions:

1. **Target funding date** reads "45 Days From Term Sheet" as a placeholder.
   The original March 13, 2026 date has passed and no replacement was supplied.
2. **Refinance vs. acquisition framing.** The Sources & Uses net-funding block
   retires a $5,736,500 existing first trust deed, which makes this a
   refinance. Slides 3–4 describe an $8,160,000 purchase price and a 25% equity
   contribution, per the model's total-capitalization view. Both views come
   from the model and are internally consistent, but the narrative framing
   should be confirmed.

Two data notes from the handoff, unchanged here:

- The model's Condo-Sale-Comps tab prices the subject at $267,143/unit
  ($18.7M sellout) while Loan-Analysis says $262,000 ($18,340,000). **The deck
  uses $262,000 throughout.** Resolve in the model before generating from it.
- The sponsor summary's 11.9% debt yield, 1.60x DSCR, 53% LTV and $18.7M exit
  against a $6,120,000 loan belong to an earlier sizing and contradict the
  current request. **They are deliberately excluded — do not reintroduce them.**

## If this becomes a generated deck

Every figure traces to `Piney Shores - Financials - 8.30.26.xlsx`, which was
not part of the handoff. The binding table in the original handoff README maps
each figure to its model cell — loan amount to Loan-Analysis, the Sources &
Uses blocks to Sources-and-Uses, the condo sellout to Condo-Presales, and so
on. That table is the contract to build against if the layouts are ever
templatized and bound to a deal record.
