# Palimpsest — backlog

Last updated: 21 October 2026. Status: prototype 0.1, frozen as a single HTML file.

Priorities: **P1** next phase · **P2** soon after · **P3** later or if time allows.
Ideas and bugs from visitors go in [issues](../../issues) first, then here once triaged.

---

## 0. Release of the prototype

- [ ] Upload the files to `barthelemyr/palimpsest`, with `index.html` at the root
- [ ] Turn on GitHub Pages (main branch, root) and check https://barthelemyr.github.io/palimpsest/ on a laptop and a phone
- [ ] Repository "About": website link, description, topics (history, atlas, data-visualization, ai-assisted)
- [ ] Optional: release v0.1.0, marked as a pre-release
- [x] (done 20 October 2026) Build sources in the repository (`source/`): the template rebuilt from the current `index.html`, the nine data blocks, every build script with relative paths, pinned Python and Node versions and step-by-step instructions (`source/README.md`). `build.py --check` confirms that `index.html` matches the template and blocks byte for byte; `build.py --extract` splits an `index.html` edited directly back into them
- [ ] **P1** Add `tools/cliopatria_errata.py`, `tools/cshapes_check.py` and `tools/cshapes_report.csv` to the repository if they are not there yet (made in another session; not in `source/`)
- [ ] **P1** Confirm HYDE 3.3's licence (the readme says CC BY 3.0, the data portal says CC BY 4.0; check `yoda-metadata.json`) and update DATA-LICENSES.md
- [ ] **P2** Copy the exact copyright lines of flag-icons and countries-list into DATA-LICENSES.md
- [x] (done 20 October 2026) Add `CANDIDATE-SOURCES.md` (open datasets for future layers), `TECHNOLOGY.md`, this backlog and the project notes (`docs/notes.md`) to the repository

## 1. Architecture (start of the next phase)

- [ ] **P1** Split the single file into `index.html`, `css/`, `js/` (data, drawing, views, UI) and `data/*.json`
- [ ] **P1** Load the heavy layers on demand: the density grid, state populations and network data load only when their view or layer is opened. Goal: the first screen in under 1 MB.
- [ ] **P2** One command that runs all the data steps of `source/README.md` in order (the steps, with relative paths, exist since 20 October 2026)
- [ ] **P2** Build manifest: source versions, checksums and parameters (thresholds, simplification, grid size)
- [ ] **P3** Cache with a service worker so the site works offline after the first visit

## 2. Navigation, search and settings (UX redesign)

From the UX review of 20 October 2026 ("Palimpsest — analyse UX, navigation et parcours"). Principle: the site's state fits on one visible line (subject · year · view · active filters), and each setting lives in one place only.

Decisions taken on 20 October 2026:
- **Core becomes an action**, not a tab. Three tabs: Timeline, Map, Network. "What ruled here?" opens from a state's or a place's panel, from a long press (or right click) on the map, and from search (cities). Old `#core/…` links open the Map with that place's stack.
- **Search result opens in the current view** when that view can show it; otherwise the site switches view and says so.
- **Geography zoom**: one visible control (10 · 27 · 63 · 122 countries) plus the continent filter in Settings; the sideways pinch stays as a shortcut.
- **Dates that differ** between the timeline and Cliopatria: each view keeps its source, and the panel shows the other one when it differs.
- **Language**: redesign first, in English; the new search takes aliases from the start, including a short list of French names; the French interface follows.
- **Visitor test**: five people, the four journeys of the review, before the redesign if possible and after.

