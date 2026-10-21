"""Early Americas and Africa (v4.5): split long single blocks into documented phases, and fill empty early centuries.
Standard archaeological chronology, approximate dates, marked unsourced until checked (like every other period).
Each phase gets an exact Wikipedia title (opened through Wikipedia's search) and, for peoples and cultures, an approximate location.
Applied to proto/data.json and the master (world_history_timeline_v4_4.json -> _v4_5.json). Landmarks follow the phase that contains their date."""
import json

# phase: (slug or existing id, name, type, start, end, description, wikipedia, (lon, lat) or None, map label or None)
SPLIT = {
 "usa.archaic-period": [
  ("early-and-middle-archaic", "Early and Middle Archaic", "archaeological_period", -8000, -3000, "Foragers of the post-glacial forests and rivers; Watson Brake, the oldest known mound complex in North America (c. 3500 BCE).", "Watson Brake", (-92.13, 32.37), "Archaic North America"),
  ("late-archaic-poverty-point", "Late Archaic and Poverty Point", "culture", -3000, -1000, "Native plants domesticated (the Eastern Agricultural Complex); the great earthworks of Poverty Point (c. 1700–1100 BCE).", "Poverty Point", (-91.41, 32.64), None)],
 "usa.woodland-period": [
  ("early-woodland-adena", "Early Woodland (Adena)", "culture", -1000, -200, "Pottery, burial mounds and the first gardens; Adena mounds in the Ohio valley.", "Adena culture", (-82.98, 39.33), None),
  ("middle-woodland-hopewell", "Middle Woodland (Hopewell)", "culture", -200, 500, "Geometric earthworks and trade networks reaching from the Rockies to the Gulf of Mexico.", "Hopewell tradition", (-83.1, 39.4), None),
  ("late-woodland", "Late Woodland", "culture", 500, 800, "Bow and arrow, maize farming and growing villages.", "Woodland period", (-88.0, 40.0), None)],
 "canada.paleo-and-archaic-peoples": [
  ("canada.paleo-and-archaic-peoples", "Paleo-Indian and Archaic peoples", "peoples", -13000, -3000, "First Nations ancestors follow the retreating ice sheets.", "Paleo-Indians", (-106.0, 53.0), None),
  ("late-archaic-maritime-and-shield-peoples", "Late Archaic: Maritime and Shield peoples", "peoples", -3000, -1000, "Maritime Archaic seal and fish hunters on the Atlantic coast (Port au Choix) and Shield Archaic peoples inland; the first Paleo-Inuit reach the Arctic (c. 2500 BCE).", "Maritime Archaic", (-57.3, 50.7), "Maritime Archaic peoples")],
 "mexico.archaic-period": [
  ("mexico.archaic-period", "Archaic period", "archaeological_period", -8000, -2000, "Foragers domesticate squash, maize and beans (Guilá Naquitz, Balsas valley).", "Mesoamerican chronology", (-98.5, 18.5), "Archaic Mesoamerica"),
  ("early-formative-villages", "Early Formative villages", "archaeological_period", -2000, -1600, "Pottery, permanent villages and the first known ball court, at Paso de la Amada (c. 1650 BCE).", "Paso de la Amada", (-92.4, 14.9), None)],
 "mexico.olmec-civilization": [
  ("olmec-san-lorenzo", "Olmec: San Lorenzo", "culture", -1600, -900, "The first great Olmec centre on the Gulf Coast; colossal stone heads.", "San Lorenzo Tenochtitlán", (-94.76, 17.75), None),
  ("olmec-la-venta", "Olmec: La Venta", "culture", -900, -400, "La Venta's pyramid and buried offerings; Olmec styles spread across Mesoamerica.", "La Venta", (-94.04, 18.1), None)],
 "guatemala.preclassic-maya": [
  ("early-preclassic-maya", "Early Preclassic Maya", "culture", -2000, -1000, "The first farming villages and pottery in the Maya lowlands and on the Pacific coast.", "Preclassic Maya", (-90.1, 16.5), None),
  ("middle-preclassic-maya", "Middle Preclassic Maya", "culture", -1000, -300, "Ceremonial centres at Nakbe, Ceibal and El Mirador; the first Maya pyramids.", "Nakbe", (-89.85, 17.67), None),
  ("late-preclassic-maya", "Late Preclassic Maya", "culture", -300, 250, "El Mirador's giant pyramids, Kaminaljuyu in the highlands and the first Maya writing.", "El Mirador", (-89.92, 17.75), None)],
 "central_america.preclassic-maya": [
  ("early-preclassic-maya", "Early Preclassic Maya", "culture", -2000, -1000, "The first farming villages and pottery.", "Preclassic Maya", None, None),
  ("middle-preclassic-maya", "Middle Preclassic Maya", "culture", -1000, -300, "Villages grow into ceremonial centres (Chalchuapa, early Copán).", "Preclassic Maya", None, None),
  ("late-preclassic-maya", "Late Preclassic Maya", "culture", -300, 250, "The first Maya cities of the southeast.", "Preclassic Maya", None, None)],
 "ecuador.valdivia-and-early-cultures": [
  ("valdivia-culture", "Valdivia culture", "culture", -3500, -1800, "Farming villages with some of the earliest pottery in the Americas.", "Valdivia culture", (-80.7, -1.9), None),
  ("machalilla-culture", "Machalilla culture", "culture", -1800, -1000, "Coastal farmers and fishers; stirrup-spout vessels.", "Machalilla culture", (-80.75, -1.55), None),
  ("chorrera-culture", "Chorrera culture", "culture", -1000, -300, "Fine ceramics and trade along the coast and into the Andes.", "Chorrera culture", (-79.9, -1.7), None),
  ("regional-development-cultures", "Regional Development cultures", "culture", -300, 500, "Bahía, Jama-Coaque and La Tolita: gold and platinum work and ceremonial centres.", "La Tolita", (-79.05, 1.2), None)],
 "libya.prehistoric-sahara": [
  ("green-sahara", "Green Sahara hunters and early herders", "archaeological_period", -12000, -3500, "Lakes and grasslands in the Sahara; hunters, fishers and the first cattle herders.", "African humid period", (10.5, 24.8), None),
  ("pastoral-sahara", "Pastoral Sahara and the drying desert", "archaeological_period", -3500, -1000, "Cattle herders and their rock art in the Acacus as the Sahara dries out.", "Tadrart Acacus", (10.5, 24.8), None)],
 "central_sahel.pastoralists-and-early-towns": [
  ("herders-and-gajiganna-villages", "Herders and the Gajiganna villages", "peoples", -2500, -800, "Cattle herders move south as the Sahara dries; Gajiganna villages near Lake Chad (c. 1800–800 BCE).", "Lake Chad", (13.0, 12.6), None),
  ("sao-and-early-towns", "Sao and early towns", "peoples", -800, 700, "Walled settlements and terracottas of the Sao around Lake Chad; trans-Saharan routes.", "Sao civilisation", (14.5, 12.0), None)],
 "west_sahara_mauritania.prehistoric-sahara-and-bafour-peoples": [
  ("saharan-herders", "Saharan herders", "peoples", -5000, -2000, "Cattle herders and fishers of a still-green western Sahara.", "African humid period", (-11.0, 21.0), None),
  ("tichitt-villages", "Tichitt villages", "culture", -2000, -300, "Stone-walled villages on the Dhar Tichitt cliffs: early millet farming and herding.", "Dhar Tichitt", (-9.5, 18.4), None),
  ("bafour-peoples-and-early-trade", "Bafour peoples and early trade", "peoples", -300, 300, "Farmers and herders of the drying Sahel; first trade routes to North Africa.", "Bafour", (-10.5, 19.6), None)],
 "guinea_coast.kintampo-and-iron-age-peoples": [
  ("kintampo-complex", "Kintampo complex", "culture", -2500, -1400, "Early farmers and herders in the forest–savanna of Ghana.", "Kintampo Complex", (-1.7, 8.05), None),
  ("late-stone-age-farmers", "Late Stone Age farmers", "peoples", -1400, -500, "Yam and oil-palm farming villages in the forest belt.", "Later Stone Age", (-0.5, 7.0), "Guinea Coast farmers"),
  ("early-iron-age-peoples", "Early Iron Age peoples", "peoples", -500, 1000, "Iron working spreads; villages grow along the Guinea coast.", "Iron metallurgy in Africa", (1.0, 7.5), "Guinea Coast Iron Age")],
 "central_africa.forest-foragers-and-bantu-homeland": [
  ("bantu-homeland-and-first-farmers", "Bantu homeland and first farmers", "peoples", -3000, -1000, "Farming communities in the Cameroon–Nigeria grasslands, where the Bantu languages began.", "Bantu expansion", (10.5, 6.0), None),
  ("bantu-expansion-into-the-rainforest", "Bantu expansion into the rainforest", "peoples", -1000, -500, "Farmers move south and east through the forest, beside forest foragers.", "Bantu expansion", (15.5, 1.5), None)],
 "angola.foragers-and-bantu-farmers": [
  ("khoisan-foragers", "Khoisan foragers", "peoples", -25000, -500, "Hunter-gatherers of the savanna and the coast.", "Khoisan", (17.0, -12.0), "Angolan foragers"),
  ("angola.foragers-and-bantu-farmers", "Foragers and Bantu farmers", "peoples", -500, 1390, "Bantu-speaking, iron-working farmers settle beside foragers.", "History of Angola", (17.0, -12.0), "Angolan foragers and farmers")],
 "south_africa.khoisan-and-bantu-societies": [
  ("khoisan-foragers-and-herders", "Khoisan foragers and herders", "peoples", -1000, 300, "San hunter-gatherers; Khoikhoi herders bring sheep and cattle about 2,000 years ago.", "Khoikhoi", (21.0, -31.0), None),
  ("south_africa.khoisan-and-bantu-societies", "Khoisan and Bantu societies", "peoples", 300, 1652, "Hunter-gatherers, herders and Bantu farming kingdoms.", "Khoisan", (22.0, -30.5), None)],
 "mozambique.foragers-and-bantu-farmers": [
  ("coastal-foragers", "Foragers", "peoples", -1000, 200, "Hunter-gatherers and fishers before the arrival of farmers.", "Later Stone Age", (35.0, -15.0), "Mozambican foragers"),
  ("mozambique.foragers-and-bantu-farmers", "Foragers and Bantu farmers", "peoples", 200, 1000, "Bantu farmers from c. 200 CE.", "History of Mozambique", (36.0, -17.0), "Mozambican foragers and farmers")],
 "zambia_malawi.foragers-and-bantu-farmers": [
  ("late-stone-age-foragers", "Late Stone Age foragers", "peoples", -1000, 300, "Hunter-gatherers and their rock art, before iron-working farmers arrive.", "Later Stone Age", (29.0, -12.5), "Zambezi foragers"),
  ("zambia_malawi.foragers-and-bantu-farmers", "Foragers and Bantu farmers", "peoples", 300, 1500, "Iron Age communities and trade centres.", "History of Zambia", (28.5, -13.5), "Zambezi foragers and farmers")],
}
PREFIX = {   # new first periods for columns that started late
 "mali": [("sahel-herders-and-millet-farmers", "Sahel herders and first millet farmers", "peoples", -3000, -250, "Herders and fishers along the Niger; pearl millet domesticated in the Sahel (c. 2500 BCE).", "Pearl millet", (-3.0, 16.5), "Sahel millet farmers")],
 "nigeria": [("late-stone-age-peoples", "Late Stone Age peoples", "peoples", -3000, -1000, "Foragers and early farmers; yam cultivation in the forest zone.", "Later Stone Age", (7.0, 8.0), "Nigerian Late Stone Age")],
 "zimbabwe": [("san-foragers", "San foragers", "peoples", -3000, 300, "Hunter-gatherers and their rock art in the Matobo hills.", "San people", (28.5, -20.5), None)],
 "congo": [("forest-foragers", "Forest foragers", "peoples", -3000, -500, "Hunter-gatherers of the Congo rainforest, ancestors of today's Mbuti, Baka and Batwa.", "Pygmy peoples", (20.0, -1.0), None)],
 "great_lakes": [("late-stone-age-foragers", "Late Stone Age foragers", "peoples", -3000, -500, "Hunter-gatherers and fishers around the great lakes.", "Later Stone Age", (31.5, -1.0), "Great Lakes foragers")],
 "swahili_coast": [("foragers-and-pastoral-neolithic", "Foragers and early herders", "peoples", -3000, -500, "Hunter-gatherers; herders of the Pastoral Neolithic reach the East African interior.", "Savanna Pastoral Neolithic", (37.0, -3.5), "East African herders")],
 "senegambia": [("fishers-and-herders", "Fishers and herders", "peoples", -3000, -800, "Shell middens of the Saloum delta; herders move south from the Sahara.", "Saloum Delta", (-16.6, 13.9), None)],
 "ethiopia": [("highland-farmers-and-herders", "Highland farmers and herders", "peoples", -3000, -980, "Herding, and the domestication of teff, finger millet and ensete in the highlands.", "Teff", (38.7, 12.5), "Ethiopian highland farmers")],
 "algeria": [("amazigh-ancestors", "Neolithic and Bronze Age Amazigh ancestors", "peoples", -3400, -800, "Herders and farmers of North Africa, ancestors of the Amazigh (Berbers).", "Berbers", (3.5, 35.5), "Amazigh ancestors")],
 "tunisia": [("amazigh-ancestors", "Neolithic and Bronze Age Amazigh ancestors", "peoples", -3400, -814, "Herders and farmers of North Africa, ancestors of the Amazigh (Berbers).", "Berbers", None, None)],
 "morocco": [("amazigh-ancestors", "Neolithic and Bronze Age Amazigh ancestors", "peoples", -3400, -800, "Herders and farmers of North Africa, ancestors of the Amazigh (Berbers).", "Berbers", None, None)],
}

