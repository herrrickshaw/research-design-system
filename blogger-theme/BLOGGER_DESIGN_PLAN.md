# Step-by-Step Web Design Plan for Blogger
### masaladeutsch.blogspot.com — using every layer Blogger actually exposes

Framework: the Discovery → Exploration → Implementation process from Beaird,
*The Principles of Beautiful Web Design* (SitePoint, 2010), mapped onto Blogger's
real feature set. Every "hard rule" below was learned on this blog, live, not from
a book.

---

## Phase 0 — Safety rails (before touching anything)

1. **Back up the theme XML**: Theme → ⋮ → Backup. Keep dated copies
   (`notable-antique-backup-2026-08-04.xml` exists in ~/Downloads).
2. **Record the post count** (69). A post silently reverting to draft is only
   detectable by count reconciliation against
   `feeds/posts/default?alt=json&max-results=1`.
3. Know the rollback: theme restore is one upload; Layout re-arrangement is not
   restored with it, so screenshot the Layout page too.

## Phase 1 — Discovery (Beaird ch.1: know the site before styling it)

4. **Define the reader task**: this is a data-analysis publication. The reader
   either (a) reads the newest piece, (b) hunts a topic, or (c) cites a number.
   Every layout decision serves one of those three.
5. **Inventory the content**: 69 posts, 10 topic groups, sizes 13KB–532KB.
   The size spread is a design constraint, not trivia — see rule R1.
6. **Inventory Blogger's levers** (the full feature set):
   - **Theme XML**: `b:skin` CSS, `b:section`/`b:widget` markup, per-pageType
     branches (`index` vs `item` vs `static_page` vs `archive`)
   - **Layout**: gadget slots per section (Featured Post, HTML/JavaScript,
     PageList, Blog Search, Blog Archive, Labels, Profile, AdSense, Attribution)
   - **Pages**: static pages for About / Methods / Sources
   - **Settings**: max posts on main page, meta description, custom permalinks,
     per-post search descriptions, HTTPS redirect, custom domain
   - **Post editor**: per-post HTML, scheduled/backdated publishing (= ordering
     control), labels, location, custom permalink
   - **Feeds**: `feeds/posts/default` (JSON/Atom) — the only reliable
     verification surface

## Phase 2 — Exploration (structure before decoration)

7. **Layout grid** (Beaird: grid theory / rule of thirds): single reading column
   capped at `--wrap:1080px`, text measure `70ch`. Wide tables scroll inside
   their own container, never the page.
8. **Page anatomy** top-to-bottom, matching reader tasks in priority order:
   sticky header + nav → *Recent analysis* (3 snippet cards) →
   *Browse all N articles by topic* (10-group grid) → pager → footer.
   Newest work first; the whole archive one scroll below.
9. **Emphasis** (Beaird: placement/contrast/proportion): one accent colour
   (#2251FF) for links and rules; display headings light-weight (300) at large
   sizes with bold reserved for the emphasised word; kickers in cyan smallcaps.
10. **Unity by repetition**: the same navy/blue/slate tokens as the in-post
    `gb-*` article template, so theme and posts read as one publication.
11. **Color** (Beaird ch.2): near-monochrome navy scale + one warm-free accent;
    AA contrast is a release gate, not an aspiration (see Phase 4).

## Phase 3 — Implementation on Blogger, in order

12. **Theme first** (`masaladeutsch.xml`, 11.5KB, zero scripts):
    - index branch renders `data:post.snippet` ONLY (rule R1)
    - `main-top` and `main-bottom` sections with `showaddelement='yes'`
      (rule R2 — modern Google themes forbid this; it is the reason for a
      custom theme at all)
    - light-only palette (rule R3)
13. **Settings**: max posts on main page = 3 (measured limit, rule R1);
    meta description filled; HTTPS redirect on.
14. **Layout gadgets**:
    - `main-bottom` ← HTML gadget with the by-topic index (68 links, 10 groups,
      regenerate from the feed when posts are added)
    - `nav` ← PageList (About, Article Index, Reportage)
    - AdSense units only after the design settles
15. **Posts**: ordering on the homepage is controlled by publish timestamp —
    backdate/re-time deliberately, never into the future (future = scheduled =
    unpublished). Add per-post search descriptions for the flagship pieces.
16. **Static pages** for About / Methods; link them from `nav`.

## Phase 4 — Verification gates (every change, no exceptions)

17. **Contrast audit in the failure mode**: measure computed contrast of
    elements that have *no background of their own* against the effective page
    background, with the OS in dark mode. Card-text-on-card passes while
    heading-on-page fails — test the second one. Gate: ≥4.5:1 everywhere.
18. **Post-count reconciliation** via the JSON feed after any save.
19. **No horizontal scroll at 375px**; wide content scrolls in its own box.
20. **Script audit on the live page**: external script hosts must be
    Google/Blogger only.
21. Re-run `validate.py` after any theme edit (XML well-formedness, snippet-only
    index, gadget slots present, zero scripts, no `--` in XML comments).

---

## Hard rules learned on THIS blog (violating any of these broke production)

- **R1 — Snippets on index pages, never `data:post.body`.** Full bodies exhaust
  Blogger's per-page render budget on 30–530KB posts and the post list comes
  back *empty with no error*. Also cap main-page posts low (3).
- **R2 — Modern Google themes (Contempo/Soho/Emporio/Notable) accept no gadgets
  in the page body** and hide the sidebar in a drawer. If content-adjacent
  gadgets are needed, the theme must declare its own sections.
- **R3 — No `prefers-color-scheme` dark block anywhere**, theme or post. The
  posts force `body{background:#fff!important}`, which beats the theme, so a
  dark block turns text near-white on a white page. Light-only until every post
  drops its force-white override.
- **R4 — No third-party scripts.** Free template marketplaces bundle
  packed/encrypted footer-credit JS (`function(p,a,c,k,e,d)`); disqualifying.
- **R5 — `--` inside an XML comment is invalid**; Blogger rejects the upload.
- **R6 — Verify on the live URL, not the editor.** "Saved" toasts, detached
  editors and stale dirty-flags all lie; the public feed and rendered page are
  the only truth.

## Maintenance loop

- New post → it appears in *Recent analysis* automatically.
- Monthly (or after a batch of posts): regenerate the by-topic gadget from the
  feed + `idx_groups.json`, paste into the `main-bottom` gadget.
- After any theme edit: `validate.py` → upload → Phase 4 gates.
