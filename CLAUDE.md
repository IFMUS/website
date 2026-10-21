# CLAUDE.md

Guidance for Claude (and humans) working on this repository.

## What this is

A static prototype of the website for **IFMUS, the International Family Medicine
Ultrasound Society**: the only international society devoted to point-of-care
ultrasound (POCUS) in family medicine. Audience: GPs/family physicians, residents,
educators and researchers worldwide. The site's main job today is to explain the
society and get people to **become members**.

Mission line: "Learn. Connect. Teach. Research. Lead."
Tagline: "Advancing POCUS · Empowering clinicians · Improving care"

## How the site is built

Plain HTML/CSS, no framework, no dependencies beyond Python 3's standard library.

- `src/build.py` holds **all page content** and the shared header, footer and
  script. Each page is an entry in `PAGES[key] = (title, active_nav_key, html_body)`.
  Page order is `ORDER`; top navigation is `NAV`.
- `src/styles.css` is the **only** stylesheet source.
- Run `python3 src/build.py` to generate the site into `dist/` (`*.html` and
  `styles.css`).
- `dist/` is generated output and is **gitignored: never commit it**, and never
  edit files in it by hand. Change `src/`, rebuild, and commit only `src/`.
- Internal links in page bodies use `href="@page"` (for example `href="@membership"`,
  `href="@home"`). The build rewrites them to `page.html` (multi-page site) or
  `#page` (single-file preview). Don't hard-code `.html` links.
- `python3 src/build.py preview.html` also writes a single-file preview
  (all pages in one HTML file with hash navigation). `preview.html` is gitignored.
- The logo is inlined from `src/brand/ifmus-logo.svg` by `logo()`, which recolours
  it to `currentColor` / `--logo-halo` so it follows the theme. If you replace the
  logo SVG, keep the blue fills `#0a5ca8` (or `#285ba3`) and white halo fills so
  that recolouring still works.

To check a change, rebuild and open `dist/index.html` in a browser (or serve the
folder: `python3 -m http.server -d dist`). Check both light and dark mode and a
narrow (phone) viewport.

## Pages

| Key | File | Content |
| --- | --- | --- |
| home | index.html | Hero, mission verbs, member highlights, clinical hubs |
| about | about.html | Who we are, goals, regional clinical hubs, people |
| membership | membership.html | The 11 member benefits, fees, FAQ |
| join | join.html | Join form (demo) leading to PayPal; nav highlights "Membership" |
| education | education.html | Image library, technique guides, scan review, webinars |
| events | events.html | Webinars and annual conference |
| research | research.html | Research network and updates |
| contact | contact.html | Contact details and contact form (demo) |

## Design system

All colours, fonts and radii are CSS custom properties on `:root` in
`src/styles.css`, with a dark-mode set under `prefers-color-scheme: dark`
and `[data-theme="dark"]`. **Use the tokens, never raw colours**, and when you add
a token add its dark value in both dark blocks.

- Primary ink: logo blue `--brand` (#0a5ca8) for buttons, links, key headings.
- Warm blush palette for grounds and tints (`--band`, `--brand-soft`, `--accent`,
  `--warm`); warm charcoal footer (`--deep`). **Never orange.**
- Font: Public Sans (Google Fonts).
- The probe-and-sound-waves motif (logo and home hero art) is the recurring brand shape.
- Reusable classes include `.wrap`, `.section`, `.band-warm`, `.page-hero`,
  `.section-head`, `.eyebrow`, `.lede`, `.grid-2`, `.grid-3`, `.card`, `.card-link`,
  `.tag`, `.btn` + `.btn-primary` / `.btn-ghost` / `.btn-accent`, `.btn-row`,
  `.prose`, `.checks`, `.stat-row`, `.form`, `.field`, `.placeholder`. Reuse them
  before writing new CSS.
- `resources/palette-options.png` shows the palettes that were considered;
  the blush + blue option is the one in use.

## Content facts (keep consistent across pages)

Source: `docs/member-invitation-letter.md` and the benefits infographic in
`resources/ifmus-benefits-infographic.jpeg`.

- Fees: standard **€50/year**; residents **€25/year**; clinicians in low- and
  lower-middle-income countries (World Bank classification) **€25/year**.
- 11 member benefits in four groups (educational resources, professional
  development, leadership, conference). Defined once in `BENEFITS` in `build.py`.
  Note the source letter lists benefit 6 before 5; the site keeps that numbering.
- 25% discount on the annual scientific conference.
- Membership Officer: Eva Leceaga-Gaztambide.
- Payment is via PayPal.

Writing style: plain, warm, direct English for busy clinicians; short sentences;
sentence-case headings; spell out POCUS on first use per page.

## Still placeholder / not real

- PayPal link, contact email and website (`[INSERT …]`, styled with `.placeholder`).
- Forms with class `js-demo-form` don't submit anything; a script shows
  "This is a prototype, so nothing was sent."
- Events, people, hub directors and scan images are illustrative examples.
- Footer says "Prototype. Content subject to change."

## Repository layout

```
src/         build.py, styles.css, brand/ logos (all sources)
resources/   reference images (original logo SVG, benefits infographic, palette options)
docs/        content sources (member invitation letter, notes on inputs)
dist/        generated site (gitignored)
```
