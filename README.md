# IFMUS website prototype

Static prototype of the International Family Medicine Ultrasound Society website.
See `CLAUDE.md` for how the build, design tokens and content are organised.

## Layout

```
src/                  Everything the site is built from
  build.py            Page content and templates; generates the site
  styles.css          Stylesheet source, copied into dist/ on build
  brand/              Logos (ifmus-logo.svg is inlined into every page)
resources/            Reference material, not used by the build
  ifmus-benefits-infographic.jpeg  Original member benefits infographic (brand source)
  ifmus-logo-source.svg            Original logo SVG as provided
  palette-options.png              Colour palette options explored for the design
docs/                 Content notes
  member-invitation-letter.md      Member invitation letter (benefits, fees)
  inputs.md                        Notes on the source inputs
dist/                 Generated site (not committed)
```

## Building

Requires Python 3 (standard library only).

```sh
python3 src/build.py
```

This writes the site to `dist/` (gitignored). Open `dist/index.html`, or serve it
with `python3 -m http.server -d dist`.

To also produce a single-file preview with hash navigation:

```sh
python3 src/build.py preview.html
```

The pages load the Public Sans font from Google Fonts; everything else is inlined
or in `dist/`.
