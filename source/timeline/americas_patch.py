"""Americas patch (v4.1): replace the single 'Pre-colonial era' blocks inherited from the original poster with the
civilisations and cultures they hid. Standard archaeological chronology; marked unsourced until checked.
Applied to both the master dataset (world_history_timeline_v4.json -> _v4_1.json) and the prototype data (proto/data.json)."""
import json, re

def lab(y, approx):
    s = f"{-y} BCE" if y < 0 else f"{y} CE"
    s = s.replace("BCE", "BCE") if True else s
    if abs(y) >= 10000: s = f"{abs(y):,} {'BCE' if y < 0 else 'CE'}"
    return ("c. " if approx else "") + s

# (slug, name, type, start, end, start_approx, end_approx, description, parallel, affiliations, landmarks)
P = {
 "mexico": ("mexico.pre-colonial-era", [
  ("archaic-period", "Archaic period", "archaeological_period", -8000, -1600, 1, 1, "Hunter-gatherers domesticate maize, beans and squash.", 0, None, None),
  ("olmec-civilization", "Olmec civilization", "culture", -1600, -400, 1, 1, "First Mesoamerican civilisation on the Gulf Coast: San Lorenzo, La Venta, colossal heads.", 0, None, None),
  ("late-formative", "Late Formative cities", "historical_period", -400, -100, 1, 1, "Cuicuilco, Monte Albán and the first writing and calendars.", 0, None, None),
  ("teotihuacan", "Teotihuacan", "state", -100, 550, 1, 1, "One of the largest cities in the world; its influence reached the Maya.", 0, None, ["lm.teotihuacan"]),
  ("epiclassic-states", "Epiclassic city-states", "historical_period", 550, 950, 1, 1, "Xochicalco, Cholula, El Tajín and Cacaxtla after Teotihuacan's fall.", 0, None, None),
  ("toltec-state", "Toltec state (Tula)", "state", 950, 1168, 1, 1, "Tula dominates central Mexico; later remembered as a golden age.", 0, None, None),
  ("postclassic-city-states", "Postclassic city-states", "historical_period", 1168, 1428, 1, 0, "Rival altepetl in the Valley of Mexico; Tenochtitlan founded c. 1325.", 0, None, None),
  ("aztec-empire-triple-alliance", "Aztec Empire (Triple Alliance)", "state", 1428, 1521, 1, 0, "Tenochtitlan, Texcoco and Tlacopan rule central Mexico until the Spanish conquest.", 0, None, None),
  ("maya-civilization", "Maya civilization (Yucatán and Chiapas)", "culture", -1000, 1697, 1, 0, "Palenque, Calakmul, Chichén Itzá and Mayapán; the last Maya kingdom, Nojpetén, fell in 1697.", 1, None, ["lm.chichen-itza"]),
  ("zapotec-monte-alban", "Zapotec (Monte Albán)", "state", -500, 850, 1, 1, "Zapotec capital in the Valley of Oaxaca.", 1, None, None),
  ("tarascan-state", "Tarascan (Purépecha) state", "state", 1350, 1530, 1, 0, "Rival the Aztecs never conquered, centred on Tzintzuntzan.", 1, None, None),
 ]),
 "usa": ("usa.pre-colonial-era", [
  ("paleo-indian-clovis", "Paleo-Indian peoples (Clovis)", "peoples", -13000, -8000, 1, 1, "First peoples of the Americas; Clovis big-game hunters.", 0, None, None),
  ("archaic-period", "Archaic period", "archaeological_period", -8000, -1000, 1, 1, "Hunting, gathering and the first mounds (Watson Brake, Poverty Point).", 0, None, None),
  ("woodland-period", "Woodland cultures (Adena, Hopewell)", "culture", -1000, 800, 1, 1, "Pottery, farming and long-distance trade; great earthworks in the Ohio valley.", 0, None, None),
  ("mississippian-culture", "Mississippian culture", "culture", 800, 1607, 1, 0, "Mound-building chiefdoms; Cahokia was the largest city north of Mexico.", 0, None, ["lm.cahokia-mounds"]),
  ("ancestral-puebloans", "Ancestral Puebloans", "culture", 750, 1300, 1, 1, "Great houses and cliff dwellings of the Southwest: Chaco Canyon, Mesa Verde.", 1, None, ["lm.chaco-canyon", "lm.mesa-verde"]),
  ("haudenosaunee-confederacy", "Haudenosaunee Confederacy", "confederation", 1450, 1777, 1, 0, "League of the Five (later Six) Nations around the Great Lakes.", 1, None, None),
 ]),
 "canada": ("canada.pre-colonial-era", [
  ("paleo-and-archaic-peoples", "Paleo-Indian and Archaic peoples", "peoples", -13000, -1000, 1, 1, "First Nations ancestors follow the retreating ice sheets.", 0, None, ["lm.head-smashed-in-buffalo-jump"]),
  ("woodland-and-dorset", "Woodland and Dorset cultures", "culture", -1000, 1000, 1, 1, "Pottery-making Woodland peoples in the south; Dorset Paleo-Inuit in the Arctic.", 0, None, None),
  ("first-nations-and-thule", "First Nations and Thule Inuit", "peoples", 1000, 1608, 1, 0, "Iroquoian farming villages, Plains and coastal nations; Thule ancestors of the Inuit cross the Arctic.", 0, None, None),
  ("norse-lanse-aux-meadows", "Norse at L'Anse aux Meadows", "foreign_rule", 1000, 1025, 1, 1, "Short-lived Viking settlement in Newfoundland.", 1, None, None),
 ]),
 "argentina": ("argentina.pre-colonial-era", [
  ("early-hunter-gatherers", "Early hunter-gatherers", "peoples", -11000, -500, 1, 1, "Patagonian hunters; hand stencils of the Cueva de las Manos.", 0, None, None),
  ("andean-northwest-cultures", "Andean Northwest cultures", "culture", -500, 1000, 1, 1, "Condorhuasi, La Aguada and other farming cultures of the northwest.", 0, None, None),
  ("diaguita-and-regional-peoples", "Diaguita and regional peoples", "peoples", 1000, 1480, 1, 1, "Diaguita towns in the northwest; Guaraní, Querandí and Tehuelche elsewhere.", 0, None, None),
  ("inca-rule-in-the-northwest", "Inca rule in the northwest", "foreign_rule", 1480, 1536, 1, 1, "The Inca road reaches Mendoza.", 0, [["inca_empire", 1480, 1533, "partial (northwest)"]], None),
 ]),
 "brazil": ("brazil.pre-colonial-era", [
  ("paleo-indian-peoples", "Paleo-Indian peoples", "peoples", -11000, -6000, 1, 1, "Rock art of Serra da Capivara; Luzia, one of the oldest skeletons in the Americas.", 0, None, None),
  ("sambaqui-and-archaic", "Sambaqui shell-mound builders", "culture", -6000, 0, 1, 1, "Coastal peoples raise huge shell mounds.", 0, None, None),
  ("amazonian-societies", "Amazonian chiefdoms (Marajoara)", "culture", 0, 1400, 1, 1, "Mound-building chiefdoms on Marajó island and along the Amazon.", 0, None, None),
  ("tupi-guarani-peoples", "Tupi and Guaraní peoples", "peoples", 1000, 1500, 1, 0, "Tupi–Guarani expansion along the coast and rivers.", 0, None, None),
 ]),
 "chile": ("chile.pre-colonial-era", [
  ("monte-verde-and-early-peoples", "Monte Verde and early peoples", "peoples", -14500, -7000, 1, 1, "Monte Verde, one of the oldest human settlements in the Americas.", 0, None, ["lm.monte-verde"]),
  ("chinchorro-culture", "Chinchorro culture", "culture", -7000, -1500, 1, 1, "Fishing people who made the world's oldest artificial mummies.", 0, None, ["lm.chinchorro-mummies"]),
  ("andean-and-mapuche-societies", "Andean and Mapuche societies", "peoples", -1500, 1470, 1, 1, "Atacameño and Diaguita in the north, Mapuche in the south.", 0, None, None),
  ("inca-rule-in-the-north", "Inca rule in the north", "foreign_rule", 1470, 1536, 1, 1, "Inca frontier on the Maule river.", 0, [["inca_empire", 1470, 1533, "partial (north and centre)"]], None),
  ("mapuche-araucania", "Mapuche (Araucanía)", "peoples", 1470, 1883, 1, 0, "Independent Mapuche lands resisted the Inca and Spain until 1883.", 1, None, None),
 ]),
 "venezuela": ("venezuela.pre-colonial-era", [
  ("paleo-indian-peoples", "Paleo-Indian peoples", "peoples", -13000, -1000, 1, 1, "Early hunters of El Jobo.", 0, None, None),
  ("agricultural-chiefdoms", "Agricultural chiefdoms", "peoples", -1000, 1498, 1, 0, "Timoto-Cuica terraces in the Andes; Arawak and Carib peoples in the lowlands.", 0, None, None),
 ]),
 "paraguay": ("paraguay.pre-colonial-era", [("guarani-peoples", "Guaraní peoples", "peoples", -3000, 1537, 1, 0, "Guaraní farming villages; their language is still spoken by most Paraguayans.", 0, None, None)]),
 "uruguay": ("uruguay.pre-colonial-era", [("charrua-and-other-peoples", "Charrúa and other peoples", "peoples", -11000, 1680, 1, 0, "Charrúa, Chaná and Guaraní peoples; cerritos (earth mounds) builders.", 0, None, None)]),
 "guianas": ("guianas.pre-colonial-era", [("arawak-and-carib-peoples", "Arawak and Carib peoples", "peoples", -5000, 1616, 1, 0, "Lokono (Arawak), Kalina (Carib) and Warao peoples.", 0, None, None)]),
 "cuba": ("cuba.pre-colonial-era", [
  ("archaic-peoples", "Archaic peoples", "peoples", -4000, 300, 1, 1, "Fishing and foraging peoples arrive from the mainland.", 0, None, None),
  ("taino-chiefdoms", "Taíno chiefdoms", "peoples", 300, 1511, 1, 0, "Taíno farming chiefdoms (cacicazgos).", 0, None, None)]),
 "dominican_republic": ("dominican_republic.pre-colonial-era", [
  ("archaic-peoples", "Archaic peoples", "peoples", -4000, 600, 1, 1, "First islanders.", 0, None, None),
  ("taino-chiefdoms", "Taíno chiefdoms", "peoples", 600, 1492, 1, 0, "Five cacicazgos ruled Hispaniola when Columbus arrived.", 0, None, None)]),
 "caribbean": ("caribbean.pre-colonial-era", [
  ("archaic-peoples", "Archaic peoples", "peoples", -4000, -500, 1, 1, "First islanders.", 0, None, None),
  ("saladoid-peoples", "Saladoid (Arawak) peoples", "peoples", -500, 1200, 1, 1, "Pottery-making farmers spread through the Lesser Antilles.", 0, None, None),
  ("taino-and-kalinago", "Taíno and Kalinago peoples", "peoples", 1200, 1493, 1, 0, "Taíno in the Greater Antilles and Bahamas, Kalinago in the Lesser Antilles.", 0, None, None)]),
 "central_america": ("central_america.maya-and-isthmo-colombian-societies", [
  ("preclassic-maya", "Preclassic Maya", "culture", -2000, 250, 1, 1, "Villages grow into the first Maya cities.", 0, None, ["lm.joya-de-ceren"]),
  ("classic-maya-city-states", "Classic Maya city-states", "state", 250, 900, 1, 1, "Copán and other kingdoms at their height.", 0, None, ["lm.copan"]),
  ("postclassic-maya-and-lenca", "Postclassic Maya, Pipil and Lenca", "peoples", 900, 1502, 1, 0, "Smaller kingdoms and Nahua (Pipil) migrations.", 0, None, None),
  ("isthmo-colombian-chiefdoms", "Isthmo-Colombian chiefdoms", "peoples", -500, 1502, 1, 0, "Gran Chiriquí, Coclé and Greater Nicoya chiefdoms; gold work and stone spheres.", 1, None, None)]),
}

