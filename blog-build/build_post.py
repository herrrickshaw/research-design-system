#!/usr/bin/env python3
"""Render the quarterly reportage as a single self-contained Blogger post.

4,034 rows of pre-rendered markup is a 2.3MB post; the same rows as a
dictionary-encoded JSON payload rendered client-side is ~515KB. The payload is
forced to pure ASCII and its &, < and > are \\u-escaped as well, because Blogger's
editor rewrites bare entities inside <script> blocks (the rupee-in-script bug).
"""
import json, datetime, collections

rows = json.load(open('rows.json'))
GEN = "2026-08-04"

schemes = sorted({s for r in rows for s in r['s'].split('; ')})
mins = sorted({r['m'] for r in rows})
si = {s: i for i, s in enumerate(schemes)}
mi = {m: i for i, m in enumerate(mins)}
R = [[r['d'], sorted(si[x] for x in r['s'].split('; ')), mi[r['m']], int(r['p']), r['t']]
     for r in rows]
R.sort(key=lambda x: (x[0], x[3]), reverse=True)

payload = json.dumps({"s": schemes, "m": mins, "r": R},
                     ensure_ascii=True, separators=(',', ':'))
# Blogger mangles bare entities inside <script>; keep the payload 7-bit and inert.
for ch, esc in (('&', '\\u0026'), ('<', '\\u003c'), ('>', '\\u003e')):
    payload = payload.replace(ch, esc)
assert payload.isascii() and '</' not in payload

