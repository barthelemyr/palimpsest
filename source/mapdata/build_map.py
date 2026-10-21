"""Builds map.json for the Palimpsest map view from Cliopatria v0.2.1 (CC BY 4.0)
and Natural Earth land (public domain). Geometry is projected (Equal Earth),
simplified and delta-encoded as Int16, base64."""
import json, math, re, base64, hashlib, sys
from array import array
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.validation import make_valid

TOL = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5   # in projected units x1000
Q = 1000.0
A1, A2, A3, A4, M = 1.340264, -0.081106, 0.000893, 0.003796, math.sqrt(3) / 2

def proj(lon, lat):
    l, p = math.radians(lon), math.radians(max(-89.999, min(89.999, lat)))
    t = math.asin(M * math.sin(p)); t2 = t * t; t6 = t2 * t2 * t2
    x = l * math.cos(t) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x * Q, -y * Q

def fix_ring(r):
    jumps = [i for i in range(1, len(r)) if abs(r[i][0] - r[i - 1][0]) > 180]
    if not jumps: return r
    lats = [q[1] for q in r]
    if len(jumps) % 2 == 1:          # ring encloses a pole: close it along the pole edge
        pole = -90 if min(lats) < -50 else 90
        i = jumps[0]; a, b = r[i - 1], r[i]
        sa = 180 if a[0] > 0 else -180
        edge = [[sa, a[1]], [sa, pole], [-sa, pole], [-sa, b[1]]]
        return r[:i] + edge + r[i:]
    out, off = [list(r[0])], 0                    # crosses the antimeridian: unwrap only past each crossing
    for i in range(1, len(r)):
        d = r[i][0] - r[i - 1][0]
        if d > 180: off -= 360
        elif d < -180: off += 360
        out.append([r[i][0] + off, r[i][1]])
    mean = sum(q[0] for q in out) / len(out)          # keep the bulk of the shape inside the map
    shift = -360 if mean > 180 else 360 if mean < -180 else 0
    return [[q[0] + shift, q[1]] for q in out] if shift else out

def project_geom(g):
    def ring(r): return [proj(x, y) for x, y in fix_ring(r)]
    if g["type"] == "Polygon": polys = [g["coordinates"]]
    else: polys = g["coordinates"]
    out = []
    for poly in polys:
        rs = [ring(r) for r in poly if len(r) >= 4]
        if not rs: continue
        try: out.append(Polygon(rs[0], rs[1:]))
        except Exception: pass
    return out

def clean(polys):
    geoms = []
    for p in polys:
        if not p.is_valid: p = make_valid(p)
        if p.geom_type == "Polygon": geoms.append(p)
        elif hasattr(p, "geoms"): geoms += [q for q in p.geoms if q.geom_type == "Polygon"]
    return geoms

def encode(polys, tol, min_area):
    simp = []
    for p in polys:
        s = p.simplify(tol, preserve_topology=True)
        if s.is_empty: continue
        for q in ([s] if s.geom_type == "Polygon" else [g for g in getattr(s, "geoms", []) if g.geom_type == "Polygon"]):
            simp.append(q)
    if not simp: return None, None
    simp.sort(key=lambda q: -q.area)
    keep = [simp[0]] + [q for q in simp[1:] if q.area >= min_area]
    arr = array("h", [len(keep)])
    for q in keep:
        rings = [q.exterior] + [r for r in q.interiors if Polygon(r).area >= min_area * 2]
        arr.append(len(rings))
        for r in rings:
            pts = [(int(round(x)), int(round(y))) for x, y in r.coords]
            ded = [pts[0]] + [pts[k] for k in range(1, len(pts)) if pts[k] != pts[k - 1]]
            if len(ded) < 4: ded = (ded * 4)[:4]
            arr.append(len(ded))
            px, py = 0, 0
            for k, (x, y) in enumerate(ded):
                if k == 0: arr.append(x); arr.append(y)
                else: arr.append(x - px); arr.append(y - py)
                px, py = x, y
    lp = keep[0].representative_point()
    return arr, (int(round(lp.x)), int(round(lp.y)))

