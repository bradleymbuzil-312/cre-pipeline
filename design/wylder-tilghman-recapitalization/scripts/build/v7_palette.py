# -*- coding: utf-8 -*-
"""Investment Overview, Palette Hotels (11.18.26).

A ten-slide operating and valuation overview. It carries no capital structure of any kind: no
preferred, no senior debt, no returns, no sources and uses, no target close. Built fresh rather
than edited down from a capitalization deck, so none of that language exists to leak.

Two standing rules of the wider library are deliberately set aside here, on instruction:
  * the valuation is attributed, to CBRE and to LW Hospitality Advisors, and the word appraisal
    is used. Every other package still states values with no source named.
  * there are no em dashes anywhere in the file. build_deck asserts it.

The pro forma is the hotel on its own. The adjacent Dogwood Cove parcel is not in this deck, so
stabilized income reads $2.29M rather than the $2.52M the combined packages carry.
"""
import io
import re

from v7_lib import *
from v7_tranche import tbl

LABEL = 'Investment Overview'
# the hotel property improvement plan, and the Dogwood Cove house renovation that sits outside
# it. The cover states the two together; the budget slide prices the hotel program by line.
PIP_HOTEL, PIP_DOGWOOD = 3_003_000, 300_000
PIP_ALL_IN = PIP_HOTEL + PIP_DOGWOOD
assert PIP_ALL_IN == 3_303_000
FOOT_L = 'Wylder Hotel Tilghman Island &middot; Investment Overview'
FOOT_R = 'MMCC &middot; The TRANCHE Group'
NAVY = 'var(--mm-navy-900)'
ORANGE = 'var(--mm-orange)'
TAIL = '\n\n</x-import>\n</x-dc>\n</body>\n</html>\n'


def foot(dark=False):
    col = 'rgba(255,255,255,.42)' if dark else 'var(--ink-400)'
    div = 'rgba(255,255,255,.28)' if dark else 'var(--hairline)'
    return ('  <div style="margin-top:auto;display:flex;justify-content:space-between;'
            f'align-items:center;{CON}font-size:13px;letter-spacing:.2em;color:{col};'
            'padding-top:26px;">\n'
            f'    <span>{FOOT_L}</span>\n'
            f'    <span style="display:flex;align-items:center;gap:18px;"><span>{FOOT_R}</span>'
            f'<span style="{MONO}letter-spacing:.08em;padding-left:18px;'
            f'border-left:1px solid {div};">@@PAGE@@</span></span>\n  </div>\n')


def dark_foot():
    """The same running footer for the two full-bleed slides, so every slide carries it."""
    return ('  <div style="position:relative;z-index:2;display:flex;'
            f'justify-content:space-between;align-items:center;{CON}font-size:12px;'
            'letter-spacing:.2em;color:rgba(255,255,255,.5);margin-top:22px;padding-top:16px;'
            'border-top:1px solid rgba(255,255,255,.16);">\n'
            f'    <span>{FOOT_L}</span>\n'
            f'    <span style="display:flex;align-items:center;gap:16px;"><span>{FOOT_R}</span>'
            f'<span style="{MONO}letter-spacing:.08em;padding-left:16px;'
            'border-left:1px solid rgba(255,255,255,.22);">@@PAGE@@</span></span>\n  </div>\n')


def page(label, notes, inner, pad='70px 100px 50px'):
    return (f'<section data-label="{label}" data-screen-label="{label}" '
            f'data-speaker-notes="{notes}" '
            'style="width:100%;height:100%;box-sizing:border-box;background:var(--paper);'
            'color:var(--ink-900);font-family:var(--font-body);display:flex;'
            f'flex-direction:column;overflow:hidden;padding:{pad};">\n'
            + inner + foot() + '</section>')


def shot(src, alt, h=None, pos='center'):
    box = f'height:{h};' if h else 'flex:1;min-height:0;'
    return (f'      <div style="position:relative;overflow:hidden;{box}">\n'
            f'        <img src="assets/{src}" alt="{alt}" style="position:absolute;inset:0;'
            f'width:100%;height:100%;object-fit:cover;object-position:{pos};">\n'
            '      </div>\n')


def rule(mb='24px'):
    return f'  <div style="width:64px;height:3px;background:{ORANGE};margin-bottom:{mb};"></div>\n'


def H2(t, fs='42px', mb='26px'):
    return (f'  <h2 style="{DISP}font-weight:700;font-size:{fs};line-height:1.14;color:{NAVY};'
            f'margin:0 0 {mb};letter-spacing:-.01em;max-width:none;'
            f'border-bottom:1px solid var(--mm-navy);padding-bottom:14px;">{t}</h2>\n')


def P(t, fs='17px', col='var(--ink-700)', mt='0', lh='1.6', ind=4):
    return (f'{" " * ind}<p style="{BODY}max-width:none;font-size:{fs};line-height:{lh};'
            f'color:{col};margin:{mt} 0 0;">{t}</p>\n')


def eyebrow(t, col=None, mb='10px', ind=4):
    return (f'{" " * ind}<div style="{CON}font-size:12.5px;letter-spacing:.2em;'
            f'color:{col or ORANGE};margin-bottom:{mb};">{t}</div>\n')


# ── 01 · cover ───────────────────────────────────────────────────────────────────────────────
def cover():
    sn = ('Wylder Hotel Tilghman Island. A fifty-key Chesapeake Bay resort repositioning to '
          'fifty-seven keys plus a whole-home suite through a three point three million dollar '
          'renovation, the three million three thousand dollar hotel program together with three '
          'hundred thousand at Dogwood Cove. An investment overview, '
          'November twenty twenty-six. Bradley M. Buzil, Senior Director and exclusive capital '
          'advisor, Marcus and Millichap Capital Corporation.')
    return ('<section data-label="Cover" data-screen-label="Cover" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     'justify-content:space-between;padding:76px 100px 46px;">\n'
     '  <img src="assets/wt-aerial-spring.png" alt="Wylder Hotel Tilghman Island from the air" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,'
     'rgba(0,17,34,.70) 0%,rgba(0,17,34,.26) 26%,rgba(0,17,34,.58) 52%,'
     'rgba(0,17,34,.84) 74%,rgba(0,17,34,.96) 100%);"></div>\n'
     f'  <div style="position:absolute;right:0;top:0;bottom:0;width:10px;background:{ORANGE};'
       '"></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.28);padding-bottom:26px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:58px;">\n'
     f'    <span style="{CON}font-size:14px;letter-spacing:.26em;'
     'color:var(--mm-orange-100);">Confidential &middot; Investment Overview</span>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;margin-top:auto;">\n'
     f'    <h1 style="{DISP}font-weight:700;font-size:92px;line-height:1.03;color:#fff;'
     'margin:0;letter-spacing:-.022em;max-width:none;">Wylder Hotel<br>Tilghman Island.</h1>\n'
     f'    <p style="{BODY}max-width:1180px;font-size:26px;line-height:1.5;'
     'color:rgba(255,255,255,.9);margin:26px 0 0;">A 50-key Chesapeake Bay resort repositioning '
     f'to 57 keys plus a whole-home suite through a ${PIP_ALL_IN / 1e6:,.1f}M renovation.</p>\n'
     f'    <div style="{CON}font-size:15px;letter-spacing:.24em;color:var(--mm-orange-100);'
     'margin-top:24px;">November 2026 &middot; Tilghman Island, MD</div>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;margin-top:64px;padding-top:30px;'
     'border-top:1px solid rgba(255,255,255,.3);display:flex;justify-content:space-between;'
     'align-items:center;gap:32px;">\n'
     '    <div style="display:flex;align-items:center;gap:22px;">\n'
     '      <img src="assets/buzil.jpg" alt="Bradley M. Buzil" style="width:84px;height:84px;'
     'object-fit:cover;border-radius:50%;flex:none;">\n'
     '      <div>\n'
     f'        <div style="{DISP}font-weight:700;font-size:31px;color:#fff;line-height:1.15;'
     'letter-spacing:-.01em;">Bradley M. Buzil</div>\n'
     f'        <div style="{BODY}font-size:19px;color:rgba(255,255,255,.8);margin-top:5px;">'
     'Senior Director &middot; Exclusive Capital Advisor</div>\n      </div>\n    </div>\n'
     f'    <span style="{CON}font-size:14.5px;letter-spacing:.2em;line-height:1.8;'
     'color:rgba(255,255,255,.75);text-align:right;">Marcus &amp; Millichap<br>Capital '
     'Corporation</span>\n  </div>\n' + dark_foot() + '</section>')


