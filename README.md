# Research Design System

A CSS design system for research reports, editorial bulletins and dashboards: one token contract,
four themes and one component set, plus the Blogger theme and post generators that publish with it.
It produces plain CSS/HTML assets (no build step) and a few self-contained Blogger post HTML files.

> Status: maintained. Extracted from design assets used across ~42 local repos and two Blogger
> properties. No licence file yet; all rights reserved. See also [How to use this repo with AI](HOW_TO_USE_WITH_AI.md).

## What it does
- Defines a three-layer token contract (palette, scale, semantic) in `tokens/tokens.css` and `tokens/tokens.json`.
- Ships four themes (`bulletin`, `report`, `reportage`, `slate`) that only rebind the semantic `--c-*` tokens.
- Provides one component set (`rds-*` classes) and an A4 print stylesheet tuned for WeasyPrint.
- Includes starter templates for a report, a bulletin and a dashboard, and a live gallery in `docs/index.html`.
- Includes a Blogger XML theme with a validator (`blogger-theme/validate.py`).
- Includes generators for the masaladeutsch.blogspot.com data posts (`blog-build/`).

## Quick start
```bash
git clone https://github.com/herrrickshaw/research-design-system.git
cd research-design-system
open docs/index.html          # live examples; or copy a file from templates/
```

Load in this order. Order matters: themes rebind tokens, components read them.

```html
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="themes/report.css">
<link rel="stylesheet" href="components/components.css">
<link rel="stylesheet" href="print/print.css" media="print">
```

```html
<body class="rds theme-report">
  <div class="rds-wrap"> ... </div>
</body>
```

## How it works
| Stage | Module | Output |
|---|---|---|
| Tokens | `tokens/tokens.css` | palette, scale and semantic custom properties |
| Theme | `themes/*.css` | rebinding of the ~12 `--c-*` tokens |
| Components | `components/components.css` | `rds-*` classes that read only semantic tokens |
| Print | `print/print.css` | A4 pagination rules |
| Blog posts | `blog-build/build_*.py` + `blog-build/blogkit.py` | one self-contained Blogger post HTML per script |

### The contract

`tokens/tokens.css` defines three layers:

| Layer | Example | Who may use it |
|---|---|---|
| **Palette** | `--teal-deep`, `--navy`, `--gray-6` | themes only |
| **Scale** | `--step-2`, `--sp-5`, `--radius` | anyone |
| **Semantic** | `--c-text`, `--c-accent`, `--c-border` | components only |

The rule that keeps it maintainable: **components never reference a raw palette value.**
A theme is therefore just a rebinding of the ~12 `--c-*` tokens. `tokens/tokens.json`
carries the same values for tooling.

### Themes

| Theme | Use for | Ground | Accent |
|---|---|---|---|
| `theme-bulletin` | editorial posts — the house style | warm paper `#fcfcfa` | teal `#1f5f5b` |
| `theme-report` | long-form analyst reports | white | navy `#051c2c` / blue `#2251ff` |
| `theme-reportage` | announcement feeds, quarterly digests | sage `#eef1ea` | teal `#1f5f5b` |
| `theme-slate` | dashboards, repo sites | slate `#0f172a` | blue `#3987e5` |

### Components

`rds-wrap` · `rds-masthead` · `rds-eyebrow` · `rds-dek` · `rds-num` · `rds-stats`/`rds-stat`
· `rds-exhibit` · `rds-table` · `rds-side` · `rds-warn` · `rds-card` · `rds-grid`/`rds-item`
· `rds-pill` · `rds-pager` · `rds-source` · `rds-note`

Starting points: [`templates/report.html`](templates/report.html),
[`templates/bulletin.html`](templates/bulletin.html), [`templates/dashboard.html`](templates/dashboard.html).

### Conventions worth keeping

- **Units go in the table header, not in every cell.** `<th>FY26 ($M)</th>`, then bare
  numbers in `.num` cells (right-aligned, `tabular-nums`).
- **Every exhibit carries a source note** with dataset, vintage and retrieval date.
- **Wide content scrolls in its own container** (`.rds-table-wrap`); the page body never
  scrolls horizontally.
- **Reading width is capped** at `--measure` (68ch). Dashboards opt out with `.rds-wrap--wide`.

## Repository layout
| Path | Purpose |
|---|---|
| `tokens/` | token contract as CSS and JSON |
| `themes/` | four theme stylesheets |
| `components/`, `print/` | component and print stylesheets |
| `templates/`, `docs/` | starter pages and the live example gallery |
| `blogger-theme/` | Blogger XML theme, design notes, gadget snippets, `validate.py` |
| `blog-build/` | Blogger post generators; shared helpers in `blogkit.py` (see its README) |
| `tests/` | pytest suite for `blogkit.py` and `validate.py` |
| `INVENTORY.md`, `inventory.json` | classified record of 67 design/template assets found in the workspace (2026-08-04 snapshot) |

## Data sources
Only the `blog-build/` generators consume data, and only from sibling local clones
(`digital-twin-for-ipa`, `india-trade-sector-policy-recommendations`) or a `rows.json` extract.
Upstream sources are sansad.in, rsdoc.nic.in, PIB and BIS WS_CBPOL; see `blog-build/README.md`.

## Configuration
None for the CSS. The generators use absolute or `~`-relative paths from the authoring machine
(documented in `blog-build/README.md`); edit them when running elsewhere. No secrets are needed or stored.

## Testing
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff
ruff check . && pytest -q
(cd blogger-theme && python3 validate.py)    # theme structure checks
```

## Limitations and known issues
- The post generators cannot run without the author's local data clones; they are kept as a record of the build.
- `build_pq_post.py` and `build_rs_post.py` write to a hard-coded scratch path. Left unchanged to preserve behaviour.
- The Blogger posts are light-only by design (see the dark-mode hazard below).

### Three bugs this system exists to prevent

Each cost real debugging time. The fixes are in the code with comments — please don't
"tidy" them away.

**1. Invisible black-on-dark text.** A `prefers-color-scheme: dark` block flipped surface
tokens dark while published text stayed force-black. Dark mode here is **opt-in**
(`<html data-theme="dark">`), and `theme-reportage` is the reference for doing it right:
it flips `--c-text` in the *same block* as the surfaces. Flip text and surface together,
or not at all.

**2. Drop-caps eating your UI.** Blogger themes apply `::first-letter` to post bodies,
which enlarged the leading character of every block — including a bare `←`, which then
read as a broken button. `components.css` neutralises `::first-letter` inside `.rds`.

**3. WeasyPrint hangs and blank first pages.** In `print/print.css`: the page-total span
must be `position:absolute` (otherwise it opens a line box and emits a blank leading
page), and you must **not** force `display:block` on flex containers during pagination
(observed hang: 6 hours).

### Provenance

Consolidated from `chemical_import_substitution/design/design_v2.css` (Open Color ramp,
fluid type), `docs/style.css` (slate shell),
`india-trade-sector-policy-recommendations/print/print.css` (A4 print), and the token
systems embedded in published posts on `masaladeutsch.blogspot.com` and
`usiponavadaaariponacoffee.blogspot.com` — which is where most of the real design
language lived, uncommitted to any repo.

## Licence
No licence file yet; all rights reserved.
