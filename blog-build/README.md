# blog-build — generators for the masaladeutsch.blogspot.com data posts

| File | Produces | Data input |
|---|---|---|
| `build_post.py` | Quarterly Reportage post (client-rendered, ~530KB) | `rows.json` extracted from digital-twin-for-ipa `docs/reportage.html` |
| `build_pq_post.py` | Lok Sabha Question Registry post | digital-twin-for-ipa `data/registers/ls_pq_registry.json` (absolute path) |
| `build_rs_post.py` | Rajya Sabha Question Registry post | digital-twin-for-ipa `data/registers/rs_pq_registry.json` (absolute path) |
| `insert_5ai.py` | Section 5a-i (BIS policy-rate table) for the green-debt article | BIS WS_CBPOL rates, embedded & verified in-script |
| `idx_groups.json` | Topic grouping consumed by the browse-by-topic gadget | curated from the Article Index post |

Paths assume the authoring session layout (Claude Code scratchpad + local
digital-twin-for-ipa clone); adjust the input paths when running elsewhere.

Shared invariants (violating these broke production — see blogger-theme/README.md):
payloads are ASCII-forced with &,<,> unicode-escaped so Blogger's editor cannot
mangle them; posts are light-only (no prefers-color-scheme blocks); posts carry the
Google-Translate widget and the AI-assistance disclaimer.