# ── 02 · the opportunity ─────────────────────────────────────────────────────────────────────
OPP_TILES = [
  ('Keys', '50 &rarr; 57 + 1', '57 hotel keys on completion, plus the Dogwood Cove suite', 1),
  ('Renovation', '$3.3M', '$3.0M hotel program at $52,684 per key, plus $300,000 at '
                          'Dogwood Cove', 0),
  ('As-Is Value', '$21.4M', 'Hotel only &middot; CBRE, September 11, 2026', 0),
  ('Stabilized Value', '$29.5M', 'Hotel only &middot; CBRE, April 1, 2029', 1),
  ('T12 NOI', '$0.63M', 'Hotel, twelve months to September 2026', 0),
  ('Stabilized NOI', '$2.29M', '2029 hotel pro forma. With the parcel, $2.52M', 1),
  ('RevPAR Index', '42.8% &rarr; ~70%', 'July 2026 TTM vs. comp set', 0),
  ('Program', 'Jan &rarr; Jun 2027', 'Starts January 4, 2027 &middot; 175 days', 0)]


def opportunity():
    sn = ('A repositioning the market has already proven. Fifty keys to fifty-seven on '
          'completion. A three million dollar renovation, fifty-two thousand six hundred '
          'eighty-four a key. Twenty-one point four million as is, twenty-nine point five '
          'million stabilized, both per C B R E. Trailing net operating income of six hundred '
          'thirty thousand against two point two nine million stabilized in the twenty '
          'twenty-nine pro forma. RevPAR index of forty-two point eight percent today against '
          'the competitive set, targeted to about seventy percent. The program runs January to '
          'June twenty twenty-seven, one hundred seventy-five days.')
    return page('The Opportunity', sn,
      rule() + H2('A repositioning the market has already proven.')
      + '  <div style="display:grid;grid-template-columns:repeat(4,1fr);flex:1;min-height:0;">\n'
      + tiles(OPP_TILES, cols=4, pad='28px 26px 28px 0') + '  </div>\n')


# ── 03 · the asset ───────────────────────────────────────────────────────────────────────────
ASSET_FACTS = [('Keys', '50 &rarr; 57', 'Four rooms returned, three added. The Dogwood Cove '
                                       'suite sits on the adjacent parcel'),
               ('Site', '8.10 ac', 'Waterfront on the Bay and the Choptank'),
               ('Positioning', 'Upper Upscale', 'Full-service waterfront resort'),
               ('Location', 'Tilghman, MD', 'Talbot County &middot; Tilghman Island')]


def asset():
    sn = ('The asset. Wylder Hotel Tilghman Island sits on Tilghman Island in Talbot County, '
          'Maryland, between the Chesapeake Bay and the Choptank River. An eight point one acre '
          'waterfront parcel with eleven hundred feet of water frontage, a marina, pool, '
          'restaurant and boat bar. Operated under the Wylder Hotels brand, the property is '
          'mid-repositioning.')
    facts = ''
    for i, (k, v, n) in enumerate(ASSET_FACTS):
        bb = '' if i == len(ASSET_FACTS) - 1 else f'border-bottom:{HAIR};'
        facts += (f'      <div style="padding:{"0 0 20px" if i == 0 else "20px 0"};{bb}">\n'
                  + eyebrow(k, col='var(--ink-500)', ind=8, mb='7px')
                  + f'        <div style="{DISP}font-weight:700;font-size:28px;color:{NAVY};'
                    f'line-height:1.1;">{v}</div>\n'
                  + P(n, fs='15px', mt='5px', lh='1.4', ind=8) + '      </div>\n')
    return page('The Asset', sn,
      rule() + H2('A 50-key waterfront resort on 8.10 acres.')
      + '  <div style="display:grid;grid-template-columns:1.32fr 1fr;gap:52px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;">\n'
      + P('Wylder Hotel Tilghman Island sits on Tilghman Island in Talbot County, Maryland, '
          'between the Chesapeake Bay and the Choptank River: an 8.10-acre waterfront parcel '
          'with a marina, pool, restaurant and boat bar. Operated under the Wylder Hotels brand, '
          'the property is mid-repositioning.', fs='18px')
      + '      <div style="margin-top:22px;display:flex;flex-direction:column;flex:1;'
        'min-height:0;gap:12px;">\n'
      + shot('wt-aerial.png', 'The resort and its marina from the air')
      + '        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;'
        'height:132px;flex:none;">\n'
      + ''.join(shot(f, a) for f, a in (
          ('wt-pool.png', 'The pool and grounds'),
          ('wt-lobby.png', 'The interior'),
          ('wt-fb-signs.jpg', 'The boat bar and restaurant'),
          ('wt-pier.png', 'The pier and the Chesapeake Bay')))
      + '        </div>\n      </div>\n    </div>\n'
        '    <div style="display:flex;flex-direction:column;justify-content:center;'
        f'border-left:{HAIR};padding-left:46px;">\n' + facts + '    </div>\n  </div>\n')


# ── 04 · the sponsor ─────────────────────────────────────────────────────────────────────────
SPONSOR_TILES = [('Ownership', '21551 Tilghman Investors LLC'),
                 ('Principal / Guarantor', 'John Flannigan'),
                 ('Operator / Brand', 'Wylder Hotels'),
                 ('Manager', 'Wylder Eastern Shore Mgmt.')]
ALIGNMENT = [
  ('Affiliate management', 'Day-to-day operations are run by an affiliate of ownership under '
   'an executed management agreement, with no split incentive between owner and operator.'),
  ('Continuous ownership since 2017', 'The sponsor has owned and operated the hotel under the '
   'Wylder brand through the pandemic cycle and the current repositioning, investing a further '
   '$642,693 of capital between 2021 and 2025.'),
  ('Single-asset ownership entity', '21551 Tilghman Investors LLC holds this property and no '
   'other operating assets, keeping the asset and its cash flow ring-fenced.'),
  ('Two-property brand platform', 'Revenue management, distribution, design and procurement are '
   'shared across Wylder Hotels in Maryland and New York, giving a 57-key asset reach it could '
   'not support standing alone.')]


def sponsor():
    sn = ('Ownership and operating structure. The property is owned by twenty-one thousand five '
          'hundred fifty-one Tilghman Investors LLC, led by principal John Flannigan, and '
          'operated under the Wylder Hotels brand through affiliate Wylder Eastern Shore '
          'Management, which controls day-to-day operations and the renovation. Owner operated '
          'with no third party manager, continuous ownership since twenty seventeen, a single '
          'asset entity, and a two property brand platform behind it.')
    tl = '  <div style="display:grid;grid-template-columns:repeat(4,1fr);margin-bottom:26px;">\n'
    for i, (k, v) in enumerate(SPONSOR_TILES):
        br = '' if i == 3 else f'border-right:{HAIR};'
        pd = '0 24px 0 0' if i == 0 else ('0 24px' if i < 3 else '0 0 0 24px')
        tl += (f'    <div style="padding:{pd};{br}">'
               f'<div style="{CON}font-size:12px;letter-spacing:.16em;color:var(--ink-500);">'
               f'{k}</div>'
               f'<div style="{BODY}font-weight:600;font-size:17px;color:{NAVY};margin-top:7px;'
               f'line-height:1.3;">{v}</div></div>\n')
    tl += '  </div>\n'
    blocks = ('  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 46px;'
              'align-content:start;">\n')
    for i, (t, d) in enumerate(ALIGNMENT):
        bb = '' if i >= 2 else f'border-bottom:{HAIR};'
        blocks += (f'    <div style="padding:{"0 0 26px" if i < 2 else "26px 0 0"};{bb}">\n'
                   f'      <div style="display:flex;align-items:baseline;gap:11px;">'
                   f'<span style="{MONO}font-size:13px;color:{ORANGE};">'
                   f'{i + 1:02d}</span>'
                   f'<span style="{BODY}font-weight:600;font-size:17.5px;color:{NAVY};">'
                   f'{t}</span></div>\n'
                   + P(d, fs='16px', mt='8px', lh='1.55', ind=6) + '    </div>\n')
    blocks += '  </div>\n'
    blocks += (f'  <div style="background:{NAVY};color:#fff;padding:22px 26px;margin-top:auto;">\n'
               + eyebrow('Reporting', ind=4, mb='9px')
               + P('Operating statements are produced monthly at the property level by the '
                   'manager. The sponsor has held and operated the asset through a full market '
                   'cycle under the same brand and the same management company, so the operating '
                   'history and the forward plan come from one source.',
                   fs='15.5px', col='rgba(255,255,255,.88)', lh='1.5', ind=4)
               + '  </div>\n')
    return page('The Sponsor', sn,
      rule() + H2('Ownership and operating structure.')
      + P('The property is owned by <strong style="color:var(--mm-navy-900);">21551 Tilghman '
          'Investors LLC</strong>, led by principal <strong style="color:var(--mm-navy-900);">'
          'John Flannigan</strong>, and operated under the Wylder Hotels brand through affiliate '
          'Wylder Eastern Shore Management, LLC, controlling day-to-day operations and the '
          'renovation.', fs='17px')
      + '  <div style="height:24px;"></div>\n' + tl
      + eyebrow('Structure and Alignment', mb='16px') + blocks)


