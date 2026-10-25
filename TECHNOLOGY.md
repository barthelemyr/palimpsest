# Technology

What the Palimpsest prototype (v0.1, October 2026) is made of: the building blocks in the browser, the tools that produced its data, and what a next version should know before changing them.

**In short:** the site uses **no JavaScript library at runtime**. It is one HTML file with hand-written JavaScript, CSS and Canvas 2D drawing, plus embedded data. Open-source tools (Python with NumPy and Shapely, Node with TopoJSON, Playwright) were used only to *build* the data and to test.

---

## 1. In the browser (runtime)

| Building block | How it is done | Library? |
|---|---|---|
| Page structure | One `index.html` (about 4.2 MB, 2.5 MB gzipped): HTML, one `<style>` block (~480 lines), one `<script>` block (~2,700 lines), twelve embedded JSON data blocks | None |
| Language | Plain JavaScript (ES2020+: arrow functions, `async`/`await`, `Map`, `Set`, template strings), no modules, no TypeScript, no framework | None |
| Drawing | **Canvas 2D** for the Timeline, Map and Network (`Path2D`, `isPointInPath` for hit testing, `ImageData` for the density layer); inline SVG for icons | None |
| Map projection | **Equal Earth**, implemented directly from its published formula (Šavrič, Patterson and Jenny, 2018); the borders are pre-projected at build time, so the browser only scales and pans | None (no d3-geo) |
| Borders format | Shared-arc topology (TopoJSON-style), delta- and varint-encoded, gzipped, base64; decoded by a small hand-written reader | None (no topojson-client) |
| Decompression | The browser's built-in `DecompressionStream("gzip")` | Web platform |
| Network view | A hand-written force simulation (anchors to geography, pull towards capitals) | None (no d3-force) |
| Population density | HYDE grid stored as one byte per cell and date on a log scale, blended between dates and reprojected row by row into an `ImageData` | None |
| Search | Index built in the browser from the embedded data; word-start matching, French aliases | None |
| Navigation and links | `history.pushState` / `replaceState` and the URL hash hold view, year, layers and subject | Web platform |
| Layout and gestures | CSS grid, media queries, `dvh` units, `ResizeObserver`, `matchMedia`, pointer and wheel events, `requestAnimationFrame` | Web platform |
| Flags | One PNG sprite rasterised from flag-icons at build time | Data only (MIT) |
| Fonts | **Archivo** and **Archivo Narrow** (SIL Open Font License) loaded from Google Fonts | External service |

### External requests at runtime

- **Google Fonts** (`fonts.googleapis.com`, `fonts.gstatic.com`): the only automatic third-party request. It shares the visitor's IP address with Google. Self-hosting the two fonts (allowed by their licence) would make the site fully self-contained and remove this request.
- **Wikipedia and Wikidata**: links only, opened when the reader clicks.

### Embedded data blocks

| Block id | Content | Size |
|---|---|---|
| `data` | Curated timeline v4.5: 122 columns, periods, empires, events, achievements, landmarks, peoples | 390 KB |
| `mapdata` | Cliopatria v0.2.1 borders: topology, hierarchy, colours, labels, search aliases | 1.9 MB |
| `todaydata` | Natural Earth: today's borders and labels | 48 KB |
| `netdata` | Network: country–state overlaps over time, relations, capitals | 161 KB |
| `flagdata` | Flag sprite (PNG) and codes | 183 KB |
| `contdata` | Continent outlines | 130 KB |
| `hydedata` | HYDE 3.3 population per country | 84 KB |
| `popgriddata` | HYDE 3.3 population per Cliopatria shape (from the grid) | 249 KB |
| `densdata` | HYDE 3.3 density grid at 0.5° | 474 KB |
| `succdata` | Wikidata succession links between map states ("Before and after") | 13 KB |
| `placedata` | Natural Earth 1:50m populated places, for search only (1,251 cities) | 82 KB |
| `todaygriddata` | Natural Earth: today's country at any point of the map, as a lookup grid of about 10 km (`source/mapdata/build_todaygrid.py`) | 89 KB |

All data is parsed on page load; nothing is loaded on demand yet. The same blocks are committed as files in `source/blocks/`.

## 2. Building the data (build time)

