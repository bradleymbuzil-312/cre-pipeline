# -*- coding: utf-8 -*-
"""The equity teaser: valuation, the renovation plan and the revenue ramp, with no figures.

An investment-sales piece in form — photography led, generously set, little type on a page — and
an equity offering in substance. It carries no dollar amount, no percentage, no ratio, no key
count and no date, and no sources and uses. The three pillars are argued qualitatively: why the
basis sits where it does, what the renovation is and when it runs, and where the revenue comes
from once it is done.

The only digits in the file are the advisor's telephone, email and license on the closing page.
"""
import io
import re

from v7_lib import load_sections, DECKDIR

MONO = 'font-family:var(--font-mono);'
BODY = 'font-family:var(--font-body);'
DISP = 'font-family:var(--font-display);'
CON = 'font-family:var(--font-condensed);font-weight:700;text-transform:uppercase;'
HAIR = '1px solid var(--hairline)'
TAIL = '\n\n</x-import>\n</x-dc>\n</body>\n</html>\n'
LABEL = 'Equity Teaser'
NAVY, ORANGE = 'var(--mm-navy-900)', 'var(--mm-orange)'


# ── page furniture ───────────────────────────────────────────────────────────────────────────
def foot(dark=False):
    col = 'rgba(255,255,255,.42)' if dark else 'var(--ink-400)'
    return ('  <div style="margin-top:auto;display:flex;justify-content:space-between;'
            f'align-items:center;{CON}font-size:13px;letter-spacing:.22em;color:{col};'
            'padding-top:30px;">\n'
            '    <span>Wylder Hotel Tilghman Island</span>\n'
            '    <span>Marcus &amp; Millichap Capital Corporation &middot; The TRANCHE Group</span>\n'
            '  </div>\n')


def page(label, notes, inner, pad='74px 104px 54px'):
    return (f'<section data-label="{label}" data-screen-label="{label}" '
            f'data-speaker-notes="{notes}" '
            'style="width:100%;height:100%;box-sizing:border-box;background:var(--paper);'
            'color:var(--ink-900);font-family:var(--font-body);display:flex;'
            f'flex-direction:column;overflow:hidden;padding:{pad};">\n'
            + inner + foot() + '</section>')


def rule():
    return f'  <div style="width:64px;height:3px;background:{ORANGE};margin-bottom:26px;"></div>\n'


def h2(t, fs='44px', mb='30px'):
    return (f'  <h2 style="{DISP}font-weight:700;font-size:{fs};line-height:1.14;color:{NAVY};'
            f'margin:0 0 {mb};letter-spacing:-.01em;max-width:none;">{t}</h2>\n')


def eyebrow(t, col=None, mb='12px', ind=4):
    return (f'{" " * ind}<div style="{CON}font-size:12.5px;letter-spacing:.2em;'
            f'color:{col or ORANGE};margin-bottom:{mb};">{t}</div>\n')


def p(t, fs='17px', col='var(--ink-700)', mt='0', lh='1.62', ind=4, mw='none'):
    return (f'{" " * ind}<p style="{BODY}max-width:{mw};font-size:{fs};line-height:{lh};'
            f'color:{col};margin:{mt} 0 0;">{t}</p>\n')


def photo(src, alt, pos='center'):
    return (f'    <img src="assets/{src}" alt="{alt}" style="position:absolute;inset:0;'
            f'width:100%;height:100%;object-fit:cover;object-position:{pos};">\n')


# ── 01 · cover ───────────────────────────────────────────────────────────────────────────────
def cover():
    sn = ('Wylder Hotel Tilghman Island, a waterfront resort on the Chesapeake Bay in Talbot '
          'County, Maryland. An equity investment opportunity. This package sets out the '
          'valuation, the renovation plan and the revenue ramp. It states no figures.')
    return ('<section data-label="Cover" data-screen-label="Cover" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:space-between;padding:84px 104px;">\n'
     + photo('wt-aerial-spring.png', 'Wylder Hotel Tilghman Island from the air')
     + '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,'
       'rgba(0,17,34,.70) 0%,rgba(0,17,34,.30) 38%,rgba(0,17,34,.58) 72%,'
       'rgba(0,17,34,.94) 100%);"></div>\n'
     f'  <div style="position:absolute;right:0;top:0;bottom:0;width:10px;background:{ORANGE};'
       '"></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.26);padding-bottom:26px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:56px;">\n'
     f'    <span style="{CON}font-size:14px;letter-spacing:.26em;'
     'color:var(--mm-orange-100);">Confidential &middot; Equity Investment</span>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;">\n'
     f'    <div style="{CON}font-size:15px;letter-spacing:.3em;color:{ORANGE};'
     'margin-bottom:22px;">An Equity Investment Opportunity</div>\n'
     f'    <h1 style="{DISP}font-weight:700;font-size:92px;line-height:1.02;color:#fff;'
     'margin:0;letter-spacing:-.022em;max-width:none;">Wylder Hotel<br>Tilghman Island</h1>\n'
     f'    <p style="{BODY}max-width:none;font-size:23px;line-height:1.5;'
     'color:rgba(255,255,255,.88);margin:26px 0 0;">A waterfront resort between the Chesapeake '
     'Bay and the Choptank River &mdash; under renovation, under the Wylder Hotels brand, '
     'and open to equity alongside the sponsor.</p>\n'
     '    <div style="margin-top:34px;padding-top:24px;border-top:1px solid '
     'rgba(255,255,255,.26);display:flex;justify-content:space-between;align-items:flex-end;">\n'
     f'      <span style="{CON}font-size:14px;letter-spacing:.22em;'
     'color:rgba(255,255,255,.72);">Tilghman Island &middot; Talbot County &middot; '
     'Maryland</span>\n'
     f'      <span style="{CON}font-size:14px;letter-spacing:.22em;'
     'color:rgba(255,255,255,.72);">Marcus &amp; Millichap Capital Corporation &middot; '
     'The TRANCHE Group</span>\n    </div>\n  </div>\n</section>')


