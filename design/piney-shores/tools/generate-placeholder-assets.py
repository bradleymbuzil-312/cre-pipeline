#!/usr/bin/env python3
"""
Generate the deck's image assets.

Two different things happen here, and the distinction matters:

  * The MMCC wordmark is *recreated*. The mark is typographic — "Marcus &
    Millichap" over a rule, with "Capital Corporation" beneath it — so it can
    be reproduced faithfully from type. It is still Marcus & Millichap
    property: in production, source it from the MMCC brand package.

  * Everything else is a *stand-in*. The client photography was not included
    in the handoff. Each stand-in renders at the exact pixel dimensions its
    layout expects and carries a corner marker naming the file it replaces,
    so nothing silently passes for real asset photography.

Drop the real files into ../assets/ under the same names and every reference
resolves with no edits to deck.html.

Usage:  python3 tools/generate-placeholder-assets.py
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("google-chrome") or "",
]

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

NAVY_DEEP = "#001A3D"
NAVY = "#002F6C"
ORANGE = "#E87722"
GHOST = "#8FA3BF"

# The marker that keeps a stand-in honest about being a stand-in.
MARKER = """
<div style="position:absolute;right:0;bottom:0;padding:14px 18px;
            font-family:'Liberation Sans',Arial,sans-serif;font-weight:700;
            font-size:{fs}px;letter-spacing:.16em;text-transform:uppercase;
            color:rgba(255,255,255,.62);background:rgba(0,26,61,.55);
            border-top:1px solid rgba(255,255,255,.18);
            border-left:1px solid rgba(255,255,255,.18);">
  Placeholder · {name}
</div>
"""


def page(width, height, body, background="#001A3D"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
      html,body{{margin:0;padding:0;width:{width}px;height:{height}px;overflow:hidden;}}
      body{{background:{background};position:relative;}}
    </style></head><body>{body}</body></html>"""