These scripts were written and run during the prototype. Since 20 October 2026 they are in `source/`, with relative paths, pinned versions (`requirements.txt`, `package.json`) and step-by-step instructions in [source/README.md](source/README.md). The two data checks (`cliopatria_errata.py`, `cshapes_check.py`) belong in `tools/`.

| Tool | Licence | Used for |
|---|---|---|
| **Python 3.13** | PSF | All build scripts (`source/build.py`; in `source/mapdata/`: `project_all.py`, `build_map2.py`, `build_today.py`, `build_network.py`, `build_continents.py`, `build_hyde.py`, `build_popgrid.py`, `build_density.py`; `source/flags/raster.py`; the timeline patches in `source/timeline/`; `tools/cliopatria_errata.py`, `tools/cshapes_check.py`, `tools/build_successions.py`) |
| **NumPy** 2.5.3 | BSD | Reading HYDE ASCII grids, aggregating and encoding the density layer, grid sums |
| **Shapely** 2.2.0 | BSD | Geometry: validity repair, overlaps between Cliopatria shapes and today's countries, points in polygons, unions |
| **Node.js** 22 | MIT | Running the TopoJSON tools (`prep_ne.js`, `topo2.js`, `today.js`) and reading the flag SVGs (`prep_flags.js`) |
| **topojson-server** 3.0.1 | ISC | Building the shared-arc topology from projected Cliopatria and Natural Earth GeoJSON |
| **topojson-simplify** 3.0.3 | ISC | Visvalingam simplification weights (`presimplify`) |
| **topojson-client** 3.1.0 | ISC | Converting world-atlas TopoJSON back to GeoJSON; today's borders as one mesh |
| **world-atlas** 2.0.2 | ISC | Natural Earth 1:50m countries and land, with ISO numeric codes |
| **i18n-iso-countries** 7.12.0 | MIT | ISO numeric to two-letter codes, to look up each country's continent |
| **flag-icons** 7.2.3 | MIT | Flag SVGs, rasterised into one sprite |
| **countries-list** 3.1.1 | MIT | Continent of each country |
| **Playwright** 1.56 (Chromium) | Apache 2.0 | Rasterising the flag sprite; screenshot checks at 1440×900 and 390×844 |
| Python standard library | PSF | `json`, `gzip`, `base64`, `colorsys` (colours), varint and delta encoding |

Hand-written in the build rather than taken from a library: the Equal Earth projection, neighbour-aware colouring, label placement at the pole of inaccessibility, the varint and run-length encoding, and the 20% / 5% overlap rule of the Network.

## 3. Data sources

See [DATA-LICENSES.md](DATA-LICENSES.md): Cliopatria v0.2.1 (CC BY 4.0), HYDE 3.3 (CC BY), Wikidata (CC0, successions), Natural Earth (public domain), flag-icons and countries-list (MIT), world-atlas (ISC). CShapes 2.0 (CC BY-NC-SA 4.0) is used only to check Cliopatria, not displayed.

## 4. Known gaps, for the next version

- **The build is reproducible, with limits.** `source/build.py --check` confirms that `index.html` is exactly the template plus the committed data blocks, and `--extract` splits an `index.html` edited directly back into them. Rebuilding the blocks from the raw downloads gives the same today's borders, continents and flags, and near-identical borders: the projection step had to be rewritten, and 55 of 13,797 Cliopatria shapes differ by one repaired vertex (see `source/README.md`). The population steps were not rerun for that check. There is no single command for all data steps yet.
- **One file, no modules.** Views, data decoding, drawing and UI share one script and global state. Splitting into modules is planned (backlog, section 1).
- **Everything loads at once.** About 2.3 MB gzipped before the first screen; the goal is under 1 MB with layers loaded on demand.
- **No automated tests** beyond screenshot checks; no CI.
- **Self-host the fonts** to remove the only third-party request.
- **Projection choice.** Mainstream open-source map libraries (for example MapLibre GL) do not offer Equal Earth; d3-geo does. Keeping Equal Earth is a design decision with consequences for the choice of libraries.

## 5. Licence of the code

MIT (see [LICENSE](LICENSE)). The curated timeline data and texts are CC BY 4.0; third-party data keeps its own licence.
