# Building Palimpsest

The site is one file, `index.html`. It is made of a **template** (all HTML, CSS and JavaScript) and twelve **data blocks** (JSON) that the build injects into it. You can work at two levels:

1. **Change the site** (code, design, texts): edit `site-template.html`, then run `python3 build.py`. No downloads needed: the data blocks are committed in `blocks/`.
2. **Rebuild a data block** from the raw sources: download the inputs below, run the scripts in `mapdata/` or `flags/`, copy the output into `blocks/`, then run `build.py`.

`python3 build.py --check` tells you whether `index.html` matches the template and blocks, byte for byte. It did when this folder was published (20 October 2026).

If you edited `index.html` directly (for example in a quick fix on GitHub), run `python3 build.py --extract` to split it back into the template and blocks, then commit all three, so they never drift apart.

## Layout

| Path | What it is |
|---|---|
| `site-template.html` | The whole site, with placeholders `__DATA__`, `__MAP__`, `__TODAY__`, `__NET__`, `__FLAGS__`, `__CONT__`, `__HYDE__`, `__POPGRID__`, `__DENS__`, `__SUCC__`, `__PLACES__`, `__TODAYGRID__` |
| `build.py` | Template + blocks → `../index.html` |
| `blocks/` | The twelve data blocks (exactly those embedded in `index.html`) |
| `mapdata/` | Borders, today's borders, continents, network, population and density |
| `flags/` | Flag sprite |
| `timeline/` | The scripts that revised the timeline data from v4.0 to v4.5 (history; see below) |
| `requirements.txt`, `package.json`, `package-lock.json` | Pinned Python and Node tools |

## Tools

Python 3.13 with `pip install -r requirements.txt`, and Node 22 with `npm install` (run in this folder). Playwright is only needed for the flag sprite.

## Raw inputs (not in the repository)

| Input | Where to get it | Put it in |
|---|---|---|
| Cliopatria v0.2.1 | [github.com/Seshat-Global-History-Databank/cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), `cliopatria.geojson.zip` (commit 5f43337) | `mapdata/raw/cliopatria_polities_only_v021.geojson` |
| Natural Earth 1:50m (countries and land) | npm package `world-atlas` 2.0.2 (installed by `npm install`) | nothing to do |
| flag-icons 7.2.3, countries-list, i18n-iso-countries | npm (installed by `npm install`) | nothing to do |
| HYDE 3.3, base scenario | [doi.org/10.24416/UU01-94FNH0](https://doi.org/10.24416/UU01-94FNH0): `txt/popc_c.txt` from `all_indicators.zip`; `popc_<year>.asc` from the `*_pop.zip` files for 3000BC, 0AD, 500AD, 1000AD, 1300AD, 1500AD, 1700AD, 1800AD, 1900AD, 2000AD, 2023AD; `maxln_cr.asc` from `general_files.zip` | a folder of your choice, `HYDE_DIR` (see below) |

## Rebuilding the data blocks

Run each command from the folder it names. Steps depend on the ones above them.

| Step | Folder | Command | Output |
|---|---|---|---|
| 0. Natural Earth to GeoJSON, with continents | `mapdata/topo` | `node prep_ne.js` | `ne_countries.geojson`, `ne_countries_cont.geojson`, `../land50.geojson` |
| 1. Project to Equal Earth | `mapdata` | `python3 project_all.py` | `topo/clio_proj.geojson`, `ne_countries_proj.geojson`, `topo/land_proj.geojson` |
| 2. Shared-arc topology | `mapdata/topo` | `node topo2.js` and `node today.js` | `topo_w.json`, `today_mesh.json` |
| 3. Borders | `mapdata` | `python3 build_map2.py` | `map2.json` |
| 4. Today's borders | `mapdata` | `python3 build_today.py` | `today.json` |
| 4b. Today's country lookup grid | `mapdata` | `python3 build_todaygrid.py` (cell 1.5 map units, about 10 km) | `todaygrid.json` |
| 5. Continents | `mapdata` | `python3 build_continents.py` | `continents.json` |
| 6. Network | `mapdata` | `python3 build_network.py` (uses `capitals.py`) | `network.json` |
| 7. Population per country | `mapdata` | `HYDE_DIR=… python3 build_hyde.py` (reads `$HYDE_DIR/hyde_txt/popc_c.txt`; `hyde_lower/` and `hyde_upper/` optional) | `hyde.json` |
| 8. Population per state | `mapdata` | `python3 build_popgrid.py <folder with popc_*.asc>` (about 3 minutes) | `popgrid.json` |
| 9. Density | `mapdata` | `python3 build_density.py <folder with popc_*.asc> <maxln_cr.asc>` | `density.json` |
| 10. Flags | `flags` | `node prep_flags.js`, then `python3 raster.py` | `flags.json` |
| 12. Places for search | `mapdata` | `python3 build_places.py <ne_50m_populated_places.geojson>` (Natural Earth v5.1.2; URL and checksum in the script) | `places.json` |
| 11. Successions | repository root | `python3 tools/build_successions.py index.html tools/wikidata-successions-2026-10-21.json tools/successions.json` (to refresh the links, rerun `tools/palimpsest-successions.rq` on query.wikidata.org first) | `tools/successions.json` |

Then copy the outputs into `blocks/` (`map2.json`, `today.json`, `todaygrid.json`, `continents.json`, `network.json`, `hyde.json`, `popgrid.json`, `density.json`, `flags.json`, `successions.json`, `places.json`) and run `python3 build.py`.

`build_map2.py` also reads the empire colours from `site-template.html` (`EMP_COLOR`) and the timeline from `../../data/world_history_timeline_v4_5.json`.

## How close a rebuild gets

Checked on 20 October 2026 by running the steps above from this folder:

- Steps 0, 4 and 10 reproduce the v0.1 blocks exactly. Step 5 reproduced them too, until the continent rules were revised on 21 October 2026 (Urals line, Turkey, Egypt, Cyprus, islands); `blocks/continents.json` is the revised output.
- Step 1 was rewritten (the original one-off run was not saved): 13,742 of 13,797 Cliopatria shapes come out identical. In the other 55, the repair of self-intersecting outlines adds one vertex at a slightly different place, and Antarctica's pole edge differs. As a result, steps 2, 3 and 6 give outputs that differ slightly from v0.1 (67,540 arcs instead of 67,516; one shape fewer), with no visible difference. Using the original projected files, step 3 reproduces v0.1, except that Teotihuacan gains its link to the timeline period of the same name, because the build now reads timeline v4.5 instead of v4.0.
- Steps 7 to 9 were not rerun for this check (they need the HYDE downloads); they are the scripts that produced v0.1's blocks.

The committed blocks are the reference. Rebuild a block only when its source or its script changes.

## Not here

- The Cliopatria corrections after 1945 (`ERRATA` in the template) and the CShapes check were made in another session with `tools/cliopatria_errata.py` and `tools/cshapes_check.py`. Those scripts belong in `tools/` in this repository; they are not in this folder.
- The timeline masters before v4.5 are not included, so the scripts in `timeline/` cannot be rerun from scratch: they record how v4.1 to v4.5 were made. From now on, edit `../data/world_history_timeline_v4_5.json` and `blocks/data.json` directly, or write a new patch that starts from v4.5.
