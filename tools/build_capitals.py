#!/usr/bin/env python3
"""Build the capitals of Palimpsest's map states from a Wikidata query result, and compare them with the hand-placed ones.

Inputs
  index.html                       the site (reads the Cliopatria entities from the `mapdata` block)
  query.json                       result of tools/palimpsest-capitals.rq run on query.wikidata.org
                                   (JSON download: a list of rows, or the SPARQL JSON format)
  source/mapdata/capitals.py       the 335 hand-placed capitals used by the Network since v0.1
Outputs
  capitals.json                    capitals per map state, with dates, projected to Equal Earth, ready to embed (block `capdata`)
  capitals_report.csv              hand-placed versus Wikidata capital, per state, with the distance and a verdict

Usage
  python3 tools/build_capitals.py index.html tools/wikidata-capitals-YYYY-MM-DD.json source/mapdata/capitals.py tools/

Rules
  * Statements of rank "deprecated" are left out by the query; "preferred" wins over "normal" when undated statements compete.
  * Dates: P580 (start) and P582 (end); P585 (point in time) counts as a start. XSD years are astronomical (0000 = 1 BCE):
    they are turned into the site's years, which have no year 0 (-0200 → 201 BCE → -201). Precision coarser than a year
    (decade, century) is kept and flagged.
  * A capital without dates holds for the whole life of the state; it is marked undated.
  * A capital with only a start holds until the next capital starts, or until the state ends; with only an end, from the state's start.
  * Several map states can share one Wikidata identifier (171 cases): a dated capital goes to the state whose dates overlap it most
    (the rule of build_successions.py); an undated one goes to each of them.
  * States whose identifier is known to be wrong in Cliopatria are skipped (BAD_QID, as in build_successions.py).
  * Capitals without coordinates (P625) are kept in the report but not in capitals.json.
  * Report verdicts, for each hand-placed capital and its years: "agree" when Wikidata's capital lies within 30 km of it for at least
    half of those years, "partly" for fewer; "listed at other dates or among several" when Wikidata names it as a capital of the
    state but not for those years (or among several undated ones); "disagree" when Wikidata never names it.
    distance_km is to the Wikidata capital that holds the most years.
"""
import base64, csv, gzip, json, math, re, sys
from collections import defaultdict
from pathlib import Path

BAD_QID = {
    "Q12544": "Cliopatria 'Roman Empire' (-31 to 632) points to the Byzantine Empire item; Roman Empire is Q2277 (to confirm)",
    "Q1068371": "Cliopatria 'Han Dynasty' points to another item; Han dynasty is Q7209 (to confirm)",
}
AGREE_KM = 30
PREC = {9: "year", 8: "decade", 7: "century", 6: "millennium"}

# Equal Earth, as in source/mapdata/build_map.py (units ×1000, y pointing down)
A1, A2, A3, A4, M = 1.340264, -0.081106, 0.000893, 0.003796, math.sqrt(3) / 2
def proj(lon, lat):
    l, p = math.radians(lon), math.radians(max(-89.999, min(89.999, lat)))
    t = math.asin(M * math.sin(p)); t2 = t * t; t6 = t2 * t2 * t2
    x = l * math.cos(t) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return round(x * 1000, 1), round(-y * 1000, 1)