# ── full-bleed section divider ───────────────────────────────────────────────────────────────
def divider(label, kicker, title, lede, src, alt, pos='center', notes=''):
    return ('<section data-label="' + label + '" data-screen-label="' + label + '" '
     f'data-speaker-notes="{notes}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:flex-end;padding:84px 104px 76px;">\n'
     + photo(src, alt, pos)
     + '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,'
       'rgba(0,17,34,.30) 0%,rgba(0,17,34,.30) 34%,rgba(0,17,34,.80) 100%);"></div>\n'
     '  <div style="position:relative;z-index:2;max-width:1180px;">\n'
     f'    <div style="{CON}font-size:14px;letter-spacing:.3em;color:{ORANGE};'
     f'margin-bottom:18px;">{kicker}</div>\n'
     f'    <h2 style="{DISP}font-weight:700;font-size:70px;line-height:1.06;color:#fff;'
     f'margin:0;letter-spacing:-.018em;max-width:none;">{title}</h2>\n'
     f'    <p style="{BODY}max-width:none;font-size:21px;line-height:1.55;'
     f'color:rgba(255,255,255,.86);margin:24px 0 0;">{lede}</p>\n  </div>\n</section>')


# ── 02 · the opportunity ─────────────────────────────────────────────────────────────────────
PILLARS = [
  ('Valuation', 'The basis is set by what the asset cost to assemble and improve, not by what a '
                'stabilized waterfront resort trades for. The gap between the two is the '
                'investment case.'),
  ('The Renovation', 'Designed, priced, scheduled and already under way, with the guest-room '
                     'specification built and standing on site. It starts in the quiet months and '
                     'delivers in waves, so the hotel never goes dark.'),
  ('The Revenue Ramp', 'Renovated rooms at a higher rate, keys returned to inventory, and whole '
                       'departments &mdash; marina, bar, events, a private residence &mdash; that '
                       'the property has never sold.')]


def opportunity():
    sn = ('An established waterfront resort, mid-repositioning. The case rests on three things: '
          'where the basis sits against value, a renovation that is designed, priced and under '
          'way, and a revenue ramp that comes from rate, from inventory returned to service and '
          'from departments the property has never sold.')
    left = (rule() + h2('An established resort,<br>mid&#8209;repositioning.')
      + p('Wylder Hotel Tilghman Island is a waterfront resort on Tilghman Island, at the mouth '
          'of the Choptank River on Maryland&rsquo;s Eastern Shore. It is open, operating and '
          'under the Wylder Hotels brand, and it is part of the way through a repositioning that '
          'the sponsor has been funding from its own capital.', fs='18px', mt='0')
      + p('What remains is the part that changes the economics: a full renovation of the guest '
          'rooms, a rebuilt and expanded marina, a replaced residence, reworked public space, and '
          'an adjacent waterfront parcel under contract that brings further slips and a private '
          'whole&#8209;home suite into the resort.', fs='18px', mt='20px')
      + p('The sponsor is seeking equity to complete that work alongside the capital it has '
          'already committed. This package sets out the three things that matter to that '
          'decision and states no figures; the model, the operating history and the full '
          'capitalization follow under a confidentiality agreement.', fs='18px', mt='20px'))
    right = ''
    for i, (t, d) in enumerate(PILLARS):
        bb = '' if i == len(PILLARS) - 1 else f'border-bottom:{HAIR};'
        right += (f'      <div style="padding:{"0 0 28px" if i == 0 else "28px 0"};{bb}">\n'
                  + eyebrow(f'{"One" if i == 0 else "Two" if i == 1 else "Three"}', ind=8)
                  + f'        <div style="{DISP}font-weight:700;font-size:27px;color:{NAVY};'
                    'line-height:1.15;">' + t + '</div>\n'
                  + p(d, fs='16.5px', mt='11px', ind=8) + '      </div>\n')
    strip = ('  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:26px;'
             'margin-top:auto;padding-top:34px;">\n')
    for src, alt, cap in (('wt-pool.png', 'The pool and grounds', 'The pool and the grounds'),
                          ('wt-fb-signs.jpg', 'The boat bar', 'The boat bar and restaurant'),
                          ('wt-dogwood-aerial.jpg', 'The marina', 'The marina and the water')):
        strip += ('    <div>\n'
                  '      <div style="position:relative;overflow:hidden;height:236px;">\n'
                  + photo(src, alt) + '      </div>\n'
                  + eyebrow(cap, col='var(--ink-400)', ind=6, mb='0') + '    </div>\n')
    strip += '  </div>\n'
    return page('The Opportunity', sn,
      '  <div style="display:grid;grid-template-columns:1.18fr 1fr;gap:72px;'
      'align-items:start;">\n    <div>\n' + left + '    </div>\n'
      '    <div style="border-left:' + HAIR + ';padding-left:52px;">\n' + right
      + '    </div>\n  </div>\n' + strip, pad='70px 104px 46px')