- [x] **P1** (done 20 October 2026) One search, the same in every view, always in the header: countries, Cliopatria states, periods, empires, peoples, cities, years ("1492" → go to 1492). Results grouped by type; Enter takes the first result; matches at the start of words only (no more "Rome" → "Prome Kingdom")
- [x] **P1** (done 20 October 2026) A stable subject: when a view can't show the subject as it is, it says so and offers the nearest one instead of switching silently; the subject chip and the panel always agree
- [x] **P1** (done 20 October 2026; the Timeline keeps its own year axis) A time bar shared by all views and never covered: panels stop above it (phone) or beside it (laptop); a year field to type a year; eras under the slider
- [x] **P1** (done 20 October 2026) Real history: each change of view, subject or year adds a browser step (`pushState`), so the browser and phone Back buttons work; the panel's Back uses the same history; Timeline links keep the subject
- [x] **P1** (done 20 October 2026; the active settings sit in the toolbar row itself) One Settings drawer per view holding every setting, and an active-filters line under the header ("Europe ×", "Today's borders ×") with "Reset all"; "Key" becomes a legend only; "Explore" becomes search only
- [x] **P1** (done 20 October 2026) Core as an action (see decisions), with the 4 keyboard shortcut and the Core tab removed
- [x] **P2** (done 20 October 2026) Panels fold to their title bar instead of only closing; zoom buttons never under a panel
- [x] **P2** (done 20 October 2026) Map and Network keep the same zoom and place when switching between them
- [x] **P2** (done 20 October 2026) Clear affordances: hover and cursor on everything clickable, including the era axis and the continent strip; a contextual "?" per view showing the gestures; the start hint kept off the controls
- [x] **P2** (done 20 October 2026; inline text links in Sources stay text size) 44 px touch targets on phones: tabs, chip ×, chips, Core layers (group any layer under 12 px high)
- [x] **P2** (changed 20 October 2026) Top 5: on by default on laptops, off at first on phones, with its own toolbar button on the Map and the Network (it was briefly off by default and only in Settings, which hid an important view)
- [x] **P2** (done 20 October 2026; a block named after its empire is titled "Roman Empire in France") Clearer panels: a block's title is its own name ("Roman Gaul", then "part of the Roman Empire"); provenance badges set apart from links; both sources' dates side by side when they differ
- [x] **P3** (done 20 October 2026) Keyboard shortcuts listed (key "?", in the How to card)
- [x] (done 21 October 2026) Periods: one chosen period for every view (Settings › Period, the Timeline's left edge, or under the slider), kept in links; the Map's and the Network's slider then cover only that period; periods renamed by their dates instead of European ages ("Middle Ages" → 500–1500)
- [ ] **P3** A position mini-map across the 122 columns; reset with undo ("View reset · Undo")

## 3. Phone experience

The Map works well, especially in landscape. The Timeline is the weak point upright: 122 columns can't fit in 390 px.

- [ ] **P1** **Phone Timeline, one region at a time** (upright screens):
  - a region strip at the top, with the current focus selected by default;
  - one full-width column with time running down: period blocks in their empire colour, name, dates and one readable line of text;
  - events and achievements as markers in the margin;
  - a draggable year scale on the left edge, sharing the year with the Map;
  - swipe left or right to the neighbouring region (same order as the laptop columns);
  - a tap opens the usual panel as a bottom sheet.
- [x] (done 21 October 2026) An empire found by search on a phone (for example the USSR) opens at the smallest geography level that shows one of its columns (not all 122), framed on the largest group of its columns that fits the screen; on a laptop it keeps every column and widens them so that most of the empire's columns fill the view (USSR, Roman and Ottoman Empires ×4; the British Empire, spread worldwide, ×1.2); on phones the Timeline can scroll its most recent years above the panel, so they are no longer hidden under it
- [ ] **P1** Landscape keeps the multi-column Timeline
- [ ] **P2** Map on a phone: larger time slider within thumb reach, and a hint to rotate the phone for a wider view
- [ ] **P2** Network on a phone: replace the force layout with a list of the states that covered a country, with bars (or hide the view)
- [ ] **P3** "What ruled here?" as an entry point on the phone, with optional geolocation (asked first, never stored)
- [ ] Switch layouts on screen width and touch input, never on the browser name; the same links (`#map/…`, `#network/…`) open the matching view on every device

## 4. Data quality

- [ ] **P1** Audit sample: about 30 timeline periods checked against references, with their badge raised to ✓ Checked
- [ ] **P1** Check the capitals against Wikidata (P36): in progress (21 October 2026), done with the Capitals layer below (`tools/capitals_report.csv`)
- [x] (done 20 October 2026) Cliopatria: colonial powers kept over former colonies after independence; 48 corrections after 1945 (`tools/cliopatria_errata.py`)
- [x] (done 25 October 2026) Cliopatria: Francia in 661–673. Aquitaine is given most of Gaul (517,000–649,000 km²) and the Franks 137 km² (661–665) or 133,000 km² (666–673), with the same outer edge as in 674; those years now use the 674 split (the Franks 445,000 km², Aquitaine 205,000 km² in the south-west) on the Map, the Network, Top 5 and population (`GEOFIX` in the template)
- [ ] **P2** Report the Francia 661–673 error to Cliopatria with the other issues, and look for similar swaps (a sudden exchange of area between two neighbours for a few years, with the same total)
- [ ] **P3** Protectorates end early in Cliopatria: it folds a state into the colonial power once it falls under its control, while Wikipedia counts it until it is abolished. Example reported on 25 October 2026: the Riau-Lingga Sultanate ends in 1856 on the map (from 1857 its islands are part of the Dutch East Indies, after the Dutch deposed Sultan Mahmud Muzaffar Shah in October 1857); Wikipedia gives 1824–1911 (abolished by the Dutch on 11 February 1911, direct rule from 1913). Same pattern for many Malay states, Indian princely states and Indonesian sultanates. Not a data error, a different definition; to mention when reporting to Cliopatria. Options for later: show Wikidata's dates (inception P571, dissolution P576) beside Cliopatria's in every state panel when they differ (generic, needs a Wikidata query), or draw selected protectorates with the existing correction mechanism (inconsistent if done case by case)
- [x] (done 26 October 2026) Names of today: the 113 states that still exist are shown by their short name of today ("Greece", "North Macedonia", "United Kingdom", "Mali") on the Map, the Network, search, Top 5 and the panels; the panel gives Cliopatria's name below, with the reason when it is outdated ("Former Yugoslav Republic of Macedonia", the UN name of 1993–2019; "Kingdom of Great Britain", the name of 1707–1800; "Mali Federation", 1959–1960). Natural Earth's short labels are spelled out ("Macedonia" → North Macedonia, "Bosnia and Herz." → Bosnia and Herzegovina). Search and links keep working with Cliopatria's and Natural Earth's names (`TODAY_NAME`, `NAME_NOTE`, `NE_NAME` in the template). "Turkey" is kept, as in the Timeline and the Network, with Türkiye as a search name and a note; "Republic of China" is kept as it is (its record starts in 1912, on the mainland)
- [x] (done 26 October 2026) The strip "Recorded states on its land" in a country's panel (Map and Network) marks the year shown with a line and a label ("623 CE"), which follow the year as it changes
- [x] (done 26 October 2026) Minor fixes: one label per continent in the Timeline's strip (a single column of another continent no longer splits "ASIA" in two); "Time not to scale" above the year axis, with an explanation on hover; the chosen period drawn as a light band with a dark rule instead of a black bar; no stale "Tap to show only Europe" tooltip after picking a continent; the Network no longer repeats "For Frankish Realm, this view shows…" when the panel already says "On the Timeline: …"; former and common names in search (FYROM, Swaziland, Burma, Ceylon, Siam, Upper Volta, Dahomey, Ivory Coast, Cape Verde, Kampuchea, Czechia, Bechuanaland, Basutoland, Nyasaland, Gold Coast, Tanganyika); on phones the subject chip leaves out the year (it is in the time bar) so that long names fit
- [x] (done 26 October 2026) Panels: a lighter footer (the three views on one compact row, "See it as" dropped; Start / Largest / End became the clickable years of "Dates", and "Widest reach" in the Network's state panel links its year), so it no longer hides a third of the panel. On screens 1,400 px wide or more, a button beside ^ and × widens the panel to 760 px with two columns: what the subject is (facts, charts, sources) on the left, its lists (sections) on the right; the Map, the Network and the Timeline keep the subject visible beside it, and the choice is remembered in the browser
- [ ] **P2** Cliopatria naming errors before today: "Denmark-Norway" until 1921 and others; report upstream with the overlaps and the names above
- [x] (done 20 October 2026) Check Cliopatria against CShapes 2.0, 1886–2019 (`tools/cshapes_check.py`, report `tools/cshapes_report.csv`); Palimpsest stays non-commercial, so CShapes (CC BY-NC-SA 4.0) may be used
- [ ] **P1** Extend the corrections with the CShapes findings, using its dates: Comoros (inside "Republic of Cabo Verde" and France), France in Berlin after 1990, Djibouti 1977–1978, South Sudan 2012–2013, East Timor 2002–2005, Bangladesh 1972, Rwanda and Burundi 1962, Luxembourg until 1916; Maldives and El Salvador 1979–1991 need shapes (CShapes)
- [ ] **P1** Report to Cliopatria the wrong Wikidata identifiers ("Roman Empire" → Q12544, the Byzantine Empire; "Han Dynasty" → Q1068371) and the 171 identifiers shared by several polities, with the other errors already listed
- [ ] **P2** Correct those identifiers in a correction table, then rerun the Wikidata query and `tools/build_successions.py`
- [ ] **P1** Report to Cliopatria: three issues (colonial powers after independence with the 48 corrections; naming errors; missing or misfiled states), with the CShapes report attached
- [ ] **P1** Run `tools/cshapes_check.py` in the build, after every Cliopatria update
- [ ] **P2** HYDE 3.4 (2024) and 3.5 (2025) have been released: check what changed since 3.3 (population, cropland, licence) and decide whether to move before the next rebuild of population, density and state populations
- [ ] **P3** Decide whether to display CShapes borders for 1946–2019 (would need the HYDE grids to recompute state populations, and CC BY-NC-SA for the derived map data)
- [ ] **P2** Check the locations of peoples and unmapped states
- [ ] **P2** Replace Wikipedia search links with verified article titles
- [ ] **P2** Fill the people gaps: Siberia, the steppe, island Southeast Asia, South Asia after the Indus Valley, the Sahel, North America after 1600
- [ ] **P3** Migration paths for peoples who moved (today each sits at one fixed point)
- [ ] **P3** More references on periods, starting with the most visited

## 5. Features

- [x] (done 20 October 2026) Pick today's countries on the Map when Today's borders is on; charts with a value scale, round years and the value at the map's year
- [x] (changed 21 October 2026) **A layer no longer changes what a click does.** Until now, with Today's borders on, a click anywhere in a country opened today's country instead of the historical state, through Cliopatria's 2024 states matched by name (it failed where Cliopatria has gaps, and it took over People markers). Now: a click on an area always opens the historical state, and its panel says **"Here today: France"** for the exact point clicked, with or without the layer; with the layer on, a click on a country's **name** opens that country; hovering an area shows "today France"; "What ruled here?" adds "Country today". Today's country comes from Natural Earth itself, through a lookup grid of about 10 km (`source/mapdata/build_todaygrid.py`, 89 KB), so it matches the dashed borders everywhere, small states included
- [x] (done 21 October 2026) Continent outlines: the Europe–Asia line follows the Urals, the Ural River and the Caspian instead of 60°E (Russia, Kazakhstan); Eastern Thrace in Europe; Sinai in Asia; both halves of Cyprus in Europe; Svalbard in Europe; the Moluccas and Timor in Asia
- [x] (done 21 October 2026) Timeline colours follow the years of each empire link: a block is coloured by its empire only for the years it belonged to it (Soviet Belarus is pale from 1919 until the USSR's founding in 1922), and other years take the colour of another empire it belonged to then, or stay pale; 85 blocks are now drawn in pieces, each opening the same period
- [x] (done 21 October 2026) **Before and after**: succession links from Wikidata (`tools/build_successions.py`, 469 links shown) in a state's panel, and marks between successive layers in "What ruled here?"
- [ ] **P2** Type the succession links (succession, conquest, partition) for the most visited states
- [x] (done 21 October 2026) "Before and after" also in the Timeline's empire and block panels and in the Network's state panel; a row stays in the current view when it can, otherwise opens the Map and says so
- [x] (done 22 October 2026) Timeline text legibility: a block's name is never cut halfway (it shrinks to 9 px, otherwise it is left out, and the name comes before the dates); the big today label (for example "United Kingdom") appears only when there is room, so it no longer covers the last period; empire labels ("Ottoman Empire") sit on a tag of the empire colour and the block text they would cover is left out (it stays in the panel and tooltip); a wider year axis with shorter labels ("10k BCE", "−2500" on phones), so the period names no longer touch the years
- [x] (done 25 October 2026) From the Timeline to the Map and the Network: a subject with dates (an empire, a period, a state) opens at its widest extent (the Frankish Realm at 806) instead of the year in the middle of the Timeline view, which meant nothing for it; a year already chosen for that subject on the Map is kept when coming back. The Map's and the Network's panels say "On the Timeline: Frankish Realm (481–843)" when Cliopatria names the state differently, and the subject chip takes the name of the panel below it. A Cliopatria group whose union holds an empire-linked realm takes that empire's colour in those years (Francia inside the Merovingian and Carolingian Empires is now blue on the Map, the Network, Top 5 and "What ruled here?", as on the Timeline)
- [x] (done 25 October 2026) A chosen period now survives a change of continent or of the number of countries on the Timeline (it used to be cleared, showing all of time again); the fit button frames the period too. Only the chip's ×, Settings › Period or the period band clear it
- [ ] **P3** Succession lines on the Timeline for the selected block (265 of the 1,192 blocks match a map state today)
- [ ] **P2** HYDE lower and upper scenarios shown as a scenario range (the code is ready; the files are still needed)
- [ ] **P2** Overlap threshold as a view setting: store the continuous shares and let readers change the 20% rule in the Network
- [ ] **P3** ArchaeoGLOBE land use as a separate layer, if its licence allows
- [ ] **P3** Coverage diagnostic: how much of each region and period Cliopatria actually records (not a "share of humanity in states" curve, which was dropped)
- [ ] **P3** French interface (the texts are in English today), after the redesign
- [ ] **P2** Timeline colour mode "Regime" (idea of 21 October 2026, next phase), next to "Empires", "Type of rule" and "Patchwork" in Settings › Colour by:
  - 1789–today only, from V-Dem's Regimes of the World (closed autocracy, electoral autocracy, electoral democracy, liberal democracy; country-year, v16 covers 1789–2025; licence reported as CC BY-SA 4.0, to confirm on v-dem.net); a block is drawn in pieces when the regime changes, as for empire years
  - before 1789: neutral, with "no comparable data" in Key; no modern categories applied to ancient states
  - columns that group several of today's countries (Estonia and Latvia, Central Asia…) need a rule: the main country, or stripes
  - form of government (monarchy or republic, parliamentary or presidential) is a different classification; if wanted later, from a separate dataset (for example Cheibub, Gandhi and Vreeland, 1946–2008), not mixed into the same colours
  - not Polity5 (copyrighted, redistribution needs written permission); possible cross-checks: Boix–Miller–Rosato (1800–2020) and LIED (1789–)
- [ ] **P3** "Footprint" metric (idea of 21 October 2026, not for the prototype): share of humanity inside a state's borders summed over its years (HYDE grid × Cliopatria; a first sketch ranks the Han 75, Roman Empire 61, Qing 60, Gupta 49, Ming 46), with land × time beside it. Raw people × time is not usable (it mostly measures recent population growth). To settle first: how states are cut up (Rome is four records, Qing one), empires versus their members (counted twice today), claimed versus controlled land, HYDE's uncertainty before 1500. Shown as a line in a state's panel and an all-time ranking next to Top 5

### New layers

Sources, licence status and caveats are in `CANDIDATE-SOURCES.md` (20 October 2026). Each new layer gets a provenance badge, a legend and a line in the credits.

- [ ] **P1** Send the licence questions listed in `CANDIDATE-SOURCES.md`, section 7: SEDAC (cities), Brecke (conflicts), Correlates of War, Abel (migration), Seshat (Polaris-2026), SlaveVoyages
- [ ] **P1** One design per kind of layer, settled before the first new one: areas, lines and points, each with its drawing, picking, legend and badge; and one record format for events (`claim_type`, `date_min`/`date_max`, `spatial_precision`, `evidence_type`, source, licence, version)
- [ ] **P1** Conquests: land gained and lost per state and year, computed from Cliopatria (*Computed* badge; it shows that land changed hands, not how)
- [ ] **P1** Land use from HYDE (cropland, pasture, rangeland, built-up area), with the density layer's pipeline
- [ ] **P1** Wars and battles: a dated Wikidata snapshot, with the query kept in the build; UCDP GED (CC BY 4.0) aggregated for 1989–2025
- [ ] **P1** **Cities layer**, the first point layer (decided 21 October 2026): split in two, and built without Reba et al. to start
  - [ ] **P1** **Capitals through time** (sub-layer 1, first; next phase, not in the prototype). Done on 21 October 2026: `tools/palimpsest-capitals.rq`, the query result (`tools/wikidata-capitals-2026-10-21.json`: 991 of 1,418 identifiers have a P36, only 15% dated), `tools/build_capitals.py` → `tools/capitals.json` (1,108 map states, 91 KB) and `tools/capitals_report.csv` (hand-placed versus Wikidata: 239 agree, 15 partly, 37 disagree, 68 missing in Wikidata). Finding: an undated Wikidata capital that contradicts the hand-placed one is usually wrong (Joseon → Pyongyang, Sasanian → Balkh, Western Göktürks → Ordu-Baliq), often because Cliopatria's identifier points to a neighbouring item. Plan: combine sources in this order:
    - after 1816: CShapes 2.0 (1886–2019, dated, coordinates; CC BY-NC-SA, already used for the checks) and the Correlates of War capitals in peacesciencer (1816–2024, dated, coordinates; licence to check)
    - before: Seshat Polaris-2026 `polity_capital` (expert-coded; 615 capitals for 415 polities, 251 linked to Cliopatria by SeshatID; names only, so placed through Wikidata, Pleiades or the hand-placed list; dated by Seshat's polity phases; "None" for states without a capital, such as the Holy Roman Empire); it sides with the hand-placed list on Sasanian, Saadi and Kushan capitals and fills Byzantium
    - China: CHGIS seats of government (licence to confirm)
    - then Wikidata dated, the hand-placed list, and Wikidata undated last (marked "undated")
    - display: Source badge for the first four, Approximate for the hand-placed list; the Network keeps its hubs on these capitals; the point-layer rules sketched on 21 October 2026 (capitals of large states only when zoomed out)
  - [ ] **P2** **Cities** (sub-layer 2, later). Sources, in this order:
    - Wikidata (CC0): cities with P625, P571 inception, P1082 population with its P585 date, P1448 dated official names, P17 country; `tools/palimpsest-cities.rq`, dated snapshot; only cities with a dated population before 1950 or an inception before 1800, to stay under a few thousand entries
    - Pleiades (CC BY): settlements and their attestation periods, for the ancient Mediterranean and Near East
    - Natural Earth populated places 1:50m (public domain): today's cities with their rank. Done for search on 21 October 2026 (1,251 cities, `source/blocks/places.json`, block `placedata`); not drawn yet
    - CHGIS (Harvard; CC BY-NC-SA, to confirm on the publisher's page): dated administrative seats of China, 222 BCE – 1911, for the Asian gap; marked non-commercial in the panel and the credits
    - Reba, Reitsma and Seto: only after SEDAC answers about the licence (see below); the `reliability` field is planned for it now
    - Not Chandler (1987) or Modelski directly: books under copyright
  - Merging: one city = one record, keyed by its Wikidata QID when it has one; Pleiades and Natural Earth matched by their Wikidata identifier, otherwise by name and a distance under 20 km (and the case is noted). Each city keeps a list of attestations `{date_min, date_max, population?, source, source_record_id, spatial_precision, evidence_type, reliability?}` (`CANDIDATE-SOURCES.md`, section 5)
  - Display rules, shared by every future point layer:
    - a city appears only in years an attestation covers; an isolated dated population is shown 50 years either side, and says so ("population in 1300, shown 1250–1350"); nothing is said when nothing is recorded
    - point size: population on a log scale when known, otherwise a fixed hollow point ("attested, population unknown"); no Top 5 of cities for now (the sources are too uneven)
    - the capital of the year: its own symbol (a square) over the city
    - Canvas 2D, no library; picked by distance, with a 44 px target on touch screens; density set by zoom (only the N largest attested that year when zoomed out); labels that avoid the states' labels
    - city panel: name (and the period's name from P1448 when it differs), coordinates, population curve with its source dates, the states whose borders contained it (reusing "What ruled here?"), provenance badges per attestation, Wikipedia and Pleiades links
    - Settings: a "Cities" layer (off by default on phones, on on laptops), a chip in the toolbar, a line in Key; on the Map only; the Network's hubs use the capitals of sub-layer 1
    - search: every city in the index (type "place"), with French names; a result opens the Map on the city, at the current year when it is attested, otherwise at its first attestation, saying so
    - links: the `s-l.` subject for places; the old links to Core's 36 cities keep working
  - Constraints: no call to Wikidata or any API at runtime; a `citydata` block under 300 KB gzipped (otherwise the first candidate for loading on demand); everything through `source/` and `build.py`; Playwright screenshots at 1440×900 and 390×844 for 500 BCE, 100, 1300, 1800 and 2000, layer on and off, with no script error
- [ ] **P2** Reba et al., *Historical Urban Population* (3700 BCE – 2000): waiting for SEDAC's answer about the licence (the data.gov record says "No license information was provided. Government Work", which is not a licence)
- [ ] **P2** Volcanic eruptions and earthquakes (NOAA NCEI); eVolv2k (CC BY 4.0) as a time strip of large eruptions, since it gives latitude only
- [ ] **P2** Languages of today (Glottography, CC BY 4.0), labelled as present-day
- [ ] **P2** Religions (Database of Religious History, CC BY 4.0), with its uneven sampling stated in the panel
- [ ] **P2** Roman roads (Itiner-e, CC BY 4.0) as the first line layer
- [ ] **P2** Extinctions of mammals and birds (PHYLACINE, AVOTREX, CC0)
- [ ] **P2** Territorial changes 1816–2018 (Correlates of War), linked to the conquests layer
- [ ] **P2** Atlantic slave trade (SlaveVoyages, CC BY-NC), framed with care
- [ ] **P3** Epidemics, exploration voyages, migrations, domestication and inventions (`CANDIDATE-SOURCES.md`, sections 2.2 and 2.9–2.14)

## 6. Tests and checks

- [ ] **P1** Automated checks on the build outputs: BCE dates and end years, spatial edge cases, population totals and joint countries
- [ ] **P1** Visitor test: five people, the four journeys of the UX review, before and after the redesign
- [ ] **P2** A small set of reviewed regression cases (for example the period navigation between views, Celtic and Germanic Tribes → Map)
- [ ] **P2** Screenshot tests at laptop (1440×900) and phone (390×844, 844×390) sizes
- [ ] **P3** Accessibility pass: keyboard navigation, contrast, screen-reader labels for the canvas views

## 7. To watch

- [ ] Timeline first screen (from the UX review): flags without names, two empire colours too close (Holy Roman Empire and Qing). Done on 26 October 2026: "ASIA" shown once, a "Time not to scale" note above the axis
- [ ] Doubtful succession links seen in testing, kept until reviewed (an exclusion list in `tools/build_successions.py` if confirmed): Western Roman Empire → Vandal Kingdom (shown at Rome for the sack of 455), Fatimid Caliphate → Almohad Caliphate
- [ ] **Crimea is drawn inside Russia** in today's borders: world-atlas 2.0.2 uses Natural Earth's de facto boundaries. It affects the dashed borders, "Here today", the Network and population per country. Decide on a point of view (for example Natural Earth's Ukrainian or UN-recognised versions, or a disputed-area style) and say it in the credits
- [ ] Clicks were reported as slow in one Chrome install (not in Edge, not on the phone, not reproducible in Chromium tests). The cause was the author's Chrome profile, most likely an extension; clearing the cache did not help. Reopen if other visitors report it.

---

## Done (prototype 0.1)

Four linked views (Timeline, Map, Network, Core) with a shared focus · One search for every view · Browser history and links that keep the subject · Stable subject with a note when a view shows something else · "What ruled here?" as an action · Time bar never covered, typed year, eras · One toolbar under the header in every view, one Settings drawer, active settings as chips (all 20 October 2026) · Cliopatria borders by year · Top 5 states by land or people · People and unmapped states layer · HYDE population per country and per state (from the grid) · Population density layer · Provenance badges · Wikipedia links · 52 phase periods for the early Americas and Africa · Navigation consistency across views · Renamed to Palimpsest · AI disclosure, licences and notes · UX review and redesign decisions (20 October 2026) · Candidate sources for future layers, with licences checked (20 October 2026) · Build sources in the repository, with a byte-for-byte check (20 October 2026) · Before and after: successions from Wikidata (21 October 2026).
