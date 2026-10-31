# -*- coding: utf-8 -*-
"""Source of truth for the 10.28.26 model — senior debt + preferred equity + common equity.

Sources and Uses is authoritative for the stack. The Loan Analysis tab still carries the
earlier no-common-equity case (pref $7,404,044 / common $0); it is not used here.
"""
import os

KEYS = 58

# ───────────────────────────────── the senior loan, sized by request
# The model solves the $10,000,000 request. Alternative requests re-derive every loan-dependent
# figure below from the same uses: the uses that do not depend on the loan are fixed, and the
# reserve, the origination fee and the broker fee all scale with it, so the common equity is the
# plug. The exit waterfall is solved only at $10,000,000 — see WATERFALL_OK.
SENIOR = int(os.environ.get('WT_SENIOR_LOAN', 10_000_000))
WATERFALL_OK = (SENIOR == 10_000_000)

COMMON   =  3_500_000      # LP commitment — a committed number, fixed at every request
GP_CASH  =  2_000_000      # John Flannigan, pari passu with the LP
PF_ORIG_PC, PF_MMCC_PC = 0.0200, 0.0200   # to the pref investor / MMCC placement

# ───────────────────────────────── senior, 1st trust deed
SOFR, SPREAD, ALLIN = 0.0379, 0.0821, 0.1200
SR_ORIG_PC, SR_BROKER_PC = 0.0200, 0.0100
SR_ADS      = round(SENIOR * ALLIN)           # interest-only
SR_ORIG     = round(SENIOR * SR_ORIG_PC)
SR_BROKER   = round(SENIOR * SR_BROKER_PC)
SR_RESERVE  = SR_ADS                          # 12-month interest and carry reserve
SR_NET      = SENIOR - SR_ORIG - SR_RESERVE   # gross less origination less reserve
SR_TERM     = 3
SR_KICKER   = 0.0500                          # share of equity value at exit
PERM_RATE   = 0.0650
PERM_ADS    = round(758_482 * SENIOR / 10_000_000)   # 30-yr amortizing at PERM_RATE

# ───────────────────────────────── the stack: the preferred is the balancing item
# The LP commitment is fixed and the senior is the request, so the preferred fills the gap. Its
# own two fees are 2.00% of itself on each side, so it solves against itself — at $10,000,000 this
# reproduces the model's $3,904,044 exactly.
FIXED_USES = 15_747_882          # uses that move with neither the loan nor the preferred

def solve_pref(loan, common=COMMON):
    base = FIXED_USES + round(loan * (ALLIN + SR_ORIG_PC + SR_BROKER_PC)) - loan - common
    pref = round(base / (1 - PF_ORIG_PC - PF_MMCC_PC))
    for _ in range(32):
        nxt = base + round(pref * PF_ORIG_PC) + round(pref * PF_MMCC_PC)
        if nxt == pref:
            return pref
        pref = nxt
    raise ValueError(f'preferred did not converge at a ${loan:,} request')

PREF        = solve_pref(SENIOR)
TOTAL       = SENIOR + PREF + COMMON
PARTNERSHIP = COMMON + GP_CASH

# ───────────────────────────────── preferred
PF_RATE_PIK, PF_RATE_CUR = 0.1700, 0.0000
PF_ORIG     = round(PREF * PF_ORIG_PC)  # to the pref investor
PF_MMCC     = round(PREF * PF_MMCC_PC)  # MMCC placement
PF_NET      = PREF - PF_ORIG            # pref less investor origination fee
PF_KICKER   = 0.1000
# sweep-adjusted balance: begin, PIK accrued, sweep, end
PF_SCHED = [(1, 3_904_044,  663_687, 1_129_314, 3_438_417),
            (2, 3_438_417,  584_531, 1_115_019, 2_907_929),
            (3, 2_907_929,  494_348, 1_470_611, 1_931_666)]
PF_DUE_AT_EXIT = 1_931_666

