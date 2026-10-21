"""Population per historical state, from the HYDE 3.3 population grid.
For every Cliopatria shape (states and empires; not relations), sum the people of the HYDE grid cells
(5 arc-minutes, about 9 km) whose centre lies inside the shape, at each available HYDE date.
Output popgrid.json: dates, and for each map record the sums at the HYDE dates that bracket its years.
Usage: python3 build_popgrid.py <dir with popc_<year>.asc files>   [--test: synthetic grid, for development only]"""
import json, gzip, base64, math, re, sys, time
from pathlib import Path
import numpy as np
import shapely
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid

M = json.load(open("map2.json"))
def gun(b): return gzip.decompress(base64.b64decode(b))
class R:
    def __init__(s, b): s.b, s.i = b, 0
    def u(s):
        v = 0; sh = 0
        while True:
            c = s.b[s.i]; s.i += 1; v |= (c & 127) << sh; sh += 7
            if not c & 128: return v
    def z(s): v = s.u(); return -(v + 1) // 2 if v & 1 else v // 2
meta = json.loads(gun(M["meta"])); G = meta["grid"]
ar = R(gun(M["arcs"])); arcs = []; x = y = 0
for _ in range(ar.u()):
    pts = []
    for _ in range(ar.u()): x += ar.z(); y += ar.z(); pts.append((x / G, y / G))
    arcs.append(pts)
gr = R(gun(M["geoms"])); geoms = []
for _ in range(gr.u()):
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
            ps += [p] if p.geom_type == "Polygon" else [q for q in getattr(p, "geoms", []) if q.geom_type == "Polygon"]
        except Exception: pass
    return MultiPolygon(ps) if ps else None
ents = meta["ents"]
recs = [dict(zip("e f t g c lx ly lr area top mem comp triv".split(), r)) for r in meta["recs"]]

# ------------------------------------------------------------------ the grid
A1, A2, A3, A4, MM = 1.340264, -0.081106, 0.000893, 0.003796, math.sqrt(3) / 2
def proj(lon, lat):   # Equal Earth, same as the site (vectorised)
    l, p = np.radians(lon), np.radians(lat); t = np.arcsin(MM * np.sin(p)); t2 = t * t; t6 = t2 * t2 * t2
    return l * np.cos(t) / (MM * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))) * 1000, -t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)) * 1000
def read_asc(p):
    with open(p, "rb") as f:
        hdr = {}
        for _ in range(6):
            k, v = f.readline().split(); hdr[k.decode().lower()] = float(v)
        a = np.array(f.read().split(), dtype=np.float32)
    a = a.reshape(int(hdr["nrows"]), int(hdr["ncols"])); a[a < 0] = 0
    return a, hdr
def year_of(name):   # popc_1000AD.asc -> 1000, popc_3000BC.asc -> -3000
    m = re.search(r"(\d+)(AD|BC)", name); v = int(m.group(1)); return -v if m.group(2) == "BC" else v

TEST = "--test" in sys.argv
if TEST:   # development only: spread HYDE country totals evenly over each country's cells (the assumption this file exists to remove)
    scr = Path(__import__("os").environ.get("HYDE_DIR", "downloads"))
    iso, hdr = read_asc(scr / "hyde_gen/iso_cr.asc"); area, _ = read_asc(scr / "hyde_gen/garea_cr.asc")
    L = [l.split() for l in open(scr / "hyde_txt/popc_c.txt")]; yrs = [int(v) for v in L[0][1:]]
    rows = {int(float(r[0])): [float(v) for v in r[1:]] for r in L[1:] if r[0] != "Total"}
    dates = [-3000, -1000, 0, 500, 1000, 1300, 1500, 1700, 1800, 1900, 2000, 2020]
    codes = iso.astype(np.int32); tot_area = np.bincount(codes.ravel(), weights=area.ravel())
    grids = []
    for d in dates:
        k = yrs.index(d); per = np.zeros(tot_area.shape[0])
        for c, v in rows.items():
            if c < per.shape[0] and tot_area[c] > 0: per[c] = v[k] / tot_area[c]
        grids.append((per[codes] * area).astype(np.float32))
