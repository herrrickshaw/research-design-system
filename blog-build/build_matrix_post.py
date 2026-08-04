#!/usr/bin/env python3
"""Render the scheme scrutiny matrix as a Blogger post: which schemes Parliament
discusses most, Lok Sabha and Rajya Sabha, against the government's own
announcement volume. 96 rows -- small enough to pre-render, no JS payload.
Light-only per site rule. Same aggregation as scripts/build_scrutiny_matrix.py.
"""
import datetime, json, os, sqlite3, sys

TWIN = os.path.expanduser("~/digital-twin-for-ipa")
sys.path.insert(0, os.path.join(TWIN, "scripts"))
from build_reportage import scheme_hits

DB = os.path.expanduser("~/india-trade-sector-policy-recommendations/data/pib_index.sqlite")
ACTIVE_MIN_Q, RECENT_DAYS = 10, 365
today = datetime.date.today()
recent = (today - datetime.timedelta(days=RECENT_DAYS)).isoformat()

pib = {}
for date, title in sqlite3.connect(DB).execute("SELECT date,title FROM pib_items"):
    if not date:
        continue
    for s in set(scheme_hits(title)):
        d = pib.setdefault(s, {"n": 0, "first": date, "last": date})
        d["n"] += 1
        d["first"] = min(d["first"], date)
        d["last"] = max(d["last"], date)

def load(path):
    rows = json.load(open(os.path.join(TWIN, "data/registers", path)))
    agg = {}
    for r in rows:
        for s in set(r["schemes"]):
            d = agg.setdefault(s, {"n": 0, "star": 0, "last": r["iso"]})
            d["n"] += 1
            d["star"] += (r["qtype"] or "").strip() == "STARRED"
            d["last"] = max(d["last"], r["iso"])
    return len(rows), agg

n_ls, ls = load("ls_pq_registry.json")
n_rs, rs = load("rs_pq_registry.json")

rows = []
for s in sorted(set(pib) | set(ls) | set(rs)):
    a = pib.get(s, {"n": 0, "first": "", "last": ""})
    l = ls.get(s, {"n": 0, "star": 0, "last": ""})
    r = rs.get(s, {"n": 0, "star": 0, "last": ""})
    tot = l["n"] + r["n"]
    last_q = max(l["last"], r["last"])
    b = "A" if (tot >= ACTIVE_MIN_Q and last_q >= recent) else ("B" if tot else "C")
    rows.append(dict(s=s, b=b, pib=a["n"], pib_first=a["first"], pib_last=a["last"], ls=l["n"], rs=r["n"],
                     star=l["star"] + r["star"], tot=tot, last=last_q))

A = sorted([r for r in rows if r["b"] == "A"], key=lambda x: -x["tot"])
B = sorted([r for r in rows if r["b"] == "B"], key=lambda x: -x["tot"])
C = sorted([r for r in rows if r["b"] == "C"], key=lambda x: -x["pib"])
ta = sum(r["pib"] for r in rows)

def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def table(rws, empty_qs=False):
    h = ('<div class="twrap"><table><thead><tr><th>Scheme</th>'
         '<th>First announced</th><th class="num">PIB anns</th><th class="num">LS Qs</th>'
         '<th class="num">RS Qs</th><th class="num">&#9733;</th>'
         '<th>Last question</th></tr></thead><tbody>')
    body = []
    for r in rws:
        body.append(f'<tr><td>{esc(r["s"])}</td><td>{r["pib_first"]}</td>'
                    f'<td class="num">{r["pib"]}</td>'
                    f'<td class="num">{r["ls"] or ""}</td><td class="num">{r["rs"] or ""}</td>'
                    f'<td class="num">{r["star"] or ""}</td>'
                    f'<td>{r["last"] or ("&#8212;" if empty_qs else "")}</td></tr>')
    return h + "".join(body) + "</tbody></table></div>"

