# Layout gadgets in production

| File | Slot | Purpose |
|---|---|---|
| `gadget_sources.html` | `main-top` | "How this site works" — sources + interpretation brief |
| `gadget_topics.html` | `main-bottom` | Browse-all-articles-by-topic (regenerate from blog-build/idx_groups.json when posts are added) |

Both are pure HTML (no scripts) and style themselves with the theme's `var(--…)`
tokens so palette changes flow through. The Featured Post gadget in the `featured`
slot is pinned to the Article Index post ("Use most recent post" OFF — leaving it
ON puts the newest 500KB data post in the hero and exhausts Blogger's render
budget, emptying the post list).
