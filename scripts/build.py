import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *
E=html.escape
CANON="https://whorunsny.org/nifa/"
def m(v): return "$"+f"{v:,.1f}"+"M"
def signed(v): return "—" if v is None else ("("+m(-v)+")" if v<0 else "+"+m(v))
def ext(u,t): return f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>'

def chart():
    W,H,L,R,T,B=1160,460,70,70,30,60; yMax,yMin,bMin,bMax=120,-360,2.8,4.0
    ph=H-T-B; step=(W-L-R)/len(DATA)
    y=lambda v:T+((yMax-v)/(yMax-yMin))*ph; yb=lambda v:T+((bMax-v)/(bMax-bMin))*ph; x=lambda i:L+step*i+step/2
    bw=min(24,step/3.2); o=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Major Funds budget vs NIFA risk vs actual result, FY2017 to FY2027">']
    for t in (120,0,-120,-240,-360):
        lab="$0" if t==0 else ("+" if t>0 else "−")+"$"+str(abs(t))+"M"
        o.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{"#3a3a44" if t==0 else "#1a1a22"}"/><text class="tk" x="{L-10}" y="{y(t)+4:.1f}" text-anchor="end">{lab}</text>')
    for t in (2.8,3.2,3.6,4.0): o.append(f'<text class="tk" style="fill:{BLUE}" x="{W-R+10}" y="{yb(t)+4:.1f}">${t:.1f}B</text>')
    for i,d in enumerate(DATA):
        fy,stage,bud,levy,lo,hi,recs,act,actual,note,fol=d
        tip=f"{fy}: NIFA risk {m(lo)}–{m(hi)}; actual {signed(actual)}; budget ${bud/1000:.2f}B"
        o.append(f'<g><title>{E(tip)}</title><rect x="{x(i)-bw-2:.1f}" y="{y(0):.1f}" width="{bw:.1f}" height="{y(-hi)-y(0):.1f}" fill="{PINK}"/>')
        if lo!=hi: o.append(f'<line x1="{x(i)-bw-6:.1f}" x2="{x(i)+2:.1f}" y1="{y(-lo):.1f}" y2="{y(-lo):.1f}" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 3"/>')
        if actual is not None:
            c=TEAL if actual>=0 else LIME
            o.append(f'<rect x="{x(i)+2:.1f}" y="{(y(actual) if actual>=0 else y(0)):.1f}" width="{bw:.1f}" height="{abs(y(actual)-y(0)):.1f}" fill="{c}"/>')
            ty=y(actual)-6 if actual>=0 else y(actual)+14
            o.append(f'<text class="vl" x="{x(i)+2+bw/2:.1f}" y="{ty:.1f}" text-anchor="middle" fill="{c}">{"+"+str(int(actual+0.5)) if actual>=0 else "("+str(int(-actual+0.5))+")"}</text>')
        o.append(f'<text class="vl" x="{x(i)-bw/2-2:.1f}" y="{y(-hi)+14:.1f}" text-anchor="middle" fill="{PINK}">{int(hi+0.5)}</text><text class="tk" style="fill:#f4f4f0" x="{x(i):.1f}" y="{H-B+22}" text-anchor="middle">{fy.replace("FY20","FY")}</text></g>')
    pts=" ".join(f"{x(i):.1f},{yb(d[2]/1000):.1f}" for i,d in enumerate(DATA))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="3" class="bl"/>')
    for i,d in enumerate(DATA): o.append(f'<circle cx="{x(i):.1f}" cy="{yb(d[2]/1000):.1f}" r="4" fill="{BLUE}"/>')
    o.append("</svg>"); return "".join(o)

def head(n,title,color,sub=None,id_=None):
    s=f'<div class="sh" id="{id_ or ""}"><div class="lbl" style="color:{color}">{E(n)}</div><h2 style="color:{color};text-shadow:0 0 18px {color}8c">{E(title)}</h2>'
    if sub: s+=f'<p class="sub">{E(sub)}</p>'
    return s+"</div>"