def lab(y):
    a = abs(y); s = f"{a:,}" if a >= 10000 else str(a)
    return f"c. {s} {'BCE' if y < 0 else 'CE'}"
def pid(track, slug): return slug if "." in slug else f"{track}.{slug}"
def compact(track, ph, old_lm, lmdate, first, old):
    slug, n, t, s, e, desc, wp, ll, ml = ph
    o = {"i": pid(track, slug), "n": n, "t": t, "s": s, "e": e, "sl": lab(s), "el": lab(e), "d": desc, "sa": 1, "ea": 1, "wp": wp}
    if ll: o["ll"] = list(ll)
    if ml: o["ml"] = ml
    lm = [x for x in old_lm if (lmdate.get(x) is None and first) or (lmdate.get(x) is not None and s <= lmdate[x] < e)]
    if lm: o["lm"] = lm
    if first and old and old.get("po"): o["po"] = 1; o["cn"] = old.get("cn", "")
    if old and old.get("par"): o["par"] = 1
    return o
def full(track, ph, compact_rec, applies, old):
    slug, n, t, s, e, desc, wp, ll, ml = ph
    o = {"id": pid(track, slug), "name": n, "entity_type": t, "temporal_type": "interval", "start": s, "end": e, "start_label": lab(s), "end_label": lab(e),
         "start_approx": True, "end_approx": True, "duration_years": e - s - (1 if s < 0 < e else 0), "applies_to": applies, "description": desc,
         "source": "added_v4_5", "verification": "unsourced_standard_chronology", "wikipedia": "https://en.wikipedia.org/wiki/" + wp.replace(" ", "_")}
    if ll: o["location"] = {"lon": ll[0], "lat": ll[1], "precision": "approximate core area"}
    if compact_rec.get("lm"): o["landmark_ids"] = compact_rec["lm"]
    if old and old.get("parallel"): o["parallel"] = True
    if old and old.get("replaces_chart_block") and compact_rec.get("po"): o["replaces_chart_block"] = old["replaces_chart_block"]
    return o

