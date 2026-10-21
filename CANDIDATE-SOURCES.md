# Candidate sources for future layers

*Palimpsest · 20 October 2026 · status: shortlist, none used on the site yet*

Open datasets that could feed new layers: wars, inventions, conquests, impact on nature, cities, trade, religions, languages, migrations, epidemics, voyages, slave trades, disasters and domestication. Sources already in use are listed in [DATA-LICENSES.md](DATA-LICENSES.md).

**How this list was made.** A first search with Perplexity (20 October 2026), then the licence and key facts of each source checked on the publisher's or repository's own page where possible. The *Checked* column says which.

## How to read

**Licence status**

| Mark | Meaning |
|---|---|
| ✅ Open | An open licence (CC0, CC BY, public domain) is stated on the publisher's page |
| 🟢 Non-commercial | CC BY-NC or similar. Fine for Palimpsest, which is and will remain non-commercial, but derived data keeps the NC terms and is marked as such |
| 🟡 Terms only | Free use with citation is stated, but no standard licence. Confirm before republishing derived data |
| 🔴 Unresolved | No licence found. Write to the maintainer before use |

**Checked**: *Publisher* = licence and dates seen on the publisher's or repository's page on 20 October 2026 · *Perplexity* = reported by the first search, not rechecked · *Known* = long-standing, well-documented terms, not rechecked this time. Counts marked † come from the first search, even in rows checked at the publisher.

**Kind of layer**: *areas* (polygons or grids), *lines* (routes, roads, voyages), *points* (events, places). Each kind needs one drawing, picking and badge design, shared by every layer of that kind.

---

## 1. Summary

| Layer | Best first source | Licence | Kind | Priority |
|---|---|---|---|---|
| Conquests | Computed from Cliopatria (territory gained or lost) | ✅ already used | areas | **P1** |
| Impact on nature: land use | HYDE land-use grids (same grids as population) | ✅ CC BY (version to confirm, as for population) | grid | **P1** |
| Largest cities | Reba et al., *Historical Urban Population* | 🔴 | points | **P1** (once cleared) |
| Wars and battles | Wikidata snapshot; UCDP GED from 1989 | ✅ | points | **P1** |
| Volcanoes and earthquakes | NOAA NCEI; eVolv2k | 🟡 / ✅ | points | P2 |
| Languages | Glottography | ✅ | areas (today) | P2 |
| Religions | Database of Religious History | ✅ | regions, entries | P2 |
| Trade routes | Itiner-e (Roman roads) | ✅ | lines | P2 |
| Extinctions | PHYLACINE, AVOTREX | ✅ | ranges, points | P2 |
| Territorial changes 1816–2018 | Correlates of War | 🟡 | events | P2 |
| Slave trades (Atlantic) | SlaveVoyages | 🟢 | lines | P2 |
| Epidemics | Plague mentions (Krauer & Schmid); Marani et al. | 🟢 / ✅ | points | P3 |
| Exploration voyages | CLIWOC logbooks; Wikidata | ✅ | lines | P3 |
| Migrations | Abel, bilateral flows (1990–2020 only) | 🔴 | flows | P3 |
| Domestication | Crop Origins; EUROEVOL | 🟡 / ✅ | points | P3 |
| Inventions | Wikidata; Seshat Polaris-2026 | ✅ / 🔴 | points | P3 |

**Important for the existing population layers:** HYDE 3.4 (2024) and HYDE 3.5 (2025) have been released since the HYDE 3.3 used today. Check what changed before the next population rebuild and before building the land-use layer.

---

## 2. Sources by layer

### 2.1 Wars and battles

