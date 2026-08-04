#!/usr/bin/env python3
"""Render the Rajya Sabha Question Registry as a self-contained Blogger post.

Same architecture as the Quarterly Reportage post: dictionary-encoded JSON payload
rendered client-side (pre-rendered rows would bloat the post), ASCII-forced and
&/<> escaped so Blogger's editor cannot mangle it. Light-only palette (site rule:
posts force white backgrounds, so no dark blocks anywhere).
"""
import json, datetime

rows = json.load(open('/Users/umashankar/digital-twin-for-ipa/data/registers/rs_pq_registry.json'))
GEN = datetime.date.today().isoformat()

schemes = sorted({s for r in rows for s in r['schemes']})
mins = sorted({r['ministry'] for r in rows})
si = {s: i for i, s in enumerate(schemes)}
mi = {m: i for i, m in enumerate(mins)}
# [iso, [schemeIdx], minIdx, session, qtype(0=UNSTARRED,1=STARRED), qno, subject, pdf, members]
R = [[r['iso'], sorted(si[s] for s in r['schemes']), mi[r['ministry']], r['session'],
      1 if (r['qtype'] or '').strip() == 'STARRED' else 0, r['qno'], r['subject'],
      r['pdf'], ', '.join(r['members'][:3]) + (' & ors.' if len(r['members']) > 3 else '')]
     for r in rows]
R.sort(key=lambda x: (x[0], x[5]), reverse=True)

payload = json.dumps({"s": schemes, "m": mins, "r": R},
                     ensure_ascii=True, separators=(',', ':'))
for ch, escp in (('&', '\\u0026'), ('<', '\\u003c'), ('>', '\\u003e')):
    payload = payload.replace(ch, escp)
assert payload.isascii() and '</' not in payload

nq = len({r['q'] for r in rows})
first, last = min(r['iso'] for r in rows), max(r['iso'] for r in rows)
starred = sum(1 for r in rows if (r['qtype'] or '').strip() == 'STARRED')

CSS = """<style>/*gs-typo-unify-v1*/
.pqx{font-family:Georgia,'Times New Roman',serif!important;}
.pqx p,.pqx li,.pqx td,.pqx th{font-family:Georgia,'Times New Roman',serif!important;}
.pqx h1,.pqx h2,.pqx h3{font-family:Georgia,'Times New Roman',serif!important;line-height:1.3!important;}
</style>
<style>
/* Light only. Site rule: posts force white backgrounds, dark blocks render
   text white-on-white. Palette = the blog's navy/blue article scale. */
.pqx{--pg:#fff;--card:#fff;--ink:#051C2C;--mut:#5A666E;--acc:#2251FF;
     --accs:#EAF0FF;--line:#D4DDE5;--chip:#F4F7FB;
     background:var(--pg);color:var(--ink);line-height:1.55;max-width:none}
.pqx *{box-sizing:border-box}
.pqx ::first-letter{font-size:inherit!important;float:none!important;font-weight:inherit!important}
.pqx .kick{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.72em;
  letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--acc)}
.pqx h1{font-size:2em;margin:.3rem 0 .7rem;letter-spacing:-.01em;color:var(--ink)}
.pqx .dek{color:var(--mut);font-size:.95em;max-width:74ch;margin:0 0 1.2rem}
.pqx .ctl{position:sticky;top:0;z-index:5;background:var(--pg);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);padding:10px 12px;margin:1.2rem -12px 0;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.82em}
.pqx select,.pqx input[type=search]{background:var(--card);color:var(--ink);
  border:1px solid var(--line);border-radius:6px;padding:6px 9px;font:inherit;max-width:100%}
.pqx input[type=search]{flex:1;min-width:160px}
.pqx .cnt{color:var(--mut);white-space:nowrap}
.pqx .qh{font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:1.05em;font-weight:700;
  border-bottom:2px solid var(--ink);display:inline-block;padding-bottom:3px;margin:2rem 0 .8rem;
  color:var(--ink)}
.pqx .qh .n{color:var(--mut);font-weight:400;font-size:.8em}
.pqx .row{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--acc);
  border-radius:8px;padding:10px 14px;margin-bottom:8px}
.pqx .top{display:flex;flex-wrap:wrap;gap:7px;align-items:baseline;margin-bottom:4px;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.74em}
.pqx .chip{background:var(--accs);color:var(--acc);border-radius:99px;padding:2px 10px;font-weight:700}
.pqx .min{color:var(--mut)}
.pqx .date{color:var(--mut);font-variant-numeric:tabular-nums}
.pqx .qn{font-family:ui-monospace,Menlo,monospace!important;font-size:.72em;color:var(--acc);
  white-space:nowrap}
.pqx .star{background:var(--ink);color:#fff;border-radius:4px;padding:1px 7px;
  font-weight:700;font-size:.95em}
.pqx .ttl{font-size:.95em}
.pqx .ttl a{color:inherit;text-decoration:none}
.pqx .ttl a:hover{text-decoration:underline;text-decoration-color:var(--acc)}
.pqx .mem{color:var(--mut);font-family:-apple-system,'Segoe UI',sans-serif!important;
  font-size:.74em;margin-top:3px}
.pqx .note{color:var(--mut);font-size:.82em;border-top:1px dashed var(--line);
  margin-top:2rem;padding-top:12px;max-width:82ch}
.pqx .more{display:block;width:100%;margin:1rem 0;padding:10px;background:var(--card);
  border:1px solid var(--line);border-radius:8px;color:var(--acc);cursor:pointer;
  font-family:-apple-system,'Segoe UI',sans-serif!important;font-size:.85em;font-weight:700}
@media(max-width:640px){.pqx .ctl{position:static}}
</style>"""

