#!/usr/bin/env python3
"""Build the distribution asset set for the Wylder Tilghman senior debt financing deck.

Copies ../deck to an output directory, resizes every image to the resolution its
display box actually needs, re-encodes photographs to JPEG, and repoints the
deck's src attributes. Leaves the masters in ../deck untouched.

    python3 build-dist.py /tmp/dist-deck

Then serve the output directory and print it to PDF at 1920x1080; deck-stage's
@media print rules lay out one slide per page.

SPEC below is measured from the live render. If the layout changes, re-measure
rather than guessing: for each <img>, read getBoundingClientRect() and
objectFit at a 1920x1080 stage.
"""
import os
import shutil
import sys

from PIL import Image

# asset -> (display box at 1920x1080, object-fit)
SPEC = {
    "wt-aerial-spring.png": ((1920, 1080), "cover"),
    "wt-aerial.png":        ((1920, 1080), "cover"),
    "wt-pier.png":          ((845, 1080), "cover"),
    "wt-lobby.png":         ((768, 1080), "cover"),
    "wt-suite.jpg":         ((766, 654), "cover"),   # hero on slide 07; thumbnail on 03
    "wt-pool.png":          ((455, 152), "cover"),
    "flannigan.png":        ((90, 90), "cover"),
    "buzil.jpg":            ((106, 106), "cover"),
    "mmcc-2018-white.png":  ((227, 60), "fill"),
}

# Only this one carries real transparency (81% non-opaque), so it stays PNG.
# The rest are photographs whose alpha is uniformly 255.
KEEP_PNG = {"mmcc-2018-white.png"}

JPEG_QUALITY = 84
SMALL_BOX_PX = 500      # below this width, supersample 2x so zoom stays clean
MID_BOX_PX = 1000       # 500-1000px: 1.5x, so hero photos survive zoom and print
DECK = "Wylder Tilghman Island - Senior Debt Financing.dc.html"


def build(src_deck, out_deck):
    if os.path.exists(out_deck):
        shutil.rmtree(out_deck)
    shutil.copytree(src_deck, out_deck)

    renames = {}
    before = after = 0

    for name, (box, fit) in SPEC.items():
        path = os.path.join(out_deck, "assets", name)
        before += os.path.getsize(path)
        im = Image.open(path)
        sw, sh = im.size
        bw, bh = box

        # cover and fill both need the larger of the two axis ratios; never upscale
        scale = max(bw / sw, bh / sh)
        boost = 2 if bw < SMALL_BOX_PX else (1.5 if bw < MID_BOX_PX else 1)
        scale = min(scale * boost, 1.0)
        target = (max(1, round(sw * scale)), max(1, round(sh * scale)))
        if target != (sw, sh):
            im = im.resize(target, Image.LANCZOS)

        if name in KEEP_PNG:
            im.save(path, "PNG", optimize=True)
            out = path
        else:
            out = os.path.join(out_deck, "assets", os.path.splitext(name)[0] + ".jpg")
            im.convert("RGB").save(
                out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
            )
            if out != path:
                os.remove(path)
                renames[name] = os.path.basename(out)
        after += os.path.getsize(out)
        print(f"  {name:24} {sw}x{sh} -> {target[0]}x{target[1]}")

    html = os.path.join(out_deck, DECK)
    with open(html, encoding="utf-8") as fh:
        s = fh.read()
    for old, new in renames.items():
        if f"assets/{old}" not in s:
            raise SystemExit(f"deck does not reference assets/{old}")
        s = s.replace(f"assets/{old}", f"assets/{new}")
    with open(html, "w", encoding="utf-8") as fh:
        fh.write(s)

    print(f"\nassets {before / 1048576:.2f} MB -> {after / 1048576:.2f} MB "
          f"({100 - after / before * 100:.0f}% smaller)")
    print(f"output: {out_deck}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "_dist-deck")
    build(os.path.join(here, os.pardir, "deck"), out)
