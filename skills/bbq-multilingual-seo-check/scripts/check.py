#!/usr/bin/env python3
"""Bounded read-only checks of HTML localization declarations and sitemap membership."""
import argparse
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


def origin(url):
    p=urllib.parse.urlsplit(url)
    return (p.scheme, p.netloc.lower())

def clean(url):
    return urllib.parse.urldefrag(url)[0]

def compatible(a,b):
    a,b=a.lower(),b.lower()
    return bool(a and b) and (a==b or a.startswith(b+'-') or b.startswith(a+'-'))

class Tags(HTMLParser):
    def __init__(self,base):
        super().__init__(convert_charrefs=True)
        self.base=base;self.lang='';self.canonical=[];self.alternates=[];self.has_base=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang') or ''
        if tag=='base':self.has_base=True
        if tag!='link':return
        rel=(a.get('rel') or '').lower().split();href=a.get('href')
        if not href:return
        target=clean(urllib.parse.urljoin(self.base,href))
        if 'canonical' in rel:self.canonical.append(target)
        if 'alternate' in rel and a.get('hreflang'):
            self.alternates.append({'lang':a['hreflang'].lower(),'url':target,'raw_href':href})

class ScopedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self,allowed):self.allowed=allowed
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if origin(newurl) not in self.allowed:raise ValueError('redirect outside allowed origins')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

class Fetcher:
    def __init__(self,allowed,budget=70,delay=.1):
        self.allowed=allowed;self.budget=budget;self.delay=delay;self.cache={};self.requests=0
        self.opener=urllib.request.build_opener(ScopedRedirect(allowed))
    def get(self,url):
        url=clean(url)
        if url in self.cache:return self.cache[url]
        result={'requested_url':url,'status':None,'final_url':None,'error':None}
        if origin(url) not in self.allowed:
            result['error']='outside_allowed_origins'
        elif self.requests>=self.budget:
            result['error']='request_budget_exhausted'
        else:
            self.requests+=1
            try:
                time.sleep(self.delay)
                req=urllib.request.Request(url,headers={'User-Agent':'BBQGrowthPlaybook/0.2 read-only-audit'})
                try:response=self.opener.open(req,timeout=15)
                except urllib.error.HTTPError as e:response=e
                with response:
                    data=response.read(5_000_001)
                    result.update(status=response.status,final_url=response.geturl(),content_type=response.headers.get('Content-Type',''))
                    if len(data)>5_000_000:raise ValueError('response exceeds 5 MB limit')
                    result['sha256']=hashlib.sha256(data).hexdigest()
                    result['text']=data.decode(response.headers.get_content_charset() or 'utf-8',errors='replace')
            except Exception as e:result['error']=str(e)
        self.cache[url]=result
        return result

def sitemap(fetch,roots,max_maps=20):
    todo=list(roots);seen=set();urls=set();evidence=[];complete=bool(roots)
    while todo and len(seen)<max_maps:
        url=todo.pop(0)
        if url in seen:continue
        seen.add(url);r=fetch.get(url)
        entry={k:v for k,v in r.items() if k!='text'};evidence.append(entry)
        if r['status']!=200 or r['error']:
            complete=False;continue
        try:root=ET.fromstring(r.get('text',''))
        except ET.ParseError:
            entry['parse_error']='invalid_xml';complete=False;continue
        kind=root.tag.rsplit('}',1)[-1]
        locs=[clean(urllib.parse.urljoin(r['final_url'],x.text.strip())) for x in root.findall('./{*}sitemap/{*}loc' if kind=='sitemapindex' else './{*}url/{*}loc') if x.text]
        if kind=='sitemapindex':todo.extend(locs)
        elif kind=='urlset':urls.update(locs)
        else:entry['parse_error']='unsupported_root';complete=False
    if todo:complete=False
    return {'complete':complete,'url_count':len(urls),'documents':evidence},urls

def page(fetch,url):
    r=fetch.get(url);e={k:v for k,v in r.items() if k!='text'}
    if r['status']!=200 or r['error']:return e,None
    if 'html' not in r.get('content_type','').lower():
        e['parse_error']='not_html';return e,None
    p=Tags(r['final_url']);p.feed(r.get('text',''))
    e.update(html_lang=p.lang,canonical=p.canonical,hreflang=p.alternates,base_element=p.has_base)
    return e,p