# ── 03 · the asset ───────────────────────────────────────────────────────────────────────────
FACTS = [
  ('Setting', 'A waterfront parcel on Tilghman Island, with frontage on both the Chesapeake Bay '
              'and the Choptank River'),
  ('The Resort', 'Guest rooms, a pool, a restaurant, a boat bar, event space and a marina, on a '
                 'single contiguous site'),
  ('Positioning', 'Upper upscale, select service &mdash; a resort that sells the water, not a '
                  'full&#8209;service box'),
  ('Operator', 'Operated under the Wylder Hotels brand, with a soft&#8209;brand affiliation '
               'planned on completion'),
  ('Adjacent Parcel', 'A neighboring waterfront property under contract, adding slips, acreage '
                      'and a private residence')]


def asset():
    sn = ('The asset. A waterfront parcel on Tilghman Island with frontage on the Chesapeake Bay '
          'and the Choptank River. Guest rooms, a pool, a restaurant, a boat bar, event space and '
          'a marina on one contiguous site, with a neighboring waterfront property under '
          'contract.')
    right = ''
    for i, (k, v) in enumerate(FACTS):
        bb = '' if i == len(FACTS) - 1 else f'border-bottom:{HAIR};'
        right += (f'      <div style="padding:{"0 0 21px" if i == 0 else "21px 0"};{bb}">\n'
                  + eyebrow(k, ind=8, mb='7px')
                  + p(v, fs='16.5px', col='var(--ink-900)', mt='0', lh='1.5', ind=8)
                  + '      </div>\n')
    return page('The Asset', sn,
      rule() + h2('Water on both sides, and one way on and off the island.', mb='26px')
      + '  <div style="display:grid;grid-template-columns:1.3fr 1fr;gap:56px;flex:1;'
        'align-items:stretch;grid-template-rows:1fr;min-height:0;">\n'
      '    <div style="position:relative;overflow:hidden;">\n'
      + photo('wt-aerial.png', 'The resort and its marina from the air')
      + '    </div>\n    <div style="display:flex;flex-direction:column;justify-content:center;">\n'
      + right + '    </div>\n  </div>\n', pad='70px 104px 50px')


# ── 05 · valuation ───────────────────────────────────────────────────────────────────────────
# schematic only: the bars carry no scale, no axis and no value, and the slide says so
LADDER = [('As It Stands', 34, 'An operating resort, part&#8209;renovated, selling a rate the '
                               'rooms no longer justify', 'var(--ink-400)'),
          ('On Completion', 66, 'Every room renovated, the marina rebuilt and expanded, the '
                                'residence replaced', 'var(--mm-navy)'),
          ('At Stabilization', 100, 'A full season behind it, the affiliation live and every '
                                    'department selling', 'var(--mm-orange)')]
UNDERPINS = [
  ('Waterfront cannot be added to', 'There is a finite quantity of improved deep&#8209;water '
   'frontage on the mid&#8209;Shore, and essentially none of it is being created. A competing '
   'resort cannot be built across the road; it has to be bought.'),
  ('The marina is its own asset', 'Slips are valued on their own terms, against slip sales and '
   'slip rents in the surrounding creeks, and they carry almost no operating overhead. The '
   'adjacent parcel roughly doubles the slip count.'),
  ('A basis set by cost, not by trade', 'The sponsor&rsquo;s basis reflects what it has paid to '
   'assemble and improve the property. A stabilized waterfront resort on the Bay does not change '
   'hands on that measure.'),
  ('Income, once it is there', 'On completion the asset is valued the way resorts are valued &mdash; '
   'on what it earns. Every argument in the two sections that follow is an argument about that '
   'number.')]


def valuation():
    sn = ('Valuation. The case is the distance between a basis set by what the property cost to '
          'assemble and improve, and what a stabilized waterfront resort on the Chesapeake is '
          'worth. It is underpinned by scarcity of improved deep water frontage, by a marina '
          'valued on its own terms, and by income once the asset is stabilized. The chart is '
          'schematic. No value and no projection is stated in this package.')
    bars = ('    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;'
            'align-items:end;height:368px;margin-top:10px;">\n')
    for lab, h, _d, col in LADDER:
        bars += ('      <div style="display:flex;flex-direction:column;justify-content:flex-end;'
                 'height:100%;">\n'
                 f'        <div style="height:{h}%;background:{col};'
                 f'{"opacity:.34;" if col == "var(--ink-400)" else ""}"></div>\n      </div>\n')
    bars += '    </div>\n'
    labs = ('    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;'
            f'border-top:2px solid {NAVY};padding-top:16px;">\n')
    for lab, _h, d, col in LADDER:
        labs += ('      <div>\n'
                 f'        <div style="{CON}font-size:13px;letter-spacing:.16em;color:{NAVY};'
                 f'">{lab}</div>\n' + p(d, fs='14.5px', mt='9px', lh='1.45', ind=8)
                 + '      </div>\n')
    labs += '    </div>\n'
    right = eyebrow('What Underpins It', mb='18px')
    for i, (t, d) in enumerate(UNDERPINS):
        bb = '' if i == len(UNDERPINS) - 1 else f'border-bottom:{HAIR};'
        right += (f'    <div style="padding:{"0 0 18px" if i == 0 else "18px 0"};{bb}">\n'
                  f'      <div style="{BODY}font-weight:600;font-size:17.5px;color:{NAVY};'
                  f'line-height:1.3;">{t}</div>\n'
                  + p(d, fs='15.5px', mt='9px', lh='1.55', ind=6) + '    </div>\n')
    return page('Valuation', sn,
      rule() + h2('The whole case is the distance between cost and worth.', mb='24px')
      + '  <div style="display:grid;grid-template-columns:1.12fr 1fr;gap:64px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;">\n'
      + eyebrow('The Value Ladder', mb='4px') + bars + labs
      + p('Schematic only. The bars carry no scale and no value, and this package states '
          'neither. What it does say is the order: the asset is worth less today than it will be '
          'with the work done, and less with the work done than it will be with a season behind '
          'it. The underwriting behind that order is available on request.',
          fs='14.5px', mt='auto', lh='1.5', ind=4)
      + '    </div>\n    <div style="display:flex;flex-direction:column;'
        'justify-content:space-between;border-left:' + HAIR
      + ';padding-left:48px;">\n' + right + '    </div>\n  </div>\n')


