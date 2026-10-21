"""Palimpsest map data v2.
Cliopatria v0.2.1 (CC BY 4.0) outlines as one shared-arc topology (neighbouring borders stay identical),
hierarchy resolved (umbrella polities vs members vs relations), neighbour-aware colours, label anchors
(pole of inaccessibility), modern-country search aliases (Natural Earth, public domain).
Input: topo/topo_w.json (topojson-server + presimplify of topo/clio_proj.geojson, topo/land_proj.geojson)."""
import json, math, re, base64, colorsys, unicodedata
from collections import defaultdict
from shapely.geometry import shape, Polygon, MultiPolygon, Point
from shapely.validation import make_valid
from shapely.ops import polylabel

Q = 1000.0
GRID = 20.0            # 1 world unit = 1/1000 earth radius (6.37 km) -> 0.32 km grid
FLOOR = 0.05           # drop vertices whose Visvalingam area is below this (world units^2): invisible at max zoom
PATCH = ["#f5a53a", "#36b3a3", "#62aee8", "#f1c84b", "#7ccb8b", "#f39a8e", "#a08fdc", "#2f86c9", "#48a46c", "#f7c1a6", "#8fd6d6", "#e7d9a9", "#ef7f4d", "#5fc2b0"]

# ------------------------------------------------------------------ varint stream
class VS:
    def __init__(s): s.b = bytearray()
    def u(s, v):
        while v >= 0x80: s.b.append((v & 0x7F) | 0x80); v >>= 7
        s.b.append(v)
    def i(s, v): s.u((v << 1) if v >= 0 else ((-v << 1) - 1))
    def b64(s): return base64.b64encode(bytes(s.b)).decode()

# ------------------------------------------------------------------ topology
T = json.load(open("topo/topo_w.json"))
arcs_in = T["arcs"]
arc_pts = []
for a in arcs_in:
    pts = [(round(q[0] * GRID), round(q[1] * GRID)) for k, q in enumerate(a) if k == 0 or k == len(a) - 1 or q[2] is None or q[2] >= FLOOR]
    ded = [pts[0]] + [pts[k] for k in range(1, len(pts)) if pts[k] != pts[k - 1]]
    if len(ded) == 1: ded = ded * 2
    arc_pts.append(ded)

def ring_coords(ring):
    out = []
    for k, ai in enumerate(ring):
        pts = arc_pts[ai] if ai >= 0 else arc_pts[~ai][::-1]
        out.extend(pts if k == 0 else pts[1:])
    return out

# ------------------------------------------------------------------ cliopatria records
F = json.load(open("raw/cliopatria_polities_only_v021.geojson"))["features"]
P = [f["properties"] for f in F]
cgeo = {g["id"]: g for g in T["objects"]["c"]["geometries"]}
FULL = json.load(open("topo/clio_proj.geojson"))["features"]   # unquantised projected coords for label anchors

ents, eidx = [], {}
def ent_of(p):
    n = p["Name"]
    if n not in eidx:
        eidx[n] = len(ents)
        kind = 2 if p["Type"] == "RELATION" else (1 if p.get("Components") else 0)
        ents.append({"n": n, "label": re.sub(r"^\((.*)\)$", r"\1", n), "k": kind, "wp": "", "wd": "", "sid": "", "f": p["FromYear"], "t": p["ToYear"]})
    e = ents[eidx[n]]
    e["f"] = min(e["f"], p["FromYear"]); e["t"] = max(e["t"], p["ToYear"])
    for k, pk in (("wp", "Wikipedia"), ("wd", "Wikidata"), ("sid", "SeshatID")):
        if not e[k] and p.get(pk): e[k] = p[pk]
    return eidx[n]

geoms, gkey, gbbox, glabel = [], {}, [], []
def largest_poly(g):
    if not g.is_valid: g = make_valid(g)
    polys = [g] if g.geom_type == "Polygon" else [q for q in getattr(g, "geoms", []) if q.geom_type == "Polygon"]
    if not polys:
        polys = [q for gg in getattr(g, "geoms", []) for q in ([gg] if gg.geom_type == "Polygon" else getattr(gg, "geoms", [])) if q.geom_type == "Polygon"]
    return max(polys, key=lambda q: q.area) if polys else None