TRANSLATE = ('\n<div id="google_translate_element" style="margin:8px 0 16px;"></div>'
 '<script type="text/javascript">function googleTranslateElementInit(){'
 'new google.translate.TranslateElement({pageLanguage:"en",'
 'layout:google.translate.TranslateElement.InlineLayout.SIMPLE,autoDisplay:false},'
 '"google_translate_element");}</script>'
 '<script type="text/javascript" '
 'src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">'
 '</script>\n')

BODY = f"""<div class="pqx">

<div class="kick">Industrial policy &middot; Parliament &middot; {datetime.date.today().strftime('%-d %B %Y')}</div>
<h1>Rajya Sabha Question Registry</h1>
<p class="dek"><strong>Every captured Rajya Sabha question</strong> on investment policies, schemes
and incentives since 2019 ({first} &rarr; {last}) &mdash; {len(R):,} at this build &mdash; each
mapped to its
scheme and answering ministry. Every row links to the official answer PDF on sansad.in
&mdash; {starred:,} starred (answered orally on the floor), the rest unstarred (written).</p>

<p class="dek">The upper-house companion to the
<a href="https://masaladeutsch.blogspot.com/2026/08/lok-sabha-question-registry-1843-scheme.html"
style="color:var(--acc)">Lok Sabha Question Registry</a> and the
<a href="https://masaladeutsch.blogspot.com/2026/08/quarterly-reportage-4034-scheme.html"
style="color:var(--acc)">Quarterly Reportage</a>: what the Rajya Sabha asked about these same
schemes, with the ministry's answer of record. All three views are classified by one
scheme-keyword map, so they filter identically. Use it to find the answer, then read the answer. The underlying data
analysis and build scripts are backed up at
<a href="https://github.com/herrrickshaw" style="color:var(--acc)">github.com/herrrickshaw</a>.</p>

<div class="ctl">
<select id="pq"><option value="">All quarters</option></select>
<select id="ps"><option value="">All schemes</option></select>
<select id="pm"><option value="">All ministries</option></select>
<select id="pt"><option value="">Starred + Unstarred</option>
<option value="1">Starred</option><option value="0">Unstarred</option></select>
<input type="search" id="pf" placeholder="Search subjects...">
<span class="cnt" id="pc"></span>
</div>

<div id="plist"></div>

<p class="note">
<strong>Method.</strong> Harvested from the rsdoc.nic.in per-question index by subject
keyword (same keyword lists as the Lok Sabha registry, from 2019), then classified against the
same scheme-regex map and acronym-veto list as the Quarterly Reportage &mdash; so
&ldquo;Sanchar Mitra&rdquo; does not file under PM MITRA and IIT (ISM) Dhanbad does not
file under the Semiconductor Mission here either. Generated {GEN} by
<code>scripts/build_rs_pq_registry.py</code> in
<a href="https://github.com/herrrickshaw/digital-twin-for-ipa" style="color:var(--acc)">digital-twin-for-ipa</a>.
</p>

<p class="note" style="border-top:none;margin-top:0">
<strong>Known limits, stated rather than hidden.</strong> The index matches
keywords against the <em>subject line only</em>, so a question whose subject names no
scheme is not captured even when its answer discusses one at length &mdash; coverage is
of scheme-titled questions, not of every mention. Ministries answer as of their date;
figures in older answers are superseded by newer ones. A row whose subject has nothing
to do with its chip is a classification bug, not a parliamentary fact.
</p>

<p class="note" style="border-top:none;margin-top:0"><em>This page was built with AI
assistance from the public rsdoc.nic.in / sansad.in Rajya Sabha Q&amp;A index linked above. AI-generated
text can misstate figures even when working from real source material &mdash; verify any
number that matters to a decision against the linked answer PDF.</em></p>

</div>
<script type="text/javascript">
(function(){{
var D={payload};
var S=D.s,M=D.m,RW=D.r,PAGE=300;
var q=document.getElementById('pq'),sf=document.getElementById('ps'),
    mf=document.getElementById('pm'),tf=document.getElementById('pf'),
    yf=document.getElementById('pt'),cn=document.getElementById('pc'),
    ls=document.getElementById('plist');
function quarter(d){{return d.slice(0,4)+'Q'+((((+d.slice(5,7))-1)/3|0)+1);}}
var qs=[];RW.forEach(function(r){{var x=quarter(r[0]);if(qs.indexOf(x)<0)qs.push(x);}});
qs.forEach(function(v){{q.add(new Option(v,v));}});
S.forEach(function(v,i){{sf.add(new Option(v,i));}});
M.forEach(function(v,i){{mf.add(new Option(v,i));}});
function esc(s){{return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
var shown=PAGE;
function match(){{
  var Q=q.value,Sv=sf.value,Mv=mf.value,T=tf.value.toLowerCase(),Y=yf.value;
  return RW.filter(function(r){{
    if(Q&&quarter(r[0])!==Q)return false;
    if(Sv!==''&&r[1].indexOf(+Sv)<0)return false;
    if(Mv!==''&&r[2]!==+Mv)return false;
    if(Y!==''&&r[4]!==+Y)return false;
    if(T&&(r[6]+' '+r[8]).toLowerCase().indexOf(T)<0)return false;
    return true;}});
}}
function render(){{
  var f=match(),out=[],cur='',n=Math.min(shown,f.length);
  for(var i=0;i<n;i++){{
    var r=f[i],Q=quarter(r[0]);
    if(Q!==cur){{cur=Q;var c=0;for(var j=i;j<f.length;j++){{if(quarter(f[j][0])===Q)c++;}}
      out.push('<div class="qh">'+Q+' <span class="n">&middot; '+c+
        (c===1?' question':' questions')+'</span></div>');}}
    var chips='';for(var k=0;k<r[1].length;k++)chips+='<span class="chip">'+esc(S[r[1][k]])+'</span>';
    out.push('<div class="row"><div class="top"><span class="date">'+r[0]+'</span>'+chips+
      '<span class="min">'+esc(M[r[2]])+'</span>'+
      '<span class="qn">RS Sess.'+r[3]+' &middot; '+(r[4]?'<span class="star">&#9733; STARRED</span>':'Unstarred')+
      ' Q.'+r[5]+'</span></div><div class="ttl">'+
      '<a href="'+esc(r[7])+'" target="_blank" rel="noopener">'+esc(r[6])+'</a></div>'+
      '<div class="mem">Asked by '+esc(r[8])+'</div></div>');
  }}
  if(n<f.length)out.push('<button class="more" id="pmore">Show '+
    Math.min(PAGE,f.length-n)+' more &mdash; '+(f.length-n)+' still hidden</button>');
  ls.innerHTML=out.join('');
  cn.textContent=f.length.toLocaleString()+' of '+RW.length.toLocaleString();
  var b=document.getElementById('pmore');
  if(b)b.onclick=function(){{shown+=PAGE;render();}};
}}
function reset(){{shown=PAGE;render();}}
[q,sf,mf,yf].forEach(function(e){{e.addEventListener('change',reset);}});
var tm;tf.addEventListener('input',function(){{clearTimeout(tm);tm=setTimeout(reset,180);}});
render();
}})();
</script>"""

post = CSS + TRANSLATE + BODY
open('/private/tmp/claude-501/-Users-umashankar/e50aaf59-8643-4790-a7e8-d74da5d3e4a2/scratchpad/rs_post.html',
     'w', encoding='utf-8').write(post)
print(f"rows={len(R)} quarters={nq} range={first}->{last} starred={starred}")
print(f"payload={len(payload):,} chars  post={len(post):,} chars")