# ── 05 · brand and sponsor track record ──────────────────────────────────────────────────────
PORTFOLIO = [('Wylder Tilghman Island', 'Chesapeake Bay, MD &middot; this asset',
              '50 &rarr; 57 keys', 'Est. 2017'),
             ('Wylder Windham', 'Catskills, NY &middot; ~$27M invested', '110 keys', 'Est. 2022')]
RESUME = [('Wylder', '&rsquo;16 to now', 'Founder &amp; CEO. Acquired, renovated and opened the '
           'Wylder portfolio; leads capital, acquisitions, design and operations.'),
          ('Proper', '&rsquo;14 to &rsquo;16', 'Chief Operating Officer, Proper Hospitality. '
           'Opened Avalon Beverly Hills and Avalon Palm Springs.'),
          ('JRK', '&rsquo;09 to &rsquo;14', 'President, JRK Hotels. Seven-hotel platform; '
           'acquired the 472-key Sheraton Nashville Downtown ($47.5M), Oceana Santa Monica and '
           'Santa Barbara, Villa Florence San Francisco.')]


def brand():
    sn = ('Operator background and brand portfolio. Wylder Hotels is a boutique brand that '
          'acquires, renovates and operates resort properties in drive-to leisure markets, with '
          'two resorts on the East Coast. Wylder Windham opened in twenty twenty-two after '
          'roughly twenty-seven million dollars of investment and was named the number one '
          'resort in New York State the following year. John Flannigan, founder and chief '
          'executive, has three decades in hospitality including chief operating officer of '
          'Proper Hospitality and president of JRK Hotels.')
    pf = ''
    for i, (name, mkt, keys, est) in enumerate(PORTFOLIO):
        bb = '' if i == len(PORTFOLIO) - 1 else f'border-bottom:{HAIR};'
        pf += (f'      <div style="display:grid;grid-template-columns:1.5fr .7fr .55fr;gap:14px;'
               f'align-items:baseline;padding:26px 0;{bb}">'
               f'<div><div style="{BODY}font-weight:600;font-size:18px;color:{NAVY};">{name}'
               f'</div><div style="{BODY}font-size:14px;color:var(--ink-500);margin-top:3px;">'
               f'{mkt}</div></div>'
               f'<div style="{MONO}font-size:15px;color:var(--ink-900);text-align:right;">{keys}'
               f'</div>'
               f'<div style="{MONO}font-size:14px;color:var(--ink-500);text-align:right;">{est}'
               '</div></div>\n')
    rs = ''
    for i, (org, yrs, d) in enumerate(RESUME):
        bb = '' if i == len(RESUME) - 1 else f'border-bottom:{HAIR};'
        rs += (f'      <div style="display:grid;grid-template-columns:104px 1fr;gap:16px;'
               f'padding:32px 0;{bb}align-items:start;">'
               f'<div><div style="{BODY}font-weight:600;font-size:16px;color:{NAVY};">{org}</div>'
               f'<div style="{MONO}font-size:12.5px;color:var(--ink-500);margin-top:2px;">{yrs}'
               '</div></div>'
               f'<div style="{BODY}font-size:15px;color:var(--ink-700);line-height:1.45;">{d}'
               '</div></div>\n')
    return page('Brand and Track Record', sn,
      rule() + H2('A brand with a proven repositioning behind it.')
      + '  <div style="display:grid;grid-template-columns:1fr 1.06fr;gap:52px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;">\n'
      + eyebrow('Wylder Hotels')
      + P('A boutique hotel brand that acquires, renovates and operates resort properties in '
          'drive-to leisure markets. Two resorts on the East Coast.', fs='16px', mt='0')
      + '      <div style="margin-top:16px;"></div>\n' + pf
      + f'      <div style="background:{NAVY};color:#fff;padding:24px 28px;margin-top:auto;">\n'
      + eyebrow('The Proof Case', ind=8, mb='10px')
      + P('Wylder Windham opened in 2022 after roughly $27,000,000 of investment and was named '
          'the number one resort in New York State the following year. It carries the American '
          'Express Fine Hotels &amp; Resorts designation. Tilghman Island follows the same path, '
          'under the same ownership and the same management company.',
          fs='15.5px', col='rgba(255,255,255,.88)', lh='1.55', ind=8)
      + '      </div>\n'
      + P('<strong style="color:var(--mm-navy-900);">Recognition.</strong> Number 8 in the U.S., '
          'Travel + Leisure World&rsquo;s Best 2023, and a MICHELIN Guide selection (Wylder '
          'Windham). Top 11 in NY and the Mid-Atlantic, Cond&eacute; Nast Traveler 2018 '
          '(Tilghman Island).', fs='15px', mt='auto', lh='1.55')
      + '    </div>\n'
      f'    <div style="display:flex;flex-direction:column;border-left:{HAIR};'
        'padding-left:46px;">\n'
      + eyebrow('John Flannigan')
      + '      <div style="display:flex;align-items:center;gap:20px;">\n'
        '        <img src="assets/flannigan.png" alt="John Flannigan" style="width:88px;'
        'height:88px;object-fit:cover;border-radius:50%;flex:none;">\n'
        '        <div>\n'
      + f'          <div style="{DISP}font-weight:700;font-size:26px;color:{NAVY};'
        'line-height:1.15;">Founder &amp; CEO</div>\n'
      + P('Wylder Hotels (JEF Management LLC). Three decades in hospitality.', fs='15.5px',
          mt='6px', ind=10)
      + '        </div>\n      </div>\n'
      + '      <div style="margin-top:18px;"></div>\n' + rs
      + P('Three decades across ownership, operations and development. The Wylder portfolio was '
          'acquired, renovated and opened under the same leadership that runs it today.',
          fs='14.5px', col='var(--ink-500)', mt='auto', lh='1.5')
      + '    </div>\n  </div>\n')


# ── 06 · business plan and value creation ────────────────────────────────────────────────────
PLAN_ITEMS = [
  ('Guest room renovation', 'Full renovation of all 57 guest rooms at $25,000 per key. Four '
   'out-of-service keys are returned and three added in the back house, taking the hotel from '
   '50 to 57: seven keys, 14% more sellable hotel inventory than today.', '$1.93M'),
  ('Add revenue streams', 'A rebuilt marina and the reimagined boat bar broaden revenue beyond '
   'the room block.', '$0.35M'),
  ('Lift rate through product', 'A fully renovated room block, repositioned toward weddings and '
   'group events, closes the rate gap to the comp set.', 'Rate + Group')]
PLAN_STATS = [
  ('RevPAR Index to Comp Set', '42.8% &rarr; ~70%',
   '$88 today vs. $206 comp set (STR, July 2026 TTM). CBRE projects a 74% index at '
   'stabilization.'),
  ('NOI &middot; T12 &rarr; 2029', '3.6&times;', 'From $0.63M trailing to $2.29M stabilized'),
  ('Value &middot; As-Is &rarr; Stab.', '$21.4 &rarr; $29.5M', 'CBRE, September 2026')]


