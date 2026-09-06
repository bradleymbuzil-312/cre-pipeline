# TRANCHE Group — Design System

**The TRANCHE Group** is a debt and equity capital advisory practice within **Marcus & Millichap Capital Corporation (MMCC)**, led by Senior Director Bradley M. Buzil. The practice engineers financing solutions across every layer of the commercial real estate capital stack — agency and life-company senior debt, bridge, mezzanine, preferred equity, and JV equity.

The brand sits inside MMCC's institutional capital-markets identity: classical Marcus & Millichap navy (PMS 295), the orange M&M accent bar, the Aptos type family across display/body/narrow/mono variants, and an underlined wordmark lockup that this system carries forward in every header and section title.

The visual concept of the system is the **tranche** itself — a layered slice. That metaphor shows up as horizontal strata (in the title slide, the contact slide, the stack diagram component), as the tier color system (senior → mezz → pref → equity), and as the underlined wordmark rule that separates a name from its qualifier the same way the M&M lockup separates "Marcus & Millichap" from "Capital Corporation".

---

## Sources & References

| Source | Status |
|---|---|
| `uploads/MMCC_logo2018_blue295.png`, `_black`, `_white`, `2021_black` | ✅ Imported → `assets/logos/` |
| `uploads/MarcusMillichapLogo.jpg` (navy + orange brand mark) | ✅ Imported → `assets/logos/` |
| `uploads/photo-010.jpg` (Bradley M. Buzil headshot) | ✅ Imported → `assets/team/` |
| `uploads/MMCC Deck_2026.pptx` | ⚠️ **NOT delivered** — referenced in the brief but never appeared in uploads. Slide system inferred from M&M public brand cues. |
| `uploads/235-237 Kent Ave Brooklyn, NY_marketing.pdf` | ⚠️ **NOT delivered** — used as a deal example in slides only |
| `uploads/401 Derby Oakland CA_Marketing (reduced).pdf` | ⚠️ **NOT delivered** — used as a deal example in slides only |
| https://www.marcusmillichap.com/financing | Public reference for institutional palette + lockup |

If the PPTX and PDFs are re-attached, the slide system and deal-card patterns can be tuned to match the actual layouts.

---

## Index

| File / folder | What's inside |
|---|---|
| `colors_and_type.css` | All design tokens: color variables, type scale, spacing, radii, elevation, motion. Import this in every artifact. |
| `assets/logos/` | All five MMCC logo variants (blue/black/white + 2021 refresh + branded JPG) |
| `assets/team/` | Bradley M. Buzil headshot |
| `preview/` | Design-system cards rendered in the Design System tab |
| `slides/` | Eight 1280×720 slide templates (title, section header, capital stack, stats, services, bio, quote, transactions, contact) |
| `SKILL.md` | Cross-compatible skill file for Claude Code |

---

## Content Fundamentals

**Voice.** Institutional, direct, no-filler. The practice speaks like a senior banker who closes deals, not a marketer. Sentences are declarative. Verbs are concrete (*originated*, *structured*, *placed*, *stress-tested*). Hedging language is absent.

**Person.** Third-person about the team ("The team's mandate…", "Bradley leads the TRANCHE Group…") and second-person to the sponsor ("aligned with **your** business plan"). Never first-person plural marketing-speak.

**Casing.**
- Display headlines: **sentence case** with a closing period for declarative statements (*"Structured capital for commercial real estate."*).
- Section headers / eyebrows: **ALL CAPS** with 0.18–0.28em tracking.
- Service lines and product names: **Title Case With Em Dashes** for definitions (*"Senior Debt Placement — Agency, life company, bank…"*).
- Numbers: always tabular, comma-grouped, with currency symbol prefixed (*$11.72B*, *$1,591*, *399*). Use abbreviations (B, M) for display, full digits for tables.

**Em dashes** are core punctuation — the practice's natural cadence is *concept — definition*. Use them liberally; the design system supports this rhythm in service-line lists and capital-stack legends.

