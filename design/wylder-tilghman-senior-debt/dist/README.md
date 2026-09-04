# Distribution build

`Wylder-Tilghman-Senior-Debt-Financing.pdf` — 2.2 MB, 15 pages, 20 × 11.25 in (16:9),
one slide per page. Text stays live (selectable and searchable); it is not
rasterised.

This is a derived artifact. The source of truth is `../deck/`, which keeps the
full-resolution masters untouched.

## How it was produced

The 23 MB first cut was not a PDF problem — it was the source imagery:

- Five `.png` files were photographs carrying a fully opaque alpha channel
  (verified: alpha range 255–255, zero non-opaque pixels). PNG is the wrong
  container for photographs and the alpha was dead weight.
- `wt-suite.jpg` was a 4032 × 3024 phone original (6.9 MB) rendering into a
  455 × 152 thumbnail; `buzil.jpg` was 2384 × 3040 for a 106 × 106 headshot.

Each image's display box was measured from the live render at 1920 × 1080, then
resized to exactly what the canvas needs — 2× for small images so thumbnails and
headshots stay crisp when zoomed — and re-encoded to JPEG q84. Assets totalled
24.67 MB before, 1.73 MB after (−93%).

The two full-bleed hero aerials keep their **native resolution**; their saving is
entirely PNG → JPEG, with no pixels lost. `mmcc-2018-white.png` is the only asset
with genuine transparency (81% non-opaque), so it stays PNG.

## Verification

- 11 of 15 slides render byte-identical to the master; the four photo slides
  measure 35.8–43.9 dB PSNR against it (visually indistinguishable).
- Images embed as `/DCTDecode` at the intended resolutions; the logo stays
  `/FlateDecode` with its alpha intact.

## Rebuilding

`build-dist.py` regenerates the optimised asset set into a scratch copy of
`../deck/`. Serve that copy over a static server and print it to PDF at
1920 × 1080 (the `deck-stage` shell lays out one slide per page under
`@media print`). Re-measure the display boxes first if the layout changes.