def business_plan():
    sn = ('Business plan and capital improvement program. Full renovation of all fifty-seven '
          'guest rooms at twenty-five thousand a key, taking the hotel from fifty keys to '
          'fifty-seven, twelve point three percent more sellable inventory. A rebuilt marina, '
          'the reimagined boat bar and a replaced three bedroom house broaden revenue beyond the '
          'room block. A fully renovated room block repositioned toward weddings and group '
          'events closes the rate gap to the competitive set. The three million three thousand '
          'dollar program starts January fourth, twenty twenty-seven and completes in late June.')
    items = ''
    for i, (t, d, v) in enumerate(PLAN_ITEMS):
        bb = '' if i == len(PLAN_ITEMS) - 1 else f'border-bottom:{HAIR};'
        items += (f'    <div style="display:grid;grid-template-columns:46px 1fr 132px;gap:18px;'
                  f'padding:32px 0;{bb}align-items:start;">\n'
                  f'      <div style="{MONO}font-size:14px;color:{ORANGE};padding-top:4px;">'
                  f'{i + 1:02d}</div>\n      <div>\n'
                  f'        <div style="{DISP}font-weight:700;font-size:23px;color:{NAVY};">'
                  f'{t}</div>\n' + P(d, fs='16.5px', mt='9px', lh='1.55', ind=8) + '      </div>\n'
                  f'      <div style="{MONO}font-size:19px;font-weight:700;color:{NAVY};'
                  f'text-align:right;padding-top:3px;">{v}</div>\n    </div>\n')
    stats = ('  <div style="display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:0 34px;'
             'margin-top:auto;padding-top:22px;border-top:2px solid var(--mm-navy);">\n')
    for i, (lab, val, note) in enumerate(PLAN_STATS):
        bl = '' if i == 0 else f'border-left:{HAIR};padding-left:34px;'
        stats += (f'    <div style="{bl}">\n'
                  f'      <div style="{CON}font-size:12px;letter-spacing:.16em;color:{ORANGE};">'
                  f'{lab}</div>\n'
                  f'      <div style="{DISP}font-weight:700;font-size:34px;color:{NAVY};'
                  f'line-height:1.1;margin-top:7px;">{val}</div>\n'
                  + P(note, fs='13.5px', col='var(--ink-500)', mt='7px', lh='1.45', ind=6)
                  + '    </div>\n')
    stats += '  </div>\n'
    return page('Business Plan', sn,
      rule() + H2('Business plan and capital improvement program.')
      + items
      + P('Exterior and interior improvements, contingency and professional fees complete the '
          f'${PIP_HOTEL:,} hotel program, which starts January 4, 2027 and completes in late '
          f'June 2027. The ${PIP_DOGWOOD:,} Dogwood Cove house renovation sits outside it.',
          fs='15.5px', mt='16px')
      + f'  <div style="border-left:3px solid {ORANGE};padding-left:18px;margin-top:16px;">\n'
      + eyebrow('Brand Optionality', mb='6px')
      + P('A <strong style="color:var(--mm-navy-900);">Small Luxury Hotels membership proposal '
          'is in hand</strong>, subject to SLH&rsquo;s application, inspection and board '
          'approval. SLH fees are not included in the pro forma.', fs='15.5px', mt='0', lh='1.5')
      + '  </div>\n'
      + stats, pad='58px 100px 42px')


# ── 07 · historical and pro forma financials ─────────────────────────────────────────────────
FIN_COLS = ['2023', '2024', '2025', 'T12 Sep-26', '2027 Renov.', '2028 Stab.', '2029 Stabilized']
FIN_ROWS = [
  ('Occupancy', ['27%', '32%', '33%', '29%', '33%', '38%', '40%'], ''),
  ('ADR', ['$312', '$291', '$265', '$298', '$383', '$395', '$415'], ''),
  ('RevPAR', ['$83', '$92', '$87', '$85', '$126', '$150', '$166'], 'sub'),
  ('Total revenue', ['$3.48M', '$3.81M', '$3.79M', '$3.72M', '$4.85M', '$6.03M', '$6.70M'], ''),
  ('NOI (EBITDA)', ['$0.49M', '$0.92M', '$0.66M', '$0.63M', '$1.41M', '$2.01M', '$2.29M'], 'tot'),
  ('NOI margin', ['14.0%', '24.0%', '17.6%', '17.1%', '29.1%', '33.3%', '34.2%'], '')]
FIN_STATS = [('Historical NOI Band', '$0.5M to $0.9M', '2023 through 2025 actual'),
             ('Stabilized NOI &middot; 2029', '$2.29M', 'Hotel only. Combined, $2.52M'),
             ('RevPAR &middot; T12 &rarr; 2029', '$85 &rarr; $166', 'A 95% increase')]


def financials():
    sn = ('Three years of history, a twenty twenty-seven renovation, stabilized by twenty '
          'twenty-nine. Occupancy has run between twenty-seven and thirty-three percent while '
          'rate fell from three hundred twelve dollars to the mid two hundreds. Net operating '
          'income has banded between four hundred ninety thousand and nine hundred twenty '
          'thousand. The pro forma reaches two point two nine million by twenty twenty-nine on a '
          'thirty-four point two percent margin. Occupancy declined in twenty twenty-six as '
          'management stopped discounting transient rate ahead of the renovation.')
    return page('Financials', sn,
      rule(mb='20px')
      + H2('Three years of history, a 2027 renovation, stabilized by 2029.', fs='38px', mb='14px')
      + P('The hotel on its own. Dogwood Cove is stated separately on the slides that follow.',
          fs='14.5px', col='var(--ink-500)', mt='0')
      + '  <div style="height:14px;"></div>\n'
      + tbl(['Metric'] + FIN_COLS, FIN_ROWS, fs='16px', pad=22, lw='1.42fr')
      + '  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 36px;'
        'margin-top:auto;padding-top:22px;border-top:2px solid var(--mm-navy);">\n'
      + ''.join(
          (f'    <div style="{"" if i == 0 else f"border-left:{HAIR};padding-left:36px;"}">\n'
           f'      <div style="{CON}font-size:12px;letter-spacing:.16em;color:{ORANGE};">'
           f'{lab}</div>\n'
           f'      <div style="{DISP}font-weight:700;font-size:32px;color:{NAVY};line-height:1.1;'
           f'margin-top:7px;">{val}</div>\n'
           + P(note, fs='13.5px', col='var(--ink-500)', mt='6px', ind=6) + '    </div>\n')
          for i, (lab, val, note) in enumerate(FIN_STATS))
      + '  </div>\n'
      + P('Occupancy declined in 2026 as management stopped discounting transient rate ahead of '
          'the renovation. 2027 reflects keys offline by wave per the renovation schedule. '
          'Actuals per operating statements; pro forma per the MMCC pro forma model. CBRE '
          'projects stabilized NOI of $2.46M (2030).',
          fs='13.5px', col='var(--ink-500)', mt='18px', lh='1.5'),
      pad='60px 96px 44px')


# ── 08 · valuation and market support ────────────────────────────────────────────────────────
VAL_ROWS = [('As-is (50 keys)', 'Sep 11, 2026', '$21.4M', '$428K'),
            ('Prospective as complete (57)', 'Apr 1, 2027', '$26.0M', '$456K'),
            ('Prospective as stabilized (57)', 'Apr 1, 2029', '$29.5M', '$518K')]
RESORT_COMPS = [('Haven Montauk, NY &middot; renovated', '2023', '26', '$577K'),
                ('Sands Motel, Montauk, NY', '2024', '43', '$541K'),
                ('Brass Lantern Inn, Nantucket, MA', '2023', '17', '$441K'),
                ('Elizabeth Pointe, Fernandina Bch, FL', '2024', '25', '$410K'),
                ('Beachside Hotel, Nantucket, MA', '2021', '94', '$404K'),
                ('Sandpiper Gulf Resort, Ft Myers, FL', '2023', '63', '$397K'),
                ('Montreal Beach Resort, Cape May, NJ', '2021', '70', '$329K'),
                ('Creekside Inn, Plantation Key, FL', '2021', '38', '$329K')]