# ------------------------------------------------------------------ poster links
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
    "hungarian_crown": ["Kingdom of Hungary"], "delhi_sultanate": ["(Delhi Sultanate)"],
}
name2emp = {}
for eid, names in EMP_ALIAS.items():
    for n in names: name2emp.setdefault(n, eid)

periods = []
for t in v["tracks"]:
    for p in t["periods"]:
        periods.append((norm(p["name"]), p["id"], p["start"], p["end"] if p["end"] is not None else 2027))

# ------------------------------------------------------------------ cliopatria
src = json.load(open("raw/cliopatria_polities_only_v021.geojson"))["features"]
ents, eidx = [], {}
def ent(props):
    n = props["Name"]
    if n not in eidx:
        eidx[n] = len(ents)
        ents.append({"n": n, "wp": props.get("Wikipedia") or "", "wd": props.get("Wikidata") or "", "sid": props.get("SeshatID") or "",
                     "f": props["FromYear"], "t": props["ToYear"]})
    e = ents[eidx[n]]
    e["f"] = min(e["f"], props["FromYear"]); e["t"] = max(e["t"], props["ToYear"])
    for k, pk in (("wp", "Wikipedia"), ("wd", "Wikidata"), ("sid", "SeshatID")):
        if not e[k] and props.get(pk): e[k] = props[pk]
    return eidx[n]

geoms, gkey, recs = [], {}, []
n_in = n_out = 0
for f in src:
    pr = f["properties"]
    ei = ent(pr)
    polys = clean(project_geom(f["geometry"]))
    n_in += sum(len(p.exterior.coords) for p in polys)
    arr, lp = encode(polys, TOL, (TOL * 3) ** 2)
    if arr is None: continue
    k = hashlib.md5(arr.tobytes()).hexdigest()
    if k not in gkey: gkey[k] = len(geoms); geoms.append(arr); n_out += len(arr) // 2
    recs.append([ei, pr["FromYear"], pr["ToYear"], 1 if pr["Type"] == "RELATION" else 0, gkey[k], lp[0], lp[1], round(pr.get("Area") or 0),
                 pr.get("MemberOf") or "", pr.get("Components") or ""])
# member/components to indices
for r in recs:
    r[8] = eidx.get(r[8], -1) if r[8] else -1
    r[9] = [eidx[c] for c in r[9].split(";") if c in eidx] if r[9] else []
for e in ents:
    e["emp"] = name2emp.get(e["n"], "")
    k = norm(e["n"])
    e["pp"] = [pid for (pn, pid, ps, pe) in periods if pn == k and ps <= e["t"] and e["f"] < pe]

# ------------------------------------------------------------------ land
land = json.load(open("land50.geojson"))
lpolys = []
for ft in land["features"]:
    lpolys += clean(project_geom(ft["geometry"]))
land_arrs = []
for p in lpolys:
    arr, _ = encode([p], 3.0, 36)
    if arr is not None and p.area > 150: land_arrs.append(arr)

def pack(arrs):
    flat, offs = array("h"), []
    for a in arrs: offs.append(len(flat)); flat.extend(a)
    return base64.b64encode(flat.tobytes()).decode(), offs

g64, goffs = pack(geoms)
l64, loffs = pack(land_arrs)
out = {"src": {"name": "Cliopatria", "version": "0.2.1", "commit": "5f43337", "licence": "CC BY 4.0",
               "url": "https://github.com/Seshat-Global-History-Databank/cliopatria",
               "credit": "Bennett, J. S. et al. Cliopatria: a geospatial database of world-wide political entities from 3400BCE to 2024CE. Seshat Global History Databank."},
       "q": Q, "ents": ents, "recs": recs, "g": g64, "go": goffs, "land": l64, "lo": loffs}
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("map.json", "w", encoding="utf-8").write(s)
linked = sum(1 for e in ents if e["pp"]); emps = sum(1 for e in ents if e["emp"])
print(f"tol={TOL} vertices in={n_in:,} out={n_out:,} geoms={len(geoms):,} recs={len(recs):,} ents={len(ents):,} "
      f"linked_to_poster={linked} empire_links={emps} land_polys={len(land_arrs)} size={len(s)/1e6:.2f} MB")