P=[]
P.append(head("01 · Latest","Latest news, newest first",LIME,"Dated items with sources. Grey tags mark items not fully verified.","news"))
P.append('<div class="stack">')
for d,t,text,v,ok,src,u in NEWS:
    P.append(f'<article class="panel news"><div class="nd"><div class="lbl" style="color:{LIME}">{E(d)}</div><span class="tag" style="color:{TEAL};border-color:{TEAL}">{E(t)}</span></div><div class="nb"><p>{E(text)}</p><div class="meta"><span class="tag" style="color:{LIME if ok else MUTED};border-color:{LIME if ok else MUTED}">{E(v)}</span> {ext(u,src)}</div></div></article>')
P.append('</div>')
P.append(head("02 · Calendar","Upcoming hearings & meetings",TEAL,"All times Eastern. The Legislature's Oct 30 adoption deadline has passed; NIFA approval is the next step before FY2027 begins Jan 1.","calendar"))
P.append('<div class="cards">')
for when,time,what,where,how,st,u,c in MEETS:
    P.append(f'<div class="panel card" style="border-color:{c}55"><div class="big" style="color:{c};text-shadow:0 0 18px {c}8c">{E(when)}</div><div class="lbl" style="color:{c}">{E(time)} · {E(st)}</div><p class="what">{E(what)}</p><p class="sm"><span class="lbl mut">Where </span>{E(where)}</p><p class="sm"><span class="lbl mut">How </span>{E(how)}</p><p class="sm">{ext(u,"Notice / agenda")}</p></div>')
