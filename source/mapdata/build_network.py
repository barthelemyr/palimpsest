"""Network data for Palimpsest.
Overlays today's countries (Natural Earth 1:50m, public domain) with Cliopatria v0.2.1 polities (CC BY 4.0):
for every country and every span of years, which state or empire covered how much of its land.
Countries covered by the same empire (Cliopatria umbrella, e.g. "(Holy Roman Empire)") are grouped under it.
Output: network.json (country anchors, per-country membership intervals, allegiances between groups)."""
import json, gzip, base64, math
from collections import defaultdict
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.strtree import STRtree

SHARE_MIN = 0.2       # a group must cover at least 20% of a country's land to count
M = json.load(open("map2.json"))
def gun(b): return gzip.decompress(base64.b64decode(b))
class R:
    def __init__(s, b): s.b, s.i = b, 0
    def u(s):
        v = m = 0; sh = 0
        while True:
            c = s.b[s.i]; s.i += 1; v |= (c & 127) << sh; sh += 7
            if not c & 128: return v
    def z(s): v = s.u(); return -(v + 1) // 2 if v & 1 else v // 2
meta = json.loads(gun(M["meta"]))
G = meta["grid"]
ar = R(gun(M["arcs"])); na = ar.u(); arcs = []; x = y = 0
for _ in range(na):
    n = ar.u(); pts = []
    for _ in range(n): x += ar.z(); y += ar.z(); pts.append((x / G, y / G))
    arcs.append(pts)
gr = R(gun(M["geoms"])); ng = gr.u(); geoms = []
for _ in range(ng):
    polys = []
    for _ in range(gr.u()):
        rings = []
        for _ in range(gr.u()):
            ring = []; prev = 0
            for _ in range(gr.u()):
                st = prev + gr.z(); c = gr.u(); ln = (c >> 1) + 1; d = -1 if c & 1 else 1
                ring += [st + d * j for j in range(ln)]; prev = st + d * (ln - 1)
            rings.append(ring)
        polys.append(rings)
    geoms.append(polys)
def ring_xy(ring):
    out = []
    for k, ai in enumerate(ring):
        pts = arcs[ai] if ai >= 0 else arcs[~ai][::-1]
        out += pts if k == 0 else pts[1:]
    return out
def geom_shape(gi):
    ps = []
    for rings in geoms[gi]:
        try:
            p = Polygon(ring_xy(rings[0]), [ring_xy(r) for r in rings[1:]])
            if not p.is_valid: p = make_valid(p)
            ps.append(p)
        except Exception: pass
    g = ps[0] if len(ps) == 1 else MultiPolygon([q for p in ps for q in ([p] if p.geom_type == "Polygon" else [h for h in getattr(p, "geoms", []) if h.geom_type == "Polygon"])])
    return g.simplify(0.8, preserve_topology=True).buffer(0)

ents = meta["ents"]
recs = [dict(zip("e f t g c lx ly lr area top mem comp triv".split(), r)) for r in meta["recs"]]
leaf = [r for r in recs if ents[r["e"]]["k"] == 0]
group_of = lambda r: r["top"] if r["top"] >= 0 else r["e"]

# ------------------------------------------------------------------ countries
today = json.load(open("today.json"))
lab = {l[0]: l for l in today["labels"]}
SHORT = {"United States of America": "United States", "Dem. Rep. Congo": "DR Congo"}
countries = []
for f in json.load(open("ne_countries_proj.geojson"))["features"]:
    nm = f["properties"]["name"]; g = shape(f["geometry"])
    if not g.is_valid: g = make_valid(g)
    g = g.simplify(0.8, preserve_topology=True).buffer(0)
    if g.area < 12: continue                       # tiny islands and city states drop out (about 500 km2)
    l = lab.get(SHORT.get(nm, nm))
    if l: ax, ay = l[1], l[2]
    else: c = g.representative_point(); ax, ay = c.x, c.y
    countries.append({"n": SHORT.get(nm, nm), "g": g, "ax": ax, "ay": ay, "area": g.area})
print(len(countries), "countries")
tree = STRtree([c["g"] for c in countries])