**No emoji. No exclamation points.** This is a capital markets practice; tone is measured. Unicode bullets (·, —, ●) are used as separators — never decorative emoji.

**Acronyms** are spelled out on first reference: *Marcus & Millichap Capital Corporation (MMCC)*, *commercial mortgage-backed securities (CMBS)*. After that, the acronym alone is fine.

**Sample voice (copy from real materials):**
> "Every engagement begins with an underwriting-first conversation. Before the team approaches the market, sizing, pricing, and structure are stress-tested against current lender appetite so sponsors enter the process with realistic expectations and lenders receive a credible, well-packaged story."

> "Not just a loan — a financing outcome clients can build on."

---

## Visual Foundations

**Color.** Two anchors, almost nothing else.
- **Navy (PMS 295, `#002F6C`)** is the practice. Used for body text on cream, full-bleed backgrounds for title/contact slides, primary buttons, table rules, the wordmark underline.
- **Orange (`#E87722`)** is the M&M corporate accent. Used surgically — eyebrows, the topmost equity layer in stack diagrams, hover/active states, single emphasis spans inside quotes. Never as a primary surface.
- **Paper (`#FAF8F4`)** — warm cream, not white — for default surfaces. Pages feel like offering memoranda, not SaaS dashboards.
- **Tier palette** — navy → blue-gray → warm brass → orange — encodes the capital stack from senior to equity. Used in stack diagrams, deal tags, badges. Never used as decorative color elsewhere.

**Type.** A single-family system based on Microsoft's **Aptos**. Aptos is a humanist sans designed to perform across UI, document, and presentation contexts — using all four optical variants together gives the system enough hierarchy to feel institutional without leaving the family.
- **Aptos Display** — used for all H1/H2 headlines, title-slide displays, and italic pull quotes. Bold 700 default; italic is meaningful for taglines (*"A tranche is a layered slice of capital."*).
- **Aptos** (text) — used for all long-form body, ledes, captions, and lockup qualifiers. Regular 400 is the default body weight; Light 300 reads well at large sizes; SemiBold 600 / Bold 700 are reserved for emphasis runs. Italic, ExtraBold, and Black are available for editorial moments.
- **Aptos Narrow** — used for eyebrows, ALL-CAPS labels, table-column headers, form labels, and tabular tags. The narrow proportions provide counter-rhythm against the wider display/body. Italic + Bold-Italic variants are loaded.
- **Aptos Bold** (uppercase, tracked) — reserved for **buttons and CTAs only**. Sits at 12px / 0.08em tracking / uppercase.
- **Aptos Mono** — used exclusively for **currency figures, deal IDs, phone numbers, recognition-year lists**. Tabular-nums is on by default for any numeric span — financial tables must align.
- **Aptos Serif** — *optional editorial alternative.* Not part of the default cascade. Available via `var(--font-serif)` for pull quotes inside long-form offering memoranda or term-sheet preambles when the brief calls for a serif voice. Default Tranche artifacts stay all-sans.
- The wordmark-rule motif (`text + underline`) is a primary device. Use `.wordmark-rule` to underline a name + sit a subordinate qualifier beneath it.

**Layout.**
- Generous whitespace; institutional density. Body containers max ~64ch.
- Hard hairline rules (`1px solid var(--hairline)`) and brand rules (`1px solid var(--mm-navy)`) divide content. Section headers always have a navy rule beneath them. Avoid soft dividers, gradients, or background "cards."
- 8pt spacing scale. 12-column grid in slides; institutional five-column grid for service breakouts.

**Backgrounds.**
- No gradients (except subtle navy → deeper navy on the title slide for atmosphere — flagged for review).
- No hand-drawn illustrations, no textures, no glassmorphism.
- The "strata" / capital-stack pattern (horizontal bands of tier colors) is the **one** decorative motif. Use sparingly — title slide edge, contact slide edge.
- Photography is on-brand only: corporate portraits, asset photography from offering memoranda. Warm, natural light. No stock photos of "diverse business teams shaking hands."