# ───────────────────────────────── common equity partnership
CE_PREF      = 0.1500                   # pari passu, accruing and compounding
CE_LP_PCT    = COMMON / PARTNERSHIP     # 63.64%
CE_GP_PCT    = GP_CASH / PARTNERSHIP    # 36.36%
CE_LP_RESID, CE_GP_RESID = 0.5000, 0.5000
CE_KICKER    = 0.8500                   # common share of residual profit at exit
GP_MIN_PROFIT, GP_TARGET_EXIT = 3_000_000, 30_000_000

# ───────────────────────────────── exit grid (3-year hold, 4.0% selling costs)
SELL_COST, HOLD = 0.0400, 3
EXITS = [18_000_000, 21_000_000, 24_000_000, 27_000_000, 30_000_000, 33_000_000, 36_000_000]
BASE_EXIT = 30_000_000
# per exit value, in EXITS order
NET_PROCEEDS = [17_280_000, 20_160_000, 23_040_000, 25_920_000, 28_800_000, 31_680_000, 34_560_000]
# kicker base = net sale proceeds less the senior principal (the model's own arithmetic; its
# label reads "less Senior and Pref", but the pref balance is deducted after the kickers)
KICKER_BASE  = [ 7_280_000, 10_160_000, 13_040_000, 15_920_000, 18_800_000, 21_680_000, 24_560_000]
SR_KICK      = [   364_000,    508_000,    652_000,    796_000,    940_000,  1_084_000,  1_228_000]
PF_KICK      = [   728_000,  1_016_000,  1_304_000,  1_592_000,  1_880_000,  2_168_000,  2_456_000]
CE_RESID     = [ 4_256_334,  6_704_334,  9_152_334, 11_600_334, 14_048_334, 16_496_334, 18_944_334]
SR_EXIT_LTV  = [0.5556, 0.4762, 0.4167, 0.3704, 0.3333, 0.3030, 0.2778]
PF_LAST_DOLLAR = [0.6629, 0.5682, 0.4972, 0.4419, 0.3977, 0.3616, 0.3314]
IMPLIED_CAP  = [0.1484, 0.1272, 0.1113, 0.0989, 0.0890, 0.0809, 0.0742]

SR_IRR  = [0.1392, 0.1434, 0.1475, 0.1517, 0.1558, 0.1598, 0.1639]
SR_MULT = [1.4249, 1.4396, 1.4543, 1.4690, 1.4837, 1.4984, 1.5131]
SR_PROFIT = [4_164_000, 4_308_000, 4_452_000, 4_596_000, 4_740_000, 4_884_000, 5_028_000]
PF_IRR  = [0.2367, 0.2574, 0.2773, 0.2965, 0.3151, 0.3331, 0.3505]
PF_MULT = [1.6661, 1.7414, 1.8167, 1.8920, 1.9672, 2.0425, 2.1178]
PF_PROFIT = [2_548_647, 2_836_647, 3_124_647, 3_412_647, 3_700_647, 3_988_647, 4_276_647]
PF_CASH = [6_374_610, 6_662_610, 6_950_610, 7_238_610, 7_526_610, 7_814_610, 8_102_610]
LP_IRR  = [-0.0819, 0.0682, 0.1777, 0.2564, 0.3263, 0.3895, 0.4474]
LP_MULT = [0.7739, 1.2190, 1.6334, 1.9831, 2.3328, 2.6825, 3.0322]
LP_CASH = [2_708_576, 4_266_395, 5_716_823, 6_940_823, 8_164_823, 9_388_823, 10_612_823]
LP_PROFIT = [-791_424, 766_395, 2_216_823, 3_440_823, 4_664_823, 5_888_823, 7_112_823]
GP_IRR  = [-0.0819, 0.0682, 0.1976, 0.3257, 0.4329, 0.5260, 0.6090]
GP_MULT = [0.7739, 1.2190, 1.7178, 2.3298, 2.9418, 3.5538, 4.1658]
GP_CASH_OUT = [1_547_758, 2_437_940, 3_435_511, 4_659_511, 5_883_511, 7_107_511, 8_331_511]
GP_PROFIT = [-452_242, 437_940, 1_435_511, 2_659_511, 3_883_511, 5_107_511, 6_331_511]
GP_PROMOTE = [0, 0, 393_761, 1_617_761, 2_841_761, 4_065_761, 5_289_761]
PARTNERSHIP_BREAKEVEN = 12_783_904       # below this, LP + GP receive no sale proceeds

