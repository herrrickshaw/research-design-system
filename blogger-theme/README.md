# Masala Deutsch — Blogger theme

A Blogger XML theme for long, data-heavy analysis posts. Built after two real
failures on masaladeutsch.blogspot.com that no off-the-shelf template addresses.

## Why it exists

**1. Gadget slots in the page body.** Blogger's modern themes (Contempo, Soho,
Emporio, Notable) expose *no* "Add a Gadget" slot in the page body — only the
sidebar, which in those themes is an off-canvas drawer. An all-articles-by-topic
index therefore cannot be placed with the content. This theme declares
`main-top` and `main-bottom` sections either side of the post list, both
accepting gadgets.

**2. Index pages render snippets, never full bodies.** With posts of 30–530KB,
rendering full bodies on the homepage exhausted Blogger's per-page budget and the
post list came back *completely empty* — no error, just nothing. The index branch
uses `data:post.snippet` only. Never put `data:post.body` in it.

## Guarantees

- Zero `<script>` tags. Zero external hosts. No packed/encrypted footer credits.
- No web fonts — system serif for reading, system sans for UI.
- Dark mode flips surface *and* text in the same rule. Safe here because a theme
  owns `<body>`; the same pattern inside a *post* is a bug, because the post does
  not own the page background.
- WCAG AA on every text element, verified in both modes:
  light minimum 5.69:1 · dark minimum 7.71:1 · zero failures.
- No horizontal page scroll at 375px.

## Sections

| id | where | gadgets |
|---|---|---|
| `nav` | header | yes (max 2) |
| `featured` | hero band | yes (max 1) |
| `main-top` | above post list | **yes** |
| `main` | post list | yes |
| `main-bottom` | below post list | **yes** |
| `footer` | footer | yes |

## Install

Blogger → Theme → ⋮ → **Backup** (save the current XML first), then
**Restore / Upload** this file. Switching themes resets the Layout arrangement,
so re-pin the Featured Post afterwards.

## Verify after any edit

    python3 validate.py

Checks XML well-formedness, required Blogger structure, and that the index
branch still uses snippets rather than post bodies.