d = json.load(open("../blocks/data.json")); lmdate = {k: v.get("y") for k, v in d["lm"].items()}
newrecs = {}   # track -> list of (position, old_id or None, phases, compact records)
n_new = 0
for tr in d["tracks"]:
    for oid, phases in SPLIT.items():
        if not oid.startswith(tr["id"] + "."): continue
        k = next(i for i, p in enumerate(tr["p"]) if p["i"] == oid); old = tr["p"][k]
        recs = [compact(tr["id"], ph, old.get("lm", []), lmdate, j == 0, old) for j, ph in enumerate(phases)]
        tr["p"][k:k + 1] = recs; n_new += len(recs); newrecs.setdefault(tr["id"], []).append((oid, phases, recs))
    if tr["id"] in PREFIX:
        phases = PREFIX[tr["id"]]; recs = [compact(tr["id"], ph, [], lmdate, False, None) for ph in phases]
        tr["p"][0:0] = recs; n_new += len(recs); newrecs.setdefault(tr["id"], []).append((None, phases, recs))
assert set(SPLIT) <= {o for v in newrecs.values() for o, _, _ in v if o}, "a split target was not found"
d["meta"]["v"] = "4.5"
json.dump(d, open("../blocks/data.json", "w"), ensure_ascii=False, separators=(",", ":"))