# ── invested basis and total cash received, by tranche (each tranche's own economics)
SR_BASIS  = SENIOR - SR_ORIG                       # 9,800,000 net funded
SR_INT_3Y = SR_ADS * SR_TERM                       # 3,600,000 interest-only over the term
SR_CASH   = [SENIOR + SR_INT_3Y + k for k in SR_KICK]
PF_BASIS  = PF_NET                                 # 3,825,963 net funded
PF_SWEEP_3Y = sum(r[3] for r in PF_SCHED)          # 3,714,944 swept against the balance
LP_BASIS  = COMMON
GP_BASIS  = GP_CASH

B = EXITS.index(BASE_EXIT)               # base-case column
# ── partnership waterfall at the base case ($30,000,000 exit, 3-year hold)
_PF = (1 + CE_PREF) ** HOLD - 1                    # 52.0875% cumulative over three years
LP_PREF  = round(COMMON  * _PF)                    # 1,823,063
GP_PREF  = round(GP_CASH * _PF)                    # 1,041,750
WF_PREF  = LP_PREF + GP_PREF
WF_CAP   = PARTNERSHIP
WF_RESID = CE_RESID[B] - WF_PREF - WF_CAP          # split 50 / 50
WF_SPLIT = WF_RESID / 2
SR_PF_DEDUCT = SR_KICK[B] + PF_KICK[B] + PF_DUE_AT_EXIT   # 4,751,666 aggregated, never itemized


# ───────────────────────────────── sources and uses
SOURCES = [('Senior loan &middot; 1st trust deed', SENIOR), ('Preferred equity', PREF),
           ('Common equity &middot; LP', COMMON)]
USES = [('Existing loan payoff', 10_714_782),
        ('PIP / renovation', 3_003_000),
        ('Interest and carry reserve &middot; 12 months', SR_RESERVE),
        ('Land and house acquisition &middot; 21441 Dogwood Cove', 1_100_000),
        ('Working capital', 500_000),
        ('Dogwood Cove house renovation', 300_000),
        (f'Senior origination fee &middot; {SR_ORIG_PC:.1%}', SR_ORIG),
        ('Closing, legal and other', 130_100),
        (f'Broker fee &middot; MMCC senior debt &middot; {SR_BROKER_PC:.1%}', SR_BROKER),
        ('Preferred origination fee &middot; investor &middot; 2.0%', PF_ORIG),
        ('MMCC preferred equity placement fee &middot; 2.0%', PF_MMCC)]
CLOSING = [('Legal &mdash; borrower', 65_000), ('Other closing costs', 40_000),
           ('Legal &mdash; lender', 15_000), ('Processing and third-party fees', 10_100)]

# ───────────────────────────────── operations (unchanged from the prior model)
VAL = {'is': 21_400_000, 'complete': 26_000_000, 'stab': 29_500_000}
PRO = [(2026, 0.33, 288,  96, 4_375_938, 1_129_314),
       (2027, 0.38, 395, 150, 6_381_867, 2_315_019),
       (2028, 0.40, 415, 166, 7_082_124, 2_670_611)]
NOI = {y: n for y, _, _, _, _, n in PRO}
DSCR  = {y: n / SR_ADS for y, n in NOI.items()}
DY    = {y: n / SENIOR for y, n in NOI.items()}
LTV   = {k: SENIOR / v for k, v in VAL.items()}
LTC   = SENIOR / TOTAL                        # loan to the cost of executing the plan
PERM_DSCR = {y: n / PERM_ADS for y, n in NOI.items()}
COMBINED_LTV = dict(zip((2026, 2027, 2028),
                        (TOTAL / VAL['is'], TOTAL / VAL['complete'], TOTAL / VAL['stab'])))
