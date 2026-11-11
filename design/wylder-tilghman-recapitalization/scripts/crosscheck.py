# -*- coding: utf-8 -*-
"""Verify the three capitalization packages.

Each package must (a) carry its own economics, (b) carry none of the other two tranches'
economics, (c) name no source document, and (d) in the common equity package, show no exit
level at which the recipient loses money.

    python3 scripts/crosscheck.py
"""
import re
import sys

import pymupdf

P = "/home/user/cre-pipeline/design/wylder-tilghman-recapitalization/package"
PKGS = {"senior": ("Senior Debt", f"{P}/Wylder Tilghman Island - Senior Debt.pdf", 29),
        "hm8": ("Senior Debt - 8M Request",
                f"{P}/Wylder Tilghman Island - Senior Debt - 8M Request.pdf", 28),
        "hm10": ("Senior Debt - 10M Request",
                 f"{P}/Wylder Tilghman Island - Senior Debt - 10M Request.pdf", 28),
        "hm11": ("Senior Debt - 11M Request",
                 f"{P}/Wylder Tilghman Island - Senior Debt - 11M Request.pdf", 28),
        "lp": ("LP Recapitalization",
               f"{P}/Wylder Tilghman Island - LP Recapitalization.pdf", 28),
        "pref": ("Preferred Equity", f"{P}/Wylder Tilghman Island - Preferred Equity.pdf", 28),
        "common": ("Common Equity", f"{P}/Wylder Tilghman Island - Common Equity.pdf", 28)}
LENDER = ["senior", "hm8", "hm10", "hm11"]
# total cost basis per key moves with the request, because the reserve and the fees are in it
BASIS_KEY = {"senior": "$331,860", "hm8": "$326,688", "hm10": "$331,860", "hm11": "$334,446",
             "lp": "$313,529", "pref": "$331,860", "common": "$331,860"}
NO_KICKER = ["hm8", "hm10", "hm11"]
# the debt packages are the same deal at different requests, so they are not "other tranches"
# to each other
OTHERS = {t: ([] if t == "lp" else ["pref", "common"] if t in LENDER
              else [o for o in ("senior", "pref", "common") if o != t]) for t in PKGS}
# The LP deck is a request for investment, not an offer. It may name the terms that are open
# ("preferred return", "promote", "residual split") but must carry no number for any of them,
# and none of the senior debt request detail.
LP_FORBID = [
    # the v4 deck's economics, which this one deliberately does not carry
    "12.0%", "2.0x", "20% IRR", "2.06x", "37.3%", "11.0%", "51% / 49%", "51%/49%",
    "$26,807,438", "$3,309,883", "$25,278,210", "$12,023,125", "$13,817,455", "$8,038,602",
    "Equity multiple", "Projected IRR", "GP share of cash",
    # "Preferred Return" is deliberately not listed: the deck names the term, with no rate.
    # the senior loan's request terms, which are being arranged separately
    # "+ 600" and "Interest-only" are not listed either: the normalizer strips separators,
    # so "600" matches inside any amount, and interest-only describes the modeled debt service
    # on page 13 rather than a term being requested.
    "SOFR", "$57,458", "Debt yield", "Debt service coverage",
    "Exit participation", "Net Funded Basis", "total cash received",
]
LP_REQUIRED = ["To be determined", "$13,255,085", "$20,255,085", "$18,184,701", "$0"]

# Letter-spaced condensed uppercase extracts as "S E N I O R", so compare on a stripped form.
norm = lambda t: re.sub(r"[^A-Za-z0-9.$%]", "", t).lower()

# ── each tranche's own economics: rate, fees, participation, returns
OWN = {
 "senior": ["$10,000,000", "12.00%", "SOFR", "8.21%", "3.79%", "interest-only",
            "$8,600,000", "$9,800,000", "$3,600,000", "5.00%", "$940,000",
            "$14,540,000", "$4,740,000", "1.48x", "15.6%", "57.46%", "46.73%"],
 "hm8": ["$8,000,000", "12.00%", "SOFR", "$6,880,000", "$960,000", "37.38%", "46.58%",
         "28.94%", "2.41x", "2.16x", "$18,947,882", "$326,688", "$5,674,878", "$3,500,000",
         "$17,174,878"],
 "hm10": ["$10,000,000", "12.00%", "SOFR", "$8,600,000", "$1,200,000", "46.73%", "57.46%",
          "23.15%", "1.93x", "1.73x", "$19,247,882", "$331,860", "$3,904,044", "$3,500,000",
          "$17,404,044"],
 "hm11": ["$11,000,000", "12.00%", "SOFR", "$9,460,000", "$1,320,000", "51.40%", "62.79%",
          "21.05%", "1.75x", "1.57x", "$19,397,882", "$334,446", "$3,018,628", "$3,500,000",
          "$17,518,628"],
 "pref": ["$3,904,044", "17.00%", "$3,825,963", "$1,931,666", "$3,714,944", "10.00%",
          "$1,880,000", "$7,526,610", "$3,700,647", "1.97x", "31.5%", "64.97%"],
 "lp": ["$13,255,085", "$12,989,984", "$7,000,000", "$20,255,085", "$18,184,701",
        "$2,070,384", "$228,536", "$313,529", "61.94%", "84.98%", "61.64%",
        "To be determined", "$0", "$10,714,782", "$530,000"],
 "common": ["$3,500,000", "$2,000,000", "$5,500,000", "15.00%", "50 / 50", "51%", "49%",
            "$1,823,062", "$1,041,750", "$14,048,334", "$8,164,823", "$4,664,823",
            "2.33x", "32.6%", "63.64%"]}
