# IFMUS website prototype

Static prototype of the International Family Medicine Ultrasound Society website.

## Layout

```
site/                 Built static site (open site/index.html in a browser)
  *.html, styles.css  Generated pages and stylesheet — do not edit by hand
  brand/              Logos used by the site (ifmus-logo.svg, ifmus-logo-white.svg)
  src/build.py        Page content and templates; generates the pages
  src/styles.css      Stylesheet source, copied to site/styles.css on build
resources/            Reference material, not used by the build
  ifmus-benefits-infographic.jpeg  Original member benefits infographic (brand source)
  ifmus-logo-source.svg            Original logo SVG as provided
  palette-options.png              Colour palette options explored for the design
docs/                 Content notes
  member-invitation-letter.md      Member invitation letter (benefits, fees)
  inputs.md                        Notes on the source inputs
```

## Building

Requires Python 3 (standard library only).

```sh
python3 site/src/build.py
```

See `CLAUDE.md` for how the build, design tokens and content are organised.

This regenerates `site/*.html` and `site/styles.css` from `site/src/`. Edit the
sources, rebuild, and commit both the sources and the generated files.

To also produce a single-file preview with hash navigation:

```sh
python3 site/src/build.py preview.html
```

The pages load the Public Sans font from Google Fonts; everything else is local.