LOCAL_COMPS = [('Hambleton Inn, Saint Michaels', '2024', '7', '$354K'),
               ('Mariners Motel, Rock Hall', '2025', '12', '$200K'),
               ('Robert Morris Inn, Oxford', '2024', '16', '$200K'),
               ('Oaks Waterfront Inn, Royal Oak', '2022', '15', '$190K'),
               ('Great Oak Landing, Chestertown', '2020', '28', '$169K'),
               ('The Wildset, Saint Michaels', '2020', '20', '$160K')]


def _comp_table(rows, head):
    g = ('      <div style="display:grid;grid-template-columns:1.9fr .46fr .36fr .5fr;'
         'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(head):
        al = '' if i == 0 else 'text-align:right;'
        g += (f'        <div style="padding:7px 5px 7px 0;border-bottom:2px solid var(--mm-navy);'
              f'{CON}font-size:11px;letter-spacing:.1em;color:var(--mm-navy);{al}">{c}</div>\n')
    for lab, yr, keys, pk in rows:
        for j, (v, al) in enumerate(((lab, ''), (yr, 'text-align:right;'),
                                     (keys, 'text-align:right;'), (pk, 'text-align:right;'))):
            fam = BODY if j == 0 else MONO
            col = 'var(--ink-900)' if j in (0, 3) else 'var(--ink-500)'
            w = 'font-weight:600;' if j == 3 else ''
            g += (f'        <div style="padding:11px 5px 11px 0;border-bottom:{HAIR};{fam}'
                  f'font-size:13.5px;color:{col};{al}{w}">{v}</div>\n')
    return g + '      </div>\n'


def valuation():
    sn = ('Valuation and market support. C B R E, fee simple, sales comparison and income '
          'approaches reconciled. Twenty-one point four million as is at fifty keys, '
          'twenty-six million prospective as complete at fifty-seven, twenty-nine point five '
          'million prospective as stabilized, five hundred eighteen thousand a key. Supported by '
          'L W Hospitality Advisors in May twenty twenty-six at twenty-one million, twenty-five '
          'point five million and twenty-eight point five million. The as complete premise '
          'assumes completion by April first, twenty twenty-seven, while the current schedule '
          'completes in late June.')
    vt = ('    <div style="display:grid;grid-template-columns:1.75fr .85fr .62fr .55fr;'
          'font-variant-numeric:tabular-nums;">\n')
    for i, c in enumerate(['Scenario', 'Date of Value', 'Value', 'Per Key']):
        al = '' if i == 0 else 'text-align:right;'
        vt += (f'      <div style="padding:9px 7px 9px 0;border-bottom:2px solid var(--mm-navy);'
               f'{CON}font-size:11.5px;letter-spacing:.11em;color:var(--mm-navy);{al}">{c}</div>\n')
    for j, (sc, dt, v, pk) in enumerate(VAL_ROWS):
        bb = '3px double var(--mm-navy)' if j == len(VAL_ROWS) - 1 else HAIR
        cc = ORANGE if j == len(VAL_ROWS) - 1 else NAVY
        vt += (f'      <div style="padding:16px 7px 16px 0;border-bottom:{bb};{BODY}'
               f'font-size:15px;font-weight:600;color:{NAVY};">{sc}</div>\n'
               f'      <div style="padding:16px 7px;border-bottom:{bb};{MONO}font-size:13.5px;'
               f'text-align:right;color:var(--ink-500);">{dt}</div>\n'
               f'      <div style="padding:16px 7px;border-bottom:{bb};{MONO}font-size:16px;'
               f'font-weight:700;text-align:right;color:{cc};">{v}</div>\n'
               f'      <div style="padding:16px 7px;border-bottom:{bb};{MONO}font-size:14px;'
               f'text-align:right;color:var(--ink-900);">{pk}</div>\n')
    vt += '    </div>\n'
    return page('Valuation', sn,
      rule(mb='18px') + H2('Valuation and market support.', fs='38px', mb='20px')
      + '  <div style="display:grid;grid-template-columns:1fr 1.04fr;gap:46px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;">\n'
      + eyebrow('CBRE Appraisal &middot; September 2026', mb='12px') + vt
      + P('CBRE, Inc. Fee simple. Sales comparison and income approaches reconciled. Supported '
          'by LW Hospitality Advisors (May 2026): $21.0M as-is, $25.5M upon completion, $28.5M '
          'stabilized.', fs='14px', col='var(--ink-500)', mt='14px', lh='1.5')
      + f'      <div style="background:{NAVY};color:#fff;padding:17px 22px;margin-top:auto;">\n'
      + P('CBRE&rsquo;s as-complete premise assumes completion by April 1, 2027; the current '
          'schedule completes in late June 2027.', fs='14.5px',
          col='rgba(255,255,255,.9)', lh='1.5', ind=8)
      + '      </div>\n    </div>\n'
        '    <div style="display:flex;flex-direction:column;">\n'
      + eyebrow('East Coast Waterfront Resort Sales', mb='10px')
      + _comp_table(RESORT_COMPS, ['Property &middot; Market', 'Year', 'Keys', '$/Key'])
      + '      <div style="height:16px;"></div>\n'
      + eyebrow('Local Eastern Shore Transactions', mb='10px')
      + _comp_table(LOCAL_COMPS, ['Property &middot; Town', 'Year', 'Keys', '$/Key'])
      + P('The $518K/key stabilized conclusion sits within the East Coast waterfront range '
          'and well below premier regional assets.', fs='14px', col=NAVY, mt='auto', lh='1.5')
      + '    </div>\n  </div>\n', pad='56px 92px 42px')


# ── 09 · renovation budget ───────────────────────────────────────────────────────────────────
BUDGET = [('Room renovation &middot; 57 @ $25,000', 1_425_000),
          ('Replace 3-bedroom house', 500_000),
          ('Exterior &amp; interior improvements', 300_000),
          ('Marina rebuild', 250_000),
          ('Boat bar &amp; public-space FF&amp;E', 100_000),
          ('Professional fees', 170_000),
          ('Contingency (10% of hard costs)', 258_000)]
BUDGET_TOTAL = 3_003_000
assert sum(a for _, a in BUDGET) == BUDGET_TOTAL
BIDS = [('House', '$488,039', 'BCO'), ('Pier', '$152,250', 'Ivans Ventures'),
        ('Electrical', '$56,800 to $82,400', 'Quoted range'), ('Water', '$7,526', 'Utility')]


def budget():
    sn = ('Every renovation dollar, by line. One million four hundred twenty-five thousand for '
          'fifty-seven rooms at twenty-five thousand a key. Five hundred thousand to replace the '
          'three bedroom house. Three hundred thousand of exterior and interior improvements. '
          'Two hundred fifty thousand for the marina rebuild. One hundred thousand for the boat '
          'bar and public space furnishings. One hundred seventy thousand of professional fees '
          'and two hundred fifty-eight thousand of contingency, ten percent of hard costs. Three '
          'million three thousand in total. Marina, house and pier utility bids are in hand.')
    rows = ''
    for lab, amt in BUDGET:
        rows += ('    <div style="display:flex;justify-content:space-between;align-items:baseline;'
                 f'padding:24px 0;border-bottom:{HAIR};gap:20px;">'
                 f'<span style="{BODY}font-size:18px;color:var(--ink-900);">{lab}</span>'
                 f'<span style="{MONO}font-size:18px;color:{NAVY};">${amt:,}</span></div>\n')
    rows += ('    <div style="display:flex;justify-content:space-between;align-items:baseline;'
             'padding:17px 0;border-bottom:3px double var(--mm-navy);gap:20px;">'
             f'<span style="{BODY}font-size:19px;font-weight:700;color:{NAVY};">Total '
             'renovation</span>'
             f'<span style="{MONO}font-size:22px;font-weight:700;color:{ORANGE};">'
             f'${BUDGET_TOTAL:,}</span></div>\n')
    bids = ''
    for i, (k, v, src) in enumerate(BIDS):
        bb = '' if i == len(BIDS) - 1 else f'border-bottom:{HAIR};'
        bids += ('      <div style="display:flex;justify-content:space-between;'
                 f'align-items:baseline;padding:19px 0;{bb}gap:16px;">'
                 f'<span><span style="{BODY}font-size:15.5px;font-weight:600;color:{NAVY};">{k}'
                 f'</span><span style="{BODY}font-size:13.5px;color:var(--ink-500);"> &middot; '
                 f'{src}</span></span>'
                 f'<span style="{MONO}font-size:15px;color:var(--ink-900);">{v}</span></div>\n')
    return page('Renovation Budget', sn,
      rule() + H2('Every renovation dollar, by line.')
      + '  <div style="display:grid;grid-template-columns:1.32fr 1fr;gap:52px;flex:1;'
        'grid-template-rows:1fr;min-height:0;">\n'
        '    <div style="display:flex;flex-direction:column;">\n' + rows
      + P(f'${PIP_HOTEL:,} is the hotel program, $52,684 per key across 57 keys, starting '
          f'January 4, 2027 and running 175 days to late June. The ${PIP_DOGWOOD:,} Dogwood Cove '
          'house renovation sits outside this budget and is priced on its own slide, taking the '
          f'combined program to ${PIP_ALL_IN:,}.', fs='15px', col='var(--ink-500)', mt='auto')
      + '    </div>\n'
        f'    <div style="display:flex;flex-direction:column;border-left:{HAIR};'
        'padding-left:46px;">\n'
      + eyebrow('Bids in Hand', mb='14px') + bids
      + '      <div style="margin-top:22px;">\n'
      + shot('wt-suite.jpg', 'The completed model room', h='186px')
      + '      </div>\n'
      + f'      <div style="background:{NAVY};color:#fff;padding:20px 24px;margin-top:auto;">\n'
      + P('Bids are in hand for the house, the pier and its utilities. Room renovation is '
          'budgeted at $25,000 per key. Contingency is 10% of hard costs, drawn pro rata with '
          'hard cost spending.', fs='15px', col='rgba(255,255,255,.88)', lh='1.5', ind=8)
      + '      </div>\n    </div>\n  </div>\n')


# ── 10 · next steps ──────────────────────────────────────────────────────────────────────────
DILIGENCE = ['CBRE appraisal', 'Renovation schedule and budget', 'Contractor bids',
             'STR reports', 'Historical operating statements', 'MMCC pro forma model',
             'Property condition report', 'Phase I ESA', 'ALTA survey',
             'Flood and insurance', 'Licenses and permits', 'Group and wedding pace',
             '2027 strategy presentation', 'CapEx history', 'Dogwood Cove projections']
assert len(DILIGENCE) == 15


def next_steps():
    sn = ('Available for review. The diligence folder includes the C B R E appraisal, the '
          'renovation schedule, budget and contractor bids, S T R reports, historical operating '
          'statements, the M M C C pro forma model, the property condition report, the Phase One '
          'environmental, the A L T A survey, flood and insurance, licenses and permits, group '
          'and wedding pace, the twenty twenty-seven strategy presentation, the capital '
          'expenditure history and the Dogwood Cove projections. Bradley M. Buzil, Senior '
          'Director, The '
          'Tranche Group at Marcus and Millichap Capital Corporation, exclusive capital advisor.')
    cols = 3
    items = (f'  <div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:0 44px;'
             'margin-top:28px;">\n')
    for i, d in enumerate(DILIGENCE):
        bb = ('' if i >= len(DILIGENCE) - cols
              else 'border-bottom:1px solid rgba(255,255,255,.16);')
        items += ('    <div style="display:flex;align-items:center;gap:12px;'
                  f'padding:{"0 0 12px" if i < cols else "12px 0"};{bb}">'
                  f'<span style="width:6px;height:6px;background:{ORANGE};flex:none;"></span>'
                  f'<span style="{BODY}font-size:16px;color:rgba(255,255,255,.9);">{d}</span>'
                  '</div>\n')
    items += '  </div>\n'
    return ('<section data-label="Next Steps" data-screen-label="Next Steps" '
     f'data-speaker-notes="{sn}" '
     'style="width:100%;height:100%;box-sizing:border-box;position:relative;overflow:hidden;'
     'color:#fff;font-family:var(--font-body);display:flex;flex-direction:column;'
     f'justify-content:space-between;padding:68px 100px 46px;background:{NAVY};">\n'
     '  <img src="assets/wt-dogwood-aerial.jpg" alt="The marina and the water" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">\n'
     '  <div style="position:absolute;inset:0;background:linear-gradient(180deg,'
     'rgba(0,26,61,.90) 0%,rgba(0,26,61,.78) 50%,rgba(0,26,61,.93) 100%);"></div>\n'
     f'  <div style="position:absolute;right:0;top:0;bottom:0;width:10px;background:{ORANGE};'
       '"></div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:center;border-bottom:1px solid rgba(255,255,255,.22);padding-bottom:22px;">\n'
     '    <img src="assets/mmcc-2018-white.png" alt="Marcus &amp; Millichap Capital Corporation" '
     'style="height:46px;">\n'
     f'    <span style="{CON}font-size:13px;letter-spacing:.26em;'
     'color:var(--mm-orange-100);">Confidential &middot; Investment Overview</span>\n  </div>\n\n'
     '  <div style="position:relative;z-index:2;flex:1;display:flex;flex-direction:column;'
     'justify-content:center;padding:40px 0;">\n'
     f'    <div style="width:64px;height:3px;background:{ORANGE};margin-bottom:22px;"></div>\n'
     f'    <h2 style="{DISP}font-weight:700;font-size:52px;line-height:1.1;color:#fff;margin:0;'
     'letter-spacing:-.016em;max-width:none;">Available for review.</h2>\n'
     + P('The diligence folder is open. It includes the appraisal, the renovation schedule, '
         'budget and contractor bids, the operating history and the third-party reports below.',
         fs='18px', col='rgba(255,255,255,.88)', mt='18px', lh='1.55')
     + items + '  </div>\n\n'
     '  <div style="position:relative;z-index:2;display:flex;justify-content:space-between;'
     'align-items:flex-end;border-top:1px solid rgba(255,255,255,.22);padding-top:24px;">\n'
     '    <div style="display:flex;align-items:center;gap:18px;">\n'
     '      <img src="assets/buzil.jpg" alt="Bradley M. Buzil" style="width:58px;height:58px;'
     'object-fit:cover;border-radius:50%;">\n'
     '      <div>\n'
     f'        <div style="{DISP}font-weight:700;font-size:23px;color:#fff;line-height:1.2;">'
     'Bradley M. Buzil</div>\n'
     f'        <div style="{BODY}font-size:15px;color:rgba(255,255,255,.72);margin-top:4px;">'
     'Senior Director &middot; The TRANCHE Group</div>\n'
     f'        <div style="{MONO}font-size:14.5px;color:{ORANGE};margin-top:9px;">'
     '310.909.5473 &nbsp;&middot;&nbsp; bradley.buzil@marcusmillichap.com</div>\n'
     '      </div>\n    </div>\n'
     f'    <div style="text-align:right;{CON}font-size:13px;letter-spacing:.2em;'
     'color:rgba(255,255,255,.55);line-height:1.9;">Marcus &amp; Millichap Capital '
     'Corporation<br>Exclusive Capital Advisor</div>\n  </div>\n' + dark_foot() + '</section>')


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Dogwood Cove: the parcel on its own, then the two together
#
# Every figure is the acquisition workbook's. The parcel carries its own expenses, which is why
# it does not run at the full margin a revenue-only treatment would imply.
# ─────────────────────────────────────────────────────────────────────────────────────────────
DOG_YEARS = ['2027', '2028', '2029', '2030', '2031']
DOG = {
  'house_rev': [0, 192_150, 191_625, 191_625, 191_625],
  'slip_rev': [101_500, 171_094, 179_648, 188_631, 198_062],
  'house_dept': [0, 48_038, 47_906, 47_906, 47_906],
  'slip_dept': [10_150, 17_109, 17_965, 18_863, 19_806],
  'cc': [3_146, 11_261, 11_509, 11_788, 12_080],
  'mgmt': [4_060, 14_530, 14_851, 15_210, 15_587],
  'util': [12_000, 12_360, 12_731, 13_113, 13_506],
  'rm': [10_000, 10_300, 10_609, 10_927, 11_255],
  'tax': [7_634, 7_863, 8_099, 8_342, 8_592],
  'ins': [12_000, 12_360, 12_731, 13_113, 13_506],
  'reserve': [0, 7_265, 11_138, 15_210, 15_587],
  'noi': [42_510, 222_159, 223_734, 225_784, 231_860],
  'am_fee': [2_030, 7_265, 7_425, 7_605, 7_794]}
_N = range(5)
# subtotals as the workbook reports them; it carries sub-dollar rounding, so the printed
# figures are its own and the derivation is checked to within a dollar
DOG['rev'] = [101_500, 363_244, 371_273, 380_256, 389_687]
DOG['dept'] = [10_150, 65_147, 65_871, 66_769, 67_712]
DOG['goi'] = [91_350, 298_097, 305_402, 313_487, 321_975]
DOG['undist'] = [29_206, 48_450, 49_700, 51_038, 52_429]
DOG['gop'] = [62_144, 249_647, 255_702, 262_448, 269_546]
DOG['fixed'] = [19_634, 27_488, 31_968, 36_665, 37_685]
DOG['cf'] = [40_480, 214_894, 216_309, 218_179, 224_067]
# every line of the parcel's statement has to foot, to the dollar of rounding the source carries
for _i in _N:
    assert DOG['house_rev'][_i] + DOG['slip_rev'][_i] == DOG['rev'][_i]
    assert DOG['house_dept'][_i] + DOG['slip_dept'][_i] == DOG['dept'][_i]
    assert DOG['rev'][_i] - DOG['dept'][_i] == DOG['goi'][_i]
    assert abs(DOG['cc'][_i] + DOG['mgmt'][_i] + DOG['util'][_i] + DOG['rm'][_i]
               - DOG['undist'][_i]) <= 1
    assert abs(DOG['goi'][_i] - DOG['undist'][_i] - DOG['gop'][_i]) <= 1
    assert DOG['tax'][_i] + DOG['ins'][_i] + DOG['reserve'][_i] == DOG['fixed'][_i]
    assert abs(DOG['gop'][_i] - DOG['fixed'][_i] - DOG['noi'][_i]) <= 1, ('Dogwood does not foot', _i)
    assert abs(DOG['noi'][_i] - DOG['am_fee'][_i] - DOG['cf'][_i]) <= 1

DOG_COST, DOG_PRICE, DOG_RENO, DOG_CLOSING_COSTS = 1_433_000, 1_100_000, 300_000, 33_000
DOG_SETTLE = 'November 16, 2026'
DOG_NO_SLIPS = 80_195
assert DOG_PRICE + DOG_RENO + DOG_CLOSING_COSTS == DOG_COST

# hotel only, from the pro forma on the financials slide
HOTEL_REV = [3_716_313, 4_850_759, 6_027_704, 6_701_388, 7_216_527, 7_648_894]
HOTEL_NOI = [634_680, 1_411_103, 2_007_969, 2_293_197, 2_478_214, 2_671_765]
HOTEL_AM = [0, 97_015, 120_554, 134_028, 144_331, 152_978]
COMB_YEARS = ['T12 Sep-26', '2027', '2028', '2029', '2030', '2031']
# the workbook's own combined column; the parts are checked against it to the dollar of rounding
COMB_REV = [3_716_313, 4_952_259, 6_390_948, 7_072_662, 7_596_783, 8_038_582]
COMB_NOI = [634_680, 1_453_613, 2_230_128, 2_516_931, 2_703_997, 2_903_626]
COMB_AM = [0, 99_045, 127_819, 141_453, 151_936, 160_772]
COMB_CF = [634_680, 1_354_568, 2_102_309, 2_375_478, 2_552_062, 2_742_854]
_DR = [0] + DOG['rev']
_DN = [0] + DOG['noi']
_DA = [0] + DOG['am_fee']
for _i in range(6):
    assert abs(HOTEL_REV[_i] + _DR[_i] - COMB_REV[_i]) <= 1, ('combined revenue', _i)
    assert abs(HOTEL_NOI[_i] + _DN[_i] - COMB_NOI[_i]) <= 1, ('combined NOI', _i)
    assert abs(HOTEL_AM[_i] + _DA[_i] - COMB_AM[_i]) <= 1, ('combined fee', _i)
    assert abs(COMB_NOI[_i] - COMB_AM[_i] - COMB_CF[_i]) <= 1, ('combined cash flow', _i)


def _m(v):
    return f'${v:,.0f}' if v else '0'


def _money(v):
    return f'${v:,.0f}' if v else '0'


def _paren(v):
    return f'(${v:,.0f})' if v else '0'


def dogwood():
    sn = ('Dogwood Cove on its own. The adjacent waterfront parcel: a four bedroom residence and '
          'twenty-four boat slips, under contract at one million one hundred thousand with '
          'settlement November sixteenth, twenty twenty-six, and three hundred thousand to bring '
          'the house online. Total project cost of one million four hundred thirty-three '
          'thousand. The house is offline through twenty twenty-seven, so that year carries slip '
          'revenue and holding costs only. From twenty twenty-eight the parcel earns about two '
          'hundred twenty-two thousand, a fifteen point five percent yield on cost, after its '
          'own housekeeping, utilities, repairs, insurance, taxes and reserve.')
    rows = [
      ('Residence', [_money(v) for v in DOG['house_rev']], ''),
      ('Slips &middot; 24', [_money(v) for v in DOG['slip_rev']], ''),
      ('Total revenues', [_money(v) for v in DOG['rev']], 'sub'),
      ('Residence rooms and housekeeping', [_paren(v) for v in DOG['house_dept']], ''),
      ('Slip operating cost', [_paren(v) for v in DOG['slip_dept']], ''),
      ('Gross operating income', [_money(v) for v in DOG['goi']], 'sub'),
      ('Credit card commissions', [_paren(v) for v in DOG['cc']], ''),
      ('Management fees', [_paren(v) for v in DOG['mgmt']], ''),
      ('Utilities', [_paren(v) for v in DOG['util']], ''),
      ('Repairs and maintenance', [_paren(v) for v in DOG['rm']], ''),
      ('Gross operating profit', [_money(v) for v in DOG['gop']], 'sub'),
      ('Real estate taxes', [_paren(v) for v in DOG['tax']], ''),
      ('Insurance', [_paren(v) for v in DOG['ins']], ''),
      ('Reserve for replacement', [_paren(v) for v in DOG['reserve']], ''),
      ('Net operating income', [_money(v) for v in DOG['noi']], 'tot'),
      ('NOI margin', [f'{DOG["noi"][i] / DOG["rev"][i]:.1%}' for i in _N], ''),
      ('Cash flow after asset management', [_money(v) for v in DOG['cf']], '')]
    stats = [('Total Project Cost', f'${DOG_COST:,}',
              f'${DOG_PRICE:,} price, ${DOG_CLOSING_COSTS:,} costs, ${DOG_RENO:,} renovation'),
             ('NOI &middot; 2029', f'${DOG["noi"][2]:,}', 'Unlevered, after its own expenses'),
             ('Yield on Cost &middot; 2029', f'{DOG["noi"][2] / DOG_COST:.2%}',
              'On total project cost, not a cap rate'),
             ('Without Slip Approval', f'${DOG_NO_SLIPS:,}',
              '2029 income if commercial use is not permitted')]
    return page('Dogwood Cove Pro Forma', sn,
      rule(mb='18px')
      + H2('Dogwood Cove, on its own.', fs='38px', mb='16px')
      + '  <div style="display:grid;grid-template-columns:1fr 250px;gap:26px;'
        'align-items:center;">\n    <div>\n'
      + P('The adjacent waterfront parcel: a four-bedroom residence and 24 boat slips, under '
          f'contract at ${DOG_PRICE:,}, settlement pending, and ${DOG_RENO:,} to bring the house '
          'online. The residence is offline through 2027, so that year carries slip revenue and '
          'holding costs only.', fs='15.5px', mt='0', ind=6)
      + '    </div>\n'
      + shot('wt-dogwood-house.jpg', '21441 Dogwood Cove Road', h='96px')
      + '  </div>\n  <div style="height:14px;"></div>\n'
      + tbl(['Line item'] + DOG_YEARS, rows, fs='13.5px', pad=5, lw='2.15fr')
      + '  <div style="display:grid;grid-template-columns:1.35fr 1fr 1fr 1.1fr;gap:0 30px;'
        'margin-top:auto;padding-top:18px;border-top:2px solid var(--mm-navy);">\n'
      + ''.join(
          (f'    <div style="{"" if i == 0 else f"border-left:{HAIR};padding-left:30px;"}">\n'
           f'      <div style="{CON}font-size:11px;letter-spacing:.15em;color:{ORANGE};">'
           f'{lab}</div>\n'
           f'      <div style="{DISP}font-weight:700;font-size:26px;color:{NAVY};line-height:1.1;'
           f'margin-top:6px;">{val}</div>\n'
           + P(note, fs='12.5px', col='var(--ink-500)', mt='5px', lh='1.4', ind=6)
           + '    </div>\n') for i, (lab, val, note) in enumerate(stats))
      + '  </div>\n'
      + P('Insurance, utilities and repairs are assumptions pending quotes.',
          fs='12.5px', col='var(--ink-500)', mt='12px'), pad='54px 92px 40px')


def combined():
    sn = ('Hotel and parcel together. Combined revenue runs from three point seven two million '
          'trailing to eight point zero four million in twenty thirty-one, with combined net '
          'operating income of two point five two million in twenty twenty-nine, the first '
          'stabilized year. Dogwood Cove contributes about nine percent of combined income once '
          'the residence is in service. The hotel pro forma on the earlier slides is the hotel '
          'on its own; this page adds the acquired parcel.')
    rows = [
      ('Hotel revenue', [f'${v:,.0f}' for v in HOTEL_REV], ''),
      ('Dogwood Cove residence', [_m(v) for v in [0] + DOG['house_rev']], ''),
      ('Dogwood Cove slips', [_m(v) for v in [0] + DOG['slip_rev']], ''),
      ('Combined revenue', [f'${v:,.0f}' for v in COMB_REV], 'sub'),
      ('Hotel net operating income', [f'${v:,.0f}' for v in HOTEL_NOI], ''),
      ('Dogwood Cove net operating income', [_m(v) for v in [0] + DOG['noi']], ''),
      ('Combined net operating income', [f'${v:,.0f}' for v in COMB_NOI], 'tot'),
      ('Combined NOI margin', [f'{COMB_NOI[i] / COMB_REV[i]:.1%}' for i in range(6)], ''),
      ('Dogwood share of combined NOI',
       [('0.0%' if i == 0 else f'{([0] + DOG["noi"])[i] / COMB_NOI[i]:.1%}')
        for i in range(6)], ''),
      ('Asset management fee', [_m(v) for v in COMB_AM], ''),
      ('Combined cash flow after fee', [f'${v:,.0f}' for v in COMB_CF], 'sub')]
    note = (f'  <div style="background:{NAVY};color:#fff;padding:20px 26px;margin-top:auto;">\n'
            + eyebrow('Read With the Hotel Pro Forma', ind=4, mb='9px')
            + P('The opportunity and financials slides state the hotel on its own, so stabilized '
                f'income there reads ${HOTEL_NOI[3] / 1e6:,.2f}M. This page adds the acquired '
                f'parcel and reads ${COMB_NOI[3] / 1e6:,.2f}M. Both are 2029. The estimated '
                'values on the valuation slide cover the hotel alone and carry nothing for the '
                'parcel.', fs='15px', col='rgba(255,255,255,.88)', lh='1.5', ind=4)
            + '  </div>\n')
    stats = ('  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 32px;'
             'margin-top:20px;padding-top:18px;border-top:2px solid var(--mm-navy);">\n')
    for i, (lab, val, nt) in enumerate(
            [('Combined NOI &middot; 2029', f'${COMB_NOI[3]:,}', 'Hotel and parcel, unlevered'),
             ('Parcel Contribution', f'{DOG["noi"][2] / COMB_NOI[3]:.1%}',
              f'${DOG["noi"][2]:,} of combined income'),
             ('Combined Margin &middot; 2029', f'{COMB_NOI[3] / COMB_REV[3]:.1%}',
              f'On ${COMB_REV[3]:,} of revenue')]):
        bl = '' if i == 0 else f'border-left:{HAIR};padding-left:32px;'
        stats += (f'    <div style="{bl}">\n'
                  f'      <div style="{CON}font-size:11.5px;letter-spacing:.15em;'
                  f'color:{ORANGE};">{lab}</div>\n'
                  f'      <div style="{DISP}font-weight:700;font-size:30px;color:{NAVY};'
                  f'line-height:1.1;margin-top:6px;">{val}</div>\n'
                  + P(nt, fs='13px', col='var(--ink-500)', mt='5px', ind=6) + '    </div>\n')
    stats += '  </div>\n'
    return page('Combined Pro Forma', sn,
      rule(mb='18px') + H2('Hotel and parcel together.', fs='38px', mb='20px')
      + tbl(['Line item'] + COMB_YEARS, rows, fs='14.5px', pad=13, lw='1.95fr')
      + stats + note, pad='56px 92px 42px')


# ── assembly ─────────────────────────────────────────────────────────────────────────────────
PAGES = [('COVER', cover), ('THE OPPORTUNITY', opportunity), ('THE ASSET', asset),
         ('THE SPONSOR', sponsor), ('BRAND AND TRACK RECORD', brand),
         ('BUSINESS PLAN', business_plan), ('FINANCIALS', financials),
         ('DOGWOOD COVE PRO FORMA', dogwood), ('COMBINED PRO FORMA', combined),
         ('VALUATION', valuation), ('RENOVATION BUDGET', budget), ('NEXT STEPS', next_steps)]
PATH = f'{DECKDIR}/Wylder Tilghman Island - Investment Overview - Palette Hotels.dc.html'

# nothing about a capital structure may appear in this deck
FORBIDDEN = [
    'preferred', 'pref ', '17.00%', 'current pay', 'accrued', 'minimum multiple', '1.20x',
    '1.55x', 'profit participation', 'kicker', 'last-dollar', 'LTV', 'senior loan',
    'LCP Investors', 'waterfall', 'redemption', 'origination fee', 'broker fee',
    'carry reserve', 'value cushion', 'sources and uses', 'target close',
    '$7,276,056', '$7.28M', '$9,000,000', '$9.00M', '$16,276,056', '$8,731,268',
    '$11,252,661', '$727,606', '$823,769',
    'Hilton', 'September 21, 2026',
]
# the affiliation may be named on the business plan slide, and nowhere else
AFFILIATION = ('Small Luxury Hotels', 'SLH')


def build_deck():
    from v7_lib import load_sections
    head, _ = load_sections()
    out = head
    for i, (name, fn) in enumerate(PAGES):
        body = fn().replace('@@PAGE@@', f'{i + 1:02d}')
        out += f'<!-- ═══════════ {i + 1:02d} · {name} ═══════════ -->' + body + '\n\n'
    out = out.rstrip('\n') + TAIL
    # rule 5: no em dashes anywhere, in markup, copy or speaker notes
    assert '—' not in out and '&mdash;' not in out, 'em dash in the Palette deck'
    io.open(PATH, 'w', encoding='utf-8').write(out)
    return PATH, len(PAGES)


if __name__ == '__main__':
    path, n = build_deck()
    s = io.open(path, encoding='utf-8').read()
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
                                     re.sub(r'data-speaker-notes="[^"]*"', ' ', s)))
    hits = [w for w in FORBIDDEN if w.lower() in txt.lower()]
    # the affiliation belongs to the business plan slide alone
    _slides = re.split(r'<!-- ═+ \d+ · ([^═]*?) ═+ -->', s)
    _elsewhere = ''.join(_slides[i + 1] for i in range(1, len(_slides), 2)
                         if _slides[i] != 'BUSINESS PLAN')
    hits += [f'{w} outside the business plan' for w in AFFILIATION if w in _elsewhere]
    brit = [w for w in ('utilise', 'organis', 'centre', 'labour', 'colour', 'analyse')
            if w in txt.lower()]
    print(f'  {path.split("/")[-1]}  ,  {n} slides')
    print(f'  capital structure or brand language: {hits or "none"}')
    print(f'  em dashes: {s.count(chr(0x2014)) + s.count("&mdash;")}')
    print(f'  British spelling: {brit or "none"}')
    print(f'  names its valuation source: {[w for w in ("CBRE", "LW Hospitality") if w in txt]}')
