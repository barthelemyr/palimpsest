"""Assemble the single-file site: site-template.html + the data blocks in blocks/ -> ../index.html.

Usage (from source/):
  python3 build.py            write ../index.html
  python3 build.py --check    rebuild in memory and say whether ../index.html matches, byte for byte
  python3 build.py --extract  the other way round: split ../index.html back into site-template.html and blocks/
                              (use it after editing index.html directly, then commit all three)

The template holds all HTML, CSS and JavaScript; each data block is a placeholder such as __MAP__.
Edit the template, then build. To refresh a data block, rerun its script in mapdata/ (see README.md)
and copy the output into blocks/."""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCKS = [("__DATA__", "data.json"), ("__MAP__", "map2.json"), ("__TODAY__", "today.json"), ("__NET__", "network.json"),
          ("__FLAGS__", "flags.json"), ("__CONT__", "continents.json"), ("__HYDE__", "hyde.json"),
          ("__POPGRID__", "popgrid.json"), ("__DENS__", "density.json"), ("__SUCC__", "successions.json"), ("__PLACES__", "places.json"),
          ("__TODAYGRID__", "todaygrid.json")]

out = HERE.parent / "index.html"
if "--extract" in sys.argv:   # the other way round, for when index.html was edited directly
    import re
    s = out.read_text(encoding="utf-8")
    ids = ["data", "mapdata", "todaydata", "netdata", "flagdata", "contdata", "hydedata", "popgriddata", "densdata", "succdata", "placedata", "todaygriddata"]
    for (ph, name), bid in zip(BLOCKS, ids):
        m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % bid, s, re.S)
        assert m, f"no data block {bid} in index.html"
        (HERE / "blocks" / name).write_text(m.group(2).replace("<\\/", "</"), encoding="utf-8")
        s = s[:m.start(2)] + ph + s[m.end(2):]
    (HERE / "site-template.html").write_text(s, encoding="utf-8")
    print("site-template.html and blocks/ updated from index.html"); sys.exit(0)

t = (HERE / "site-template.html").read_text(encoding="utf-8")
for ph, name in BLOCKS:
    assert t.count(ph) == 1, f"{ph} should appear once in the template"
    s = (HERE / "blocks" / name).read_text(encoding="utf-8")
    if name == "popgrid.json" and json.loads(s).get("test"): sys.exit("blocks/popgrid.json is synthetic test data: rebuild it from the HYDE grids")
    t = t.replace(ph, s.replace("</", "<\\/"))   # keep "</script>" out of the JSON

if "--check" in sys.argv:
    same = out.exists() and out.read_text(encoding="utf-8") == t
    print("index.html matches the template and blocks" if same else "index.html differs from the template and blocks")
    sys.exit(0 if same else 1)
out.write_text(t, encoding="utf-8")
print(f"index.html {len(t.encode()) / 1e6:.2f} MB")