M = json.load(open("../../data/world_history_timeline_v4_4.json"))
for tr in M["tracks"]:
    for oid, phases, recs in newrecs.get(tr["id"], []):
        if oid:
            k = next(i for i, p in enumerate(tr["periods"]) if p["id"] == oid); old = tr["periods"][k]; applies = old.get("applies_to", [])
            tr["periods"][k:k + 1] = [full(tr["id"], ph, r, applies, old) for ph, r in zip(phases, recs)]
        else:
            applies = tr["periods"][0].get("applies_to", []) if tr["periods"] else []
            tr["periods"][0:0] = [full(tr["id"], ph, r, applies, None) for ph, r in zip(phases, recs)]
newid = {}
for v in newrecs.values():
    for _, _, recs in v:
        for r in recs:
            for x in r.get("lm", []): newid[x] = r["i"]
for l in M.get("landmarks", []):
    if l.get("id") in newid: l["period_id"] = newid[l["id"]]
M["version"] = "4.5"; M.setdefault("changelog", []).append({"version": "4.5", "change": "Early Americas and Africa: long blocks split into documented phases (Archaic, Formative, Olmec, Preclassic Maya, Valdivia to La Tolita, Green and Pastoral Sahara, Tichitt, Kintampo, Bantu homeland and expansion, Khoisan foragers) and empty early centuries filled (Sahel millet farmers, forest foragers, Pastoral Neolithic herders, Ethiopian highland farmers, Amazigh ancestors, San foragers)."})
if isinstance(M.get("meta"), dict): M["meta"]["version"] = "4.5"
json.dump(M, open("../../data/world_history_timeline_v4_5.json", "w"), ensure_ascii=False, indent=1)
print(f"{n_new} periods written ({len(SPLIT)} blocks split, {len(PREFIX)} columns extended); master v4.5")
