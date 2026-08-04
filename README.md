# Research Design System

One token contract, four themes, one component set — extracted from the design assets
already in use across ~42 local repos and two Blogger properties, then consolidated so
new work doesn't reinvent them.

Includes [`INVENTORY.md`](INVENTORY.md): a classified record of every HTML, CSS and JSON
design/template asset found in the workspace.

## Install

Load in this order. Order matters — themes rebind tokens, components read them.

```html
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="themes/report.css">
<link rel="stylesheet" href="components/components.css">
<link rel="stylesheet" href="print/print.css" media="print">
```

```html
<body class="rds theme-report">
  <div class="rds-wrap"> … </div>
</body>
```

## The contract

`tokens/tokens.css` defines three layers:

| Layer | Example | Who may use it |
|---|---|---|
| **Palette** | `--teal-deep`, `--navy`, `--gray-6` | themes only |
| **Scale** | `--step-2`, `--sp-5`, `--radius` | anyone |
| **Semantic** | `--c-text`, `--c-accent`, `--c-border` | components only |

The rule that keeps it maintainable: **components never reference a raw palette value.**
A theme is therefore just a rebinding of the ~12 `--c-*` tokens. `tokens/tokens.json`
carries the same values for tooling.

## Themes

| Theme | Use for | Ground | Accent |
|---|---|---|---|
| `theme-bulletin` | editorial posts — the house style | warm paper `#fcfcfa` | teal `#1f5f5b` |
| `theme-report` | long-form analyst reports | white | navy `#051c2c` / blue `#2251ff` |
| `theme-reportage` | announcement feeds, quarterly digests | sage `#eef1ea` | teal `#1f5f5b` |
| `theme-slate` | dashboards, repo sites | slate `#0f172a` | blue `#3987e5` |

## Components

`rds-wrap` · `rds-masthead` · `rds-eyebrow` · `rds-dek` · `rds-num` · `rds-stats`/`rds-stat`
· `rds-exhibit` · `rds-table` · `rds-side` · `rds-warn` · `rds-card` · `rds-grid`/`rds-item`
· `rds-pill` · `rds-pager` · `rds-source` · `rds-note`

Live examples: [`docs/index.html`](docs/index.html). Starting points:
[`templates/report.html`](templates/report.html),
[`templates/bulletin.html`](templates/bulletin.html),
[`templates/dashboard.html`](templates/dashboard.html).

## Conventions worth keeping

- **Units go in the table header, not in every cell.** `<th>FY26 ($M)</th>`, then bare
  numbers in `.num` cells (right-aligned, `tabular-nums`).
- **Every exhibit carries a source note** with dataset, vintage and retrieval date.
- **Wide content scrolls in its own container** (`.rds-table-wrap`); the page body never
  scrolls horizontally.
- **Reading width is capped** at `--measure` (68ch). Dashboards opt out with `.rds-wrap--wide`.

## Three bugs this system exists to prevent

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

## Provenance

Consolidated from `chemical_import_substitution/design/design_v2.css` (Open Color ramp,
fluid type), `docs/style.css` (slate shell),
`india-trade-sector-policy-recommendations/print/print.css` (A4 print), and the token
systems embedded in published posts on `masaladeutsch.blogspot.com` and
`usiponavadaaariponacoffee.blogspot.com` — which is where most of the real design
language lived, uncommitted to any repo.
