# -*- coding: utf-8 -*-
"""The LP recapitalization: the limited partner funds the entire closing.

This is the capital plan the recapitalization deck was built on — LP equity is the only source
at closing, and a senior refinance in month three funds the business plan and returns capital.
It is a different plan from the senior-plus-preferred-plus-common capitalization in figs_v7.py,
which solves a $10,000,000 senior request. The operating projections are common to both.

The model carries a $1 rounding difference between the fee components and the gross equity; the
deck discloses it, as the source deck did.
"""
KEYS = 58

LP_EQUITY   = 13_255_085          # gross, the only source at closing
LP_ORIG_PC  = 0.0200
LP_ORIG     = 265_102             # origination fee retained by the LP at funding
MMCC_PC     = 0.0200
MMCC_FEE    = 265_102             # placement fee to MMCC
LP_NET      = 12_989_984          # net cash invested
FEES_TOTAL  = 530_203

SENIOR      = 7_000_000           # refinance, month 3 — not requested in this deck
SENIOR_MO_INTEREST = 57_458       # from month 19, once the reserve is exhausted
SENIOR_ADS  = SENIOR_MO_INTEREST * 12
TOTAL_CAPITAL   = LP_EQUITY + SENIOR
RETURN_OF_CAP   = 2_070_384       # to the LP at the refinance
NET_CAPITAL     = TOTAL_CAPITAL - RETURN_OF_CAP
PRIOR_INVESTED  = 642_693         # put into the hotel 2021-2025, outside this plan

USES_CLOSE = [('Existing loan payoff', 10_714_782),
              ('Merchant cash advance payoff', 530_000),
              ('Dogwood Cove acquisition', 1_100_000),
              ('Working capital', 250_000),
              ('Closing, legal and other', 130_100),
              (f'LP origination fee &middot; {LP_ORIG_PC:.2%}', LP_ORIG),
              (f'MMCC placement fee &middot; {MMCC_PC:.2%}', MMCC_FEE)]
CLOSING_DETAIL = [('Legal &mdash; borrower', 65_000), ('Other closing costs', 40_000),
                  ('Legal &mdash; LP', 15_000), ('Third-party reports and fees', 10_100)]

REFI_ALLOC = [('Capital improvement plan holdback', 3_003_000),
              ('Return of capital to the LP', RETURN_OF_CAP),
              ('Interest reserve &middot; 15 months', 732_434),
              ('Working capital reserve', 500_000),
              ('Lender fees, recordation, title and legal', 394_182),
              ('Dogwood Cove renovation holdback', 300_000)]

VAL = {'is': 21_400_000, 'complete': 26_000_000, 'stab': 29_500_000}
RENOVATION = 3_303_000
BASIS = 18_184_701

_u = sum(a for _, a in USES_CLOSE)
assert abs(_u - LP_EQUITY) <= 1, (_u, LP_EQUITY)
assert sum(a for _, a in CLOSING_DETAIL) == 130_100
assert sum(a for _, a in REFI_ALLOC) == SENIOR
assert round(LP_EQUITY * LP_ORIG_PC) == LP_ORIG and round(LP_EQUITY * MMCC_PC) == MMCC_FEE
assert abs(LP_ORIG + MMCC_FEE - FEES_TOTAL) <= 1
assert abs(LP_EQUITY - LP_ORIG - LP_NET) <= 1
assert TOTAL_CAPITAL == 20_255_085 and NET_CAPITAL == 18_184_701 == BASIS
assert round(LP_EQUITY / KEYS) == 228_536 and round(NET_CAPITAL / KEYS) == 313_529
assert SENIOR_ADS == 689_496

if __name__ == '__main__':
    print(f'  LP equity {LP_EQUITY:,} gross · {LP_NET:,} net cash invested · '
          f'${round(LP_EQUITY/KEYS):,}/key')
    print(f'  uses at closing foot to {_u:,} (${_u - LP_EQUITY} rounding, disclosed)')
    print(f'  senior refinance {SENIOR:,} month 3 · allocation foots · '
          f'{RETURN_OF_CAP:,} returned ({RETURN_OF_CAP/LP_NET:.1%} of net cash invested)')
    print(f'  total capital {TOTAL_CAPITAL:,} · net capital in the asset {NET_CAPITAL:,} '
          f'(${round(NET_CAPITAL/KEYS):,}/key)')
    print(f'  LP equity to as-is {LP_EQUITY/VAL["is"]:.2%} · net capital to as-is '
          f'{NET_CAPITAL/VAL["is"]:.2%} · to stabilized {NET_CAPITAL/VAL["stab"]:.2%}')
    print(f'  senior annual debt service {SENIOR_ADS:,} ({SENIOR_ADS/SENIOR:.2%} on {SENIOR:,})')
    print('  all LP recapitalization figures reconcile')