# top-10 bar strip for the A list
mx = A[0]["tot"]
bars = "".join(
    f'<div class="bar"><span class="bl">{esc(r["s"][:38])}</span>'
    f'<span class="bt"><i style="width:{r["tot"]/mx*100:.1f}%"></i></span>'
    f'<span class="bn">{r["tot"]}</span></div>'
    for r in A[:10])

CSS = """<style>/*gs-typo-unify-v1*/
.smx{font-family:Georgia,'Times New Roman',serif!important;}
.smx p,.smx li,.smx td,.smx th{font-family:Georgia,'Times New Roman',serif!important;}
.smx h1,.smx h2,.smx h3{font-family:Georgia,'Times New Roman',serif!important;line-height:1.3!important;}
</style>
<style>
/* Light only. Site rule: posts force white backgrounds; no dark blocks anywhere. */
.smx{--ink:#051C2C;--mut:#5A666E;--acc:#2251FF;--accs:#EAF0FF;--line:#D4DDE5;--chip:#F4F7FB;
 background:#fff;color:var(--ink);line-height:1.6;max-width:none}
.smx *{box-sizing:border-box}
.smx ::first-letter{font-size:inherit!important;float:none!important;font-weight:inherit!important}
.smx .kick{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.72em;
 letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--acc)}
.smx h1{font-size:2em;margin:.3rem 0 .7rem;letter-spacing:-.01em}
.smx .dek{color:var(--mut);font-size:.95em;max-width:74ch;margin:0 0 1.1rem}
.smx h2{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:1.2em;font-weight:700;
 border-top:2px solid var(--ink);padding-top:.6rem;margin:2.2rem 0 .6rem}
.smx h2 .n{color:var(--mut);font-weight:400;font-size:.8em}
.smx .twrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 .5rem}
.smx table{border-collapse:collapse;width:100%;font-family:-apple-system,'Segoe UI',sans-serif!important;
 font-size:.82em}
.smx thead th{background:var(--ink);color:#fff;text-align:left;padding:7px 10px;white-space:nowrap}
.smx td,.smx th{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.smx tbody tr:nth-child(even){background:var(--chip)}
.smx .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.smx .bars{margin:1.2rem 0 .4rem;font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.8em}
.smx .bar{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.smx .bl{flex:0 0 240px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.smx .bt{flex:1;background:var(--chip);border-radius:4px;height:14px;overflow:hidden}
.smx .bt i{display:block;height:100%;background:var(--acc)}
.smx .bn{flex:0 0 44px;text-align:right;font-variant-numeric:tabular-nums;font-weight:700}
.smx .note{color:var(--mut);font-size:.82em;border-top:1px dashed var(--line);
 margin-top:2rem;padding-top:12px;max-width:82ch}
@media(max-width:640px){.smx .bl{flex-basis:130px}}
</style>"""

TRANSLATE = ('\n<div id="google_translate_element" style="margin:8px 0 16px;"></div>'
 '<script type="text/javascript">function googleTranslateElementInit(){'
 'new google.translate.TranslateElement({pageLanguage:"en",'
 'layout:google.translate.TranslateElement.InlineLayout.SIMPLE,autoDisplay:false},'
 '"google_translate_element");}</script>'
 '<script type="text/javascript" '
 'src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">'
 '</script>\n')

QR = "https://masaladeutsch.blogspot.com/2026/08/quarterly-reportage-4034-scheme.html"
LS = "https://masaladeutsch.blogspot.com/2026/08/lok-sabha-question-registry-1843-scheme.html"
RS = "https://masaladeutsch.blogspot.com/2026/08/rajya-sabha-question-registry-scheme.html"

wg = "STILL running since 2021 with none" if any("White Goods" in r["s"] for r in C) else "now questioned"