recs = []
for k, p in enumerate(P):
    ei = ent_of(p)
    tg = cgeo[k]
    if not tg.get("arcs"): continue
    arcs = tg["arcs"] if tg["type"] == "MultiPolygon" else [tg["arcs"]]
    key = json.dumps(arcs, separators=(",", ":"))
    if key not in gkey:
        gkey[key] = len(geoms); geoms.append(arcs)
        xs, ys = [], []
        for poly in arcs:
            for c in ring_coords(poly[0]): xs.append(c[0]); ys.append(c[1])
        gbbox.append([min(xs), min(ys), max(xs), max(ys)])
        lp = largest_poly(shape(FULL[k]["geometry"]))
        if lp is None or lp.area <= 0:
            glabel.append([(gbbox[-1][0] + gbbox[-1][2]) / 2 / GRID, (gbbox[-1][1] + gbbox[-1][3]) / 2 / GRID, 0.5])
        else:
            tol = max(0.05, math.sqrt(lp.area) / 60)
            c = polylabel(lp, tolerance=tol)
            glabel.append([c.x, c.y, max(0.3, lp.exterior.distance(c) if lp.contains(c) else 0.3)])
    gi = gkey[key]
    recs.append({"e": ei, "f": p["FromYear"], "t": p["ToYear"], "g": gi, "area": round(p.get("Area") or 0),
                 "mem": [m for m in (p.get("MemberOf") or "").split(";") if m], "comp": [c for c in (p.get("Components") or "").split(";") if c]})

# ------------------------------------------------------------------ hierarchy: top umbrella for each leaf record
by_name = defaultdict(list)
for r in recs: by_name[ents[r["e"]]["n"]].append(r)
def rec_at(name, f, t):
    c = [q for q in by_name.get(name, []) if q["f"] <= t and f <= q["t"]]
    return max(c, key=lambda q: min(q["t"], t) - max(q["f"], f)) if c else None
def trivial(u):          # an umbrella with a single component is just an alias of it
    return len(u["comp"]) <= 1
def top_of(r, depth=0):
    best = None
    for m in r["mem"]:
        u = rec_at(m, r["f"], r["t"])
        if not u or trivial(u): continue
        up = top_of(u, depth + 1) if depth < 6 else None
        cand = up or u
        if best is None or recs_area(cand) > recs_area(best): best = cand
    return best
recs_area = lambda q: q["area"]
for r in recs:
    k = ents[r["e"]]["k"]
    r["top"] = -1
    if k == 0:
        u = top_of(r)
        if u: r["top"] = u["e"]
    elif k == 1:
        r["trivial"] = trivial(r)
        u = top_of(r)
        if u: r["top"] = u["e"]

# ------------------------------------------------------------------ adjacency (shared arcs, overlapping time) among leaves
arc_users = defaultdict(list)
leaf_recs = [r for r in recs if ents[r["e"]]["k"] == 0]
for ri, r in enumerate(leaf_recs):
    for poly in geoms[r["g"]]:
        for ring in poly:
            for a in ring: arc_users[a if a >= 0 else ~a].append(ri)
group = lambda r: r["top"] if r["top"] >= 0 else r["e"]
gadj, madj = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
garea = defaultdict(float)
for r in leaf_recs: garea[group(r)] += r["area"] * (r["t"] - r["f"] + 1)
for a, users in arc_users.items():
    if len(users) < 2 or len(users) > 400: continue
    w = len(arc_pts[a])
    for i in range(len(users)):
        A = leaf_recs[users[i]]
        for j in range(i + 1, len(users)):
            B = leaf_recs[users[j]]
            if A["e"] == B["e"] or not (A["f"] <= B["t"] and B["f"] <= A["t"]): continue
            ga, gb = group(A), group(B)
            if ga != gb: gadj[ga][gb] += w; gadj[gb][ga] += w
            else: madj[(ga, A["e"])][(gb, B["e"])] += w; madj[(gb, B["e"])][(ga, A["e"])] += w