nq = len({d[:4] + 'Q' + str((int(d[5:7]) - 1) // 3 + 1) for d, *_ in R})
first, last = min(r[0] for r in R), max(r[0] for r in R)
cab = sum(1 for r in R if 'Cabinet' in mins[r[2]])

CSS = """<style>/*gs-typo-unify-v1*/
.rpx,.artx,.fertx,.ecx,.mapx,.idx,.wrap,.slide,.stat{font-family:Georgia,'Times New Roman',serif!important;}
.rpx p,.rpx li,.rpx td,.rpx th,.rpx blockquote{font-family:Georgia,'Times New Roman',serif!important;}
.rpx h1,.rpx h2,.rpx h3{font-family:Georgia,'Times New Roman',serif!important;line-height:1.3!important;}
</style>
<style>
/* NO prefers-color-scheme block here, deliberately. This markup is embedded in a
   Blogger post, so the THEME owns the page background and it is light-only
   (rgb(238,238,238)). A dark block flips only the tokens this component controls:
   .row and .ctl paint themselves dark while h1 and .qh -- which have no background
   of their own -- render light text straight onto the theme's light page at 1.05:1,
   i.e. invisible. Flip text and surface together or not at all; here the surface is
   not ours to flip, so: light only.
   The standalone docs/reportage.html in digital-twin-for-ipa KEEPS its dark mode --
   that file styles <body> itself, so the whole page flips together and it is correct. */
/* Palette: the same navy/blue this blog already uses in the gb-* article template
   (#051C2C ink, #2251FF accent, #5A666E muted), so the archive matches the essays. */
.rpx{--pg:#fff;--card:#fff;--ink:#051C2C;--mut:#5A666E;--acc:#2251FF;
     --accs:#EAF0FF;--line:#D4DDE5;--chip:#F4F7FB;--warn:#8a5a12;
     background:var(--pg);color:var(--ink);line-height:1.55;max-width:none}
.rpx *{box-sizing:border-box}
.rpx ::first-letter{font-size:inherit!important;float:none!important;font-weight:inherit!important}
.rpx .kick{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.72em;
  letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--acc)}
.rpx h1{font-size:2em;margin:.3rem 0 .7rem;letter-spacing:-.01em;color:var(--ink)}
.rpx .dek{color:var(--mut);font-size:.95em;max-width:74ch;margin:0 0 1.2rem}
.rpx .ctl{position:sticky;top:0;z-index:5;background:var(--pg);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);padding:10px 12px;margin:1.2rem -12px 0;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.82em}
.rpx select,.rpx input[type=search]{background:var(--card);color:var(--ink);
  border:1px solid var(--line);border-radius:6px;padding:6px 9px;font:inherit;max-width:100%}
.rpx input[type=search]{flex:1;min-width:170px}
.rpx .cnt{color:var(--mut);white-space:nowrap}
.rpx .qh{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:1.05em;font-weight:700;
  border-bottom:2px solid var(--ink);display:inline-block;padding-bottom:3px;margin:2rem 0 .8rem;
  color:var(--ink)}
.rpx .qh .n{color:var(--mut);font-weight:400;font-size:.8em}
.rpx .row{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--acc);
  border-radius:8px;padding:10px 14px;margin-bottom:8px}
.rpx .top{display:flex;flex-wrap:wrap;gap:7px;align-items:baseline;margin-bottom:4px;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.74em}
.rpx .chip{background:var(--accs);color:var(--acc);border-radius:99px;padding:2px 10px;font-weight:700}
.rpx .min{color:var(--mut)}
.rpx .date{color:var(--mut);font-variant-numeric:tabular-nums}
.rpx .ttl{font-size:.95em}
.rpx .ttl a{color:inherit;text-decoration:none}
.rpx .ttl a:hover{text-decoration:underline;text-decoration-color:var(--acc)}
.rpx .prid{font-family:ui-monospace,Menlo,monospace!important;font-size:.72em;color:var(--acc);
  white-space:nowrap}
.rpx .note{color:var(--mut);font-size:.82em;border-top:1px dashed var(--line);
  margin-top:2rem;padding-top:12px;max-width:80ch}
.rpx .more{display:block;width:100%;margin:1rem 0;padding:10px;background:var(--card);
  border:1px solid var(--line);border-radius:8px;color:var(--acc);cursor:pointer;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.85em;font-weight:700}
@media(max-width:640px){.rpx .ctl{position:static}}
</style>"""

TRANSLATE = ('\n<div id="google_translate_element" style="margin:8px 0 16px;"></div>'
 '<script type="text/javascript">function googleTranslateElementInit(){'
 'new google.translate.TranslateElement({pageLanguage:"en",'
 'layout:google.translate.TranslateElement.InlineLayout.SIMPLE,autoDisplay:false},'
 '"google_translate_element");}</script>'
 '<script type="text/javascript" '
 'src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">'
 '</script>\n')

BODY = f"""<div class="rpx">

<div class="kick">Industrial policy &middot; PIB register &middot; {datetime.date(2026,8,4).strftime('%-d %B %Y')}</div>
<h1>Quarterly Reportage</h1>
<p class="dek"><strong>{len(R):,} incentive-scheme announcements</strong> across {nq} quarters
({first} &rarr; {last}), each mapped to its scheme and owning ministry from the Press
Information Bureau register. Every line links to the original release by PRID. Filter by
quarter, scheme or ministry; search titles.</p>

<p class="dek">This is <em>an index into the register, not a reading of it</em>. Mapping is by
keyword against release titles, so it will miss a scheme referred to obliquely and it
cannot tell an approval from a progress report &mdash; a Parliament answer about PM E-DRIVE
and the Cabinet decision creating it look alike here. Use it to find the release, then
read the release. {cab:,} of these rows are Cabinet or CCEA items.</p>

<div class="ctl">
<select id="rq"><option value="">All quarters</option></select>
<select id="rs"><option value="">All schemes</option></select>
<select id="rm"><option value="">All ministries</option></select>
<input type="search" id="rt" placeholder="Search titles...">
<span class="cnt" id="rc"></span>
</div>

<div id="rlist"></div>

<p class="note">
<strong>Method.</strong> Source: the PIB release register (123,169 releases, 2017&rarr;today),
refreshed daily. A release qualifies as an announcement here if its title matches the
scheme-keyword map, or if it is a Cabinet/CCEA approval carrying incentive language.
Quarters are calendar quarters, so 2026Q3 is Jul&ndash;Sep 2026. Generated {GEN} by
<code>scripts/build_reportage.py</code> in
<a href="https://github.com/herrrickshaw/digital-twin-for-ipa" style="color:var(--acc)">digital-twin-for-ipa</a>,
where the fuller ministry-wise and state-wise views also live.
</p>

<p class="note" style="border-top:none;margin-top:0">
<strong>Companion view.</strong> For the last 30 days only &mdash; central releases plus the
state-government wire, which this page does not carry &mdash; see
<a href="https://masaladeutsch.blogspot.com/2026/08/root-bgfff-fg1a1a1a-mut666-cardf6f6f4.html" style="color:var(--acc)">Reportage: Latest Updates</a>.
That page is the running feed; this one is the archive.
</p>

<p class="note" style="border-top:none;margin-top:0">
<strong>Known limits, stated rather than hidden.</strong> Acronyms collide, and the map
used to fall for them: IIT (ISM) Dhanbad is a mining school and was being read as the
India Semiconductor Mission; Sanchar, Paryatan, Nyaya and Monument <em>Mitra</em> are
unrelated to PM MITRA textile parks; &ldquo;AIF&rdquo; in a Competition Commission order
is an Alternative Investment Fund, not the Agriculture Infrastructure Fund; and Krishi
Unnati Mela is not UNNATI 2024. Thirty-two such rows were removed on {GEN} by an explicit
veto list. Others may remain &mdash; a row whose title has nothing to do with its chip is
a mapping error, not a policy fact.
</p>

<p class="note" style="border-top:none;margin-top:0"><em>This page was built with AI
assistance from the public PIB release register linked above. AI-generated text can
misstate figures even when working from real source material &mdash; verify any number
that matters to a decision against the cited primary source.</em></p>

</div>
<script type="text/javascript">
(function(){{
var D={payload};
var S=D.s,M=D.m,RW=D.r,PAGE=400;
var q=document.getElementById('rq'),sf=document.getElementById('rs'),
    mf=document.getElementById('rm'),tf=document.getElementById('rt'),
    cn=document.getElementById('rc'),ls=document.getElementById('rlist');
function qof(d){{return d.slice(0,4)+'Q'+(((+d.slice(5,7))-1)/3|0);}}
function quarter(d){{return d.slice(0,4)+'Q'+((((+d.slice(5,7))-1)/3|0)+1);}}
var qs=[];RW.forEach(function(r){{var x=quarter(r[0]);if(qs.indexOf(x)<0)qs.push(x);}});
qs.forEach(function(v){{q.add(new Option(v,v));}});
S.forEach(function(v,i){{sf.add(new Option(v,i));}});
M.forEach(function(v,i){{mf.add(new Option(v,i));}});
function esc(s){{return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
var shown=PAGE;
function match(){{
  var Q=q.value,Sv=sf.value,Mv=mf.value,T=tf.value.toLowerCase();
  return RW.filter(function(r){{
    if(Q&&quarter(r[0])!==Q)return false;
    if(Sv!==''&&r[1].indexOf(+Sv)<0)return false;
    if(Mv!==''&&r[2]!==+Mv)return false;
    if(T&&r[4].toLowerCase().indexOf(T)<0)return false;
    return true;}});
}}
function render(){{
  var f=match(),out=[],cur='',n=Math.min(shown,f.length);
  for(var i=0;i<n;i++){{
    var r=f[i],Q=quarter(r[0]);
    if(Q!==cur){{cur=Q;var c=0;for(var j=i;j<f.length;j++){{if(quarter(f[j][0])===Q)c++;}}
      out.push('<div class="qh">'+Q+' <span class="n">&middot; '+c+
        (c===1?' announcement':' announcements')+'</span></div>');}}
    var chips='';for(var k=0;k<r[1].length;k++)chips+='<span class="chip">'+esc(S[r[1][k]])+'</span>';
    out.push('<div class="row"><div class="top"><span class="date">'+r[0]+'</span>'+chips+
      '<span class="min">'+esc(M[r[2]])+'</span></div><div class="ttl">'+
      '<a href="https://www.pib.gov.in/PressReleasePage.aspx?PRID='+r[3]+
      '" target="_blank" rel="noopener">'+esc(r[4])+'</a> '+
      '<span class="prid">PRID '+r[3]+'</span></div></div>');
  }}
  if(n<f.length)out.push('<button class="more" id="rmore">Show '+
    Math.min(PAGE,f.length-n)+' more &mdash; '+(f.length-n)+' still hidden</button>');
  ls.innerHTML=out.join('');
  cn.textContent=f.length.toLocaleString()+' of '+RW.length.toLocaleString();
  var b=document.getElementById('rmore');
  if(b)b.onclick=function(){{shown+=PAGE;render();}};
}}
function reset(){{shown=PAGE;render();}}
[q,sf,mf].forEach(function(e){{e.addEventListener('change',reset);}});
var tm;tf.addEventListener('input',function(){{clearTimeout(tm);tm=setTimeout(reset,180);}});
render();
}})();
</script>"""

post = CSS + TRANSLATE + BODY
open('reportage_post.html', 'w', encoding='utf-8').write(post)
print(f"rows={len(R)} quarters={nq} range={first}->{last} cabinet={cab}")
print(f"payload chars={len(payload):,}  post chars={len(post):,}")
