#!/usr/bin/env python3
"""Build the static pages with Python's standard library; no runtime framework."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]

def event_review():
 d=json.loads((ROOT/'research/precedents.json').read_text())
 items=[]
 for e in d['events']:
  items.append('<article class="event-card" id="event-'+escape(e['id'])+'"><div class="event-heading"><span class="label">'+escape(e['format'])+'</span><h3>'+escape(e['name'])+'</h3><p class="event-status">'+escape(e['status'])+'</p></div><dl>'+''.join('<div><dt>'+label+'</dt><dd>'+escape(e[key])+'</dd></div>' for key,label in [('requested','What participants were asked to do'),('outputs','Expected output / evidence'),('overlap','Overlap with our current proposals'),('decision','Our proposed response')])+'</dl><div class="event-links"><a href="'+escape(e['url'],quote=True)+'">Primary source ↗</a><a href="'+e['target']+'">Related Oxford brief →</a></div></article>')
 deck=d['supplied_deck']
 deck_rows=''.join('<tr><th scope="row">'+escape(e['name'])+'</th><td>'+escape(e['task'])+'</td><td>'+escape(e['decision'])+'</td></tr>' for e in deck['examples'])
 overlap=[('Cancer vaccine epitopes','Already included; TESLA is a direct prior challenge.','Refine the existing family around one disease setting, reference evidence and assay budget.','vaccines.html'),('Protein binding and confidence','Already covered in part by binding; Adaptyv/GEM are precedents.','Expand that brief with triage, calibration and separate functional evidence.','challenges.html#binding'),('Negative assay outcomes','Overlaps the existing harmonisation task.','Add an assay-evidence work package; do not count it as another challenge.','challenges.html#harmonise'),('Assay hardware for tumour–immune work','Not a separate task in our earlier catalogue. External prototyping precedents exist.','Add one scoped device/measurement concept with an assay owner.','challenges.html#assay-prototypes'),('Functional omics evidence','Adjacent to tissue profiling and response prediction, but measured function is a different endpoint.','Add one paired functional-data concept; select one deck work package.','challenges.html#functional-omics'),('General TCR activation','CASP–DREAM TAP is a closely overlapping benchmark.','Do not add a generic competing task. Check collaboration or a justified disease-specific extension.','vaccines.html#prior-art'),('Immunotherapy response','Already on our site; DREAM has a direct clinical precedent.','Retain one example and require a new cohort, endpoint or other defensible extension.','challenges.html#immuno')]
 rows=''.join('<tr><th scope="row">'+escape(a)+'</th><td>'+escape(b)+'</td><td>'+escape(c)+' <a href="'+u+'">Read brief →</a></td></tr>' for a,b,c,u in overlap)
 return '''<section class="section"><div class="wrap"><div class="section-head"><span class="label">Targeted review · 16 November 2026</span><h2>Useful precedents, not a claim of novelty.</h2><p>We reviewed the supplied Assay-A-Thon opening deck, its public event brief and six related competitions or consortium challenges. The comparison asks both whether an idea is already on our site and whether a similar task has been run elsewhere.</p></div><div class="review-summary"><div><b>Expand, don’t duplicate</b><p>Retain one vaccine family and one binding brief. Put negative-results work into harmonisation.</p></div><div><b>Two added scoping concepts</b><p>Assay prototyping and paired functional-omics evidence, with cancer-specific owners and endpoints to agree.</p></div><div><b>Novelty remains to establish</b><p>A new cancer type alone is not proof of novelty. Check cohorts, labels, HLA coverage, experimental endpoints and existing organisers.</p></div></div><p class="fine">This is a targeted landscape check, not an exhaustive literature, patent or novelty search. Where an event page describes planned tests or prizes, we report the brief rather than infer completed experiments or results. None of these organisations is an Oxford programme partner by virtue of appearing here.</p></div></section>
<section class="section tint" id="events"><div class="wrap"><div class="section-head"><h2>What similar events asked for</h2><p>Source descriptions are separated from our interpretation of overlap and our proposed adaptations.</p></div><div class="event-list">'''+''.join(items)+'''</div></div></section>
<section class="section" id="deck-mapping"><div class="wrap"><div class="section-head"><h2>From the opening deck to a manageable portfolio</h2><p>The saved 25-slide deck was supplied for review and read locally after the public Claude link returned an access-check page. Protein examples are on slides 10–11; hardware on 13–15; functional omics on 17–18. They are illustrative hypotheses and workflows, not evidence that those projects succeeded.</p><p><a href="'''+escape(deck['url'],quote=True)+'''">Original opening-deck link ↗</a> · <a href="https://immunos.bio/assay-a-thon/">Public event brief ↗</a></p></div><div class="table-scroll ruled" tabindex="0" role="region" aria-label="Opening deck examples and catalogue mapping"><table class="review-table"><thead><tr><th scope="col">Deck example</th><th scope="col">Research prompt, summarised</th><th scope="col">Our catalogue decision</th></tr></thead><tbody>'''+deck_rows+'''</tbody></table></div><p class="fine">External project names are used only to identify the reviewed examples. The raw deck, photographs, attendee information and third-party assets are not republished. Its equipment, credits, prizes and IP arrangements are not offers made by this programme.</p></div></section>
<section class="section tint" id="overlap"><div class="wrap"><div class="section-head"><h2>Has this already been proposed or tried?</h2><p>“Not previously listed here” and “not previously attempted” are different claims. The decisions below deliberately avoid claiming that an unlisted concept is scientifically novel.</p></div><div class="table-scroll ruled" tabindex="0" role="region" aria-label="Challenge overlap and portfolio decisions"><table class="review-table"><thead><tr><th scope="col">Candidate idea</th><th scope="col">What overlaps</th><th scope="col">Decision for this site</th></tr></thead><tbody>'''+rows+'''</tbody></table></div></div></section>
<section class="section" id="review-before-launch"><div class="wrap"><div class="section-head"><h2>The next check belongs with the challenge owner.</h2><p>Before presenting a task as a competition, establish the additional research value and a feasible evidence pathway.</p></div><ol class="review-checks"><li>Define the clinical or experimental decision and compare it with the closest published challenge.</li><li>Identify the exact cohort, assay labels, endpoint and permissions; check reuse and model-training exposure.</li><li>Explain what changes: for example an independent prospective cohort, an underrepresented HLA context or a different measured function.</li><li>Discuss collaboration or reuse with existing organisers where a close overlap makes that preferable.</li><li>Agree a baseline, independent evaluation, support capacity and publication/credit terms before recruitment.</li></ol><div class="actions section-actions"><a class="btn" href="propose.html#join">Propose a question to scope</a><a href="vaccines.html#vaccine-brief">See the vaccine specification →</a></div></div></section>'''

def build():
 pages=json.loads((ROOT/'content/pages.json').read_text())
 content={p['slug']: (event_review() if p['slug']=='precedents' else (ROOT/f"content/pages/{p['slug']}.html").read_text()) for p in pages}
 # Keep catalogue filter counts derived from the actual brief list.
 cat=content['challenges']
 total=len(re.findall(r'<article class="ch"',cat))
 cat=re.sub(r'>All \d+</button>', '>All '+str(total)+'</button>',cat,count=1)
 for tier in ['open','mixed','partner']:
  count=cat.count('data-ready="'+tier+'"')
  pattern=r'(<button[^>]*data-v="'+tier+r'"[^>]*>[^<]*?)\(\d+\)(</button>)'
  cat=re.sub(pattern,lambda m:m.group(1)+'('+str(count)+')'+m.group(2),cat)
 content['challenges']=cat
 # Preserve old single-page fragment URLs and turn internal links into cross-page links.
 routes={}
 for p in pages:
  for id in re.findall(r'\bid="([^"]+)"',content[p['slug']]):routes.setdefault(id,p['slug']+'.html')
 routes['data-protection']='resources.html'
 (ROOT/'research/legacy-routes.json').write_text(json.dumps(routes,ensure_ascii=False,indent=2)+'\n')
 template=(ROOT/'content/layout.html').read_text()
 for p in pages:
  slug=p['slug'];body=content[slug];own_ids=set(re.findall(r'\bid="([^"]+)"',body))
  def link(m):
   tag=m.group(0);hm=re.search(r'href="#([^"]+)"',tag)
   if not hm:return tag
   id=hm.group(1)
   if id=='main' or id in own_ids:return tag
   if id not in routes:raise ValueError(f'Unknown anchor {id} in {slug}')
   target=routes[id]
   role=re.search(r'data-role="(team|infrastructure)"',tag)
   if role and target=='propose.html':target+='?role='+role.group(1)
   return tag.replace('href="#'+id+'"','href="'+target+'#'+id+'"')
  body=re.sub(r'<a\b[^>]*>',link,body)
  nav=[]
  for target,label in [('index','Overview'),('programme','Programme'),('challenges','Challenges'),('resources','Data & partners'),('precedents','Similar events'),('propose','Propose a challenge')]:
   active=target==slug
   extra=' aria-current="page"' if active else (' class="section-current"' if target=='challenges' and slug=='vaccines' else '')
   nav.append('<a href="'+target+'.html"'+extra+'>'+escape(label)+'</a>')
  intro=''
  if slug!='index':
   extra='<a href="challenges.html">Challenges</a><span aria-hidden="true">/</span>' if slug=='vaccines' else ''
   intro='<section class="page-intro"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Overview</a><span aria-hidden="true">/</span>'+extra+'<span aria-current="page">'+escape(p['label'])+'</span></nav><p class="label">Oxford Cancer AI Challenges · PI discussion draft</p><h1>'+escape(p['title'])+'</h1><p>'+escape(p['description'])+'</p></div></section>'
  replacements={'TITLE':p['label'],'DESCRIPTION':p['description'],'SLUG':slug,'NAV':''.join(nav),'INTRO':intro,'BODY':body}
  result=template
  for key,value in replacements.items():result=result.replace('{{'+key+'}}',escape(value,quote=True) if key in ['TITLE','DESCRIPTION'] else value)
  if '{{' in result:raise ValueError('Unfilled template token')
  (ROOT/(slug+'.html')).write_text(result)
 # The manifest is injected as data into the shared script; no runtime JSON request needed.
 js=(ROOT/'site.js').read_text()
 marker='// LEGACY_SINGLE_PAGE_ROUTES'
 if marker in js:js=js[:js.index(marker)]
 js=js.rstrip()+'\n'
 js+='\n'+marker+'\nconst LEGACY_ROUTES = '+json.dumps(routes,ensure_ascii=False)+';\n'
 js+='''if (document.body.dataset.page === 'index.html' && location.hash) {
  const id = location.hash.slice(1); const page = LEGACY_ROUTES[id];
  if (page && page !== 'index.html' && !document.getElementById(id)) location.replace(page + location.hash);
}
'''
 (ROOT/'site.js').write_text(js)
 print('Built '+str(len(pages))+' pages; '+str(len(routes))+' legacy anchors mapped.')

if __name__=='__main__':build()