# ── 07 · the renovation, by area ─────────────────────────────────────────────────────────────
SCOPE = [
  ('Guest rooms', 'Every room rebuilt &mdash; finishes, casegoods, lighting, soft goods and bath '
                  'to a single specification.'),
  ('Inventory returned', 'Rooms long out of service come back, and further keys are added in the '
                         'back house. Sellable inventory that has never produced revenue.'),
  ('The marina', 'Slips replaced and the dock expanded, with the adjacent parcel bringing further '
                 'slips into the same operation.'),
  ('The residence', 'The waterfront house on the property is replaced rather than patched, and '
                    'let as a whole&#8209;home suite.'),
  ('Public space and furnishings', 'Lobby, restaurant and the shared interiors reworked, with '
                                   'furniture, fixtures and equipment throughout.'),
  ('The boat bar', 'Reconfigured into a room that sells through the season rather than on '
                   'weekends in high summer.'),
  ('Event space', 'Upgraded for weddings and buyouts, the demand this stretch of shoreline '
                  'already generates and the property has been turning away.'),
  ('The adjacent residence', 'The neighboring house brought online as a private whole&#8209;home '
                             'suite, with its own water frontage.')]


def scope():
    sn = ('The renovation by area. Every guest room rebuilt to one specification. Rooms long out '
          'of service returned and further keys added. The marina replaced and expanded. The '
          'waterfront residence replaced. Public space, furnishings, the boat bar and the event '
          'space reworked, and the adjacent residence brought online as a whole home suite.')
    cells = ''
    for i, (t, d) in enumerate(SCOPE):
        bb = '' if i >= len(SCOPE) - 2 else f'border-bottom:{HAIR};'
        cells += (f'      <div style="padding:{"0 0 22px" if i < 2 else "22px 0"};{bb}">\n'
                  '        <div style="display:flex;align-items:center;gap:11px;">'
                  f'<span style="width:7px;height:7px;background:{ORANGE};flex:none;"></span>'
                  f'<span style="{BODY}font-weight:600;font-size:18.5px;color:{NAVY};">{t}</span>'
                  '</div>\n' + p(d, fs='16px', mt='8px', lh='1.55', ind=8) + '      </div>\n')
    return page('The Renovation &middot; Scope', sn,
      rule() + h2('What is actually being built.', mb='26px')
      + '  <div style="display:grid;grid-template-columns:1.62fr .82fr;gap:56px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 48px;'
        'align-content:space-between;">\n' + cells + '    </div>\n'
      '    <div style="position:relative;overflow:hidden;">\n'
      + photo('wt-lobby.png', 'Interior of the resort', 'center')
      + '    </div>\n  </div>\n', pad='70px 104px 50px')


# ── 08 · the renovation, when it runs ────────────────────────────────────────────────────────
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
BANDS = [('Guest rooms &middot; four waves', 1, 7), ('The residence', 1, 7),
         ('Furnishings and fittings', 2, 7), ('Exterior and interior works', 1, 4),
         ('Marina replacement', 1, 3), ('Event space upgrade', 3, 5),
         ('Punch list to completion', 5, 7)]


def schedule():
    sn = ('When the renovation runs. Work begins in November and completes in April. The whole '
          'program begins in the depth of winter, when the property earns least, and guest rooms '
          'come back in four waves rather than all at once, so the hotel keeps selling throughout '
          'and the last wave lands for the back half of the season. The model room is already '
          'built and can be inspected on site, which takes design and specification risk out of '
          'the remaining rooms.')
    head = ('    <div style="display:grid;grid-template-columns:230px repeat(6,1fr);gap:0 10px;'
            f'border-bottom:2px solid {NAVY};padding-bottom:9px;margin-bottom:6px;">\n'
            '      <div></div>\n')
    for m in MONTHS:
        head += (f'      <div style="{CON}font-size:12.5px;letter-spacing:.16em;'
                 f'color:{NAVY};text-align:center;">{m}</div>\n')
    head += '    </div>\n'
    rows = ''
    for i, (lab, a, b) in enumerate(BANDS):
        rows += ('    <div style="display:grid;grid-template-columns:230px repeat(6,1fr);'
                 f'gap:0 10px;align-items:center;padding:11px 0;border-bottom:{HAIR};">\n'
                 f'      <div style="{BODY}font-size:15.5px;color:var(--ink-900);">{lab}</div>\n'
                 f'      <div style="grid-column:{a + 1} / {b + 1};height:13px;'
                 f'background:{ORANGE if b - a <= 2 else "var(--mm-navy)"};"></div>\n    </div>\n')
    return page('The Renovation &middot; Schedule', sn,
      rule() + h2('It starts in the quiet months, and delivers wave by wave.', mb='26px')
      + '  <div style="display:grid;grid-template-columns:1.28fr .88fr;gap:58px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n    <div style="display:flex;flex-direction:column;">\n'
      + eyebrow('Program Sequence', mb='14px') + head + rows
      + p('Work starts in the new year and finishes at the end of June. It opens in the months '
          'the property earns least, and because the rooms come back in waves the hotel trades '
          'through the whole program rather than closing for it.',
          fs='15px', mt='auto', lh='1.55', ind=4)
      + '    </div>\n'
      '    <div style="display:flex;flex-direction:column;">\n'
      '      <div style="position:relative;overflow:hidden;flex:1;min-height:0;">\n'
      + photo('wt-dogwood-house.jpg', 'The adjacent waterfront residence')
      + '      </div>\n'
      f'      <div style="background:{NAVY};color:#fff;padding:22px 26px;margin-top:20px;">\n'
      + eyebrow('The Model Room Is Already Built', ind=8, mb='9px')
      + p('The guest&#8209;room specification is finished and standing on site, and can be walked '
          'before a dollar is committed. The rooms that follow are a rollout of something that '
          'exists rather than a drawing.', fs='15px', col='rgba(255,255,255,.88)', mt='0',
          lh='1.5', ind=8)
      + '      </div>\n    </div>\n  </div>\n', pad='70px 104px 50px')