No single dataset covers 3400 BCE to today. Modern data is strong from 1946; earlier wars rely on Wikidata and editorial work.

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Wikidata](https://query.wikidata.org/) (Wikimedia) | ✅ [CC0](https://www.wikidata.org/wiki/Wikidata:Licensing) | World, all periods; uneven | Query output (CSV, JSON); live, so keep a dated snapshot | Known | Main source before 1946. Keep battles and wars apart; keep date precision; never use a country centroid as a battle location |
| [UCDP Georeferenced Event Dataset](https://ucdp.uu.se/downloads/) 26.1 (Uppsala University) | ✅ CC BY 4.0, stated for all UCDP datasets | 1989–2025, world; events geocoded to village level, by day | CSV, Excel, codebook | Publisher | Modern organised violence only. Very many events: aggregate by year and place. (Perplexity had marked the licence unresolved; the download page states CC BY 4.0) |
| [UCDP/PRIO Armed Conflict Dataset](https://ucdp.uu.se/downloads/) 26.1 | ✅ CC BY 4.0 | 1946–2025, conflict-years | CSV, Excel | Publisher | Conflicts and parties, not places |
| [Conflict Catalog](https://brecke.inta.gatech.edu/research/conflict/taxonomy-of-violent-conflict/) (Peter Brecke, Georgia Tech) | 🔴 none found | From 1400 CE; about 3,700 conflicts | XLSX | Perplexity | Long chronology with fatalities; locations are names, not coordinates. Ask permission |

### 2.2 Inventions and technologies

No open "first recorded invention, place and date" dataset exists. Label any such layer **"earliest attested evidence in this dataset"**, never "invented here".

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| Wikidata: `P575` time of invention, `P61` inventor, `P1071` location of creation | ✅ CC0 | Uneven, recent bias | Query output | Known | Do not use an inventor's birthplace as the place of invention |
| [Seshat Polaris-2026](https://github.com/Seshat-Global-History-Databank/build_polaris_dataset) (Seshat Global History Databank) | 🔴 not checked | Pre-industrial polities; a military-technology sheet among others | XLSX snapshot | Publisher (existence only) | Same project as Cliopatria, so polities may match. Records adoption by polities, not invention |

### 2.3 Conquests and territorial changes

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| **Computed from Cliopatria** v0.2.1 (this atlas) | ✅ CC BY 4.0 (already used) | As the Map | Land gained and lost per state and year | Computed | Shows that land changed hands, not how (war, treaty, inheritance). *Computed* badge |
| [Territorial Change v6](https://correlatesofwar.org/data-sets/territorial-change/) (Correlates of War; host Steven V. Miller, Clemson) | 🟡 COW [FAQ](https://correlatesofwar.org/faq/): free use with citation, no charging for access; no standard licence | 1816–2018; changes involving at least one COW state | CSV and XLS, 255 KB zip; released 25 March 2019 | Publisher | Gainer, loser, type of change (conquest, cession, …) and date. Territories are named, so they need geocoding |
| Wikidata: sieges, annexations, treaties; `P1346` winner, `P361` part of | ✅ CC0 | Uneven | Query output | Known | A winner does not say which land was taken |

### 2.4 Impact on nature

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [HYDE 3.3](https://doi.org/10.24416/UU01-94FNH0) land use (Klein Goldewijk, Utrecht University) | ✅ CC BY (version to confirm, as for population) | 10,000 BCE – 2023, 5′ grid | ASCII grids: cropland (irrigated and rain-fed, rice), pasture, rangeland, built-up area | Publisher | **Best first choice**: same grids, licence and pipeline as the density layer. HYDE 3.4 (2024) and 3.5 (2025) exist; check first. Modelled, like the population |
| [Land-Use Harmonization 2](https://luh.umd.edu/data.shtml), historical v2h (University of Maryland) | 🔴 licence of the historical files not found | 850–2015, annual, 0.25° grid | NetCDF | Perplexity | Adds transitions and wood harvest, but is partly built on HYDE, so little independent evidence |
| [PHYLACINE 1.2](https://doi.org/10.5061/dryad.bp26v20) (MegaPast2Future, Aarhus and Gothenburg) | ✅ CC0 (Dryad publishes all data under CC0, [terms](https://datadryad.org/terms)) | Mammals of the last ~130,000 years, 5,831 species † | Ranges, traits, phylogenies; v1.2.1 (28 February 2020, [Zenodo](https://zenodo.org/records/3690867), 106 MB) | Publisher | "Present-natural" versus current ranges: shows what was lost, not when. Use the Dryad deposit for the licence |
| [AVOTREX](https://doi.org/10.5061/dryad.zgmsbcckk) v1.0 (Sayol et al.) | ✅ CC0 (Dryad) | 610 bird species extinct in the last 130,000 years | CSV, 1.86 MB; published 26 October 2024, updated 22 January 2025 | Publisher | Location and period of extinction, not exact years. (Perplexity had marked the licence unresolved) |
| [Global Forest Change](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html) v1.13 (Hansen, University of Maryland) | 🔴 CC BY 4.0 reported, not seen at the publisher | 2000–2025, tree-cover loss | Raster tiles, large | Perplexity | Modern only; tree-cover loss is not the same as deforestation |

### 2.5 Largest cities over time

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Historical Urban Population, 3700 BC – AD 2000](https://sedac.ciesin.columbia.edu/data/set/urbanspatial-hist-urban-pop-3700bc-ad2000) v1.00 (Reba, Reitsma and Seto; NASA SEDAC, 2018; DOI [10.7927/H4ZG6QBX](https://doi.org/10.7927/H4ZG6QBX)) | 🔴 the NASA data portal says "licence not specified"; the SEDAC page gives only a citation | 3700 BCE – 2000 CE, world | City, latitude, longitude, year, population, reliability rank; about 1,700 cities † | Publisher | **Best long-run fit**, and it would lift the 36-city limit of search. Uneven evidence and observation dates; rankings are fragile. Paper: [Scientific Data 2016](https://doi.org/10.1038/sdata.2016.34). Ask SEDAC about the licence |
| [GHS Urban Centre Database](https://human-settlement.emergency.copernicus.eu/datasets.php) R2024A (European Commission JRC) | ✅ CC BY 4.0 | 1975–2030 (values after 2025 are projections); about 11,000 urban centres | CSV, GeoPackage | Perplexity | Modern complement only; its city definition differs from historical estimates |

### 2.6 Trade routes

No open, dated network covers the Silk Roads or the Indian Ocean. Keep roads, observed voyages and inferred trade corridors as separate kinds of line.

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Itiner-e](https://zenodo.org/records/17122148), static version 2024, v1.3 (Aarhus University, Universitat Autònoma de Barcelona) | ✅ CC BY 4.0 | Roads of the Roman Empire, about 300 BCE – 300 CE; 14,769 segments † | GeoJSON 78 MB, GeoPackage 34 MB, shapefile; 15 September 2025 | Publisher | Roads, not trade flows. Keep its certainty categories; needs heavy simplification. Paper: [Scientific Data 2025](https://doi.org/10.1038/s41597-025-06140-z) |
| [OWTRAD, Moroccan and trans-Saharan routes](http://www.ciolek.com/owtrad/data/tmcMAm1500.html) (T. M. Ciolek) | 🟢 CC BY-NC 2.5 | 200–1930 CE, 20 points | CSV; page of 2001 | Perplexity | Small, schematic, archival |
| [CLIWOC 2.1](https://doi.org/10.1594/PANGAEA.743343) ship logbooks | ✅ CC BY 3.0 (PANGAEA release of 25 September 2007; CC0 on [DANS](https://doi.org/10.17026/DANS-ZE8-D3C8) according to Perplexity) | 1750–1854, oceans; about 280,000 logbook records † | IMMA format | Publisher | Observed ship tracks, mostly British, Dutch, French and Spanish |

### 2.7 Religions and their spread

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Database of Religious History](https://religiondatabase.org): Standard Cross-Cultural Sample of Religion ([SCCSR](https://github.com/religionhistory/SCCSR), University of British Columbia) | ✅ CC BY 4.0 (stated in the repository) | World; entries for groups, places and texts, with start and end years and **GIS region polygons** | Seven CSV tables; v2 from the 25 February 2025 database; v3 of 20 January 2026 according to Perplexity | Publisher | Expert answers; the repository warns that some regions and periods are heavily over-represented. A region is where an entry applies, not where a religion was the majority |
| Wikidata: `P140` religion of dated institutions | ✅ CC0 | Uneven | Query output | Known | A monastery shows an institution at a place, not the faith of the people around it |

### 2.8 Languages and scripts

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Glottography, *asher2007world*](https://zenodo.org/records/15287258) (Glottography Consortium, from Asher and Moseley's 2007 atlas) | ✅ CC BY 4.0 | Speaker areas of today's languages, world, linked to Glottolog | CLDF with polygons; v1.0.0 (26 April 2025, 145 MB); a newer version exists (v2.0, February 2026) | Publisher | Present-day areas: like today's countries, a labelled anachronism if shown in the past. Never project them back to ancient languages |
| Wikidata: `P282` writing system; `P407` language of a work | ✅ CC0 | Uneven | Query output | Known | Scripts and spoken languages stay separate layers |

### 2.9 Migrations and diasporas

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Bilateral international migration flow estimates](https://figshare.com/articles/dataset/Bilateral_international_migration_flow_estimates_for_200_countries_1990-1995_to_2010-2015_/7731233) (Guy Abel; Abel and Cohen 2019) | 🔴 licence not shown on the item | 1990–2020 in five-year periods, country to country | CSV, 310,557 rows (UN IMS2020 and WPP2024 inputs) | Publisher | Modern and modelled; endpoints, not routes |
| [FLOW](https://data.humdata.org/dataset/annual-migration-flow-estimates-by-sex-between-all-countries-since-1960), annual flows since 1960 (HDX) | 🔴 | 1960 onwards | CSV v1.0 | Perplexity | Check method and licence before choosing it over Abel |

No open dataset covers ancient migrations. The peoples layer's planned migration paths stay editorial.

### 2.10 Epidemics and pandemics

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Mapping the plague](https://zenodo.org/records/6587267) v1.0 (Krauer and Schmid, University of Oslo) | 🟢 CC BY-NC 4.0 | Geocoded plague mentions from Sticker (1908) and Biraben (1975); mostly Europe and the Mediterranean | CSV in a 24 MB zip; 2021 | Publisher | **Mentions, not cases or deaths.** The Biraben corpus is known to be incomplete |
| [A Global Epidemics Dataset (1500–2020)](https://zenodo.org/records/4626111) (Marani, Katul, Pan and Parolari) | ✅ CC BY 4.0 | Titled 1500–2020; the CSV covers 1600–1945 | CSV, XLSX, 0.7 MB; V1.0 of 28 March 2021, a newer version exists | Publisher | Check its location fields before use |

### 2.11 Exploration voyages

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| CLIWOC 2.1 (see 2.6) | ✅ CC BY 3.0 | 1750–1854 | Dated positions per ship | Publisher | Includes some exploration voyages, to be picked out by ship and captain; mostly European |
| Wikidata: `P1427` start point, `P1444` destination, `P527` stops | ✅ CC0 | Uneven | Query output | Known | Endpoints alone do not give a route; draw only dated stops |

### 2.12 Slave trades

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [SlaveVoyages](https://www.slavevoyages.org): Trans-Atlantic and Intra-American databases | 🟢 historical data public domain; imputed data (marked \*) and estimates CC BY-NC 3.0 US ([legal page](https://legacy.slavevoyages.org/blog/legal)); the [FAQ](https://slavevoyages.org/blog/faqs) (2024) says CC BY-NC covers much of the content | Trans-Atlantic 1514–1866 | CSV downloads | Publisher | Strongest source. Port to port, not tracks; many figures imputed. The project is moving to Harvard (announced October 2026, according to Perplexity): recheck terms before use. Needs careful framing |
| [ESTA Database Locations](https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/JV0VBF) (Exploring Slave Trade in Asia) | 🔴 | Places of the Asian slave trade | Gazetteer | Perplexity | Places only, not movements |

No open dataset covers the trans-Saharan or Indian Ocean slave trades.

### 2.13 Climate, disasters and famines

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Significant Volcanic Eruptions](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.hazards:G10147) (NOAA NCEI; DOI 10.7289/V5JW8BSH) | 🟡 access unrestricted and free; no licence statement (US federal data is normally public domain) | 4360 BCE – present; over 600 eruptions | TSV; updated as needed | Publisher | Only eruptions that killed, did damage, reached VEI 6 or caused a tsunami |
| [Significant Earthquakes](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.hazards:G012153) (NOAA NCEI; DOI 10.7289/V5TD9V7K) | 🟡 as above | 2150 BCE – present; over 5,700 earthquakes | Table | Perplexity | Destructive events only |
| [eVolv2k](https://doi.org/10.1594/PANGAEA.971968) v4 (Sigl and Toohey, PANGAEA) | ✅ CC BY 4.0 | 500 BCE – 1900 CE; 256 eruptions found in ice cores | TSV; 29 August 2024 | Publisher | Gives **latitude only**: 41 eruptions are tied to a known volcano, the rest get a default latitude (45°N, 45°S or the equator). Better as a time strip of cold years than as map points |
| [Medieval climate, famine, grain trade and plague](https://zenodo.org/records/17441026) (Bauch and Büntgen) | ✅ CC BY 4.0 | Europe and the Mediterranean around the Black Death | XLSX, 2 MB; v1 of 25 October 2025 | Perplexity | Regional, not a global famine catalogue |

No open global famine catalogue was found.

### 2.14 Domestication of plants and animals

| Dataset | Licence | Coverage | Data | Checked | Fit and caveats |
|---|---|---|---|---|---|
| [Crop Origins and Phylo Food](https://rubenmilla.github.io/Crop_Origins_Phylo/) (Rubén Milla) | 🟡 free download and use, citing the source (own terms) | Food crops; 866 species in v1.0 †; a live version is updated | CSV on GitHub | Publisher | Where the wild ancestors grew and how old cultivation is; not domestication sites |
| EUROEVOL datasets 2 and 3 (UCL) | ✅ CC0 (data papers) | Neolithic Europe, about 8000–4000 BP | CSV | Perplexity | Plant and animal remains at sites, not domestication origins |

No open global dataset of animal domestication origins was found. Domestication is a long process: show date ranges and evidence, not single "firsts".

---

## 3. Gazetteers for placing events

Most pre-modern events come with place names, not coordinates. These help place them.

| Dataset | Licence | Coverage | Data | Checked |
|---|---|---|---|---|
| [Pleiades](https://pleiades.stoa.org) (ISAW, New York University; Ancient World Mapping Center) | ✅ CC BY | Ancient places, mostly the Mediterranean and the Near East | Pleiades Datasets 4.1 on [Zenodo](https://zenodo.org/records/8206033/latest) and GitHub, about 290 MB | Publisher |
| [World Historical Gazetteer](https://whgazetteer.org) (University of Pittsburgh) | ✅ CC BY 4.0 for each dataset marked public (the site's general [licensing page](https://whgazetteer.org/licensing) also mentions a non-commercial licence: check each dataset) | World, contributed datasets | Linked Places format | Publisher |
| Wikidata | ✅ CC0 | World | Query output | Known |

## 4. Wikidata extracts

For layers with no open dataset, a Wikidata extract is the fallback. Save the query and a dated snapshot with the build, and read full statements and references, not only the simple `wdt:` values.

| Layer | Useful properties | Watch out |
|---|---|---|
| Wars and battles | `P31/P279` class; `P585` date, `P580` start, `P582` end; `P625` coordinates, `P276` place; `P710` participants; `P361` part of | Battles and wars apart; event coordinates versus a place's coordinates |
| Inventions | `P575`, `P61`, `P1071` | "First recorded", invention, patent and adoption are different claims |
| Conquests | Event class, dates, `P276`, `P710`, `P1346` winner, `P361` | The winner does not say which land was taken |
| Religion | `P140` on dated institutions, `P571` inception, `P625`/`P276` | Institutions are attestations, not majorities |
| Languages and scripts | `P282` writing system, `P407` language of a work | Scripts and spoken languages apart |
| Voyages and migrations | `P1427` start, `P1444` destination, `P710`, `P527` stops | Endpoints are not a route |
| Epidemics and disasters | Event class, dates, places, `P828` cause, `P1120` deaths, `P1603` cases | Keep the date and source of each changing total |

## 5. One record format for point and line layers

So that every new layer can carry the provenance badges, each record should hold:

| Field | Meaning |
|---|---|
| `claim_type` | What is claimed: battle, eruption, first attestation, mention, … |
| `date_min`, `date_max` | Date range (a single date when known) |
| `spatial_precision` | Exact, settlement, region, default latitude, … |
| `evidence_type` | Documentary, archaeological, ice core, modelled, editorial |
| `source`, `source_record_id` | Dataset and its own identifier for the record |
| `dataset_version`, `licence`, `retrieved_at` | For the build manifest and the credits |

## 6. Before using a source

1. Check the licence again on the publisher's page at download time, and keep a copy of it.
2. Record the version, date and checksum in the build manifest (backlog, section 1).
3. Add the source to DATA-LICENSES.md and to the credits on the site.
4. Mark non-commercial (🟢) data as such in the panel and in the credits.

## 7. Questions to send

| To | About |
|---|---|
| NASA SEDAC (CIESIN, Columbia University) | Licence of *Historical Urban Population* v1.00 |
| Peter Brecke (Georgia Tech) | Permission to show data derived from the Conflict Catalog |
| Correlates of War | Confirm that a free, non-commercial site may republish data derived from Territorial Change v6 |
| Guy Abel | Licence of the bilateral migration flow estimates |
| Seshat Global History Databank | Licence of Polaris-2026 |
| SlaveVoyages | Terms after the move to Harvard |

## Sources consulted (20 October 2026)

UCDP [Download Center](https://ucdp.uu.se/downloads/) · Correlates of War [Territorial Change v6](https://correlatesofwar.org/data-sets/territorial-change/) and [FAQ](https://correlatesofwar.org/faq/) · Dryad [AVOTREX](https://datadryad.org/dataset/doi:10.5061/dryad.zgmsbcckk) and [terms](https://datadryad.org/terms) · Zenodo [PHYLACINE 1.2.1](https://zenodo.org/records/3690867), [Glottography](https://zenodo.org/records/15287258), [Itiner-e](https://zenodo.org/records/17122148), [Mapping the plague](https://zenodo.org/records/6587267), [Global Epidemics Dataset](https://zenodo.org/records/4626111) · NASA [data portal](https://data.nasa.gov/dataset/historical-urban-population-3700-bc-ad-2000) and [SEDAC](https://sedac.ciesin.columbia.edu/data/set/urbanspatial-hist-urban-pop-3700bc-ad2000) · GitHub [SCCSR](https://github.com/religionhistory/SCCSR) · Figshare [Abel](https://figshare.com/articles/dataset/Bilateral_international_migration_flow_estimates_for_200_countries_1990-1995_to_2010-2015_/7731233) · NOAA NCEI [volcanoes](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.hazards:G10147) · PANGAEA [eVolv2k v4](https://doi.org/10.1594/PANGAEA.971968) and [CLIWOC 2.1](https://doi.org/10.1594/PANGAEA.743343) · SlaveVoyages [legal page](https://legacy.slavevoyages.org/blog/legal) and [FAQ](https://slavevoyages.org/blog/faqs) · [Seshat data](https://seshatdatabank.info/data) · [Crop Origins](https://rubenmilla.github.io/Crop_Origins_Phylo/) · Pleiades [Zenodo](https://zenodo.org/records/8206033/latest) · World Historical Gazetteer [licensing](https://whgazetteer.org/licensing) · HYDE on the [Utrecht data portal](https://public.yoda.uu.nl/geo/UU01/94FNH0.html) and the [Utrecht land-use datasets page](https://landuse.sites.uu.nl/datasets/).