# ------------------------------------------------------------------ colours
v = json.load(open("../../data/world_history_timeline_v4_5.json"))
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower().replace("the ", "")).strip()
EMP_ALIAS = {
    "roman_empire": ["Roman Empire"], "roman_republic": ["Roman Republic"], "western_roman_empire": ["Western Roman Empire"],
    "persian_empire": ["Achaemenid Empire"], "macedonian_empire": ["Macedonian Empire"], "byzantine_empire": ["Byzantine Empire"],
    "arab_caliphate": ["Rashidun Caliphate", "Umayyad Caliphate"], "abbasid_caliphate": ["Abbasid Caliphate"], "ottoman_empire": ["Ottoman Empire"],
    "mongol_empire": ["Mongol Empire", "Golden Horde", "Ilkhanate", "Yuan Dynasty"], "safavid_empire": ["Safavid Dynasty"],
    "holy_roman_empire": ["Holy Roman Empire"], "inca_empire": ["Inca Empire"], "mughal_empire": ["Mughal Empire"], "maurya_empire": ["Maurya Empire"],
    "qing_dynasty": ["Qing Dynasty"], "seleucid_empire": ["Seleucid Empire"], "parthian_empire": ["Parthian Empire"], "sasanian_empire": ["Sasanian Empire"],
    "khmer_empire": ["Khmer Empire"], "kievan_rus": ["Kievan Rus'"], "russian_empire": ["Russian Empire"], "soviet_union": ["Union of Soviet Socialist Republics"],
    "frankish_realm": ["Kingdom of the Franks"], "polish_lithuanian_commonwealth": ["Polish-Lithuanian Commonwealth"],
    "grand_duchy_lithuania": ["Grand Duchy of Lithuania"], "habsburg_monarchy": ["Habsburg Monarchy", "Austrian Empire", "Austria-Hungary"],
    "japanese_empire": ["Empire of Japan"], "kalmar_union": ["Kalmar Union"], "republic_of_venice": ["Republic of Venice"],
    "hungarian_crown": ["Kingdom of Hungary"], "delhi_sultanate": ["Delhi Sultanate"],
}
name2emp = {n: eid for eid, ns in EMP_ALIAS.items() for n in ns}
# poster colours for the big empires (kept in sync with EMP_COLOR in the page)
import subprocess
tpl = open("../site-template.html", encoding="utf-8").read()
emp_block = tpl.split("const EMP_COLOR = {")[1].split("};")[0]
EMP_COLOR = dict(re.findall(r'(\w+):\s*"(#[0-9a-fA-F]{6})"', emp_block))
for e in ents:
    e["emp"] = name2emp.get(e["label"], "")

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
def rgb2hex(c): return "#" + "".join(f"{max(0, min(255, round(x * 255))):02x}" for x in c)
def shade(h, k):   # k in -1..1: darker / lighter, keeping hue
    r, g, b = hex2rgb(h); hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = ll + (1 - ll) * k * 0.55 if k > 0 else ll * (1 + k * 0.35)
    return rgb2hex(colorsys.hls_to_rgb(hh, ll, ss))

def lab(h):
    r, g, b = hex2rgb(h)
    f = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
    r, g, b = f(r), f(g), f(b)
    X, Y, Z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    t = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return (116 * t(Y) - 16, 500 * (t(X) - t(Y)), 200 * (t(Y) - t(Z)))
