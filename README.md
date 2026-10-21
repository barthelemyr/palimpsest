# Palimpsest

**World history, layer by layer.** An interactive atlas of 5,000 years of history: who ruled where, who lived where, and how many people there were, with the source of every layer.

**Live prototype:** https://barthelemyr.github.io/palimpsest/

> **Status: prototype.** This is an exploratory build, not a finished reference work. Dates, locations and descriptions can contain mistakes; see [Limitations](#limitations).

> **Made with AI.** This project was built in conversation with **Claude**, an AI model by Anthropic. Claude wrote the code, the design, the data processing and the curated timeline text, directed and reviewed by the author. Details: [AI_DISCLOSURE.md](AI_DISCLOSURE.md).

---

## What it does

One subject (a country, state, period, place or year) stays in focus while you switch between three views:

| View | Shows |
|---|---|
| **Timeline** | 122 country and region columns, time running downward; colour = empire; zoom in time and in geography |
| **Map** | Historical borders year by year (Equal Earth projection), Top 5 states by land or by people |
| **Network** | Today's countries pulled towards the recorded states whose territory covered them (a computed overlap) |

**What ruled here?** works on any place (long press or right click on the map, a panel, or a city in search): every recorded state whose borders contained it, oldest to newest, plus peoples recorded nearby, with a mark where Wikidata links one state to the next. A state's panel lists the states recorded **before and after** it, from Wikidata, in every view. One search box in the header finds countries, states, periods, peoples, cities and years in every view, and the browser's Back button follows your steps.

**Settings** adds today's borders, **population density** (HYDE 3.3), and **peoples and unmapped states**: peoples, cultures and kingdoms from the timeline that the borders dataset does not draw, shown at approximate locations.

Every panel says where its content comes from with a badge: **Source** (taken from a published dataset), **Computed** (calculated by this site), **Editorial** (curated, AI-assisted, not individually referenced), **Approximate** (hand-placed location) and **✓ Checked** (has specific references).

## Data sources

| Source | Licence | Used for |
|---|---|---|
| [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria) v0.2.1, Seshat Global History Databank (Bennett et al.) | CC BY 4.0 | Historical borders (1,637 polities, 12,765 dated shapes) |
| [HYDE 3.3](https://doi.org/10.24416/UU01-94FNH0), Klein Goldewijk et al., Utrecht University | Creative Commons Attribution | Population per country, per state (computed from the grid) and density |
| [Natural Earth](https://www.naturalearthdata.com) | Public domain | Coastlines and today's borders |
| [world-atlas](https://github.com/topojson/world-atlas) | ISC | ISO codes of countries |
| [flag-icons](https://github.com/lipis/flag-icons) | MIT | Flags |
| [countries-list](https://github.com/annexare/Countries) | MIT | Continents |
| [Wikidata](https://www.wikidata.org) | CC0 | "Before and after": succession links between the map's states (query of 21 October 2026, in `tools/`) |
| Wikipedia | linked only | "W" links in panels |

Inspired by ChartOrigin's poster *Timeline of World History*; the content was re-made and corrected, and no artwork is reused. Full attributions: [DATA-LICENSES.md](DATA-LICENSES.md).

## How it is built

- `index.html` is the whole site: one file (about 3.9 MB) with all data embedded; only its two fonts come from Google Fonts. No server, no tracking, no build step needed to view it.
- `source/` holds everything needed to rebuild it: `site-template.html` (all HTML, CSS and JavaScript), the ten data blocks in `source/blocks/`, and `build.py`, which puts them together (`python3 build.py --check` confirms that `index.html` matches). The Python and Node scripts that made the data blocks from the raw sources (Cliopatria, Natural Earth, HYDE) are there too, with pinned versions and step-by-step instructions: [source/README.md](source/README.md).
- `data/world_history_timeline_v4_5.json` is the curated timeline dataset (122 columns, about 1,200 periods, events, achievements, landmarks), readable on its own.
- `docs/notes.md` documents the process, the methods and the open questions in detail; [TECHNOLOGY.md](TECHNOLOGY.md) lists what the site is made of; [BACKLOG.md](BACKLOG.md) lists what comes next; [CANDIDATE-SOURCES.md](CANDIDATE-SOURCES.md) lists open datasets for future layers.

## Limitations

- Most timeline periods follow standard chronology and are **not individually referenced** (marked *Editorial*); only a small number carry specific sources.
- Capitals, people locations and the positions of unmapped states were **placed by hand** and are approximate.
- Cliopatria is thin before 1500 CE, and coverage favours regions with written records. Empty areas mean "no recorded state", not "no people".
- HYDE population figures are **modelled estimates**, often uncertain by a factor of two before 1500 CE; between HYDE's dates the site interpolates.
- Network links and state populations are **computed** by this site (territorial overlap, grid allocation), not taken from a source.

Corrections are very welcome: please open an [issue](../../issues).

## Licence

- **Code** (HTML, CSS, JavaScript and build scripts): [MIT](LICENSE).
- **Curated timeline data and texts** (`data/`, descriptions in the site): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **Third-party data** embedded in the site remains under its own licence (see the table above and [DATA-LICENSES.md](DATA-LICENSES.md)).

---

### En bref (français)

Palimpsest est un prototype d'atlas interactif de l'histoire du monde, couche par couche : frontières, peuples et population sur 5 000 ans, avec la source de chaque couche. Il a été réalisé avec l'IA (Claude, d'Anthropic) : code, design, traitement des données et textes de la frise ont été produits par l'IA, sous la direction et la relecture de l'auteur. Les dates et textes non sourcés sont signalés « Editorial » ; les corrections sont bienvenues via les *issues*.
