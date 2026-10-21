#!/usr/bin/env python3
"""Build the succession links of Palimpsest from a Wikidata query result.

Inputs
  index.html          the site (reads the Cliopatria entities and records from the `mapdata` block)
  query.json          result of tools/palimpsest-successions.rq run on query.wikidata.org
                      (JSON download: a list of {item, prop, other} rows)
Output
  successions.json    compact links between Cliopatria entities, ready to embed as <script id="succdata">

Usage
  python3 tools/build_successions.py index.html tools/wikidata-successions-2026-10-21.json tools/successions.json

Rules (see the implementation prompt)
  * Wikidata properties: P1365 replaces, P1366 replaced by, P155 follows, P156 followed by.
    A link A -> B is stated by A (P1366/P156 = B) or by B (P1365/P155 = A).
  * Only links whose two ends are both Cliopatria entities are kept.
  * Several entities can share one QID: the pair kept is the one whose dates join best
    (smallest |start of B - end of A|).
  * show = 1 when the date gap is between -150 and +200 years and neither end is in BAD_QID.
  * dist = distance between the centre of A's last shape and the centre of B's first shape,
    in map units (Equal Earth, about 7.5 km per unit); information only, not a filter.
"""
import base64, gzip, json, math, re, sys
from collections import defaultdict

# QIDs that Cliopatria v0.2.1 attaches to the wrong Wikidata item (found 21 October 2026).
# Links touching these entities are hidden until the QID is corrected and the query re-run.
BAD_QID = {
    "Q12544": "Cliopatria 'Roman Empire' (-31 to 632) points to the Byzantine Empire item; Roman Empire is Q2277 (to confirm)",
    "Q1068371": "Cliopatria 'Han Dynasty' points to another item; Han dynasty is Q7209 (to confirm)",
}

PROP_BIT = {"P1365": 1, "P1366": 2, "P155": 4, "P156": 8}
FORWARD = {"P1366", "P156"}   # stated by A about B
BACKWARD = {"P1365", "P155"}  # stated by B about A


def qid(uri):
    return uri.rsplit("/", 1)[1]


def main(html_path, query_path, out_path):
    html = open(html_path, encoding="utf-8").read()
    blocks = dict(re.findall(r'<script[^>]*id="([^"]+)"[^>]*>(.*?)</script>', html, re.S))
    meta = json.loads(gzip.decompress(base64.b64decode(json.loads(blocks["mapdata"])["meta"])))
    ents, recs = meta["ents"], meta["recs"]

    first, last = {}, {}
    for r in recs:  # r[0] entity index, r[1] from, r[2] to, r[5], r[6] centre x, y
        i = r[0]
        if i not in first or r[1] < first[i][1]:
            first[i] = r
        if i not in last or r[2] > last[i][2]:
            last[i] = r

    by_q = defaultdict(list)
    for i, e in enumerate(ents):
        by_q[e["wd"]].append(i)

    rows = json.load(open(query_path, encoding="utf-8"))
    if isinstance(rows, dict):  # SPARQL JSON format
        rows = [{k: v["value"] for k, v in b.items()} for b in rows["results"]["bindings"]]

    stated = defaultdict(set)  # (qA, qB) -> set of props
    for r in rows:
        a, p, o = qid(r["item"]), qid(r["prop"]), qid(r["other"])
        if p in FORWARD:
            stated[(a, o)].add(p)
        elif p in BACKWARD:
            stated[(o, a)].add(p)

    links = []
    for (qa, qb), props in stated.items():
        if qa == qb or qa not in by_q or qb not in by_q:
            continue
        best = None
        for ia in by_q[qa]:
            for ib in by_q[qb]:
                if ia == ib:
                    continue
                gap = ents[ib]["f"] - ents[ia]["t"]
                if best is None or abs(gap) < abs(best[2]):
                    best = (ia, ib, gap)
        if best is None:
            continue
        ia, ib, gap = best
        la, fb = last.get(ia), first.get(ib)
        dist = round(math.hypot(la[5] - fb[5], la[6] - fb[6])) if la and fb else -1
        both = 1 if (props & FORWARD) and (props & BACKWARD) else 0
        bits = sum(PROP_BIT[p] for p in props)
        show = 1 if (-150 <= gap <= 200 and qa not in BAD_QID and qb not in BAD_QID) else 0
        links.append([ia, ib, both, bits, gap, dist, show])

    links.sort(key=lambda x: (x[0], x[1]))
    out = {
        "src": "Wikidata (CC0): P1365 replaces, P1366 replaced by, P155 follows, P156 followed by",
        "asof": "2026-10-21",
        "cols": ["a", "b", "both", "props", "gap", "dist", "show"],
        "props": PROP_BIT,
        "bad_qid": BAD_QID,
        "l": links,
    }
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    shown = [l for l in links if l[6]]
    print(f"{len(links)} links between map entities, {sum(l[2] for l in links)} stated both ways, "
          f"{len(shown)} shown ({sum(l[2] for l in shown)} of them both ways)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