P.append('</div><p class="note">Past: Legislature budget hearings Oct 5–7 (e.g. Government Services &amp; Operations, Oct 7, 9 AM), Rules Oct 26, special budget meeting Oct 30, 10 AM (adoption deadline Oct 30), committees Nov 9. The County Executive\'s signing date was not verified. NIFA\'s December meeting date is not posted yet.</p>')
P.append(head("03 · NIFA's asks","NIFA's seven FY2027 recommendations",PINK,"Quoted from the Oct 22, 2026 review, p.21: “The County should:”","recs"))
P.append('<ol class="panel recs">'+"".join(f'<li><span class="num">{i+1}</span><span>{E(r)}</span></li>' for i,r in enumerate(RECS))+'</ol>')
P.append('<p>NIFA also asks the County to fund contingency reserves, answer its prior unanswered information requests, cooperate with the assessment audit, and have NCC produce a gap-closing plan with milestones (pp.3, 18, 20).</p>')
P.append(f'<h3 style="color:{PINK};text-shadow:0 0 18px {PINK}8c">Key prior recommendations — followed?</h3><div class="panel scroll"><table><thead><tr><th>Year</th><th>NIFA recommendation / demand</th><th>Followed?</th></tr></thead><tbody>')
for fy,rec,fol,c in PRIOR: P.append(f'<tr><td class="yr">{E(fy)}</td><td>{E(rec)}</td><td style="color:{c};font-weight:600">{E(fol)}</td></tr>')
P.append('</tbody></table></div>')
P.append(head("04 · The numbers","Every number NIFA cites",BLUE2,"From NIFA's Oct 22, 2026 review (printed page numbers), Oct 6, 2026 FY2025 follow-up, Aug 7, 2026 update and Res. 25-69.","numbers"))
P.append('<div class="btns" data-group="cat">'+"".join(f'<button type="button" data-cat="{E(c)}" class="{"on" if c=="Risk" else ""}">{E(c)}</button>' for c in CATS)+'</div>')
P.append('<div class="panel scroll"><table id="figs"><thead><tr><th>Item</th><th>Figure</th><th>Source</th><th>Page</th></tr></thead><tbody>')
for cat,item,fig,doc,pg in FIGS: P.append(f'<tr data-cat="{E(cat)}"{"" if cat=="Risk" else " hidden"}><td>{E(item)}</td><td class="fig">{E(fig)}</td><td>{ext(DOCURL[doc],doc)}</td><td class="pg">{E(pg)}</td></tr>')
P.append('</tbody></table></div><noscript><p class="note">Turn on JavaScript to switch categories; all figures are also in the downloads below.</p></noscript>')
P.append(head("05 · Takeaways","Conclusions — tax levy first",LIME,"“Derived” marks arithmetic from the cited figures, not NIFA's numbers.","conclusions"))
P.append('<ol class="concl">'+"".join(f'<li><span class="cn" style="color:{c};text-shadow:0 0 18px {c}8c">{i+1:02d}</span><span>{E(t)}</span></li>' for i,(t,c) in enumerate(CONCL))+'</ol>')
P.append(f'<h3 style="color:{BLUE2};text-shadow:0 0 18px {BLUE2}8c">Levy math (derived)</h3><div class="panel scroll"><table><thead><tr><th>Question</th><th>Math ($M)</th><th>Result</th></tr></thead><tbody>'+"".join(f'<tr><td>{E(a)}</td><td class="pg">{E(b)}</td><td class="res">{E(c)}</td></tr>' for a,b,c in LEVY)+'</tbody></table></div>')
P.append("<p class=\"note\">Caveats: the state cap applies to the County's total levy, not just the Major Funds, and also depends on the tax-base growth factor, PILOTs, exclusions and up to 1.5% carryover, so this is an illustration. NIFA's risk ranges already assume budgeted reserves, so \"without reserves\" adds them back. Sources: NIFA Oct 22, 2026 review pp.2, 22; OSC 2027 cap release.</p>")
P.append(head("06 · Ten-year view","Budget vs NIFA-flagged risk vs actual result",PINK,None,"chart"))
leg="".join(f'<span class="li"><i style="background:{c};box-shadow:0 0 18px {c}8c"></i>{E(t)}</span>' for c,t in ((PINK,"NIFA risk, high case ($M, down)"),(LIME,"Actual deficit"),(TEAL,"Actual surplus"),(BLUE,"Major Funds budget ($B, right)")))
P.append(f'<div class="panel"><div class="legend">{leg}</div><div class="chartwrap">{chart()}</div><p class="note">The dashed white tick marks NIFA\'s low case. FY2020–21 surpluses include CARES aid and restructuring savings. FY2026 is still open.</p></div>')
P.append(head("07 · Year by year","FY2017–FY2027 table",TEAL,None,"years"))
P.append('<div class="btns" data-group="view">'+"".join(f'<button type="button" data-view="{v}" class="{"on" if v=="nifa" else ""}">{l}</button>' for v,l in (("budget","Budget"),("nifa","NIFA review"),("outcome","Outcome")))+'</div>')
views={"budget":(["Year","Stage","Major Funds budget","Levy"],[[d[0],d[1],m(d[2]),m(d[3])] for d in DATA]),
"nifa":(["Year","NIFA risk (yr 1)","NIFA ask","NIFA action"],[[d[0],m(d[5]) if d[4]==d[5] else m(d[4])+"–"+m(d[5]),d[6],d[7]] for d in DATA]),
"outcome":(["Year","Actual result","Note","Followed NIFA?"],[[d[0],signed(d[8]),d[9],d[10]] for d in DATA])}
for v,(cols,rows) in views.items():
    P.append(f'<div class="panel scroll" data-viewtable="{v}"{"" if v=="nifa" else " hidden"}><table><thead><tr>'+"".join(f"<th>{E(c)}</th>" for c in cols)+'</tr></thead><tbody>'+"".join("<tr>"+"".join(f'<td{" class=yr" if j==0 else ""}>{E(c)}</td>' for j,c in enumerate(r))+"</tr>" for r in rows)+'</tbody></table></div>')
