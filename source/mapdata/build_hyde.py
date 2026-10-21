"""Population per today's country, from HYDE 3.3 (Klein Goldewijk et al., Utrecht University, DOI 10.24416/UU01-94FNH0).
Input : HYDE 3.3 txt/popc_c.txt (population per country and date) for the base scenario, and optionally lower/upper.
Output: hyde.json, aligned with network.json's country list (same order), so the site can look a country up by index.
Where HYDE counts several of today's countries together (e.g. Israel and Palestine, Serbia and Montenegro with Kosovo),
the site shows the joint figure as such; only the circle sizes in the network split it, by land area."""
import json, sys, math
from pathlib import Path

SCR = Path(__import__("os").environ.get("HYDE_DIR", "downloads"))
SRC = {"base": SCR / "hyde_txt/popc_c.txt", "lower": SCR / "hyde_lower/popc_c.txt", "upper": SCR / "hyde_upper/popc_c.txt"}
KEEP = lambda y: y <= 1700 or (y <= 1950 and y % 10 == 0) or (y % 10 == 0) or y == 2023   # 1000-yr, 100-yr, then 10-yr steps

def load(p):
    L = [l.split() for l in open(p)]
    yrs = [int(x) for x in L[0][1:]]; rows = {}; tot = None
    for r in L[1:]:
        if r[0] == "Total": tot = [float(v) for v in r[1:]]; continue
        rows[int(float(r[0]))] = [float(v) for v in r[1:]]
    return yrs, rows, tot

def sig3(v):
    if v <= 0: return 0
    k = int(math.floor(math.log10(v))) - 2
    return int(round(v / 10 ** k) * 10 ** k) if k > 0 else int(round(v))

ne = {f["properties"]["name"]: (int(f["id"]) if f.get("id") else None) for f in json.load(open("topo/ne_countries.geojson"))["features"]}
SHORT = {"United States": "United States of America", "DR Congo": "Dem. Rep. Congo"}
# today's countries that HYDE folds into another code
JOINT = {"Sudan": 736, "S. Sudan": 736, "Serbia": 891, "Montenegro": 891, "Kosovo": 891, "Israel": 376, "Palestine": 376,
         "Somalia": 706, "Somaliland": 706, "Cyprus": 196, "N. Cyprus": 196}
net = json.load(open("network.json"))["countries"]

out = {"src": "HYDE 3.3 (History Database of the Global Environment), Klein Goldewijk et al., Utrecht University, 2023. Population per country, base scenario.",
       "doi": "https://doi.org/10.24416/UU01-94FNH0", "lic": "Creative Commons Attribution"}
for scen, p in SRC.items():
    if not p.exists(): print("no", scen); continue
    yrs, rows, tot = load(p)
    idx = [i for i, y in enumerate(yrs) if KEEP(y)]
    if scen == "base": out["y"] = [yrs[i] for i in idx]; out["w"] = [sig3(tot[i]) for i in idx]
    else: out["w_" + scen] = [sig3(tot[i]) for i in idx]
    vals, joint, miss = [], {}, []
    # area of each joint group, for the size split
    garea = {}
    for c in net:
        code = JOINT.get(c[0])
        if code: garea[code] = garea.get(code, 0) + c[3]
    for c in net:
        n = c[0]; code = JOINT.get(n) or ne.get(SHORT.get(n, n))
        if code is None or code not in rows: vals.append(None); miss.append(n); continue
        v = rows[code]
        if n in JOINT:
            members = [m for m in JOINT if JOINT[m] == code and any(x[0] == m for x in net)]
            if len(members) > 1:
                share = c[3] / garea[code]
                joint[n] = ", ".join(sorted(members, key=lambda m: m != "Israel" and m != "Sudan" and m != "Serbia" and m != "Somalia" and m != "Cyprus" and m != "Finland"))
                vals.append([sig3(v[i] * share) for i in idx])
                out.setdefault("jv_" + scen, {})[n] = [sig3(v[i]) for i in idx]
                continue
        vals.append([sig3(v[i]) for i in idx])
    out["c" if scen == "base" else "c_" + scen] = vals
    if scen == "base": out["j"] = joint; print("no HYDE figure for:", miss)
    print(scen, "world 1 CE", out["w" if scen == "base" else "w_" + scen][out["y"].index(0)])
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("hyde.json", "w", encoding="utf-8").write(s)
print(f"{len(out['y'])} dates, {sum(v is not None for v in out['c'])} of {len(net)} countries, {len(s)/1e3:.0f} KB")
