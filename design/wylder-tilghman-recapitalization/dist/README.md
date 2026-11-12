# Distribution build

The nine decks export to `../package/` — about 3.1 MB each, 20 × 11.25 in
(16:9), one slide per page (30 for the kicker package, 29 for the lender-facing set and the equity packages):

- `Wylder Tilghman Island - Senior Debt.pdf`
- `Wylder Tilghman Island - Senior Debt - 8M Request.pdf`
- `Wylder Tilghman Island - Senior Debt - 10M Request.pdf`
- `Wylder Tilghman Island - Senior Debt - 11M Request.pdf`
- `Wylder Tilghman Island - Senior Debt - 12.5M Request.pdf`
- `Wylder Tilghman Island - LP Recapitalization.pdf` (29 pages)
- `Wylder Tilghman Island - Preferred Equity.pdf`
- `Wylder Tilghman Island - Common Equity.pdf`
- `Wylder Tilghman Island - Marina Valuation.pdf` (9 pages)

Text stays live (selectable and searchable); it is not rasterized.

This is a derived artifact. The source of truth is `../deck/`, which keeps the
full-resolution masters untouched.

## How it was produced

The first cut was not a PDF problem — it was the source imagery:

- Five `.png` files were photographs carrying a fully opaque alpha channel
  (verified: alpha range 255–255, zero non-opaque pixels). PNG is the wrong
  container for photographs and the alpha was dead weight.
- `wt-suite.jpg` was a 4032 × 3024 phone original (6.9 MB) rendering into a
  766 × 654 hero and a 455 × 128 thumbnail; `buzil.jpg` was 2384 × 3040 for a
  106 × 106 headshot.

Each image's display box is measured from the live render at 1920 × 1080, then
resized to exactly what the canvas needs — 2× for small images so thumbnails and
headshots stay crisp when zoomed, 1.5× for mid-size — and re-encoded to JPEG q84.
Assets totaled 25.33 MB before, 2.33 MB after (−91%), shared across all nine decks.

The two full-bleed hero aerials keep their **native resolution**; their saving is
entirely PNG → JPEG, with no pixels lost. `mmcc-2018-white.png` is the only asset
with genuine transparency (81% non-opaque), so it stays PNG.

## Rebuilding

```
python3 ../scripts/build/v7_loans.py   # regenerate all six decks first, if the content changed
python3 build-dist.py                 # writes ./_dist-deck
cd _dist-deck && python3 -m http.server 8732
# then print each of
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Senior%20Debt.dc.html
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Senior%20Debt%20-%208M%20Request.dc.html
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Senior%20Debt%20-%2010M%20Request.dc.html
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Senior%20Debt%20-%2011M%20Request.dc.html
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Preferred%20Equity.dc.html
#   http://127.0.0.1:8732/Wylder%20Tilghman%20Island%20-%20Common%20Equity.dc.html
# to PDF at 1920x1080, pages 1-30 (1-29 for the lender-facing set)
python3 ../scripts/crosscheck.py      # verify the exported PDFs
```

`build-dist.py` rewrites the asset references in all nine decks and drops any
other `.dc.html` (the superseded v4 deck) from the distribution copy.

`build-dist.py` regenerates the optimized asset set into a scratch copy of
`../deck/`. Serve that copy over a static server and print it to PDF at
1920 × 1080 (the `deck-stage` shell lays out one slide per page under
`@media print`).

**`SPEC` in `build-dist.py` is measured from the live render.** If the layout
changes, re-measure rather than guessing — a stale entry silently degrades an
image. For each `<img>`, read `getBoundingClientRect()` and `objectFit` at a
1920 × 1080 stage and take the largest box each asset is used at.
