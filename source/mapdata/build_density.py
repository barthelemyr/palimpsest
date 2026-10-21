"""Population density layer: HYDE 3.3 population grids (popc, 5 arc-minutes) aggregated to 0.5 degree cells,
divided by land area (HYDE maxln_cr), stored as one byte per land cell and date on a log scale.
q = 0 below 0.1 people/km2, else 1 + round((log10(density) + 1) * 38), capped at 255.
Output density.json: {w, h, y: dates, mask: gzip+base64 bitset of land cells (row-major from the north), q: gzip+base64 bytes (date-major)}.
Usage: python3 build_density.py <dir with popc_<year>.asc> <maxln_cr.asc>"""
import json, gzip, base64, re, sys, math
from pathlib import Path
import numpy as np

def read_asc(p):
    with open(p, "rb") as f:
        hdr = {}
        for _ in range(6):
            k, v = f.readline().split(); hdr[k.decode().lower()] = float(v)
        a = np.array(f.read().split(), dtype=np.float32)
    a = a.reshape(int(hdr["nrows"]), int(hdr["ncols"])); a[a < 0] = 0
    return a
def year_of(name):
    m = re.search(r"(\d+)(AD|BC)", name); v = int(m.group(1)); return -v if m.group(2) == "BC" else v
def block(a, k=6):   # sum k x k blocks: 2160 x 4320 -> 360 x 720
    h, w = a.shape; return a.reshape(h // k, k, w // k, k).sum(axis=(1, 3))

files = sorted(Path(sys.argv[1]).glob("popc_*.asc"), key=lambda p: year_of(p.name))
land = block(read_asc(sys.argv[2]).astype(np.float64))        # km2 of land per 0.5 degree cell
mask = land > 1.0
qs, dates = [], []
for p in files:
    pop = block(read_asc(p).astype(np.float64)); d = np.where(mask, pop / np.maximum(land, 1e-9), 0)
    q = np.zeros(d.shape, dtype=np.uint8); ok = d >= 0.1
    q[ok] = np.clip(1 + np.round((np.log10(d[ok]) + 1) * 38), 1, 255).astype(np.uint8)
    qs.append(q[mask]); dates.append(year_of(p.name))
    print(p.name, f"world {pop.sum()/1e6:.0f} M, max density {d.max():.0f}/km2, cells with people {int(ok.sum()):,}")
b64 = lambda b: base64.b64encode(gzip.compress(b, 9)).decode()
out = {"w": int(mask.shape[1]), "h": int(mask.shape[0]), "y": dates, "n": int(mask.sum()),
       "mask": b64(np.packbits(mask.ravel()).tobytes()), "q": b64(np.concatenate(qs).tobytes()),
       "src": "HYDE 3.3 population grid (popc, base scenario), aggregated to 0.5 degree cells; density per km2 of land (maxln_cr)"}
s = json.dumps(out, separators=(",", ":")); open("density.json", "w").write(s)
print(f"{len(dates)} dates, {out['n']:,} land cells, density.json {len(s)/1e3:.0f} KB")