def km(lon1, lat1, lon2, lat2):
    a, b, c, d = map(math.radians, (lat1, lon1, lat2, lon2))
    return 6371 * 2 * math.asin(math.sqrt(math.sin((c - a) / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin((d - b) / 2) ** 2))

qid = lambda uri: re.split(r"[/#]", uri)[-1] if uri else None

def year(v):   # "-0200-01-01T00:00:00Z" → -201 (site years have no year 0)
    if not v: return None
    m = re.match(r"^([+-]?)(\d+)-", v)
    if not m: return None
    y = int(m.group(2)) * (-1 if m.group(1) == "-" else 1)
    return y if y > 0 else y - 1

def point(wkt):   # "Point(12.48 41.89)" → (12.48, 41.89)
    m = re.match(r"Point\(([-\d.eE]+) ([-\d.eE]+)\)", wkt or "")
    return (float(m.group(1)), float(m.group(2))) if m else None

def load_manual(path):
    ns = {}; exec(Path(path).read_text(encoding="utf-8"), ns); return ns["C"]

def main(html_path, query_path, manual_path, out_dir):
    out_dir = Path(out_dir)
    html = Path(html_path).read_text(encoding="utf-8")
    blocks = dict(re.findall(r'<script[^>]*id="([^"]+)"[^>]*>(.*?)</script>', html, re.S))
    ents = json.loads(gzip.decompress(base64.b64decode(json.loads(blocks["mapdata"])["meta"])))["ents"]
    by_q = defaultdict(list)
    for i, e in enumerate(ents):
        if e.get("wd") and e["k"] != 2: by_q[e["wd"]].append(i)

    rows = json.loads(Path(query_path).read_text(encoding="utf-8"))
    if isinstance(rows, dict): rows = [{k: v["value"] for k, v in b.items()} for b in rows["results"]["bindings"]]

    # one record per statement (rows repeat it for each coordinate and label)
    st, caps = {}, {}
    for r in rows:
        s = st.setdefault(r["st"], {"item": qid(r["item"]), "cap": qid(r["cap"]), "rank": qid(r.get("rank")) or "NormalRank",
                                    "start": None, "end": None, "prec": 9})
        for key, prec in (("start", "startPrec"), ("pit", "pitPrec"), ("end", "endPrec")):
            y = year(r.get(key))
            if y is None: continue
            slot = "end" if key == "end" else "start"
            if s[slot] is None or (slot == "start" and key == "start"): s[slot] = y
            s["prec"] = min(s["prec"], int(r.get(prec) or 9))
        c = caps.setdefault(qid(r["cap"]), {"en": None, "fr": None, "ll": None})
        c["en"] = c["en"] or r.get("en"); c["fr"] = c["fr"] or r.get("fr"); c["ll"] = c["ll"] or point(r.get("coord"))

    # statements → map states
    per_ent = defaultdict(list); skipped_bad = skipped_nomatch = 0
    for s in st.values():
        q = s["item"]
        if q in BAD_QID: skipped_bad += 1; continue
        cands = by_q.get(q, [])
        if not cands: continue
        dated = s["start"] is not None or s["end"] is not None
        if dated and len(cands) > 1:
            a0 = s["start"] if s["start"] is not None else -99999; b0 = s["end"] if s["end"] is not None else 99999
            ov = [(min(b0, ents[i]["t"]) - max(a0, ents[i]["f"]), i) for i in cands]
            best = max(v for v, _ in ov)
            if best < 0: skipped_nomatch += 1; continue
            cands = [i for v, i in ov if v == best]
        for i in cands: per_ent[i].append(s)

    # dated intervals per state, clipped to its dates
    cap_list, cap_idx, links = [], {}, []
    def cidx(q):
        if q not in cap_idx:
            c = caps[q]; x, y = proj(*c["ll"])
            cap_idx[q] = len(cap_list); cap_list.append([q, c["en"] or q, c["fr"] if c["fr"] and c["fr"] != c["en"] else "", x, y, round(c["ll"][0], 4), round(c["ll"][1], 4)])
        return cap_idx[q]
    timeline = {}
    for i, ss in per_ent.items():
        e = ents[i]; dated = sorted([s for s in ss if s["start"] is not None or s["end"] is not None], key=lambda s: (s["start"] if s["start"] is not None else e["f"]))
        undated = [s for s in ss if s not in dated]
        iv = []
        for k, s in enumerate(dated):
            a = s["start"] if s["start"] is not None else e["f"]
            nxt = next((d["start"] for d in dated[k + 1:] if d["start"] is not None and d["start"] > a), None)
            b = s["end"] if s["end"] is not None else (nxt - 1 if nxt is not None else e["t"])
            a, b = max(a, e["f"]), min(b, e["t"])
            if b >= a: iv.append([a, b, s, 1])
        if undated:   # undated capitals (the preferred one, or all of them when ranks tie) fill the years no dated capital covers
            top = [s for s in undated if s["rank"] == "PreferredRank"] or undated
            gaps, at = [], e["f"]
            for a, b, *_ in sorted(iv, key=lambda v: v[0]):
                if a > at: gaps.append([at, a - 1])
                at = max(at, b + 1)
            if at <= e["t"]: gaps.append([at, e["t"]])
            iv += [[a, b, s, 0] for a, b in gaps for s in top]
            iv.sort(key=lambda v: (v[0], v[2]["rank"] != "PreferredRank"))
        timeline[i] = iv
        for a, b, s, d in iv:
            if caps[s["cap"]]["ll"] is None: continue
            links.append([i, cidx(s["cap"]), a, b, d, 1 if s["prec"] < 9 else 0])
    links.sort()
    out = {"src": "Wikidata (CC0): P36 capital, with P580 start time, P582 end time, P585 point in time; P625 coordinates",
           "asof": re.search(r"(\d{4}-\d{2}-\d{2})", Path(query_path).name).group(1) if re.search(r"\d{4}-\d{2}-\d{2}", Path(query_path).name) else "",
           "cols": ["ent", "cap", "from", "to", "dated", "approx_date"], "caps_cols": ["qid", "en", "fr", "x", "y", "lon", "lat"],
           "bad_qid": BAD_QID, "caps": cap_list, "l": links}
    (out_dir / "capitals.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # report: hand-placed versus Wikidata
    manual = load_manual(manual_path)
    name_to = defaultdict(list)
    for i, e in enumerate(ents): name_to[e["n"]].append(i)
    rep = []
    def wd_over(i, ys, ye):   # the Wikidata capitals over a span of years: {capital: years}, and whether they are dated
        out, dated = defaultdict(int), False
        for a, b, s, d in timeline.get(i, []):
            n = min(b, ye) - max(a, ys) + 1
            if n > 0: out[s["cap"]] += n; dated = dated or bool(d)
        return out, dated
    for name, entries in manual.items():
        for i in name_to.get(name, [None]):
            e = ents[i] if i is not None else None
            for k, (y0, lon, lat, city) in enumerate(entries):
                ys = max(y0, e["f"]) if e else y0; ye = (entries[k + 1][0] - 1) if k + 1 < len(entries) else (e["t"] if e else 2024)
                over, d = wd_over(i, ys, ye) if e else ({}, False)
                row = {"state": name, "wikidata": e.get("wd", "") if e else "", "from": ys if e else "", "to": ye if e else "",
                       "manual_city": city, "manual_lon": lon, "manual_lat": lat}
                if e is None: row.update(verdict="state not on the map")
                elif e.get("wd") in BAD_QID: row.update(verdict="skipped: wrong Wikidata identifier in Cliopatria")
                elif not over: row.update(verdict="missing in Wikidata")
                else:   # the share of the years where Wikidata's capital lies within 30 km of the hand-placed one
                    span = max(1, ye - ys + 1); main = max(over, key=over.get); c = caps[main]
                    near = sum(n for q, n in over.items() if caps[q]["ll"] and km(lon, lat, *caps[q]["ll"]) < AGREE_KM)
                    row.update(wikidata_city=" / ".join(caps[q]["en"] or q for q in sorted(over, key=over.get, reverse=True)[:3]), wikidata_capital=main,
                               wikidata_dated="yes" if d else "no (whole life)", agree_share=f"{round(100 * near / span)}%")
                    listed = any(caps[s2["cap"]]["ll"] and km(lon, lat, *caps[s2["cap"]]["ll"]) < AGREE_KM for *_, s2, _d in timeline.get(i, []))
                    if c["ll"] is None: row.update(verdict="Wikidata capital has no coordinates")
                    else:
                        row.update(wikidata_lon=c["ll"][0], wikidata_lat=c["ll"][1], distance_km=round(km(lon, lat, *c["ll"])))
                        row.update(verdict="agree" if near >= span * 0.5 else "partly" if near > 0 else
                                   "listed at other dates or among several" if listed else "disagree")
                rep.append(row)
    manual_ents = {i for n in manual for i in name_to.get(n, [])}
    for i, iv in sorted(timeline.items()):
        if i in manual_ents or not iv: continue
        a, b, s, d = iv[0]; c = caps[s["cap"]]
        rep.append({"state": ents[i]["n"], "wikidata": ents[i]["wd"], "from": a, "to": b, "wikidata_city": c["en"] or s["cap"], "wikidata_capital": s["cap"],
                    "wikidata_dated": "yes" if d else "no (whole life)", "wikidata_lon": c["ll"][0] if c["ll"] else "", "wikidata_lat": c["ll"][1] if c["ll"] else "",
                    "verdict": "missing in the hand-placed list"})
    cols = ["state", "wikidata", "from", "to", "manual_city", "manual_lon", "manual_lat", "wikidata_city", "wikidata_capital", "wikidata_dated",
            "wikidata_lon", "wikidata_lat", "distance_km", "agree_share", "verdict"]
    with open(out_dir / "capitals_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rep]

    # summary
    with_cap = {i for i, iv in timeline.items() if iv}
    print(f"{len(st)} statements for {len({s['item'] for s in st.values()})} identifiers; skipped {skipped_bad} (wrong identifier), {skipped_nomatch} (dates match no state)")
    print(f"{len(with_cap)} of {sum(1 for e in ents if e['k'] != 2)} map states have a capital; {sum(1 for i in with_cap if any(d for *_, d in timeline[i]))} of them dated; "
          f"{len(cap_list)} distinct capitals with coordinates, {sum(1 for c in caps.values() if c['ll'] is None)} without")
    v = defaultdict(int)
    for r in rep: v[r["verdict"]] += 1
    print("report:", dict(v))
    print(f"capitals.json {len(json.dumps(out, separators=(',', ':'))) / 1e3:.0f} KB, {len(gzip.compress(json.dumps(out, separators=(',', ':')).encode())) / 1e3:.0f} KB gzipped")

if __name__ == "__main__":
    if len(sys.argv) != 5: sys.exit(__doc__)
    main(*sys.argv[1:])