# ── 10 · the revenue ramp ────────────────────────────────────────────────────────────────────
STAGES = [('Today', 28, 'Tired rooms, a short selling season and a rate the market will not pay '
                        'twice'),
          ('The Work', 44, 'Rooms returning in waves, with the hotel trading throughout and the '
                           'program running around it'),
          ('First Full Season', 80, 'Renovated rooms, the marina back, the residences let and '
                                    'every room sellable'),
          ('Stabilized', 100, 'The affiliation live, the shoulder season working and the new '
                              'departments trading through the year')]
DRIVERS = [
  ('Rate', 'The rooms are being sold today at a rate a renovated waterfront resort does not '
           'accept. The comparable set on this stretch of shore holds a materially higher rate '
           'the whole season. The renovation is what closes that gap; the specification is '
           'already built and can be inspected.'),
  ('Inventory', 'Rooms that have sat out of service come back, and further keys are added within '
                'the existing footprint. That is inventory the property already owns, already '
                'heats and already insures, and has never been able to sell.'),
  ('Departments', 'The marina, the bar, the event space and the whole&#8209;home residences are '
                  'either new or being rebuilt. They carry very little operating overhead, so '
                  'what they bring in largely stays in.')]


def ramp():
    sn = ('The revenue ramp. It is rate first, then rooms, then whole departments. Rooms are sold '
          'today at a rate a renovated waterfront resort does not accept. Rooms long out of '
          'service come back within the existing footprint. The marina, the bar, the event space '
          'and the residences are new or rebuilt and carry very little overhead. The chart is '
          'schematic and no projection is stated in this package.')
    bars = ('    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;'
            'align-items:end;height:188px;">\n')
    for i, (_l, h, _d) in enumerate(STAGES):
        col = ORANGE if i == len(STAGES) - 1 else 'var(--mm-navy)'
        op = f'opacity:{.30 + .23 * i:.2f};' if i < len(STAGES) - 1 else ''
        bars += ('      <div style="display:flex;flex-direction:column;justify-content:flex-end;'
                 f'height:100%;"><div style="height:{h}%;background:{col};{op}"></div></div>\n')
    bars += '    </div>\n'
    labs = ('    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;'
            f'border-top:2px solid {NAVY};padding-top:14px;margin-bottom:30px;">\n')
    for lab, _h, d in STAGES:
        labs += ('      <div>\n'
                 f'        <div style="{CON}font-size:12.5px;letter-spacing:.16em;color:{NAVY};'
                 f'">{lab}</div>\n' + p(d, fs='14px', mt='8px', lh='1.42', ind=8) + '      </div>\n')
    labs += '    </div>\n'
    dr = ('    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 44px;'
          f'border-top:{HAIR};padding-top:26px;">\n')
    for i, (t, d) in enumerate(DRIVERS):
        bl = '' if i == 0 else f'border-left:{HAIR};padding-left:44px;'
        dr += (f'      <div style="{bl}">\n' + eyebrow(f'Driver {"One" if i == 0 else "Two" if i == 1 else "Three"}', ind=8, mb='8px')
               + f'        <div style="{DISP}font-weight:700;font-size:25px;color:{NAVY};'
                 f'line-height:1.15;">{t}</div>\n'
               + p(d, fs='15px', mt='10px', lh='1.5', ind=8) + '      </div>\n')
    dr += '    </div>\n'
    return page('The Revenue Ramp', sn,
      rule() + h2('Rate first, then rooms, then whole departments.', mb='22px')
      + bars + labs + dr
      + p('Schematic only. The steps carry no scale and this package states no projection. The '
          'sequence, and what sits behind each step, is set out in full in the model.',
          fs='14px', mt='auto', lh='1.5', ind=4), pad='66px 104px 46px')


# ── 11 · where the revenue comes from ────────────────────────────────────────────────────────
SOURCES = [
  ('Guest rooms', 'Sold at a rate the rooms no longer support, across a short season',
   'Every room renovated to one specification, with rooms long out of service back in '
   'inventory and further keys added'),
  ('The marina', 'A modest number of slips, aging, and let well below what the creeks around it '
                 'achieve',
   'Slips replaced and the count sharply increased with the adjacent parcel &mdash; a department '
   'with almost no overhead attached to it'),
  ('Food and beverage', 'A restaurant and a boat bar trading hard in high summer and quiet either '
                        'side of it',
   'Reconfigured to sell through the shoulder season, to marina traffic and to event business as '
   'well as to house guests'),
  ('Events', 'Weddings and buyouts the property turns away for want of a room to put them in',
   'Dedicated event space, with renovated rooms and whole&#8209;home residences to hold the party '
   'that comes with it'),
  ('The residences', 'One tired house on the property, and nothing next door',
   'A replaced waterfront house and the adjacent residence, both let whole&#8209;home at the top '
   'of the rate card')]


