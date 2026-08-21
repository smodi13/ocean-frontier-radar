"""
NSF SBIR/STTR harvester — Ocean Frontier Radar, Phase 1.

Queries the public NSF Awards API (no authentication required) across an
ocean-technology vocabulary and keeps only awards whose fundProgramName
indicates SBIR or STTR — i.e. a company that has won competitive
non-dilutive funding judged partly on commercial merit.

Output: data/nsf_sbir_raw.json

Note: shells out to `curl` rather than using urllib/requests. On the
development machine TLS interception caused urllib to fail certificate
verification. Disabling verification would be the wrong fix; Phase 2
should use `requests` with a proper certifi CA bundle instead.

Precision caveat: NSF keyword search matches abstract text, so roughly
80% of returned records are false positives (biomedical "vessel",
ultrasound "acoustic", etc.). Classification is a downstream step.
"""
import json, urllib.parse, subprocess, sys, time

KWS = ["ocean","marine","underwater","subsea","aquaculture","seaweed","kelp","coastal",
       "offshore","seawater","corrosion","desalination","alkalinity","carbon removal",
       "sonar","hydrofoil","biofouling","fisheries","shellfish","vessel","buoy","tidal",
       "wave energy","maritime","estuary","harmful algal","aquatic","port","ship","hull",
       "oyster","salmon","reef","sediment","bathymetry","acoustic","glider","mooring"]

FIELDS="id,title,awardeeName,awardeeStateCode,awardeeCity,date,startDate,estimatedTotalAmt,fundProgramName,piFirstName,piLastName,abstractText"

def fetch(kw, offset):
    q = urllib.parse.urlencode({"keyword":kw,"dateStart":"01/01/2025","offset":offset,
                                "rpp":25,"printFields":FIELDS})
    url="https://api.nsf.gov/services/v1/awards.json?"+q
    r=subprocess.run(["curl","-s","--max-time","60","-A","OceanFrontierRadar/0.1 research",url],
                     capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get("response",{}).get("award",[])
    except Exception:
        return []

out={}
for kw in KWS:
    for off in range(1, 300, 25):
        aws=fetch(kw,off)
        if not aws: break
        for a in aws:
            fp=(a.get("fundProgramName") or "").upper()
            if "SBIR" in fp or "STTR" in fp:
                a["_kw"]=kw
                out[a["id"]]=a
        time.sleep(0.1)
    print("done",kw,"cum:",len(out), file=sys.stderr)

json.dump(list(out.values()), open("data/nsf_sbir_raw.json","w"), indent=1)
print("TOTAL NSF SBIR/STTR (2025+):", len(out))
