# -*- coding: utf-8 -*-
"""Build every package: the $10,000,000 set, plus the lender-facing package at other requests.

Each request runs in its own process so the loan-dependent figures are derived cleanly from
WT_SENIOR_LOAN rather than reloaded over a live module.
"""
import os, subprocess, sys

REQUESTS = [10_000_000, 11_000_000, 8_000_000]
HERE = os.path.dirname(os.path.abspath(__file__))

for loan in REQUESTS:
    env = dict(os.environ, WT_SENIOR_LOAN=str(loan))
    print(f'\n{"═" * 70}\n  ${loan:,} request\n{"═" * 70}')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'v7_build.py')],
                       env=env, cwd=HERE, text=True, capture_output=True)
    print(r.stdout.rstrip())
    if r.returncode:
        print(r.stderr.rstrip())
        raise SystemExit(f'build failed at ${loan:,}')

print(f'\n{"═" * 70}\n  standalone marina valuation\n{"═" * 70}')
r = subprocess.run([sys.executable, os.path.join(HERE, 'v7_marina.py')],
                   cwd=HERE, text=True, capture_output=True)
print(r.stdout.rstrip())
if r.returncode:
    print(r.stderr.rstrip())
    raise SystemExit('marina deck build failed')
