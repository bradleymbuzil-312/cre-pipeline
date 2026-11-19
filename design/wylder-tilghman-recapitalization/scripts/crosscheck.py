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
PKGS = {"senior": ("Senior Debt", f"{P}/Wylder Tilghman Island - Senior Debt.pdf", 30),
        "hm8": ("Senior Debt - 8M Request",
                f"{P}/Wylder Tilghman Island - Senior Debt - 8M Request.pdf", 29),
        "hm10": ("Senior Debt - 10M Request",
                 f"{P}/Wylder Tilghman Island - Senior Debt - 10M Request.pdf", 29),
        "hm11": ("Senior Debt - 11M Request",
                 f"{P}/Wylder Tilghman Island - Senior Debt - 11M Request.pdf", 29),
        "hm125": ("Senior Debt - 12.5M Request",
                  f"{P}/Wylder Tilghman Island - Senior Debt - 12.5M Request.pdf", 29),
        "lp": ("LP Recapitalization",
               f"{P}/Wylder Tilghman Island - LP Recapitalization.pdf", 29),
        "pref": ("Preferred Equity", f"{P}/Wylder Tilghman Island - Preferred Equity.pdf", 29),
        "common": ("Common Equity", f"{P}/Wylder Tilghman Island - Common Equity.pdf", 29),
        "eq": ("LP Equity", f"{P}/Wylder Tilghman Island - LP Equity.pdf", 30)}
# The LP Equity package alone carries four addenda, and its valuation slide alone names CBRE.
# Every other page of every package still states values with no source named.
EQ_VALUATION_PAGE = 26
EQ_ADDENDA = [
    # cash flow historicals: the actual operating statement must foot on the page
    "$3,475,020", "$3,810,275", "$3,786,028", "$3,716,313", "$485,761", "$915,792",
    "$664,922", "$634,680", "T12 Sep 2026", "$642,693",
    # the renovation, restated to the sponsor's 175-day program
    "$3,003,000", "175 days", "$52,684", "Jan 4", "Jun 28", "$446,908", "$3,003,000",
    # the valuation, attributed
    "CBRE", "CB26US098551-1", "Michael Cummings", "$21,400,000", "$26,000,000", "$29,500,000",
    "11.25%", "8.75%", "8.25%",
    # the membership proposal
    "$4,500", "$13,220", "$20,902", "$33,050", "$100,222", "24,110",
]
LENDER = ["senior", "hm8", "hm10", "hm11", "hm125"]
# total cost basis per key moves with the request, because the reserve and the fees are in it
BASIS_KEY = {"senior": "$331,860", "hm8": "$326,688", "hm10": "$331,860", "hm11": "$334,446",
             "hm125": "$338,326", "lp": "$313,529", "pref": "$331,860",
             "common": "$331,860", "eq": "$331,860"}