def full(track, rec, old):
    slug, n, t, s, e, sa, ea, d, par, af, lm = rec
    o = {"id": f"{track}.{slug}", "name": n, "entity_type": t, "temporal_type": "interval", "start": s, "end": e,
         "start_label": lab(s, sa), "end_label": lab(e, ea), "start_approx": bool(sa), "end_approx": bool(ea),
         "duration_years": e - s - (1 if s < 0 < e else 0), "applies_to": old.get("applies_to", []), "description": d,
         "source": "added_v4_1", "verification": "unsourced_standard_chronology"}
    if par: o["parallel"] = True
    if af: o["affiliations"] = [{"empire_id": a[0], "start": a[1], "end": a[2], "extent": a[3], "applies_to": old.get("applies_to", [])} for a in af]
    if lm: o["landmark_ids"] = lm
    if old.get("chart_name") and not par and rec is P[track][1][0]: o["replaces_chart_block"] = {"chart_name": old["chart_name"], "id": old["id"]}
    return o
def compact(track, rec, old):
    slug, n, t, s, e, sa, ea, d, par, af, lm = rec
    o = {"i": f"{track}.{slug}", "n": n, "t": t, "s": s, "e": e, "sl": lab(s, sa), "el": lab(e, ea), "d": d}
    if sa: o["sa"] = 1
    if ea: o["ea"] = 1
    if par: o["par"] = 1
    if af: o["af"] = af
    if lm: o["lm"] = lm
    if old.get("po") and rec is P[track][1][0]: o["po"] = 1; o["cn"] = old.get("cn", "")
    return o