BODY = f"""<div class="smx">
<div class="kick">Industrial policy &middot; Parliament &middot; {today.strftime('%-d %B %Y')}</div>
<h1>The Most Discussed Schemes in Parliament</h1>
<p class="dek">Cross-referencing the <a href="{QR}" style="color:var(--acc)">PIB announcement
register</a> ({ta:,} scheme-mapped announcements) with the
<a href="{LS}" style="color:var(--acc)">Lok Sabha</a> and
<a href="{RS}" style="color:var(--acc)">Rajya Sabha</a> question registries
({n_ls:,} and {n_rs:,} questions since 2019), all classified by one scheme map &mdash;
so the join is exact. Which schemes does Parliament actively monitor, and which have
been announced but never questioned in detail?</p>
<p class="dek"><strong>{len(A)} schemes actively discussed &amp; monitored</strong>
(&ge;{ACTIVE_MIN_Q} questions across both houses, one within 12 months) &middot;
<strong>{len(B)} with some discussion</strong> &middot;
<strong>{len(C)} announced but never questioned</strong> in either house.</p>

<h2>The ten Parliament asks about most <span class="n">&middot; combined LS + RS questions</span></h2>
<div class="bars">{bars}</div>
<p class="dek">UDAN is the outlier twice over: Parliament&#39;s most-questioned incentive scheme,
and the one where the Rajya Sabha asks <em>more</em> than the Lok Sabha
({A[0]["rs"]} vs {A[0]["ls"]}). Note the inversions further down: PM-KUSUM draws
three times more parliamentary attention than government publicity, while the
Semiconductor Mission is the reverse.</p>

<h2>A. Actively discussed &amp; progress-monitored <span class="n">&middot; {len(A)} schemes</span></h2>
{table(A)}

<h2>B. Some discussion, not sustained <span class="n">&middot; {len(B)} schemes</span></h2>
{table(B)}

<h2>C. Announced, never questioned in either house <span class="n">&middot; {len(C)} schemes</span></h2>
{table(C, empty_qs=True)}
<p class="dek">Read this list honestly: most entries are 2025&ndash;26 launches &mdash; zero
questions mostly means <em>not yet</em>, since Parliament has not had a full session
cycle. The exception is <strong>PLI &mdash; White Goods</strong>: {wg} subject-titled
question in either house across four years of operation, though white-goods questions
may hide under generic &ldquo;PLI Scheme&rdquo; subjects.</p>

<p class="note">
<strong>Method.</strong> Questions are captured by subject line only (a limitation of both
houses&#39; indexes), so zero captured questions is an upper bound on neglect, not proof
of it. &ldquo;Monitored&rdquo; means Parliament keeps asking &mdash; whether the answers show
progress is in the linked answer PDFs of the two registries, not in these counts. PIB
counts include progress releases, not only launches; &ldquo;first announced&rdquo; is the
scheme&#39;s first appearance in the register (which starts January 2017), so schemes
older than 2017 show their first register mention, not their launch. Thresholds (&ge;{ACTIVE_MIN_Q}
questions, 12-month recency) are stated, tunable constants. Generated {today} by
<code>scripts/build_scrutiny_matrix.py</code> in
<a href="https://github.com/herrrickshaw/digital-twin-for-ipa" style="color:var(--acc)">digital-twin-for-ipa</a>;
the underlying analysis is backed up at
<a href="https://github.com/herrrickshaw" style="color:var(--acc)">github.com/herrrickshaw</a>.
</p>
<p class="note" style="border-top:none;margin-top:0"><em>This page was built with AI
assistance from the public PIB and sansad.in indexes linked above. AI-generated text can
misstate figures even when working from real source material &mdash; verify any number
that matters to a decision against the linked primary source.</em></p>
</div>"""

post = CSS + TRANSLATE + BODY
out = os.path.dirname(os.path.abspath(__file__)) + "/matrix_post.html"
open(out, "w", encoding="utf-8").write(post)
print(f"A {len(A)} / B {len(B)} / C {len(C)} | post {len(post):,} chars -> {out}")