NO_KICKER = ["hm8", "hm10", "hm11", "hm125"]
# the debt packages are the same deal at different requests, so they are not "other tranches"
# to each other
OTHERS = {t: ([] if t in ("lp", "eq") else ["pref", "common"] if t in LENDER
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

# The LP equity marketing deck states one economic objective — a 2.0x target over a 36-month
# hold — and nothing else. Every other term is named and left open, and the senior request is
# not in the package at all.
EQ_FORBID = [
    # no proposed economics for any tranche
    "12.00%", "17.00%", "15.00%", "50 / 50", "50/50", "51% / 49%", "51%/49%",
    "Equity multiple of", "Projected IRR", "Projected Return", "Exit participation",
    "$1,823,062", "$1,041,750", "$14,048,334", "$8,164,823", "$7,526,610", "$3,700,647",
    "$3,825,963", "$1,931,666", "$3,714,944", "$4,740,000", "$14,540,000",
    # no senior debt request detail
    "SOFR", "$10,000,000", "$8,600,000", "$3,904,044", "Debt yield", "Debt service coverage",
    "Loan to value", "Loan to cost", "first trust deed", "Net Funded Basis",
    # the v4 recapitalization plan, which this package does not carry
    "$13,255,085", "$20,255,085", "$18,184,701",
]
# "2.0x" is required here, so NO_RETURN_WORDS cannot be reused wholesale: only IRR is barred.
EQ_REQUIRED = ["2.0x", "36 months", "To be negotiated", "$17,404,044", "$15,747,882",
               "$19,247,882", "$29,500,000", "$2,516,931", "13.08%", "7.77%", "$2,000,000",
               "Target equity multiple", "Preferred return", "Sponsor promote",
               # the combined pro forma, every year of it
               "$4,952,259", "$2,331,825", "$1,453,613", "$6,390,948", "$2,230,128",
               "$7,072,662", "$2,703,997", "$2,903,626", "2031",
               # the parcel priced and expensed on its own terms
               "$1,433,000", "$223,734", "15.61%", "November 16, 2026", "$143,719"]

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
 "hm125": ["$12,500,000", "12.00%", "SOFR", "$10,750,000", "$1,500,000", "58.41%", "70.66%",
           "18.52%", "1.54x", "1.38x", "$19,622,882", "$338,326", "$1,690,502", "$3,500,000",
           "$17,690,502"],
 "hm11": ["$11,000,000", "12.00%", "SOFR", "$9,460,000", "$1,320,000", "51.40%", "62.79%",
          "21.05%", "1.75x", "1.57x", "$19,397,882", "$334,446", "$3,018,628", "$3,500,000",
          "$17,518,628"],
 "pref": ["$3,904,044", "17.00%", "$3,825,963", "$1,931,666", "$3,714,944", "10.00%",
          "$1,880,000", "$7,526,610", "$3,700,647", "1.97x", "31.5%", "64.97%"],
 "lp": ["$13,255,085", "$12,989,984", "$7,000,000", "$20,255,085", "$18,184,701",
        "$2,070,384", "$228,536", "$313,529", "61.94%", "84.98%", "61.64%",
        "To be determined", "$0", "$10,714,782", "$530,000"],
 # the LP equity package's only economics are the target and the plan it is built on
 # LP Equity runs on the reconciled pro forma: the November 16 workbook with the Dogwood
 # residence and the 24 new slips added back, so 2029 is the first stabilized year
 # LP Equity runs on the combined pro forma: hotel plus Dogwood Cove, the parcel carrying
 # its own expenses. 2029 is the first stabilized year; the implied cap is on hotel income
 # only, because the estimated values are for the hotel alone.
 "eq": ["2.0x", "36 months", "$17,404,044", "$15,747,882", "$19,247,882", "$331,860",
        "$29,500,000", "13.08%", "7.77%", "To be negotiated"],
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
                 "hm10": ["$8,000,000", "$11,000,000", "$12,500,000", "$1,500,000", "$1,320,000",
                          "$5,674,878", "$3,018,628", "$17,174,878", "$17,518,628"],
                 # "$960,000" is left out here too: it is 24 Dogwood Cove slips at the $40,000
                 # top of the marina range as well as the $8M request's debt service.
                 "hm125": ["$8,000,000", "$10,000,000", "$11,000,000",
                           "$1,200,000", "$1,320,000", "$5,674,878", "$3,904,044", "$3,018,628",
                           "$17,174,878", "$17,404,044", "$17,518,628"],
                 "hm11": ["$8,000,000", "$10,000,000", "$12,500,000", "$1,500,000", "$1,200,000",
                          "$5,674,878", "$3,904,044", "$17,174,878", "$17,404,044"]}
# the LP commitment is fixed at every request; the preferred fills the gap
FIXED_COMMON = "$3,500,000"
MARINA = ["$30,000", "$1,410,000", "$690,000", "$720,000", "$1,175,000", "$1,880,000",
          "$280,000", "$27,000", "$30,837", "47 slips", "23 slips", "24 slips"]
MARINA_PDF = f"{P}/Wylder Tilghman Island - Marina Valuation.pdf"
# the Dogwood Cove acquisition detail page, carried by every capitalization package
# the acquisition workbook prices the parcel at cost and yields it; no appraisal allocates
# value to it, so the capitalized-value claim is gone
DOGWOOD = ["$1,100,000", "$300,000", "$1,433,000", "$33,000", "November 16, 2026",
           "21551 Tilghman Investors LLC", "$1,500", "$191,625", "$223,734"]
# claims the acquisition workbook does not support, in any package
UNSUPPORTED = ["$4,285,714", "$2,885,714", "$1,400,000", "November 18, 2026"]
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

    missing = [v for v in DOGWOOD if norm(v) not in flat]
    check(not missing, "carries the Dogwood Cove acquisition detail", f"missing {missing}")
    hits = [v for v in UNSUPPORTED if norm(v) in flat]
    check(not hits, "no unsupported Dogwood value or superseded date", f"found {hits}")

    if t == "eq":
        # the valuation slide is the one page in the library allowed to name its source
        others = re.sub(r"\s+", " ", "".join(
            p.get_text() for i, p in enumerate(d) if i + 1 != EQ_VALUATION_PAGE))
        val = re.sub(r"\s+", " ", d[EQ_VALUATION_PAGE - 1].get_text())
        named = [w for w in FORBIDDEN if re.search(w, others, re.I)]
        check(not named, "no source named outside the valuation slide", f"found {named}")
        check("CBRE" in val, "the valuation slide names CBRE")
        check(not re.search(r"LWHA|Newmark", raw, re.I),
              "the superseded appraisal is never named")
    else:
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

    if t == "eq":
        hits = ([v for v in EQ_FORBID if norm(v) in flat]
                + [w for w in (r"\bIRR\b",) if re.search(w, raw)])
        check(not hits, "no proposed economics and no senior request detail", f"found {hits}")
        missing = [v for v in EQ_REQUIRED if norm(v) not in flat]
        check(not missing, "states the 2.0x target and leaves the structure open",
              f"missing {missing}")
        missing = [v for v in MARINA if norm(v) not in flat]
        check(not missing, "carries the marina valuation", f"missing {missing}")
        missing = [v for v in EQ_ADDENDA if norm(v) not in flat]
        check(not missing, "carries the four addenda in full", f"missing {missing}")
        # the renovation is restated here and nowhere else
        check(not re.search(r"Nov 1, 2026", raw), "no trace of the superseded schedule")
        # projections are relabelled a year forward against the actuals now carried
        check(norm("2031") in flat and norm("2026 is a transition year") not in flat,
              "projection years restated against the actuals")

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
# ── the equity teaser: an offering-style piece that states no figure at all
TEASER_PDF = f"{P}/Wylder Tilghman Island - Equity Teaser.pdf"
# the closing page carries the advisor's telephone, email and license and nothing else
TEASER_CONTACT = ["310.909.5473", "01927157"]
d = pymupdf.open(TEASER_PDF)
print(f"\n── Equity Teaser · {len(d)} pages ──")
check(len(d) == 14, "14 pages", f"got {len(d)}")
body = re.sub(r"\s+", " ", "".join(pg.get_text() for pg in d[:-1]))
closing = re.sub(r"\s+", " ", d[-1].get_text())
stray = sorted(set(re.findall(r"\S*\d\S*", body)))
check(not stray, "no figure on any page but the last", f"found {stray}")
left = sorted(set(re.findall(r"\S*\d\S*", closing)) - set(TEASER_CONTACT))
check(not left, "the closing page carries contact details only", f"found {left}")
raw = body + " " + closing
check(not re.search(r"sources and uses", raw, re.I), "no sources and uses")
named = [w for w in FORBIDDEN if re.search(w, raw, re.I)]
check(not named, "no source document named", f"found {named}")
brit = [w for w in BRITISH if w in raw.lower()]
check(not brit, "US spelling", f"found {brit}")
for word in ("Valuation", "renovation", "revenue"):
    check(re.search(word, raw, re.I) is not None, f"carries the {word.lower()} section")

# ── the Palette Hotels investment overview
#
# This deck is the one exception to the no-source rule in the whole library, by instruction: it
# names CBRE and LW Hospitality Advisors and uses the word appraisal. What it must not carry is
# any capital structure at all.
PALETTE_PDF = f"{P}/Wylder Tilghman Island - Investment Overview - Palette Hotels (11.18.26).pdf"
PALETTE_FORBID = [
    "preferred", "17.00%", "current pay", "accrued", "minimum multiple", "1.20x", "1.55x",
    "profit participation", "kicker", "last-dollar", "LTV", "senior loan", "LCP Investors",
    "waterfall", "redemption", "origination fee", "broker fee", "carry reserve",
    "value cushion", "sources and uses", "target close",
    # Hilton stays out; the affiliation itself is named on the business plan slide only
    "Hilton", "September 21, 2026",
    "$7,276,056", "$7.28M", "$9,000,000", "$9.00M", "$16,276,056", "$8,731,268",
    "$11,252,661", "$727,606", "$823,769",
]
PALETTE_REQUIRED = [
    # the cover states the combined program; the budget slide prices the hotel one by line
    "50 \u2192 57", "$3.3M", "whole-home suite", "$3.0M", "Hotel program", "$3,303,000",
    "$52,684", "$21.4M", "$29.5M", "$0.63M", "$2.29M",
    "42.8%", "Jan \u2192 Jun 2027", "January 4, 2027", "175 days",
    "$3,003,000", "$1,425,000", "$258,000", "$488,039", "$152,250",
    "CBRE", "LW Hospitality Advisors", "$518K", "3.6", "$85 \u2192 $166",
    # the parcel on its own, and the two together
    # settlement is not confirmed in file, so the slide says pending rather than a date
    "$1,433,000", "$1,100,000", "settlement pending", "$223,734", "15.61%", "$80,195",
    "$192,150", "$191,625", "$179,648", "$47,906", "$222,159",
    "$2,516,931", "$7,072,662", "$1,453,613", "$2,230,128", "$2,903,626", "8.9%", "35.6%",
    "$2,375,478",
]
d = pymupdf.open(PALETTE_PDF)
raw = re.sub(r"\s+", " ", "".join(pg.get_text() for pg in d))
flat = norm(raw)
print(f"\n\u2500\u2500 Investment Overview, Palette Hotels \u00b7 {len(d)} pages \u2500\u2500")
check(len(d) == 12, "12 slides", f"got {len(d)}")
hits = [w for w in PALETTE_FORBID if w.lower() in raw.lower()]
check(not hits, "no capital structure, no brand affiliation", f"found {hits}")
missing = [v for v in PALETTE_REQUIRED if norm(v) not in flat]
check(not missing, "carries the figures the brief specifies", f"missing {missing}")
check("\u2014" not in raw, "no em dashes",
      f"found {raw.count(chr(0x2014))}")
brit = [w for w in BRITISH if w in raw.lower()]
check(not brit, "US spelling", f"found {brit}")
# letter-spaced condensed type extracts one character at a time, so compare on the stripped form
_footed = sum(1 for pg in d
              if norm("Investment Overview") in norm(pg.get_text())
              and norm("The TRANCHE Group") in norm(pg.get_text()))
check(_footed == len(d), "running footer on every slide", f"only {_footed} of {len(d)}")
# the parcel is stated on its own and in combination, and the two reconcile on the page
check(norm("Hotel and parcel together") in flat and norm("Dogwood Cove, on its own") in flat,
      "carries the parcel individually and combined")
check(norm("$2.29M") in flat and norm("$2.52M") in flat,
      "reconciles the hotel-only and combined stabilized income")
# the affiliation is a proposal in hand on the business plan slide, and appears nowhere else
_plan = next((pg.get_text() for pg in d if norm("Business plan and capital") in norm(pg.get_text())),
             "")
_other = "".join(pg.get_text() for pg in d if pg.get_text() != _plan)
check(norm("Small Luxury Hotels membership proposal is in hand") in norm(_plan),
      "the business plan states the affiliation proposal is in hand")
check(norm("SLH fees are not included in the pro forma") in norm(_plan),
      "the business plan says the affiliation fees are not in the pro forma")
# corrections of record: the claims these replaced were wrong
_gone = ["12.3%", "$488K", "no third-party management agreement", "1,100 feet",
         "Marina, house and pier utility bids", "57-key waterfront resort",
         "Select-service resort", "that has never produced revenue"]
check(not [w for w in _gone if w.lower() in raw.lower()],
      "none of the corrected claims survive",
      f"found {[w for w in _gone if w.lower() in raw.lower()]}")
# the two renovation figures must never appear unlabelled against each other
check(norm("sits outside this budget") in flat,
      "the budget slide says the Dogwood renovation is outside it")
# scope is stated wherever a count or a figure could be read for either the hotel or the whole
_scoped = ["57 + 1", "57 hotel keys on completion", "$3,003,000 hotel program",
           "Hotel only \u00b7 CBRE, September 11, 2026", "Hotel only \u00b7 CBRE, April 1, 2029",
           "2029 hotel pro forma", "The hotel on its own",
           "The Dogwood Cove suite sits on the adjacent parcel",
           "more sellable hotel inventory"]
_miss = [v for v in _scoped if norm(v) not in flat]
check(not _miss, "every count and figure states the scope it covers", f"missing {_miss}")
check(all(norm(v) in flat for v in ("$1.93M", "$0.35M", "14% more sellable hotel inventory",
                                    "50-key waterfront resort", "Full-service waterfront resort",
                                    "Affiliate management", "executed management agreement",
                                    "Phase I ESA", "ALTA survey", "Dogwood Cove projections",
                                    "assumptions pending quotes")),
      "carries the corrected copy")
check(norm("Small Luxury Hotels") not in norm(_other) and norm("SLH") not in norm(_other),
      "the affiliation appears on no other slide")

# ── corrections of record: claims that were wrong and must not return, in any package
WITHDRAWN = ["12.3%", "never produced revenue", "no third-party management",
             "1,100 feet", "Select-service", "select service",
             "rebuilt three-bedroom house add further"]
print("\n\u2500\u2500 Corrections of record, across every package \u2500\u2500")
_bad = []
for _label, _path, *_ in list(PKGS.values()) + [("Marina Valuation", MARINA_PDF),
                                                ("Equity Teaser", TEASER_PDF),
                                                ("Palette overview", PALETTE_PDF)]:
    _raw = re.sub(r"\s+", " ", "".join(pg.get_text() for pg in pymupdf.open(_path)))
    _hits = [w for w in WITHDRAWN if w.lower() in _raw.lower()]
    if _hits:
        _bad.append(f"{_label}: {_hits}")
check(not _bad, "no withdrawn claim survives in any package", f"{_bad}")

if fails:
    print(f"{len(fails)} check(s) failed")
    sys.exit(1)
print("all checks passed")