**Cards & elevation.**
- Cards are flat: white surface, 1px hairline border, no rounding past 4px.
- Elevation is paper-like (`shadow-1`/`shadow-2`) — a 1px shadow on the bottom edge plus a faint blur. Reserve `shadow-3` for modals.
- No "colored left-border accent" cards.

**Corners.** Default `0–2px` everywhere. Cards `4px` max. Pills `999px`. Buttons `2px`. The system feels printed, not "app-like".

**Borders.** Always 1px. Brand-emphasis borders use `--mm-navy` solid; structural dividers use `--hairline` (`rgba(0,26,61,.12)`).

**Motion.**
- 120ms / 200ms / 320ms only, all with `cubic-bezier(.2,0,0,1)`. Mostly opacity and color crossfades.
- No bounces, no parallax, no scroll-jacking. Hover states are color shifts, never scale transforms.

**States.**
- Hover (button primary): background `--mm-navy` → `--mm-navy-900`.
- Hover (button secondary/link): fill the outline (border navy → background navy, text white).
- Press: 0.5px Y-translate, no scale.
- Focus: `box-shadow: inset 0 0 0 1px var(--mm-navy)` on inputs.

**Transparency & blur.** Almost never. Tag backgrounds use opaque tier-tinted swatches (`#EEF2F8`, `#FBE3CF`), not `rgba` over the surface. The one acceptable use of `rgba()` is the `--hairline` family.

**Imagery vibe.** Warm-natural. Daylit portraits, ground-up asset shots, no filters, no black-and-white. The Marcus & Millichap photo language is sober and direct.

---

## Iconography

The brand has **no proprietary icon font**. M&M and MMCC materials are typographic — they rely on rules, underlines, numerals, and the wordmark itself, not on icon systems.

**Recommendation:** Use **Lucide** (CDN: `https://unpkg.com/lucide@latest`) — 1.75px stroke, paired with `--mm-navy` on paper or `#fff` on navy. Lucide's line-icon weight matches the institutional feel; thicker or rounded icon families (Heroicons solid, Material) feel too consumer.

- **Stroke color:** `--mm-navy` on light surfaces, `--white` on navy.
- **Stroke weight:** 1.75 (Lucide default 2 is acceptable but slightly heavy).
- **Size:** 16 / 20 / 24 / 32. Never larger than the heading they sit beside.
- **No emoji.** No unicode pictographs as decoration. The bullet character `·` is the one accepted separator.
- **SVG over PNG** for any icon use. PNGs reserved for logos and photography.

When an existing M&M asset (the wordmark, the orange-bar branded JPG, the headshot) can do the job, prefer it over an icon. This brand earns trust through its marks and its photography, not pictograms.

> ⚠️ **Substitution flag:** Lucide is being used as a stand-in. If MMCC has an internal icon set (the PPTX may have contained one), please attach and the system will switch.

> ✅ **Brand fonts loaded.** The full Aptos family — Aptos, Aptos Display, Aptos Narrow, Aptos Mono, and Aptos Serif — across regular / semibold / bold / extrabold / black / italic weights, is present in `fonts/` and wired through `colors_and_type.css`. No external font CDN is used.

---

## CAVEATS — please read

1. **PPTX and marketing PDFs never came through uploads.** The slide system is inferred from public M&M brand cues + your TRANCHE narrative. Re-attach `MMCC Deck_2026.pptx` and the two marketing PDFs and I will re-tune layouts to match.
2. **Typography is Aptos.** Aptos Display (headlines), Aptos (body), Aptos Narrow (eyebrows/labels), and Aptos Mono (figures) are loaded from `fonts/` as Microsoft-issued TTFs. Buttons use Aptos Bold in uppercase. Replaces the prior serif/condensed/Plex stack at client direction.
3. **No proprietary icon set was supplied.** Lucide is the placeholder.
4. **No website source code was importable** for marcusmillichap.com — the financing page was treated as a reference for color/tone only, not pixel-perfect recreation. If you'd like full UI kits for the website or an internal MMCC portal, attach the codebase or Figma file and I'll build them.