# master
v = json.load(open("../../data/world_history_timeline_v4_5.json"))
for tr in v["tracks"]:
    if tr["id"] not in P: continue
    oid, recs = P[tr["id"]]
    k = next(i for i, p in enumerate(tr["periods"]) if p["id"] == oid)
    old = tr["periods"][k]
    tr["periods"][k:k + 1] = [full(tr["id"], r, old) for r in recs]
v["version"] = "4.1"; v.setdefault("changelog", []).append({"version": "4.1", "change": "Americas: pre-colonial blocks split into the civilisations and cultures they contained (Olmec, Teotihuacan, Toltec, Aztec, Maya, Mississippian, Puebloans, Chinchorro, Taíno and others)."})
json.dump(v, open("../../data/world_history_timeline_v4_1.json", "w"), ensure_ascii=False, indent=1)
# prototype
d = json.load(open("../blocks/data.json"))
n = 0
for tr in d["tracks"]:
    if tr["id"] not in P: continue
    oid, recs = P[tr["id"]]
    k = next(i for i, p in enumerate(tr["p"]) if p["i"] == oid)
    old = tr["p"][k]; tr["p"][k:k + 1] = [compact(tr["id"], r, old) for r in recs]; n += len(recs)
d["meta"]["v"] = "4.1"
json.dump(d, open("../blocks/data.json", "w"), ensure_ascii=False)
print("added", n, "periods in", len(P), "tracks")