def sources():
    sn = ('Where the revenue comes from. Five departments. Guest rooms, the marina, food and '
          'beverage, events and the whole home residences. Three of the five are either new or '
          'being rebuilt, and the property has never sold them.')
    rows = ('    <div style="display:grid;grid-template-columns:230px 1fr 1fr;gap:0 44px;'
            f'border-bottom:2px solid {NAVY};padding-bottom:10px;">\n'
            '      <div></div>\n'
            + eyebrow('As It Stands', col='var(--ink-400)', ind=6, mb='0')
            + eyebrow('With the Work Done', ind=6, mb='0') + '    </div>\n')
    for i, (t, a, b) in enumerate(SOURCES):
        bb = '' if i == len(SOURCES) - 1 else f'border-bottom:{HAIR};'
        rows += ('    <div style="display:grid;grid-template-columns:230px 1fr 1fr;gap:0 44px;'
                 f'padding:42px 0;{bb}align-items:start;">\n'
                 f'      <div style="{BODY}font-weight:600;font-size:20px;color:{NAVY};'
                 f'line-height:1.25;">{t}</div>\n'
                 + p(a, fs='16.5px', col='var(--ink-500)', mt='0', lh='1.58', ind=6)
                 + p(b, fs='16.5px', col='var(--ink-900)', mt='0', lh='1.58', ind=6)
                 + '    </div>\n')
    return page('Revenue Sources', sn,
      rule() + h2('Five departments. Three of them barely exist today.', mb='26px')
      + rows
      + p('The right&#8209;hand column is the business plan. Nothing in it depends on the market '
          'moving &mdash; it depends on the work being finished and the departments being opened.',
          fs='15px', mt='auto', lh='1.55', ind=4), pad='68px 104px 48px')


# ── 12 · brand and distribution ──────────────────────────────────────────────────────────────
DIST = [
  ('The Wylder brand', 'The property already trades under Wylder Hotels, a boutique brand that '
   'buys, restores and operates resorts in drive&#8209;to leisure markets. It is not being '
   'rebranded; it is being finished.'),
  ('A soft&#8209;brand affiliation, on completion', 'A Small Luxury Hotels affiliation is planned '
   'once the renovation is done. SLH member hotels are bookable through Hilton&rsquo;s site, app '
   'and loyalty program, which moves the resort out of dependence on direct booking and the '
   'online travel agents.'),
  ('A relationship that already works', 'The sponsor&rsquo;s sister resort in the Catskills is an '
   'SLH member &mdash; the first in that market &mdash; and carries the American Express Fine '
   'Hotels &amp; Resorts designation. This is an extension of a working relationship, not a cold '
   'application.'),
  ('Why it matters here', 'Rate on the Eastern Shore is made in the shoulder months, and the '
   'shoulder months are made by distribution. The affiliation is the mechanism behind the rate '
   'and occupancy the plan assumes.')]


def brand():
    sn = ('Brand and distribution. The property already trades under the Wylder Hotels brand. A '
          'Small Luxury Hotels affiliation is planned on completion of the renovation, which '
          'makes the resort bookable through Hilton channels and loyalty. The sponsor already '
          'operates an SLH member in the Catskills carrying the American Express Fine Hotels and '
          'Resorts designation.')
    right = ''
    for i, (t, d) in enumerate(DIST):
        bb = '' if i == len(DIST) - 1 else f'border-bottom:{HAIR};'
        right += (f'      <div style="padding:{"0 0 20px" if i == 0 else "20px 0"};{bb}">\n'
                  f'        <div style="{BODY}font-weight:600;font-size:18px;color:{NAVY};'
                  f'line-height:1.3;">{t}</div>\n'
                  + p(d, fs='15.5px', mt='8px', lh='1.5', ind=8) + '      </div>\n')
    return page('Brand and Distribution', sn,
      rule() + h2('Rate is made in the shoulder months, and distribution makes the shoulder '
                  'months.', mb='26px')
      + '  <div style="display:grid;grid-template-columns:.9fr 1.22fr;gap:56px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="position:relative;overflow:hidden;">\n'
      + photo('wt-pool.png', 'The pool and grounds at the resort')
      + '    </div>\n'
      '    <div style="display:flex;flex-direction:column;justify-content:center;">\n'
      + right
      + p('Affiliation is targeted on completion of the renovation and remains subject to '
          'application, inspection, board approval and an executed brand agreement.',
          fs='13.5px', col='var(--ink-400)', mt='22px', lh='1.5', ind=6)
      + '    </div>\n  </div>\n', pad='70px 104px 50px')


# ── 13 · the sponsor ─────────────────────────────────────────────────────────────────────────
SPONSOR = [
  ('Owner&#8209;operated', 'Day&#8209;to&#8209;day operations and the renovation are run by an '
   'affiliate of ownership. There is no third&#8209;party management agreement to terminate and '
   'no split incentive between the owner and the operator.'),
  ('Continuous ownership', 'The sponsor has owned and operated this hotel under the Wylder brand '
   'through the pandemic cycle and the current repositioning, and has put further capital in '
   'along the way.'),
  ('A single&#8209;asset entity', 'The ownership entity holds this property and, on closing, the '
   'adjacent parcel &mdash; and nothing else &mdash; keeping the asset and its cash flow '
   'ring&#8209;fenced.'),
  ('A platform behind it', 'Revenue management, distribution, design and procurement are shared '
   'across the two Wylder resorts, giving a property of this size a reach it could not support '
   'standing alone.')]