# basis = acquisition and payoff + renovation + other costs; the loan-driven part moves with it
FIXED_BASIS = 17_747_882
COST_BASIS  = FIXED_BASIS + SR_RESERVE + SR_ORIG + SR_BROKER
COST_BASIS_KEY = round(COST_BASIS / KEYS)

if __name__ == '__main__' and not WATERFALL_OK:
    print(f'── ${SENIOR:,} request · the exit waterfall is solved only at $10,000,000 ──')
    ok = lambda a, b, lab: print(f'  {"OK " if abs(a-b)<=2 else "!! "}{lab:44s}{a:>14,.0f}{b:>14,.0f}')
    ok(sum(a for _, a in USES), TOTAL, '  uses foot to the capitalization')
    ok(SENIOR + PREF + COMMON, TOTAL, '  sources foot to the capitalization')
    ok(SR_NET, SENIOR - SR_ORIG - SR_RESERVE, '  net senior proceeds at close')
    ok(COST_BASIS, FIXED_BASIS + SR_RESERVE + SR_ORIG + SR_BROKER, '  total cost basis')
    ok(SR_ADS, round(SENIOR * ALLIN), '  annual debt service, interest-only')
    print(f'  LTV as-is {LTV["is"]:.2%} | LTC {LTC:.2%} | DSCR {DSCR[2027]:.2f}x | '
          f'DY {DY[2027]:.2%} | common equity plug ${COMMON:,}')
    raise SystemExit

