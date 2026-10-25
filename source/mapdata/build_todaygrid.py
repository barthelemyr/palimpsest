"""Today's country at any point of the map: a lookup grid of Natural Earth 1:50m countries (public domain),
in the map's own units (Equal Earth x1000, y pointing down), so the browser finds the country under a click
with one array read, without polygons.

Each cell holds the country that contains its centre (0 = sea or no country). A country too small to hold
any cell centre (a city state, a small island) still gets the cell under its representative point.
Encoding: row-major runs (value, length) as varints, gzip, base64.

Input (cwd = mapdata/): ne_countries_proj.geojson (step 1, project_all.py)
Output: todaygrid.json {cell, x0, y0, w, h, names, runs, src}
Usage: python3 build_todaygrid.py [cell size in map units, default 1.5 = about 10 km]"""
import json, sys, math, gzip, base64
import numpy as np
import shapely
from shapely.geometry import shape
from shapely.validation import make_valid

CELL = float(sys.argv[1]) if len(sys.argv) > 1 else 1.5
SHORT = {"United States of America": "United States", "Dem. Rep. Congo": "DR Congo"}   # same names as build_network.py

feats = json.load(open("ne_countries_proj.geojson"))["features"]
geoms, names = [], []
for f in feats:
    g = shape(f["geometry"])
    if not g.is_valid: g = make_valid(g)
    if g.is_empty: continue
    geoms.append(g); names.append(SHORT.get(f["properties"]["name"], f["properties"]["name"]))

x0, y0, x1, y1 = shapely.total_bounds(geoms)
x0, y0 = math.floor(x0 / CELL) * CELL, math.floor(y0 / CELL) * CELL
w, h = math.ceil((x1 - x0) / CELL), math.ceil((y1 - y0) / CELL)
grid = np.zeros((h, w), dtype=np.uint16)
order = sorted(range(len(geoms)), key=lambda i: -geoms[i].area)   # small countries last, so enclaves win over their surroundings
for i in order:
    g = geoms[i]; shapely.prepare(g)
    bx0, by0, bx1, by1 = g.bounds
    c0, c1 = max(0, int((bx0 - x0) / CELL)), min(w - 1, int((bx1 - x0) / CELL))
    r0, r1 = max(0, int((by0 - y0) / CELL)), min(h - 1, int((by1 - y0) / CELL))
    xs = x0 + (np.arange(c0, c1 + 1) + 0.5) * CELL; ys = y0 + (np.arange(r0, r1 + 1) + 0.5) * CELL
    X, Y = np.meshgrid(xs, ys)
    inside = shapely.contains_xy(g, X, Y)
    if not inside.any():   # too small for any cell centre
        p = g.representative_point(); grid[int((p.y - y0) / CELL), int((p.x - x0) / CELL)] = i + 1; continue
    sub = grid[r0:r1 + 1, c0:c1 + 1]; sub[inside] = i + 1

def varint(v, out):
    while True:
        b = v & 127; v >>= 7
        if v: out.append(b | 128)
        else: out.append(b); return

flat = grid.ravel(); out = bytearray()
change = np.flatnonzero(np.diff(flat)) + 1
starts = np.concatenate([[0], change]); ends = np.concatenate([change, [flat.size]])
for s, e in zip(starts, ends): varint(int(flat[s]), out); varint(int(e - s), out)
runs = base64.b64encode(gzip.compress(bytes(out), 9)).decode()
res = {"cell": CELL, "x0": round(x0, 3), "y0": round(y0, 3), "w": w, "h": h, "names": names, "runs": runs,
       "src": "Natural Earth 1:50m admin-0 countries (public domain), via world-atlas 2.0.2; country containing each cell centre"}
s = json.dumps(res, ensure_ascii=False, separators=(",", ":"))
open("todaygrid.json", "w", encoding="utf-8").write(s)
missing = len(names) - len(set(int(v) for v in np.unique(grid)) - {0})
print(f"cell {CELL}: {w} x {h}, {len(starts):,} runs, {len(names)} countries ({missing} without a cell), todaygrid.json {len(s) / 1e3:.0f} KB")
