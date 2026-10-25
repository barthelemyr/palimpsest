"""Places for search: Natural Earth 1:50m populated places (public domain), today's cities.
Used only by search, to open "What ruled here?" on a city (before: Core's 36 cities only). Not drawn on the map.
Input : ne_50m_populated_places.geojson, Natural Earth v5.1.2
        (https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_50m_populated_places.geojson,
        sha256 da4662b7bbfeb897d02f228c5839131dce27acff5717630f91ccff4f67828ee7)
Output: places.json, copied to source/blocks/places.json (block `placedata`)
Usage : python3 build_places.py <ne_50m_populated_places.geojson>"""
import json, sys, unicodedata, re

def norm(s): return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()).strip()

feats = json.load(open(sys.argv[1], encoding="utf-8"))["features"]
rows = []
for f in feats:
    p = f["properties"]; n = p.get("NAME") or p.get("NAMEASCII")
    if not n: continue
    fr = p.get("NAME_FR") or ""
    alts = [a.strip() for a in (p.get("NAMEALT") or "").split("|") + [p.get("NAME_EN") or "", p.get("NAMEASCII") or ""] if a and a.strip()]
    alts = [a for a in alts if not ("-" in a and "-" not in n and len(a) <= 5)]   # some ASCII forms are garbled ("F-s" for Fès)
    alts = sorted({a for a in alts if norm(a) and norm(a) not in (norm(n), norm(fr))})
    rows.append([n, fr if norm(fr) != norm(n) else "", "|".join(alts), round(p["LONGITUDE"], 3), round(p["LATITUDE"], 3), p.get("ADM0NAME") or "",
                 int(p.get("POP_MAX") or 0), p.get("WIKIDATAID") or ""])
rows.sort(key=lambda r: -r[6])
out = {"src": "Natural Earth 1:50m populated places (public domain), v5.1.2", "cols": ["name", "fr", "alt", "lon", "lat", "country", "pop_max", "wikidata"], "l": rows}
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("places.json", "w", encoding="utf-8").write(s)
print(len(rows), "places,", f"{len(s) / 1e3:.0f} KB")