def dE(a, b): A, B = lab(a), lab(b); return math.dist(A, B)
sim = lambda a, b: max(0.0, 1 - dE(a, b) / 42)
gcol = {}
for gi_ in sorted(garea, key=lambda g: -garea[g]):
    emp = ents[gi_]["emp"]
    if emp and emp in EMP_COLOR: gcol[gi_] = EMP_COLOR[emp]; continue
    cost = defaultdict(float)
    for nb, w in gadj[gi_].items():
        if nb in gcol:
            for c in PATCH: cost[c] += w * sim(c, gcol[nb])
    h = 2166136261
    for ch in ents[gi_]["n"]: h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    order = PATCH[h % len(PATCH):] + PATCH[:h % len(PATCH)]
    gcol[gi_] = min(order, key=lambda c: cost[c])
SHADES = [0, 0.3, -0.24, 0.52]
mshade = {}
for key in sorted({(group(r), r["e"]) for r in leaf_recs if r["top"] >= 0}, key=lambda k: -sum(q["area"] for q in by_name[ents[k[1]]["n"]])):
    cost = defaultdict(float)
    for nb, w in madj[key].items():
        if nb in mshade: cost[mshade[nb]] += w
    mshade[key] = min(range(len(SHADES)), key=lambda s: (cost[s], s))
colors, cidx = [], {}
def soften(h, k=0.1):   # a touch of paper in every fill keeps the map calm
    r, g, b = hex2rgb(h); P = (0.984, 0.98, 0.965)
    return rgb2hex((r + (P[0] - r) * k, g + (P[1] - g) * k, b + (P[2] - b) * k))
def col_id(h):
    if h not in cidx: cidx[h] = len(colors); colors.append(h)
    return cidx[h]
for r in recs:
    k = ents[r["e"]]["k"]
    if k == 0:
        base = gcol.get(group(r), PATCH[0])
        r["c"] = col_id(soften(shade(base, SHADES[mshade[(group(r), r["e"])]]) if r["top"] >= 0 else base))
    elif k == 1:
        h_ = gcol.get(r["e"], gcol.get(r["top"], "#888888")); rr, gg, bb = hex2rgb(h_); hh, ll, ss = colorsys.rgb_to_hls(rr, gg, bb)
        r["c"] = col_id(rgb2hex(colorsys.hls_to_rgb(hh, ll * 0.48, min(1, ss * 0.9))))   # darker outline colour
    else: r["c"] = col_id("#555555")

# ------------------------------------------------------------------ poster links and peaks
periods = [(norm(p["name"]), p["id"], p["start"], p["end"] if p["end"] is not None else 2027) for t in v["tracks"] for p in t["periods"]]
for i, e in enumerate(ents):
    k = norm(e["label"])
    e["pp"] = [pid for (pn, pid, ps, pe) in periods if pn == k and ps <= e["t"] and e["f"] < pe]
    rs = by_name[e["n"]]
    pk = max(rs, key=lambda q: q["area"]) if rs else None
    e["py"] = pk["f"] if pk else e["f"]

# ------------------------------------------------------------------ modern-country aliases (Natural Earth names -> polity in 2024)
ne = json.load(open("ne_countries_proj.geojson"))["features"]
alias = defaultdict(set)
leaf2024 = [(r, shape(FULL_IDX)) for r, FULL_IDX in []]
cands = [r for r in leaf_recs if r["t"] >= 2024]
cand_shapes = []
for r in cands:
    polys = []
    for poly in geoms[r["g"]]:
        rings = [[(x / GRID, y / GRID) for x, y in ring_coords(rg)] for rg in poly]
        try: polys.append(Polygon(rings[0], rings[1:]))
        except Exception: pass
    g = make_valid(MultiPolygon([p for p in polys if p.is_valid] or polys)) if polys else None
    cand_shapes.append(g)
for f in ne:
    nm = f["properties"]["name"]
    g = shape(f["geometry"])
    if g.is_empty: continue
    lp = largest_poly(g); pt = lp.representative_point() if lp else g.representative_point()
    for r, sg in zip(cands, cand_shapes):
        if sg is not None and sg.contains(pt):
            if norm(nm) != norm(ents[r["e"]]["label"]): alias[r["e"]].add(nm)
            break
for i, s in alias.items(): ents[i]["al"] = sorted(s)