def sponsor():
    sn = ('The sponsor. Wylder Hotels, founded and led by John Flannigan, who has spent three '
          'decades in hospitality including chief operating officer of Proper Hospitality and '
          'president of JRK Hotels. The property is owner operated with no third party manager, '
          'held in a single asset entity, and supported by the platform behind the two Wylder '
          'resorts.')
    blocks = ''
    for i, (t, d) in enumerate(SPONSOR):
        bb = '' if i == len(SPONSOR) - 1 else f'border-bottom:{HAIR};'
        blocks += (f'      <div style="padding:{"0 0 22px" if i == 0 else "22px 0"};{bb}">\n'
                   f'        <div style="display:flex;align-items:center;gap:11px;">'
                   f'<span style="width:7px;height:7px;background:{ORANGE};flex:none;"></span>'
                   f'<span style="{BODY}font-weight:600;font-size:18.5px;color:{NAVY};">{t}</span>'
                   '</div>\n' + p(d, fs='16px', mt='9px', lh='1.55', ind=8) + '      </div>\n')
    return page('The Sponsor', sn,
      rule() + h2('Owner&#8209;operated, and already living with the decision.', mb='28px')
      + '  <div style="display:grid;grid-template-columns:1fr 1.02fr;gap:62px;'
        'grid-template-rows:1fr;flex:1;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;'
        'justify-content:space-between;">\n'
      + eyebrow('Structure and Alignment', mb='18px') + blocks + '    </div>\n'
      f'    <div style="display:flex;flex-direction:column;border-left:{HAIR};'
        'padding-left:52px;">\n'
      + eyebrow('The Operator', mb='18px')
      + f'      <div style="{DISP}font-weight:700;font-size:34px;color:{NAVY};'
        'line-height:1.12;">Wylder Hotels</div>\n'
      + p('A boutique brand that acquires, renovates and operates resorts in drive&#8209;to '
          'leisure markets, founded and led by John Flannigan. Before Wylder he was chief '
          'operating officer of Proper Hospitality and president of JRK Hotels, across roughly '
          'three decades in hospitality.', fs='17px', mt='14px', lh='1.6', ind=6)
      + f'      <div style="margin-top:28px;padding-top:26px;border-top:{HAIR};">\n'
      + eyebrow('The Proof Case', ind=8, mb='10px')
      + p('The sister resort in the Catskills opened after a substantial program of investment '
          'and was named the leading resort in New York State the following year. It is a Small '
          'Luxury Hotels member, the first in that market, holds the American Express Fine Hotels '
          '&amp; Resorts designation, sits among Travel + Leisure&rsquo;s World&rsquo;s Best and '
          'is a MICHELIN Guide selection.', fs='16.5px', mt='0', lh='1.6', ind=8)
      + '      </div>\n'
      f'      <div style="margin-top:auto;padding-top:26px;border-top:{HAIR};">\n'
      + p('Tilghman Island follows the same path &mdash; the same ownership, the same management '
          'company, the same brand platform and the same affiliation route &mdash; on an asset '
          'with water on both sides and a marina the Catskills could never have.',
          fs='16.5px', col=NAVY, mt='0', lh='1.6', ind=8)
      + '      </div>\n    </div>\n  </div>\n', pad='70px 104px 50px')

# ── 14 · the invitation ──────────────────────────────────────────────────────────────────────
NEXT = [('What is open', 'Equity alongside the sponsor&rsquo;s own capital, in a structure to be '
                         'agreed with the lead investor.'),
        ('What follows', 'The financial model, the operating history, the renovation budget and '
                         'schedule, the contract on the adjacent parcel and sponsor materials.'),
        ('How it starts', 'An indication of interest and a confidentiality agreement. Site visits '
                          'are welcome; the model room can be walked.')]