else:
    files = sorted(Path(sys.argv[1]).glob("popc_*.asc"), key=lambda p: year_of(p.name))
    dates = [year_of(p.name) for p in files]; grids = []
    for p in files:
        t0 = time.time(); g, hdr = read_asc(p); grids.append(g); print("read", p.name, f"{g.sum()/1e6:.1f} M people", f"{time.time()-t0:.0f}s")
nr, nc = grids[0].shape; cs = hdr["cellsize"]
stack = np.stack(grids)                                   # dates x rows x cols
popd = stack.reshape(len(dates), -1)
keep = np.nonzero(popd.max(axis=0) > 0)[0]                # cells with people at some date
rr, cc = np.divmod(keep, nc)
lon = hdr["xllcorner"] + (cc + 0.5) * cs; lat = hdr["yllcorner"] + (nr - rr - 0.5) * cs
X, Y = proj(lon, lat); P = popd[:, keep].T.astype(np.float64)   # cells x dates
print(f"{len(dates)} dates, {len(keep):,} populated cells, world {[round(v/1e6) for v in P.sum(0)]} M")
# coarse bins for fast bounding-box lookups
B = 40.0; bx = np.floor(X / B).astype(np.int32); by = np.floor(Y / B).astype(np.int32)
order = np.lexsort((bx, by)); bxs, bys = bx[order], by[order]; keys = (bys.astype(np.int64) << 20) + (bxs + 1000)
def candidates(b):
    x0, y0, x1, y1 = b; out = []
    for yy in range(int(math.floor(y0 / B)), int(math.floor(y1 / B)) + 1):
        k0 = (np.int64(yy) << 20) + int(math.floor(x0 / B)) + 1000; k1 = (np.int64(yy) << 20) + int(math.floor(x1 / B)) + 1000
        i0, i1 = np.searchsorted(keys, k0, "left"), np.searchsorted(keys, k1, "right")
        if i1 > i0: out.append(order[i0:i1])
    return np.concatenate(out) if out else np.zeros(0, dtype=np.int64)

need = sorted({r["g"] for r in recs if ents[r["e"]]["k"] in (0, 1)})
sums = {}; t0 = time.time()
for n, gi in enumerate(need):
    g = geom_shape(gi)
    if g is None or g.is_empty: sums[gi] = np.zeros(len(dates)); continue
    idx = candidates(g.bounds)
    if len(idx): shapely.prepare(g); inside = shapely.contains_xy(g, X[idx], Y[idx]); sums[gi] = P[idx[inside]].sum(0)
    else: sums[gi] = np.zeros(len(dates))
    if n % 1000 == 0: print(f"  {n}/{len(need)} shapes, {time.time()-t0:.0f}s")

def sig3(v):
    if v <= 0: return 0
    k = int(math.floor(math.log10(v))) - 2
    return int(round(v / 10 ** k) * 10 ** k) if k > 0 else int(round(v))
out_r = []
for r in recs:
    if ents[r["e"]]["k"] not in (0, 1): out_r.append(None); continue
    i0 = max([i for i, d in enumerate(dates) if d <= r["f"]] or [0]); i1 = min([i for i, d in enumerate(dates) if d >= r["t"]] or [len(dates) - 1])
    out_r.append([i0] + [sig3(v) for v in sums[r["g"]][i0:i1 + 1]])
out = {"y": dates, "r": out_r, "test": TEST,
       "src": "HYDE 3.3 population grid (popc, 5 arc-minutes, base scenario), Klein Goldewijk et al., Utrecht University; borders from Cliopatria v0.2.1",
       "method": "People in grid cells whose centre lies inside a state's recorded borders, summed at each HYDE date; between dates the site interpolates."}
s = json.dumps(out, separators=(",", ":")); open("popgrid.json", "w").write(s)
print(f"done: {len(need)} shapes in {time.time()-t0:.0f}s, popgrid.json {len(s)/1e3:.0f} KB{' (TEST DATA)' if TEST else ''}")