# ------------------------------------------------------------------ overlay: share of each country covered by each leaf geometry
share_cache = {}
def shares(gi):
    if gi in share_cache: return share_cache[gi]
    g = geom_shape(gi); out = []
    for ci in tree.query(g):
        c = countries[ci]
        try: a = c["g"].intersection(g).area
        except Exception: a = 0
        if a / c["area"] >= 0.03: out.append((int(ci), a / c["area"]))
    share_cache[gi] = out; return out
events = defaultdict(list)    # country -> list of (f, t, group, share)
for k, r in enumerate(leaf):
    for ci, sh in shares(r["g"]):
        events[ci].append((r["f"], r["t"], group_of(r), sh))
    if k % 2000 == 0: print("overlay", k, "/", len(leaf))

# ------------------------------------------------------------------ per country: intervals of group membership
out_c = []
for ci, c in enumerate(countries):
    ev = events.get(ci, [])
    cuts = sorted({e[0] for e in ev} | {e[1] + 1 for e in ev})
    segs = []
    for a, b in zip(cuts, cuts[1:]):
        acc = defaultdict(float)
        for f, t, gr_, sh in ev:
            if f <= a and b - 1 <= t: acc[gr_] += sh
        mem = sorted([(g_, round(min(1, s) * 10)) for g_, s in acc.items() if s >= SHARE_MIN], key=lambda x: -x[1])
        if not mem and acc:   # no state covers 20%: still show the largest one if it covers at least 5% (e.g. the Aztec heartland in Mexico)
            g_, s_ = max(acc.items(), key=lambda kv: kv[1])
            if s_ >= 0.05: mem = [(g_, max(1, round(s_ * 10)))]
        if segs and segs[-1][2] == mem and segs[-1][1] + 1 == a: segs[-1][1] = b - 1
        elif mem: segs.append([a, b - 1, mem])
    out_c.append([c["n"], round(c["ax"], 1), round(c["ay"], 1), round(c["area"]), [[s[0], s[1], [x for m in s[2] for x in m]] for s in segs]])

# ------------------------------------------------------------------ allegiances between groups (Cliopatria RELATION records)
by_e = defaultdict(list)
for r in leaf: by_e[r["e"]].append(r)
def group_at(e, y):
    for r in by_e.get(e, []):
        if r["f"] <= y <= r["t"]: return group_of(r)
    return -1
rels = set()
for r in recs:
    if ents[r["e"]]["k"] != 2 or len(r["comp"]) < 2: continue
    v, o = r["comp"][0], r["comp"][1]
    gv, go = group_at(v, r["f"]), group_at(o, r["f"])
    if gv >= 0 and go >= 0 and gv != go: rels.add((r["f"], r["t"], gv, go))
groups = sorted({m for c in out_c for s in c[4] for m in s[2][0::2]})
gcol = {int(k): v for k, v in meta["gcol"].items()}
# capitals (hand-curated, see capitals.py), projected like everything else
from capitals import C as CAPS
A1, A2, A3, A4, MM = 1.340264, -0.081106, 0.000893, 0.003796, math.sqrt(3) / 2
def proj(lon, lat):
    l, p = math.radians(lon), math.radians(lat); t = math.asin(MM * math.sin(p)); t2 = t * t; t6 = t2 * t2 * t2
    return l * math.cos(t) / (MM * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))) * 1000, -t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)) * 1000
cap = {}
for g_ in groups:
    lst = CAPS.get(ents[g_]["n"])
    if lst: cap[str(g_)] = [[f, round(proj(lo, la)[0], 1), round(proj(lo, la)[1], 1), city] for f, lo, la, city in lst]
used = {ents[g_]["n"] for g_ in groups}
print("capitals for", len(cap), "of", len(groups), "groups; unused names:", sorted(set(CAPS) - used))
out = {"src": "Cliopatria v0.2.1 (Seshat, CC BY 4.0) overlaid on Natural Earth 1:50m countries (public domain)", "share_min": SHARE_MIN, "share_fallback": 0.05,
       "countries": out_c, "rels": sorted(rels), "gcol": {str(g): gcol.get(g, "#9a958a") for g in groups}, "cap": cap,
       "cap_src": "Capitals hand-curated from standard references (approximate locations); to be verified against Wikidata P36."}
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("network.json", "w", encoding="utf-8").write(s)
print(f"countries={len(out_c)} segments={sum(len(c[4]) for c in out_c)} groups={len(groups)} rels={len(rels)} size={len(s)/1e3:.0f} KB")
