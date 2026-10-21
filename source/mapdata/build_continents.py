"""Continent outlines for the map's 'one continent' filter.
Natural Earth 1:50m countries (public domain), continent from ISO codes (countries-list, MIT).
Europe and Asia meet along the usual line: the crest of the Urals, the Ural River and the Caspian (through Russia and
Kazakhstan), the Bosphorus and the Dardanelles (Turkey), and the Suez Canal (Egypt: Sinai is in Asia). Far-flung islands
follow the nearest mainland country, with exceptions where that rule goes wrong (Svalbard, Greenland, eastern Indonesia).
Revised 21 October 2026; v0.1 cut Russia along the 60°E meridian."""
import json, math, base64, gzip
from collections import defaultdict
from shapely.geometry import shape, box, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

exec(open("build_map.py").read().split("def project_geom")[0].replace("TOL = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5", "TOL=1"))
NAMES = {"AF": "Africa", "EU": "Europe", "AS": "Asia", "NA": "North America", "SA": "South America", "OC": "Oceania", "AN": "Antarctica"}
FIX = {"Somaliland": "AF", "Kosovo": "EU", "N. Cyprus": "EU", "Indian Ocean Ter.": "OC", "Siachen Glacier": "AS"}
fc = json.load(open("topo/ne_countries_cont.geojson"))["features"]
def polys(g):
    g = shape(g)
    if not g.is_valid: g = make_valid(g)
    return [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
# west of this line is Europe (lon, lat): Kara Sea east of Novaya Zemlya, the crest of the Urals, the Ural River, the Caspian
URALS = [(70, 90), (70, 77), (68, 71), (66.5, 68.6), (64.8, 67.3), (62.0, 65.9), (59.5, 65.0), (59.2, 63.9), (59.3, 61.5), (59.6, 59.6),
         (59.8, 57.5), (59.6, 55.8), (59.4, 54.5), (59.0, 53.4), (58.6, 51.3), (57.0, 51.2), (55.1, 51.8), (53.0, 51.6), (51.4, 51.2),
         (51.6, 49.5), (51.9, 47.1), (51.8, 46.8), (50.0, 44.0), (49.0, 40.0), (49.0, -90)]
EUROPE_SIDE = Polygon(URALS + [(-400, -90), (-400, 90)])
# east of this line is Asia (lon, lat): the Suez Canal and the axis of the Gulf of Suez
SINAI = Polygon([(32.3, 31.7), (32.3, 31.3), (32.35, 30.6), (32.55, 29.95), (32.75, 29.6), (33.05, 29.0), (33.35, 28.5), (33.55, 28.1), (33.8, 27.8),
                 (34.2, 27.55), (34.6, 27.0), (35.5, 26.0), (37, 26.0), (37, 31.7)])
SPLIT = {"Kazakhstan": lambda g: [("EU", g.intersection(EUROPE_SIDE)), ("AS", g.difference(EUROPE_SIDE))],
         "Egypt": lambda g: [("AS", g.intersection(SINAI)), ("AF", g.difference(SINAI))]}
def island_rule(name, p):   # may this far-flung island take the nearest mainland's continent?
    if name in ("Norway", "Greenland"): return False                      # Svalbard is Europe; south Greenland's islands are North America
    if name == "Indonesia": return p.centroid.x >= 135                    # western New Guinea is Oceania; the Moluccas and Timor stay in Asia
    if name == "United States of America": return p.centroid.y < 30       # Hawaii is Oceania; the Aleutians stay in North America
    return True
mains = []          # (centroid, continent) of each country's main polygon
items = []          # (polygon in lon/lat, country continent, main centroid)
for f in fc:
    if not f["geometry"]: continue
    c = f["properties"].get("cont") or FIX.get(f["properties"]["name"])
    ps = polys(f["geometry"])
    if not ps or not c: continue
    if f["properties"]["name"] == "Russia":
        raw = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
        for poly in raw:
            p = Polygon(fix_ring(poly[0]), [fix_ring(r) for r in poly[1:]]).buffer(0)   # unwrap rings that cross the date line (before any repair)
            if p.is_empty: continue
            if p.centroid.x < 0 or p.centroid.x > 180: items.append((p, "AS", None)); continue      # Chukotka beyond the date line
            for cc, q in (("EU", p.intersection(EUROPE_SIDE)), ("AS", p.difference(EUROPE_SIDE))):
                for qq in ([q] if q.geom_type == "Polygon" else [x for x in getattr(q, "geoms", []) if x.geom_type == "Polygon"]):
                    if qq.area > 0: items.append((qq, cc, None))
        continue
    main = max(ps, key=lambda p: p.area); mc = main.centroid
    mains.append((mc, c)); nm = f["properties"]["name"]
    if nm == "Turkey":   # Eastern Thrace and Gökçeada are in Europe
        for p in ps: items.append((p, "EU" if p.centroid.x < 29.2 and p.centroid.y > 40 else "AS", None))
        continue
    if nm in SPLIT:
        for p in ps:
            for cc, q in SPLIT[nm](p):
                for qq in ([q] if q.geom_type == "Polygon" else [x for x in getattr(q, "geoms", []) if x.geom_type == "Polygon"]):
                    if qq.area > 0: items.append((qq, cc, None))
        continue
    for p in ps: items.append((p, c, mc if island_rule(nm, p) else None))
def dist_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a.y, a.x, b.y, b.x))
    return 6371 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
groups = defaultdict(list)
for p, c, mc in items:
    if mc is not None and dist_km(p.centroid, mc) > 1500:
        pc = p.centroid; c = min(mains, key=lambda m: dist_km(pc, m[0]))[1]
    groups[c].append(p)
out = {}
for c, ps in groups.items():
    proj_polys = []
    for p in ps:
        rings = [[proj(x, y) for x, y in fix_ring(list(r.coords))] for r in [p.exterior] + list(p.interiors)]
        try:
            q = Polygon(rings[0], rings[1:]).buffer(0)
            if not q.is_empty: proj_polys.append(q)
        except Exception: pass
    u = unary_union(proj_polys).simplify(2.0, preserve_topology=True)
    parts = [u] if u.geom_type == "Polygon" else list(u.geoms)
    parts = [q for q in parts if q.area > 2]
    total = sum(q.area for q in parts)
    big = [q for q in parts if q.area > total * 0.02]
    bx = [min(q.bounds[0] for q in big), min(q.bounds[1] for q in big), max(q.bounds[2] for q in big), max(q.bounds[3] for q in big)]
    flat = []
    for q in parts:
        for r in [q.exterior] + list(q.interiors):
            flat.append([round(v, 1) for xy in r.coords for v in xy])
    out[NAMES[c]] = {"box": [round(v, 1) for v in bx], "rings": flat}
s = json.dumps({"src": "Natural Earth 1:50m countries (public domain); continents from countries-list (MIT)", "c": out}, separators=(",", ":"))
open("continents.json", "w").write(s)
print({k: (len(v["rings"]), sum(len(r) for r in v["rings"]) // 2) for k, v in out.items()}, f"{len(s)/1e3:.0f} KB")