def audit(fetch,urls,maps):
    sm,members=sitemap(fetch,maps);results=[]
    for url in urls:
        evidence,p=page(fetch,url);checks=[]
        def add(name,status,detail):checks.append({'check':name,'status':status,'evidence':detail})
        add('http_status','pass' if evidence['status']==200 and not evidence['error'] else 'unknown' if evidence['status'] is None else 'fail',evidence)
        final=evidence.get('final_url') or url
        add('sitemap_membership','pass' if final in members else 'review' if sm['complete'] else 'unknown',{'url':final,'found':final in members,'sitemap_complete':sm['complete']})
        if p:
            if p.has_base:add('base_element','unknown','Relative URL resolution assumes document URL; inspect base href manually')
            add('canonical_count','pass' if len(p.canonical)==1 else 'review',p.canonical)
            for target in p.canonical:
                target_e,target_p=page(fetch,target)
                add('canonical_target_status','pass' if target_e['status']==200 and not target_e.get('error') else 'unknown' if target_e['status'] is None else 'review',target_e)
                add('canonical_language','unknown' if not target_p or not target_p.lang or not p.lang else 'pass' if compatible(p.lang,target_p.lang) else 'review',{'source_lang':p.lang,'target_lang':target_p.lang if target_p else None,'url':target})
            labels=[a['lang'] for a in p.alternates]
            add('hreflang_declarations','pass' if labels and len(set(labels))==len(labels) else 'review',labels)
            add('hreflang_self_reference','pass' if any(a['url']==final for a in p.alternates) else 'review',{'page':final,'note':'HTML declarations only; HTTP headers or sitemap alternatives may supply annotations'})
            for alt in p.alternates:
                te,tp=page(fetch,alt['url'])
                add('hreflang_target_status','pass' if te['status']==200 and not te.get('error') else 'unknown' if te['status'] is None else 'review',{'alternate':alt,'target':te})
                add('hreflang_target_language','unknown' if alt['lang']=='x-default' or not tp or not tp.lang else 'pass' if compatible(alt['lang'],tp.lang) else 'review',{'declared':alt['lang'],'target_html_lang':tp.lang if tp else None,'target_url':alt['url'],'note':'HTML lang is a declaration, not detected body language'})
                add('hreflang_return_link','unknown' if not tp else 'pass' if any(a['url']==final for a in tp.alternates) else 'review',{'target_url':alt['url'],'expected_return_url':final,'target_alternates':tp.alternates if tp else None})
                add('hreflang_sitemap_membership','pass' if alt['url'] in members else 'review' if sm['complete'] else 'unknown',{'target_url':alt['url'],'found':alt['url'] in members,'sitemap_complete':sm['complete']})
        results.append({'url':url,'checks':checks})
    counts={s:sum(c['status']==s for r in results for c in r['checks']) for s in ['pass','review','fail','unknown']}
    return {'schema_version':1,'observed_at':datetime.now(timezone.utc).isoformat(),'mode':'bounded_http_html_sample','summary':{'seed_pages':len(urls),'requests':fetch.requests,'checks':counts},'sitemap':sm,'pages':results,'limits':['Sample only; not a complete website audit or indexing/ranking proof','HTML head declarations only; HTTP Link and XML hreflang extensions not evaluated','HTML lang and hreflang are declared labels; body language, translation quality and equivalent meaning require review','Canonical alternatives, regional fallbacks and absent sitemap entries may be intentional','No JavaScript rendering, robots rules, noindex, or Search Console data checked','Network failures, request limits and external origins remain unknown; redirects stay within allowed origins']}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--url',action='append',required=True)
    ap.add_argument('--sitemap',action='append',default=[])
    ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--max-requests',type=int,default=70)
    args=ap.parse_args()
    if not 1<=args.max_requests<=200:ap.error('--max-requests must be 1..200')
    if len(args.url)>20:ap.error('At most 20 seed URLs per sample')
    if any(origin(u)[0] not in {'http','https'} or not origin(u)[1] for u in args.url+args.sitemap):ap.error('Use absolute HTTP(S) URLs')
    fetch=Fetcher({origin(u) for u in args.url+args.sitemap},args.max_requests)
    result=audit(fetch,args.url,args.sitemap)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['summary'],ensure_ascii=False))
if __name__=='__main__':main()
