#!/usr/bin/env python3
"""Build the 5a-i subsection for the green-debt article.

Rates are BIS WS_CBPOL (v1 API, last observation per economy, retrieved 4 Aug 2026),
which is the source section 5a already cites. Defunct pre-euro national series are
excluded. "Issuable" is a judgement about market depth, flagged as such in the note.
"""
IND = 5.25
# (economy, policy rate %, deep offshore market a foreign issuer can realistically tap)
ROWS = [
 ("Switzerland",      0.00, True),
 ("Japan",            1.00, True),
 ("Thailand",         1.00, False),
 ("Sweden",           1.75, True),
 ("Denmark",          1.85, True),
 ("Canada",           2.25, True),
 ("Morocco",          2.25, False),
 ("Euro area",        2.25, True),
 ("Korea",            2.50, True),
 ("New Zealand",      2.50, False),
 ("Malaysia",         2.75, False),
 ("China",            3.00, True),
 ("Kuwait",           3.50, False),
 ("United States",    3.62, True),
 ("Czechia",          3.75, False),
 ("United Kingdom",   3.75, True),
 ("Israel",           3.75, False),
 ("Poland",           3.75, False),
 ("Hong Kong SAR",    4.00, True),
 ("North Macedonia",  4.25, False),
 ("Norway",           4.25, True),
 ("Peru",             4.25, False),
 ("Saudi Arabia",     4.25, False),
 ("Australia",        4.35, True),
 ("Chile",            4.50, False),
]
deep = [r for r in ROWS if r[2]]
assert len(ROWS) == 25 and len(deep) == 13

body = "\n".join(
    f'<tr><td>{n}</td><td style="text-align:right;font-variant-numeric:tabular-nums">{v:.2f}</td>'
    f'<td style="text-align:right;font-variant-numeric:tabular-nums">{IND-v:.2f}</td>'
    f'<td>{"Yes" if d else "&mdash;"}</td></tr>'
    for n, v, d in ROWS)

HTML = f'''
<div class="gb-h2" style="font-size:1.08em;margin:2rem 0 .7rem">5a&#8209;i. Cheaper than India, on paper &mdash; and why most of it is unreachable</div>
<p>The four lines above are the trade this article is about, but they are a sample, not the
field. On the BIS policy-rate panel, <strong>25 of the 38 live economies sit below India's
5.25% repo</strong> &mdash; a menu of funding currencies far longer than the yen-dollar-euro
story the deals actually use. It is worth seeing the whole menu, because the reason most of
it is unusable is the same reason the yen trade works.</p>

<div class="gb-tblwrap"><table class="gb-table">
<thead><tr><th>Economy</th><th style="text-align:right">Policy rate (%)</th><th style="text-align:right">Gap vs India (pp)</th><th>Issuance currency for an Indian PSU/NBFC?</th></tr></thead>
<tbody>
{body}
</tbody>
</table></div>
<p class="gb-note">Source: BIS central bank policy rate statistics (WS_CBPOL, daily series,
last observation per economy, retrieved 4&nbsp;Aug&nbsp;2026) &mdash; the same series behind
the chart above. India is the RBI repo rate; the US figure is the Fed's mid-target, so the
upper bound is 12.5bp higher. Eleven defunct pre-euro national series (Germany, France, Italy
and others, last observed 1998&ndash;2000) are excluded &mdash; they would otherwise pad the
list with phantom entries. The final column is a judgement about market depth, not a legal
restriction. Secondary rate aggregators were not used: several still carry Japan at 0.75%,
missing the June&nbsp;2026 BoJ hike discussed above.</p>

<p><strong>Now the deflating part.</strong> Of those 25, only about 13 have an offshore market
deep enough for an Indian PSU or NBFC to price a benchmark in &mdash; roughly the Swiss franc,
yen, Swedish and Danish krona, Canadian dollar, euro, won, renminbi, US dollar, sterling, Hong
Kong dollar, Norwegian krone and Australian dollar. The other twelve are real rates in real
economies, but Thailand, Morocco, Kuwait, Peru or North Macedonia will not absorb a
&#8377;5,000&nbsp;crore-equivalent green benchmark from an Indian issuer at any price.</p>

<p>And the rate gap is <em>not</em> the funding-cost gap. Covered interest parity means the
currency with the lower policy rate carries the more expensive hedge, and the two very nearly
cancel: the forward points on USD/INR or JPY/INR price in almost exactly the interest
differential the borrower is trying to harvest. That is the whole reason IREDA's hedged yen
landed <strong>below 7%</strong> rather than near 3%, as section 5a already notes. Read the
table with that in mind and the ranking inverts: <strong>Switzerland shows the widest headline
gap in the entire panel at 5.25pp and is close to the least useful of the deep markets</strong>,
because a CHF/INR hedge costs about what the cheap coupon saves. The gap is only worth
harvesting where an issuer can leave part of it unhedged against matching foreign-currency
cash flows, or where hedging is subsidised or partly waived &mdash; which is a structuring
question, not a rate-map question.</p>

<div class="gb-pull">Twenty-five countries are cheaper than India. Roughly thirteen are
reachable. After hedging, the ranking of the thirteen barely resembles the ranking of the
twenty-five.</div>
'''

open('insert_5ai.html', 'w', encoding='utf-8').write(HTML)
print(f"rows={len(ROWS)} deep={len(deep)} chars={len(HTML)}")
print("gap range: %.2f .. %.2f" % (min(IND-v for _, v, _ in ROWS), max(IND-v for _, v, _ in ROWS)))
