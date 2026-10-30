# -*- coding: utf-8 -*-
"""Rebuild the page 9 Gantt from real dates. Axis and bars are computed, never hand-tuned."""
from datetime import date

AXIS0, AXIS1 = date(2026, 11, 1), date(2027, 5, 1)       # 181 days
SPAN = (AXIS1 - AXIS0).days
TICKS = [(date(2026, 11, 1), 'Nov'), (date(2026, 12, 1), 'Dec'), (date(2027, 1, 1), 'Jan'),
         (date(2027, 2, 1), 'Feb'), (date(2027, 3, 1), 'Mar'), (date(2027, 4, 1), 'Apr')]

MAIN_END = date(2027, 4, 15)
TASKS = [('Rooms renovation',                   date(2026, 11, 1), MAIN_END,          False),
         ('House renovation',                   date(2026, 11, 1), MAIN_END,          False),
         ('Exterior and interior FF&amp;E',     date(2026, 11, 1), MAIN_END,          False),
         ('Exterior and interior improvements', date(2026, 11, 1), MAIN_END,          False),
         ('Marina replacement',                 date(2026, 11, 1), date(2026, 12, 15), False),
         ('Event space upgrade',                date(2027, 1, 4),  date(2027, 2, 2),  False),
         ('Punch list to completion',           date(2027, 4, 1),  date(2027, 4, 30), True)]
START, COMPLETE = date(2026, 11, 1), date(2027, 4, 30)

pct = lambda d: (d - AXIS0).days / SPAN * 100
fmt = lambda d: f'{d:%b} {d.day}, {d.year}'
CON = ('font-family:var(--font-condensed);font-size:12px;font-weight:700;letter-spacing:.12em;'
       'text-transform:uppercase;color:var(--ink-500);')
ROW = ('display:grid;grid-template-columns:250px 1fr;column-gap:14px;align-items:center;'
       'padding:9px 0;border-bottom:1px solid var(--hairline);')
SUBHD = ('font-family:var(--font-condensed);font-size:14px;font-weight:700;letter-spacing:.18em;'
         'text-transform:uppercase;color:var(--mm-navy);border-bottom:1px solid var(--mm-navy);'
         'padding-bottom:9px;')
DATEROW = ('display:flex;justify-content:space-between;align-items:baseline;padding:7px 0;'
           'border-bottom:1px solid var(--hairline);')


PROSE = (f'Work begins <strong style="color:var(--mm-navy-900);">{AXIS0:%B %-d, %Y}</strong> and '
         f'completes <strong style="color:var(--mm-navy-900);">{COMPLETE:%B %-d, %Y}</strong>. The '
         'program runs entirely within the low season and completes before the 2027 summer peak '
         '&mdash; the four months to September carry 72% market occupancy against 40% from November '
         'to March.')

def left_column():
    out = (f'      <div style="{SUBHD}">Renovation Schedule &middot; '
           f'{AXIS0:%B %Y} to {COMPLETE:%B %Y}</div>\n'
           '      <div style="display:grid;grid-template-columns:250px 1fr;column-gap:14px;'
           'margin-top:14px;">\n        <div></div>\n'
           '        <div style="position:relative;height:20px;">\n')
    for d, lab in TICKS:
        out += f'          <span style="position:absolute;left:{pct(d):.2f}%;{CON}">{lab}</span>\n'
    out += '        </div>\n      </div>\n'
    for lab, s, e, accent in TASKS:
        col = 'var(--mm-orange)' if accent else 'var(--mm-navy)'
        out += (f'      <div style="{ROW}">\n'
                f'        <div style="font-family:var(--font-body);font-size:15px;'
                f'color:var(--ink-900);">{lab}</div>\n'
                '        <div style="position:relative;height:22px;">\n'
                '          <div style="position:absolute;inset:9px 0 auto 0;height:1px;'
                'background:var(--hairline);"></div>\n'
                f'          <div style="position:absolute;left:{pct(s):.2f}%;'
                f'width:{pct(e)-pct(s):.2f}%;top:3px;height:16px;background:{col};'
                'border-radius:2px;"></div>\n        </div>\n      </div>\n')
    out += ('      <div style="height:16px;"></div>\n'
            f'      <div style="{SUBHD}">Start and Completion Dates</div>\n')
    for lab, s, e, accent in TASKS:
        vc = 'var(--mm-orange);font-weight:700;' if accent else 'var(--ink-900);'
        out += (f'      <div style="{DATEROW}"><span style="font-family:var(--font-body);'
                f'font-size:15px;color:var(--ink-700);">{lab}</span>'
                f'<span style="font-family:var(--font-mono);font-size:15px;color:{vc}">'
                f'{fmt(s)} &rarr; {fmt(e)}</span></div>\n')
    out += ('      <p style="font-family:var(--font-body);max-width:none;font-size:15px;'
            'line-height:1.45;color:var(--ink-500);margin:auto 0 0;padding-top:14px;">'
            + PROSE + '</p>\n')
    return out


SPEAKER = (
 'The renovation schedule and the completed model room. Work starts November first, twenty twenty-six. '
 'Rooms, the house, exterior and interior FF and E and exterior and interior improvements all run from '
 'November first to April fifteenth, twenty twenty-seven. The marina is replaced between November first '
 'and December fifteenth, ahead of the winter. The event space is upgraded in January. Punch list runs '
 'April first to April thirtieth, twenty twenty-seven, which is the completion date the value estimate '
 'upon completion is dated to. The whole program sits inside the low season and finishes before the '
 'twenty twenty-seven summer peak. The model room is already built: finishes, casegoods, lighting, soft '
 'goods and bath are complete and can be inspected on site, so the twenty-five thousand dollars per key '
 'is priced against a room that exists rather than a drawing.')

# page 24 "Start and Completion Dates", grouped
BASIS_DATES = [('Rooms, house, FF&amp;E and exterior work', date(2026, 11, 1), MAIN_END),
               ('Marina replacement and expansion', date(2026, 11, 1), date(2026, 12, 15)),
               ('Event space upgrade', date(2027, 1, 4), date(2027, 2, 2)),
               ('Punch list to completion', date(2027, 4, 1), COMPLETE)]