# ------------------------------------------------------------------ merge consecutive identical records
recs.sort(key=lambda r: (r["e"], r["f"]))
merged = []
for r in recs:
    m = merged[-1] if merged else None
    if m and m["e"] == r["e"] and m["g"] == r["g"] and m["t"] + 1 >= r["f"] and m["mem"] == r["mem"] and m["top"] == r["top"] and m["c"] == r["c"]:
        m["t"] = max(m["t"], r["t"]); m["comp"] = sorted(set(m["comp"]) | set(r["comp"]))
    else: merged.append(dict(r))
recs = merged

# ------------------------------------------------------------------ encode (varint streams, arc refs run-length coded, gzip)
import gzip
def rle_ring(vs, ring):
    R = []; i = 0
    while i < len(ring):
        st = ring[i]; d = 0; n = 1
        if i + 1 < len(ring) and abs(ring[i + 1] - st) == 1:
            d = ring[i + 1] - st
            while i + n < len(ring) and ring[i + n] == st + d * n: n += 1
        R.append((st, n, d)); i += n
    vs.u(len(R)); prev = 0
    for st, n, d in R: vs.i(st - prev); vs.u((n - 1) * 2 + (1 if d < 0 else 0)); prev = st + d * (n - 1)
def geoms_stream(glist):
    vs = VS(); vs.u(len(glist))
    for arcs in glist:
        vs.u(len(arcs))
        for poly in arcs:
            vs.u(len(poly))
            for ring in poly: rle_ring(vs, ring)
    return vs
vs = VS(); vs.u(len(arc_pts)); px = py = 0
for pts in arc_pts:
    vs.u(len(pts))
    for x, y in pts: vs.i(x - px); vs.i(y - py); px, py = x, y
lpolys = []
for g in T["objects"]["l"]["geometries"]:
    if g.get("arcs"): lpolys += g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
z = lambda b: base64.b64encode(gzip.compress(bytes(b), 9)).decode()

out_ents = []
for e in ents:
    o = {"n": e["label"], "k": e["k"], "f": e["f"], "t": e["t"], "py": e["py"]}
    for k in ("wp", "wd", "sid", "emp"):
        if e.get(k): o[k] = e[k]
    if e["pp"]: o["pp"] = e["pp"]
    if e.get("al"): o["al"] = e["al"]
    out_ents.append(o)
R = []
for r in recs:
    lx, ly, lr = glabel[r["g"]]
    mem = [eidx[m] for m in r["mem"] if m in eidx]
    comp = [eidx[c] for c in r["comp"] if c in eidx]
    R.append([r["e"], r["f"], r["t"], r["g"], r["c"], round(lx, 1), round(ly, 1), round(lr, 1), r["area"], r["top"], mem, comp, 1 if r.get("trivial") else 0])
meta = {"gcol": {str(k): v for k, v in gcol.items()}, "q": Q, "grid": GRID, "gbox": [[round(c) for c in b] for b in gbbox], "colors": colors, "ents": out_ents, "recs": R}
mj = json.dumps(meta, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
out = {"src": {"name": "Cliopatria", "version": "0.2.1", "commit": "5f43337", "licence": "CC BY 4.0",
               "url": "https://github.com/Seshat-Global-History-Databank/cliopatria"},
       "arcs": z(vs.b), "geoms": z(geoms_stream(geoms).b), "land": z(geoms_stream([lpolys]).b), "meta": z(mj)}
s = json.dumps(out, separators=(",", ":"))
open("map2.json", "w", encoding="utf-8").write(s)
print(f"arcs={len(arc_pts):,} pts={sum(len(a) for a in arc_pts):,} geoms={len(geoms):,} recs={len(R):,} ents={len(ents):,} colours={len(colors)} "
      f"aliases={sum(len(x) for x in alias.values())} " + " ".join(f"{k}={len(out[k])/1e6:.2f}MB" for k in ("arcs","geoms","land","meta")) + f" total={len(s)/1e6:.2f}MB")