if __name__ == '__main__':
    ok = lambda a, b, lab: print(f'  {"OK " if abs(a-b)<=2 else "!! "}{lab:44s}{a:>14,.0f}{b:>14,.0f}')
    print('── the stack')
    ok(SENIOR + PREF + COMMON, TOTAL, 'senior + pref + LP common = total')
    ok(sum(v for _, v in USES), TOTAL, 'uses = total')
    ok(sum(v for _, v in CLOSING), 130_100, 'closing detail')
    ok(SENIOR - SR_ORIG - SR_RESERVE, SR_NET, 'senior net funding')
    ok(round(PREF * PF_ORIG_PC), PF_ORIG, 'pref origination fee at 2.0%')
    ok(PREF - PF_ORIG, PF_NET, 'pref net funding')
    ok(round(SENIOR * ALLIN), SR_ADS, 'senior ADS at 12.00%')
    ok(COMMON + GP_CASH, PARTNERSHIP, 'LP + GP = partnership')
    print(f'  SOFR {SOFR:.2%} + spread {SPREAD:.2%} = {SOFR+SPREAD:.2%} (model {ALLIN:.2%})')
    print('\n── pref roll-forward (PIK less cash sweep)')
    for yr, beg, pik, sweep, end in PF_SCHED:
        ok(beg + pik - sweep, end, f'  year {yr}: {beg:,.0f} + {pik:,.0f} - {sweep:,.0f}')
        assert abs(pik - beg * PF_RATE_PIK) <= 2, (yr, pik, beg * PF_RATE_PIK)
    print('\n── exit waterfall foots at every exit value')
    for i, gx in enumerate(EXITS):
        net = gx * (1 - SELL_COST)
        kb  = net - SENIOR
        tot = SENIOR + PF_DUE_AT_EXIT + SR_KICK[i] + PF_KICK[i] + CE_RESID[i]
        bad = (abs(net-NET_PROCEEDS[i])>2 or abs(kb-KICKER_BASE[i])>2 or abs(tot-net)>2
               or abs(SR_KICK[i]-kb*SR_KICKER)>2 or abs(PF_KICK[i]-kb*PF_KICKER)>2)
        print(f'  {"OK " if not bad else "!! "}${gx/1e6:>4,.0f}M  net {net:>12,.0f}  kicker base {kb:>12,.0f}'
              f'  sr {SR_KICK[i]:>9,.0f}  pf {PF_KICK[i]:>9,.0f}  common {CE_RESID[i]:>11,.0f}'
              f'  (allocated {tot:>12,.0f})')
    print('\n── base case: $30.0M exit, 3-year hold')
    for lab, mult, irr, prof in [('Senior 1st TD', SR_MULT[B], SR_IRR[B], SR_PROFIT[B]),
                                 ('Preferred equity', PF_MULT[B], PF_IRR[B], PF_PROFIT[B]),
                                 ('Common equity · LP', LP_MULT[B], LP_IRR[B], LP_PROFIT[B]),
                                 ('Common equity · GP', GP_MULT[B], GP_IRR[B], GP_PROFIT[B])]:
        print(f'  {lab:22s}{mult:>7.2f}x{irr:>9.1%}{prof:>14,.0f}')
    print(f'  GP profit {GP_PROFIT[B]:,} vs {GP_MIN_PROFIT:,} minimum -> '
          f'cushion {GP_PROFIT[B]-GP_MIN_PROFIT:,}')
    print('\n── tranche basis, cash received and profit reconcile to the multiples')
    for lab, basis, cash, prof, mult in [
            ('Senior 1st TD', SR_BASIS, SR_CASH, SR_PROFIT, SR_MULT),
            ('Preferred equity', PF_BASIS, PF_CASH, PF_PROFIT, PF_MULT),
            ('Common equity · LP', LP_BASIS, LP_CASH, LP_PROFIT, LP_MULT),
            ('Common equity · GP', GP_BASIS, GP_CASH_OUT, GP_PROFIT, GP_MULT)]:
        for i in range(len(EXITS)):
            ok(cash[i] - basis, prof[i], f'  {lab:20s} ${EXITS[i]/1e6:>4,.0f}M  cash-basis = profit')
            assert abs(cash[i] / basis - mult[i]) < 0.0005, (lab, i, cash[i]/basis, mult[i])
    for i in range(len(EXITS)):
        ok(PF_SWEEP_3Y + PF_DUE_AT_EXIT + PF_KICK[i], PF_CASH[i],
           f'  pref cash components ${EXITS[i]/1e6:>4,.0f}M (sweep + balance + participation)')
    ok(LP_CASH[B] + GP_CASH_OUT[B], CE_RESID[B], '  LP + GP cash = common residual')
    print('\n── partnership waterfall at the base case')
    ok(LP_PREF + COMMON + WF_SPLIT, LP_CASH[B], '  LP: pref + capital + half the residual')
    ok(GP_PREF + GP_CASH + WF_SPLIT, GP_CASH_OUT[B], '  GP: pref + capital + half the residual')
    ok(WF_PREF + WF_CAP + WF_RESID, CE_RESID[B], '  tiers foot to the common residual')
    ok(NET_PROCEEDS[B] - SENIOR - SR_PF_DEDUCT, CE_RESID[B],
       '  net proceeds less senior principal and the aggregated senior/pref deduction')
    ok(GP_PREF + GP_CASH + WF_SPLIT - GP_CASH, GP_CASH_OUT[B] - GP_CASH, '  GP profit')
    print(f'  LP share of partnership cash {LP_CASH[B]/CE_RESID[B]:.1%} on '
          f'{COMMON/PARTNERSHIP:.1%} of capital | GP {GP_CASH_OUT[B]/CE_RESID[B]:.1%} on '
          f'{GP_CASH/PARTNERSHIP:.1%}')
    print(f'  aggregated senior/pref deduction at base case ${SR_PF_DEDUCT:,.0f}')
    print(f'  partnership breakeven exit {PARTNERSHIP_BREAKEVEN:,}')
    print(f'  per key on {KEYS}: senior ${SENIOR/KEYS:,.0f} | pref ${PREF/KEYS:,.0f} | '
          f'LP ${COMMON/KEYS:,.0f} | total ${TOTAL/KEYS:,.0f}')
