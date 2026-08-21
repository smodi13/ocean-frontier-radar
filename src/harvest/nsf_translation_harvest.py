"""
NSF research-translation harvester — Ocean Frontier Radar, Phase 1.

Queries the public NSF Awards API across an ocean-technology vocabulary
and keeps only awards from commercialization-track programs: I-Corps,
PFI (Partnerships for Innovation), Convergence Accelerator, and
Translation to Practice.

These are the highest-differentiation signal identified in Phase 1:
I-Corps in particular funds *pre-company* customer discovery, catching
researchers 6-24 months before a company exists.

Output: data/nsf_translation_raw.json

See the note in nsf_sbir_harvest.py about the use of curl.
"""
import json, urllib.parse, subprocess, sys, time
KWS=["ocean","marine","underwater","subsea","aquaculture","seaweed","coastal","offshore",
     "seawater","corrosion","biofouling","desalination","fisheries","maritime","vessel",
     "sonar","buoy","tidal","wave energy","kelp","shellfish","hull","antifouling","reef"]
FIELDS="id,title,awardeeName,awardeeStateCode,awardeeCity,date,estimatedTotalAmt,fundProgramName,piFirstName,piLastName,abstractText"
def fetch(kw,off):
    q=urllib.parse.urlencode({"keyword":kw,"dateStart":"01/01/2024","offset":off,"rpp":25,"printFields":FIELDS})
    r=subprocess.run(["curl","-s","--max-time","60","-A","OceanFrontierRadar/0.1 research",
                      "https://api.nsf.gov/services/v1/awards.json?"+q],capture_output=True,text=True)
    try: return json.loads(r.stdout).get("response",{}).get("award",[])
    except: return []
TARGET=["PFI","I-CORPS","ICORPS","TRANSLATION","CONVERGENCE ACCELERATOR","ACCELERATING RESEARCH TRANSLATION","TECHNOLOGY TRANSLATION"]
out={}
for kw in KWS:
    for off in range(1,250,25):
        aws=fetch(kw,off)
        if not aws: break
        for a in aws:
            fp=(a.get("fundProgramName") or "").upper()
            if any(t in fp for t in TARGET):
                a["_kw"]=kw; out[a["id"]]=a
        time.sleep(0.1)
    print("done",kw,len(out),file=sys.stderr)
json.dump(list(out.values()),open("data/nsf_translation_raw.json","w"),indent=1)
print("TOTAL:",len(out))
