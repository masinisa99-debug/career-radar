#!/usr/bin/env python3
"""Update curated job listings from public Ashby/Greenhouse APIs; no LinkedIn scraping."""
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FEED=ROOT/"feed/jobs.json"
BOARDS=[("ashby","perk","Perk"),("ashby","lexroom","Lexroom"),("ashby","fonio","fonio"),("ashby","pillar-srl","Pillar"),("greenhouse","scalapaysrl","Scalapay")]
ROLE=re.compile(r"account.?manager|account.?executive|customer.?success|onboarding|partner(ship)?|sponsorship|commercial.?operations|business.?development|sales.?operations|events?|activation|project.?manager|merchant.?success",re.I)
EXCLUDE=re.compile(r"\b(sdr|bdr|intern|internship|stage|stagista|director|vice president|head of|principal|staff|senior manager)\b",re.I)
GEO=re.compile(r"italy|italia|milan|milano|monza|spain|españa|barcelona|madrid|valencia|sevilla|seville|málaga|malaga",re.I)
SPANISH=re.compile(r"(?:fluent|native|professional|advanced|c1|c2|b2).{0,24}(?:spanish|español|castellano)|(?:spanish|español|castellano).{0,35}(?:mandatory|required|essential|fluent|native|c1|c2|b2|obligatorio|imprescindible)",re.I|re.S)
ITALIAN=re.compile(r"italian|italiano|italiana|mercato italiano",re.I)
def fetch(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"CareerRadar/1.0"})
    with urllib.request.urlopen(req,timeout=20) as response:return json.load(response)
def city_country(location):
    for name,pattern in [("Milano","milano|milan"),("Monza","monza"),("Madrid","madrid"),("Barcellona","barcelona|barcellona"),("Valencia","valencia"),("Siviglia","sevilla|seville|siviglia"),("Málaga","malaga|málaga")]:
        if re.search(pattern,location,re.I):return name,("Italia" if name in ("Milano","Monza") else "Spagna")
    if re.search("spain|españa",location,re.I):return "Remote Spagna","Spagna"
    if re.search("italy|italia",location,re.I):return "Italia remoto","Italia"
    return None,None
def record(name,title,location,url,description,posted,source,identity):
    if not ROLE.search(title) or EXCLUDE.search(title) or not GEO.search(location) or SPANISH.search(description):return None
    city,country=city_country(location)
    if not city or not url:return None
    it=bool(ITALIAN.search(title+" "+description))
    score=round(min(4.9,3.4+(.7 if ITALIAN.search(title) else .2)+(0.25 if country=="Italia" else 0)+(.25 if re.search("partner|account|customer success",title,re.I) else 0)),2)
    return {"id":"ATS-"+re.sub("[^A-Za-z0-9_-]","",str(identity)),"company":name,"title":title,"location":location,"city":city,"country":country,"industry":"Tech / SaaS","url":url,"language":"Italiano + inglese: da confermare" if it else "Lingua da verificare","score":score,"fit":3,"interest":3,"access":3,"reason":"Annuncio sul sito carriera. Verificare requisiti, lingue e retribuzione.","status":"Da valutare","verification":"ATS pubblica · da controllare","source":source,"origin":"Feed online","addedAt":dt.date.today().isoformat(),"postedAt":str(posted or "")[:10],"saved":False,"appliedAt":"","followUp":"","contact":"","salary":"","notes":""}
def read_board(kind,slug,name):
    if kind=="ashby":
        for j in fetch("https://api.ashbyhq.com/posting-api/job-board/"+slug+"?includeCompensation=true").get("jobs",[]):
            if j.get("isListed") is False:continue
            places=[str(j.get("location",""))]+[str(x.get("location","")) for x in j.get("secondaryLocations",[]) if isinstance(x,dict)]
            rec=record(name,str(j.get("title",""))," / ".join(x for x in places if x),str(j.get("jobUrl") or j.get("applyUrl") or ""),str(j.get("descriptionPlain","")),j.get("publishedAt"),"Ashby · azienda",slug+"-"+str(j.get("id") or j.get("jobUrl")))
            if rec:
                rec["salary"]=str((j.get("compensation") or {}).get("compensationTierSummary") or "")
                yield rec
    else:
        for j in fetch("https://boards-api.greenhouse.io/v1/boards/"+slug+"/jobs?content=true").get("jobs",[]):
            desc=re.sub("<[^>]*>"," ",str(j.get("content","")))
            rec=record(name,str(j.get("title","")),str((j.get("location") or {}).get("name","")),str(j.get("absolute_url","")),desc,j.get("first_published"),"Greenhouse · azienda",slug+"-"+str(j.get("id")))
            if rec:yield rec
def main():
    results=[];errors=[];successful=0
    for kind,slug,name in BOARDS:
        try:
            jobs=list(read_board(kind,slug,name))
            results.extend(jobs);successful+=1
            print(name,len(jobs))
        except Exception as exc:
            errors.append(name+": "+str(exc))
    if not successful:
        print("All sources failed; existing feed preserved.",errors)
        raise SystemExit(1)
    seen=set();dedup=[]
    for item in results:
        if item["url"] not in seen:
            seen.add(item["url"]);dedup.append(item)
    data={"updatedAt":dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),"jobs":dedup,"sources":[{"company":name,"source":kind+":"+slug} for kind,slug,name in BOARDS],"errors":errors,"disclaimer":"Solo alcune ATS pubbliche, non LinkedIn. Verificare sempre ogni annuncio."}
    FEED.parent.mkdir(exist_ok=True)
    FEED.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Saved",len(dedup),"matches")
if __name__=="__main__":main()