def invitation():
    sn = ('The invitation. Equity alongside the sponsor in a structure to be agreed with the lead '
          'investor. The financial model, the operating history, the renovation budget and '
          'schedule, the contract on the adjacent parcel and sponsor materials follow under a '
          'confidentiality agreement. Site visits are welcome and the model room can be walked. '
          'Bradley M. Buzil, Senior Director, The TRANCHE Group at Marcus and Millichap Capital '
          'Corporation.')
    cols = ('  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 52px;'
            'margin-top:44px;">\n')
    for i, (t, d) in enumerate(NEXT):
        bl = '' if i == 0 else 'border-left:1px solid rgba(255,255,255,.2);padding-left:52px;'
        cols += (f'    <div style="{bl}">\n' + eyebrow(t, ind=6, mb='10px')
                 + p(d, fs='16.5px', col='rgba(255,255,255,.86)', mt='0', lh='1.55', ind=6)
                 + '    </div>\n')
    cols += '  </div>\n'
    return ('<section data-label="The Invitation" data-screen-label="The Invitation" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:space-between;padding:78px 104px 66px;'
     f'background:{NAVY};">\n'
     f'  <div style="position:absolute;right:0;top:0;bottom:0;width:10px;background:{ORANGE};'
       '"></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.22);padding-bottom:24px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:48px;">\n'
     f'    <span style="{CON}font-size:13.5px;letter-spacing:.26em;'
     'color:var(--mm-orange-100);">Confidential &middot; Equity Investment</span>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;flex:1;display:flex;flex-direction:column;'
     'justify-content:center;padding:44px 0;">\n'
     f'    <div style="width:64px;height:3px;background:{ORANGE};margin-bottom:24px;"></div>\n'
     f'    <h2 style="{DISP}font-weight:700;font-size:54px;line-height:1.1;color:#fff;margin:0;'
     'letter-spacing:-.016em;max-width:none;">An invitation, not an offer.</h2>\n'
     + p('Nothing in this package is a solicitation or a proposal of terms. It is a description '
         'of an asset, a plan and a case, put to investors who buy waterfront resorts and '
         'understand what a renovation season costs and returns. The economics are open and will '
         'be set with the lead investor.', fs='19px', col='rgba(255,255,255,.88)', mt='22px',
         lh='1.55', ind=4)
     + cols + '  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:flex-end;border-top:1px solid rgba(255,255,255,.22);padding-top:26px;">\n'
     '    <div>\n'
     f'      <div style="{DISP}font-weight:700;font-size:25px;color:#fff;line-height:1.2;">'
     'Bradley M. Buzil</div>\n'
     f'      <div style="{BODY}font-size:16px;color:rgba(255,255,255,.72);margin-top:5px;">'
     'Senior Director &middot; The TRANCHE Group</div>\n'
     f'      <div style="{MONO}font-size:15px;color:{ORANGE};margin-top:11px;letter-spacing:.02em;">'
     '310.909.5473 &nbsp;&middot;&nbsp; bradley.buzil@marcusmillichap.com</div>\n'
     f'      <div style="{BODY}font-size:13px;color:rgba(255,255,255,.5);margin-top:8px;">'
     'CA DRE Lic. 01927157</div>\n    </div>\n'
     f'    <div style="text-align:right;{CON}font-size:13px;letter-spacing:.2em;'
     'color:rgba(255,255,255,.55);line-height:1.9;">Marcus &amp; Millichap Capital '
     'Corporation<br>Exclusive Capital Advisor</div>\n  </div>\n</section>')


# ── assembly ─────────────────────────────────────────────────────────────────────────────────
PAGES = [
  ('COVER', cover),
  ('THE OPPORTUNITY', opportunity),
  ('THE ASSET', asset),
  ('DIVIDER VALUATION', lambda: divider(
      'Valuation', 'One', 'Valuation',
      'An asset carried at what it cost to assemble and improve, on a shoreline where nothing '
      'comparable is being built.', 'wt-pier.png', 'The pier at dusk', 'center',
      'Section one. Valuation.')),
  ('VALUATION', valuation),
  ('DIVIDER RENOVATION', lambda: divider(
      'The Renovation', 'Two', 'The renovation plan',
      'Designed, priced, scheduled and delivered in waves &mdash; with the guest&#8209;room '
      'specification already standing on site.', 'wt-suite.jpg', 'A renovated guest room', 'center',
      'Section two. The renovation plan.')),
  ('RENOVATION SCOPE', scope),
  ('RENOVATION SCHEDULE', schedule),
  ('DIVIDER REVENUE', lambda: divider(
      'The Revenue Ramp', 'Three', 'The revenue ramp',
      'Rate the rooms will finally support, inventory the property already owns, and departments '
      'it has never been able to sell.', 'wt-dogwood-aerial.jpg',
      'The marina and the adjacent waterfront parcel', 'center',
      'Section three. The revenue ramp.')),
  ('REVENUE RAMP', ramp),
  ('REVENUE SOURCES', sources),
  ('BRAND AND DISTRIBUTION', brand),
  ('THE SPONSOR', sponsor),
  ('THE INVITATION', invitation)]

PATH = f'{DECKDIR}/Wylder Tilghman Island - Equity Teaser.dc.html'
# the closing page carries the advisor's telephone, email and license; nothing else may hold a digit
CONTACT_PAGE = 'THE INVITATION'


def build_deck():
    head, _ = load_sections()
    out = head
    for i, (name, fn) in enumerate(PAGES):
        out += f'<!-- ═══════════ {i + 1:02d} · {name} ═══════════ -->' + fn() + '\n\n'
    out = out.rstrip('\n') + TAIL
    io.open(PATH, 'w', encoding='utf-8').write(out)
    return PATH, len(PAGES)


def digits(html):
    """Every digit in the rendered text, page by page — attributes and CSS excluded."""
    found = []
    parts = re.split(r'<!-- ═+ \d+ · ([^═]*?) ═+ -->', html)
    for k in range(1, len(parts), 2):
        name, body = parts[k], parts[k + 1]
        body = re.sub(r'data-speaker-notes="[^"]*"', ' ', body)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'&[a-zA-Z#0-9]+;', ' ', text)
        for m in re.finditer(r'\S*\d\S*', text):
            found.append((name, m.group(0)))
    return found


if __name__ == '__main__':
    path, n = build_deck()
    s = io.open(path, encoding='utf-8').read()
    stray = [(pg, tok) for pg, tok in digits(s) if pg != CONTACT_PAGE]
    contact = [tok for pg, tok in digits(s) if pg == CONTACT_PAGE]
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'data-speaker-notes="[^"]*"', ' ', s))
    bad = [w for w in ('appraisal', 'appraised', 'LWHA', 'Newmark', 'CBRE', 'New Day',
                       'sources and uses', 'Sources and Uses') if w.lower() in txt.lower()]
    brit = [w for w in ('utilise', 'organis', 'centre', 'labour', 'metres', 'colour', 'favour',
                        'analyse') if w in txt.lower()]
    print(f'  {path.split("/")[-1]}  —  {n} pages')
    print(f'  figures anywhere but the contact block: {stray or "none"}')
    print(f'  contact block carries: {contact}')
    print(f'  forbidden references: {bad or "none"}')
    print(f'  British spelling: {brit or "none"}')