P.append(head("08 · Status","Control period: still in effect",LIME,None,"status"))
P.append('<div class="panel">NIFA imposed the control period on Jan 26, 2011. Its Oct 22, 2026 resolution says the County "continues to operate in a control period," and the staff report projects Major Funds deficits above the 1% trigger through FY2030. There was no 2022 vote moving NIFA to advisory status. Separately, NIFA imposed a control period on Nassau Health Care Corp. on June 5, 2025.</div>')
P.append(head("09 · Caveats","Not verified / not found",PINK,None,"caveats"))
P.append('<div class="panel">'+"".join(f'<p class="cv">— {E(t)}</p>' for t in CAVEATS)+'</div>')
P.append(head("10 · Downloads","Data downloads",TEAL,None,"downloads"))
DL=[("Workbook (all sheets)","data/nassau_budget_vs_nifa.xlsx","XLSX"),("Year-by-year table","data/nassau_budget_vs_nifa.csv","CSV"),("Every NIFA figure","data/nassau_nifa_figures.csv","CSV"),("News & hearings","data/nassau_news_hearings.csv","CSV"),("Levy math (derived)","data/nassau_levy_math_derived.csv","CSV")]
P.append('<div class="srcs">'+"".join(f'<a class="panel src" href="{u}" download><div class="lbl" style="color:{TEAL}">{k}</div><div class="st">{E(t)}</div></a>' for t,u,k in DL)+'</div>')
P.append(head("11 · Sources","Sources",BLUE2,None,"sources"))
P.append('<div class="srcs">'+"".join(f'<a class="panel src" href="{E(u)}" target="_blank" rel="noopener"><div class="lbl" style="color:{LIME}">{E(u.replace("https://","").split("/")[0])}</div><div class="st">{E(t)}</div></a>' for t,u in SOURCES)+'</div>')

stats=[("$755.3M","Levy, frozen FY22–FY27",LIME),("$145.5M","NIFA FY27 risk, high",PINK),("($129.4M)","FY25 restated deficit",PINK),("$615.9M","Reserves at 9/30/26",TEAL),("Nov 19","NIFA vote on FY27 plan",BLUE2)]
statsH="".join(f'<div class="stat"><div class="sv" style="color:{c};text-shadow:0 0 18px {c}8c">{E(v)}</div><div class="lbl mut">{E(l)}</div></div>' for v,l,c in stats)
title="Nassau County Budget vs NIFA, 2017–2026"
desc="Nassau's FY2027 budget froze the levy at $755.3M for a sixth year. NIFA flags $60.5M–$145.5M of FY2027 risk and votes on the plan Nov 19, 2026. News, hearings, NIFA's seven recommendations, every NIFA figure and ten years of budgets vs results."
nav="".join(f'<a href="#{i}">{t}</a>' for i,t in (("news","News"),("calendar","Hearings"),("recs","NIFA asks"),("numbers","Numbers"),("conclusions","Takeaways"),("chart","Chart"),("downloads","Data")))
doc=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)} — Who Runs NY</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{CANON}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Rae Arora · Who Runs NY">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{CANON}">
<meta property="og:image" content="{CANON}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Neon on black: Nassau levy frozen at $755.3M; NIFA flags up to $145.5M of FY2027 risk; FY2025 restated deficit $129.4M.">
<meta property="article:modified_time" content="2026-11-14">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{CANON}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800;9..144,900&family=IBM+Plex+Mono:wght@500;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/app.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="brand"><a class="wordmark" href="https://whorunsny.org" rel="noopener">Who Runs NY</a><span class="dot" aria-hidden="true"></span><span class="kicker">Nassau vs NIFA</span></div><nav class="nav" aria-label="On this page">{nav}</nav></header>
<main id="main" class="wrap">
<section class="hero">
<div class="lbl" style="color:{TEAL}">Nassau County · NIFA oversight · FY2017–FY2027</div>
<h1>{E(title)}</h1>
<p class="dek">The Legislature adopted FY2027 on Oct 30 with the levy frozen at $755.3M for a sixth year. NIFA flags $60.5M–$145.5M of FY2027 risk and votes on the plan Nov 19. Figures are Major Funds unless noted.</p>
<p class="updated lbl">Last updated Nov 14, 2026 · ET</p>
<div class="stats">{statsH}</div>
</section>
{"".join(P)}
<p class="note foot">Last updated Nov 14, 2026. Full per-year sources, NIFA figures, news and the derived levy math are in the workbook above.</p>
</main>
<script src="js/app.js"></script>
</body>
</html>'''
os.makedirs("public/css",exist_ok=True); os.makedirs("public/js",exist_ok=True)
open("public/index.html","w").write(doc)
print("ok",len(doc))