# ── what the other packages must never see. Bare IRR percentages are deliberately left out:
# they collide with unrelated ratios (the 2031 debt yield is 31.5%, so is the preferred IRR).
# Distinctive dollar amounts, two-decimal rates and x-multiples identify a tranche without them.
SECRET = {
 "hm8": [], "hm10": [], "hm11": [],
 "senior": ["12.00%", "SOFR", "8.21%", "$8,600,000", "$9,800,000", "$3,600,000", "$940,000",
            "$14,540,000", "$4,740,000", "1.48x", "$364,000", "$1,228,000",
            "$4,164,000", "$5,028,000", "$14,828,000"],
 "pref": ["17.00%", "$3,825,963", "$1,931,666", "$3,714,944", "$78,081",
          "$7,526,610", "$3,700,647", "1.97x", "$728,000", "$2,456,000",
          # "$1,880,000" is left out: 47 slips at the $40,000 top of the marina range is the
          # same number as the preferred's base-case exit participation.
          "$2,548,647", "$4,276,647", "$8,102,610"],
 "common": ["$1,823,062", "$1,041,750", "$2,864,812", "$5,683,522", "$2,841,761",
            "$14,048,334", "$8,164,823", "$4,664,823", "$5,883,511", "$3,883,511",
            "$6,704,334", "$18,944,334", "$10,612,823", "$7,112,823"]}
# capital amounts, the stack and aggregates every recipient is entitled to see
SHARED_OK = {"$10,000,000", "$3,904,044", "$3,500,000", "$2,000,000", "$5,500,000",
             "$17,404,044", "$4,751,666", "$19,247,882", "51%", "49%"}
# the common equity recipient must see no exit level at which it loses money
LOSS = ["$18,000,000", "$18M", "$12,783,904", "$791,424", "$452,242", "0.77x", "-8.2%"]
PARTNERSHIP_WORDS = ["partnership", "Partnership", "pari passu", "general partner",
                     "General Partner", "limited partner", "Limited Partner", "· LP",
                     "GP co-investment", "GP share", "GP ownership", "LP share", "LP commitment",
                     "promote", "residual split", "preferred return"]
NO_RETURN_WORDS = [r"\bIRR\b", r"\bequity kicker\b"]     # matched on raw text, with boundaries
NO_RETURN = ["Exit participation", "exit participation", "participation in equity",
             "5.00%", "Equity multiple", "equity multiple", "Projected Return",
             "total cash received", "Net Funded Basis", "not for distribution", "$9,800,000",
             "$3,600,000", "$940,000", "$364,000", "$1,228,000", "$14,540,000", "$4,740,000",
             "1.48x", "1.51x", "15.6%", "16.4%"]
# the loan-dependent figures that must not appear in a package built for a different request
WRONG_REQUEST = {"hm8": ["$10,000,000", "$11,000,000", "$1,200,000", "$1,320,000",
                          "$3,904,044", "$3,018,628", "$17,404,044", "$17,518,628"],
                 # "$960,000" is left out: it is the $8M debt service and also 24 Dogwood Cove
                 # slips at the $40,000 top of the marina range.
                 "hm10": ["$8,000,000", "$11,000,000", "$1,320,000",
                          "$5,674,878", "$3,018,628", "$17,174,878", "$17,518,628"],
                 "hm11": ["$8,000,000", "$10,000,000", "$1,200,000",
                          "$5,674,878", "$3,904,044", "$17,174,878", "$17,404,044"]}
# the LP commitment is fixed at every request; the preferred fills the gap
FIXED_COMMON = "$3,500,000"
MARINA = ["$30,000", "$1,410,000", "$690,000", "$720,000", "$1,175,000", "$1,880,000",
          "$280,000", "$27,000", "$30,837", "47 slips", "23 slips", "24 slips"]