def caption(text, sub, fs=44, subfs=17):
    return f"""
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                align-items:center;justify-content:center;text-align:center;
                font-family:'Liberation Sans',Arial,sans-serif;padding:0 8%;">
      <div style="font-weight:700;font-size:{fs}px;letter-spacing:.04em;
                  color:rgba(255,255,255,.90);line-height:1.15;">{text}</div>
      <div style="margin-top:18px;font-weight:700;font-size:{subfs}px;
                  letter-spacing:.22em;text-transform:uppercase;
                  color:{GHOST};">{sub}</div>
    </div>"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    sys.exit("No Chromium binary found — set one in CHROME_CANDIDATES.")


def transcode_jpeg(png, out, quality=88):
    """PNG -> JPEG, so each file is what its extension says it is; these get
    swapped for real photography one file at a time.

    Pillow is a generation-time convenience only — the deck itself has no
    dependencies. Without it the PNG bytes are written under the .jpg name;
    browsers sniff content type, so the deck still renders correctly.
    """
    try:
        from PIL import Image
    except ImportError:
        print(f"    (Pillow not installed — writing PNG bytes as {out.name};"
              f" `pip install Pillow` for a real JPEG)")
        shutil.copy(png, out)
        return
    with Image.open(png) as im:
        im.convert("RGB").save(out, "JPEG", quality=quality,
                               subsampling=0, optimize=True)


def shoot(chrome, html, out, width, height, transparent=False):
    """Render an HTML string to a PNG or JPEG at exactly width x height."""
    with tempfile.TemporaryDirectory() as td:
        src = pathlib.Path(td) / "page.html"
        src.write_text(html, encoding="utf-8")
        png = pathlib.Path(td) / "shot.png"
        cmd = [
            chrome, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={png}",
        ]
        if transparent:
            cmd.append("--default-background-color=00000000")
        cmd.append(src.as_uri())
        subprocess.run(cmd, check=True, capture_output=True)

        out.parent.mkdir(parents=True, exist_ok=True)
        if out.suffix.lower() in (".jpg", ".jpeg"):
            # Chromium only writes PNG, so transcode to a real JPEG — the
            # file should be what its extension says it is, since these get
            # swapped for real photography one file at a time.
            transcode_jpeg(png, out)
        else:
            shutil.copy(png, out)
    print(f"  {out.name}  {width}x{height}")


# --------------------------------------------------------------------------
# 1 · MMCC wordmark — recreated from type, transparent background
# --------------------------------------------------------------------------
def wordmark(chrome, color, out, pad=28):
    """The MMCC lockup: "Marcus & Millichap" over a rule, with "Capital
    Corporation" beneath — the wordmark-rule motif the whole system is built
    on. The rule stretches to the width of the longer line.

    Rendered onto a deliberately oversized canvas and then cropped to the
    ink: Chromium enforces a minimum window height, so a short canvas
    silently clips the descenders off the bottom line. Cropping to the alpha
    bounding box also makes the output tight, so `height:52px;width:auto` in
    the deck lands the lockup at its true proportions.
    """
    body = f"""
    <div style="position:absolute;inset:0;display:flex;align-items:center;
                justify-content:center;">
      <div style="display:inline-flex;flex-direction:column;align-items:stretch;
                  font-family:'Liberation Serif','Times New Roman',Georgia,serif;
                  color:{color};text-align:center;">
        <div style="font-size:104px;line-height:1.22;white-space:nowrap;">
          Marcus <span style="font-style:italic;">&amp;</span> Millichap
        </div>
        <div style="height:4px;background:{color};margin:2px 0 6px;"></div>
        <div style="font-size:72px;line-height:1.26;white-space:nowrap;">
          <span style="font-style:italic;">C</span>apital
          <span style="font-style:italic;">C</span>orporation
        </div>
      </div>
    </div>"""
    shoot(chrome, page(1400, 700, body, "transparent"), out, 1400, 700,
          transparent=True)
    crop_to_ink(out, pad)


def crop_to_ink(png, pad):
    """Trim a transparent PNG to its alpha bounding box plus even padding."""
    try:
        from PIL import Image
    except ImportError:
        return
    with Image.open(png) as im:
        im = im.convert("RGBA")
        box = im.getchannel("A").getbbox()
        if not box:
            return
        l, t, r, b = box
        l, t = max(0, l - pad), max(0, t - pad)
        r, b = min(im.width, r + pad), min(im.height, b + pad)
        im.crop((l, t, r, b)).save(png)
    with Image.open(png) as im:
        print(f"    cropped to {im.width}x{im.height}")


# --------------------------------------------------------------------------
# 2 · Aerial — an abstract lake/treeline field, not a fake photograph.
#     Composed so the Cover's 94%→28% navy scrim reads correctly across it.
# --------------------------------------------------------------------------
def aerial(chrome, out):
    body = f"""
    <div style="position:absolute;inset:0;background:
      linear-gradient(#8FB6DE 0%, #B9D2EC 26%, #CFE0F0 33%, #CFE0F0 34%,
                      #6F8E6A 35%, #55764F 39%,
                      #3D6E9B 42%, #2C5C8C 62%, #24507E 70%,
                      #5C7A56 72%, #6E8A5E 84%, #7C8F63 100%);"></div>
    <div style="position:absolute;left:0;right:0;top:41%;height:31%;
      background:linear-gradient(90deg,rgba(255,255,255,.10),rgba(255,255,255,0) 40%),
                 radial-gradient(ellipse at 30% 40%,rgba(255,255,255,.16),transparent 60%);"></div>
    <div style="position:absolute;left:0;right:0;top:34%;height:8%;
      background:repeating-linear-gradient(90deg,
        rgba(40,70,45,.34) 0 26px, rgba(40,70,45,0) 26px 62px);"></div>
    <div style="position:absolute;left:0;right:0;top:72%;bottom:0;
      background:repeating-linear-gradient(90deg,
        rgba(60,80,50,.26) 0 44px, rgba(60,80,50,0) 44px 108px),
        repeating-linear-gradient(0deg,
        rgba(0,0,0,.08) 0 70px, rgba(0,0,0,0) 70px 160px);"></div>
    {caption("Lake Conroe — Aerial", "client photography to be supplied", 58, 19)}
    {MARKER.format(name="aerial-lake.jpg", fs=15)}"""
    shoot(chrome, page(2000, 1333, body), out, 2000, 1333)


# --------------------------------------------------------------------------
# 3 · Property photography stand-ins
# --------------------------------------------------------------------------
def property_shot(chrome, name, title, w, h, out):
    body = f"""
    <div style="position:absolute;inset:0;background:
      linear-gradient(135deg,#0B2A50 0%,#123763 46%,#0A2447 100%);"></div>
    <div style="position:absolute;inset:0;
      background:repeating-linear-gradient(135deg,
        rgba(255,255,255,.030) 0 2px, rgba(255,255,255,0) 2px 26px);"></div>
    <div style="position:absolute;left:0;top:0;bottom:0;width:8px;
      background:{ORANGE};"></div>
    {caption(title, "client photography to be supplied")}
    {MARKER.format(name=name, fs=14)}"""
    shoot(chrome, page(w, h, body), out, w, h)


# --------------------------------------------------------------------------
# 4 · Portrait stand-ins — initials tile, never a synthesized likeness
# --------------------------------------------------------------------------
def portrait(chrome, name, initials, full, w, h, out):
    body = f"""
    <div style="position:absolute;inset:0;background:
      linear-gradient(160deg,#123763 0%,#0B2A50 60%,#08203E 100%);"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                align-items:center;justify-content:center;
                font-family:'Liberation Sans',Arial,sans-serif;text-align:center;">
      <div style="font-weight:700;font-size:{int(w*0.30)}px;letter-spacing:.02em;
                  color:rgba(255,255,255,.88);line-height:1;">{initials}</div>
      <div style="margin-top:{int(w*0.055)}px;font-weight:700;
                  font-size:{max(11,int(w*0.052))}px;letter-spacing:.18em;
                  text-transform:uppercase;color:{GHOST};">{full}</div>
      <div style="margin-top:{int(w*0.028)}px;font-weight:700;
                  font-size:{max(9,int(w*0.040))}px;letter-spacing:.14em;
                  text-transform:uppercase;color:rgba(255,255,255,.42);">
        Headshot to be supplied</div>
    </div>"""
    shoot(chrome, page(w, h, body), out, w, h)


def main():
    chrome = find_chrome()
    ASSETS.mkdir(parents=True, exist_ok=True)
    print("Recreated brand marks:")
    wordmark(chrome, "#FFFFFF", ASSETS / "mmcc-white.png")
    wordmark(chrome, NAVY, ASSETS / "mmcc-blue.png")

    print("Stand-ins:")
    aerial(chrome, ASSETS / "aerial-lake.jpg")
    property_shot(chrome, "presidential-building.jpg",
                  "Presidential Residential Building", 1600, 1200,
                  ASSETS / "presidential-building.jpg")
    property_shot(chrome, "pool-aerial.jpg",
                  "Resort Pool &amp; Sun Deck — Aerial", 1200, 1600,
                  ASSETS / "pool-aerial.jpg")
    property_shot(chrome, "pool-ground.jpg",
                  "Outdoor Pool &amp; Activity Center", 1200, 800,
                  ASSETS / "pool-ground.jpg")
    property_shot(chrome, "registration.jpg",
                  "Registration, Grill &amp; Commercial", 1200, 800,
                  ASSETS / "registration.jpg")
    portrait(chrome, "michael-bastan.png", "MB", "Michael Bastan", 600, 600,
             ASSETS / "michael-bastan.png")
    portrait(chrome, "bradley-buzil.jpg", "BB", "Bradley M. Buzil", 528, 528,
             ASSETS / "bradley-buzil.jpg")
    print("\nDone. Replace any file in assets/ with the real image, same name.")


if __name__ == "__main__":
    main()
