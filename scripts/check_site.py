#!/usr/bin/env python3
"""Check static page links, assets, fragment targets and basic document semantics."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import sys
ROOT=Path(__file__).resolve().parents[1]
class Scan(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.assets=[];self.h1=0;self.images=[];self.labels=[];self.controls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ('img','script') and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
  if tag=='img' and 'alt' not in a:self.images.append(a.get('src','unknown'))
  if tag=='label' and a.get('for'):self.labels.append(a['for'])
  if tag in ('input','select','textarea') and a.get('type')!='checkbox':self.controls.append(a.get('id'))
pages={}
for path in ROOT.glob('*.html'):
 parsed=Scan();parsed.feed(path.read_text());pages[path.name]=parsed
errors=[]
for name,page in pages.items():
 if page.h1!=1:errors.append(f'{name}: expected one h1; found {page.h1}')
 for id,n in Counter(page.ids).items():
  if n>1:errors.append(f'{name}: duplicate id {id}')
 for asset in page.images:errors.append(f'{name}: image lacks alt: {asset}')
 for id in page.controls:
  if not id or id not in page.labels:errors.append(f'{name}: control lacks an explicit label: {id}')
 for url in page.links+page.assets:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  if not (ROOT/target).is_file():errors.append(f'{name}: missing local file {url}');continue
  if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{name}: missing fragment {url}')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'Checked {len(pages)} pages: local links, assets, fragments, IDs, headings and control labels pass.')