MARINA_PDF = f"{P}/Wylder Tilghman Island - Marina Valuation.pdf"
FORBIDDEN = ["appraisal", "appraised", "appraiser", "LWHA", "Newmark", "CBRE", "New Day"]
BRITISH = ["utilise", "organis", "centre", "labour", "metres", "colour", "favour", "analyse"]

fails = []


def check(cond, label, detail=""):
    print(f'  {"OK " if cond else "!! "}{label}{"" if cond else "  " + detail}')
    if not cond:
        fails.append(label)


for t, (name, path, pages) in PKGS.items():
    d = pymupdf.open(path)
    flat = norm("".join(p.get_text() for p in d))
    raw = re.sub(r"\s+", " ", "".join(p.get_text() for p in d))
    print(f"\n── {name} · {len(d)} pages ──")
    check(len(d) == pages, f"{pages} pages", f"got {len(d)}")

    missing = [v for v in OWN[t] if norm(v) not in flat]
    check(not missing, "carries its own economics", f"missing {missing}")

    leaked = []
    for other in OTHERS[t]:
        leaked += [v for v in SECRET[other] if v not in SHARED_OK and norm(v) in flat]
    check(not leaked, "no other tranche's economics", f"leaked {sorted(set(leaked))}")

    named = [w for w in FORBIDDEN if re.search(w, raw, re.I)]
    check(not named, "no source document named", f"found {named}")

    brit = [w for w in BRITISH if w in raw.lower()]
    check(not brit, "US spelling", f"found {brit}")

    check(norm("58 keys") in flat and norm(BASIS_KEY[t]) in flat,
          "per-key figures on 58 keys", f"cost basis per key {BASIS_KEY[t]} not found")

    if t == "lp":
        hits = ([v for v in LP_FORBID if norm(v) in flat]
                + [w for w in NO_RETURN_WORDS if re.search(w, raw)])
        check(not hits, "no economics and no debt request detail", f"found {hits}")
        missing = [v for v in LP_REQUIRED if norm(v) not in flat]
        check(not missing, "states the request and that the terms are open", f"missing {missing}")
        missing = [v for v in MARINA if norm(v) not in flat]
        check(not missing, "carries the marina valuation", f"missing {missing}")

    if t in LENDER:
        missing = [v for v in MARINA if norm(v) not in flat]
        check(not missing, "carries the marina valuation", f"missing {missing}")
        hits = [w for w in PARTNERSHIP_WORDS if w in raw]
        check(not hits, "no partnership, GP or LP vocabulary", f"found {hits}")

    if t in NO_KICKER:
        hits = ([v for v in NO_RETURN if norm(v) in flat]
                + [w for w in NO_RETURN_WORDS if re.search(w, raw)])
        check(not hits, "no participation and no lender return", f"found {hits}")
        hits = [v for v in WRONG_REQUEST[t] if norm(v) in flat]
        check(not hits, "no figures from another loan request", f"found {hits}")
        check(norm(FIXED_COMMON) in flat, "LP commitment held at $3,500,000")

    if t == "common":
        hits = [v for v in LOSS if norm(v) in flat]
        check(not hits, "no exit level showing a loss", f"found {hits}")

# ── the standalone marina valuation deck
d = pymupdf.open(MARINA_PDF)
flat = norm("".join(pg.get_text() for pg in d))
raw = re.sub(r"\s+", " ", "".join(pg.get_text() for pg in d))
print(f"\n── Marina Valuation · {len(d)} pages ──")
check(len(d) == 9, "9 pages", f"got {len(d)}")
missing = [v for v in MARINA + ["$35,219", "$39,428", "$1,269,000", "$2,295", "8.50%",
                                "$359,296", "$820,833", "$1,100,000"] if norm(v) not in flat]
check(not missing, "carries every valuation figure", f"missing {missing}")
named = [w for w in FORBIDDEN if re.search(w, raw, re.I)]
check(not named, "no source document named", f"found {named}")
brit = [w for w in BRITISH if w in raw.lower()]
check(not brit, "US spelling", f"found {brit}")
tranche = ([v for v in ["12.00%", "17.00%", "SOFR", "$10,000,000", "$3,904,044",
                        "preferred equity", "senior loan", "equity multiple"] if norm(v) in flat]
           + [w for w in NO_RETURN_WORDS if re.search(w, raw)])
check(not tranche, "no capitalization economics", f"found {tranche}")

print()
if fails:
    print(f"{len(fails)} check(s) failed")
    sys.exit(1)
print("all checks passed")
