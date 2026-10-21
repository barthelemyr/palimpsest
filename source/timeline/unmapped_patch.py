"""Unmapped polities: states, kingdoms and chiefdoms in the timeline that the borders dataset (Cliopatria) does not map.
Each gets an approximate location (capital or core area, lon/lat) as `ul` in proto/data.json (v4.4) and `map_location` in the master.
The site shows one only when, in that year, no Cliopatria polity is recorded at its location, so mapped states never get a duplicate."""
import json
U = {  # period id: (lon, lat)  capital or core area, approximate
 # Americas
 "usa.haudenosaunee-confederacy": (-76.1, 42.9), "mexico.teotihuacan": (-98.84, 19.69), "mexico.toltec-state": (-99.34, 20.06),
 "mexico.aztec-empire-triple-alliance": (-99.13, 19.43), "mexico.zapotec-monte-alban": (-96.77, 17.04), "mexico.tarascan-state": (-101.63, 19.62),
 "guatemala.classic-maya-city-states": (-89.62, 17.22), "guatemala.postclassic-maya-kingdoms": (-91.17, 15.02),
 "peru.wari-and-tiwanaku": (-74.2, -13.06), "peru.chimu-and-regional-kingdoms": (-79.07, -8.11), "bolivia.tiwanaku": (-68.67, -16.55), "bolivia.aymara-lordships": (-68.5, -17.6),
 # Africa
 "egypt.early-dynastic-period": (31.25, 29.85), "egypt.old-kingdom": (31.25, 29.85), "egypt.middle-kingdom": (31.25, 29.6), "egypt.new-kingdom": (32.65, 25.7), "egypt.late-period": (30.75, 30.95),
 "sudan.kingdom-of-kush-napata": (31.83, 18.54), "sudan.kingdom-of-kush-meroe": (33.75, 16.94), "sudan.christian-nubian-kingdoms": (30.47, 18.22),
 "ethiopia.kingdom-of-d-mt": (39.02, 14.29), "ethiopia.kingdom-of-aksum": (38.72, 14.13), "ethiopia.post-aksumite-and-zagwe-dynasty": (39.04, 12.03), "ethiopia.ethiopian-empire-solomonic": (37.47, 12.6),
 "libya.garamantes": (13.05, 26.55), "mali.sosso-kingdom": (-7.2, 13.4), "nigeria.sokoto-caliphate-and-southern-kingdoms": (5.24, 13.06),
 "zimbabwe.mapungubwe": (29.24, -22.19), "zimbabwe.kingdom-of-zimbabwe": (30.93, -20.27), "zimbabwe.mutapa-and-rozvi-states": (31.3, -16.6), "zimbabwe.matabele-kingdom": (28.58, -20.15),
 "south_africa.swazi-kingdom": (31.4, -26.5), "south_africa.basotho-kingdom": (27.9, -29.5),
 "morocco.mauretania-and-phoenician-posts": (-5.55, 34.07), "algeria.numidia-and-carthaginian-posts": (6.61, 36.37), "morocco.almoravid-empire": (-7.99, 31.63),
 "swahili_coast.swahili-city-states": (39.51, -8.96), "swahili_coast.omani-sultanate-and-zanzibar": (39.19, -6.16),
 "madagascar.malagasy-kingdoms": (47.52, -18.91), "madagascar.kingdom-of-madagascar": (47.52, -18.91),
 "senegambia.takrur-and-mali-era-states": (-14.2, 16.4), "senegambia.jolof-empire-and-coastal-kingdoms": (-15.4, 15.4),
 "west_sahara_mauritania.sanhaja-and-hassani-emirates": (-11.4, 20.5),
 "guinea_coast.akan-mossi-and-aja-fon-states": (-1.5, 9.5), "guinea_coast.asante-dahomey-and-mossi-kingdoms": (-1.62, 6.69),
 "central_sahel.kanembornu-empire-and-hausa-and-tuareg-states": (13.2, 12.9), "central_africa.kingdoms-and-sultanates": (19.0, 11.5),
 "congo.kingdom-of-kongo": (14.24, -6.27), "great_lakes.kitara-and-chwezi-states": (31.4, 0.9), "great_lakes.kingdoms-of-buganda-bunyoro-rwanda-and-burundi": (32.58, 0.32),
 "zambia_malawi.maravi-kazembe-and-lozi-kingdoms": (30.5, -12.5),
 "horn_of_africa.islamic-sultanates": (43.5, 10.4), "horn_of_africa.adal-ajuran-and-the-ottoman-coast": (42.12, 9.31), "horn_of_africa.eritrean-highlands-and-coast": (38.93, 15.33),
 # Near East and Arabia
 "turkey.hittite-empire": (34.61, 40.02), "turkey.neo-hittite-kingdoms": (38.0, 36.83), "turkey.kingdom-of-lydia": (28.04, 38.49),
 "iraq.old-babylonian-kingdom": (44.42, 32.54), "iraq.kassite-babylon": (44.42, 32.54), "iraq.assyrian-empire": (43.26, 35.46), "iran.median-empire": (48.51, 34.8),
 "levant.canaanite-city-states": (35.5, 33.0), "arabia.kingdom-of-saba": (45.33, 15.42), "arabia.kingdom-of-himyar": (44.41, 14.2), "arabia.nabataean-kingdom": (35.44, 30.33),
 "arabia.oman-imamates-and-sultanate": (57.5, 23.0), "arabia.yemeni-imamates-and-dynasties": (44.2, 15.35), "arabia.sharifate-of-mecca": (39.83, 21.42), "arabia.saudi-states-in-najd": (46.57, 24.73),
 "cyprus.city-kingdoms": (33.4, 35.1), "cyprus.lusignan-kingdom-of-cyprus": (33.36, 35.17),
 # Caucasus, Central and South Asia
 "georgia.bagrationi-unification": (44.8, 41.7), "armenia.orontid-armenia": (44.5, 40.0), "armenia.artaxiad-kingdom": (44.6, 39.95), "armenia.arsacid-armenia": (44.6, 39.95),
 "azerbaijan.caucasian-albania-and-atropatene": (47.3, 40.9), "azerbaijan.azerbaijani-khanates": (48.0, 40.4),
 "central_asia.yuezhi-and-kushan-empire": (68.0, 37.3), "central_asia.turkic-khaganates": (71.0, 43.0), "central_asia.uzbek-and-kazakh-khanates": (64.42, 39.77),
 "afghanistan.greco-bactrian-and-indo-greek-kingdoms": (66.9, 36.76), "afghanistan.ghurid-empire": (64.52, 34.39), "afghanistan.hotak-and-durrani-empires": (65.71, 31.61),
 "bangladesh.pala-and-sena-dynasties": (88.5, 25.0), "sri_lanka.anuradhapura-kingdom": (80.4, 8.35), "sri_lanka.polonnaruwa-kingdom": (81.0, 7.94), "sri_lanka.maldive-sultanate": (73.51, 4.18),
 "himalaya.licchavi-kingdom": (85.32, 27.7), "himalaya.zhabdrung-and-desi-rule": (89.64, 27.47), "himalaya.kingdom-of-nepal": (85.32, 27.7),
 "mongolia.xianbei-and-rouran": (104.0, 46.0), "mongolia.turkic-and-uyghur-khaganates": (102.7, 47.4),
 # East and Southeast Asia, Pacific
 "china.xia-dynasty": (112.7, 34.7), "korea.unified-silla-and-balhae": (129.2, 35.8), "japan.yamato-state": (135.8, 34.5), "taiwan.kingdom-of-tungning": (120.2, 23.0),
 "vietnam.au-lac-and-nanyue": (105.85, 21.1), "vietnam.champa": (108.3, 15.8), "vietnam.ai-viet-dynasties": (105.85, 21.03),
 "indonesia.early-hindu-buddhist-kingdoms": (107.0, -6.5), "indonesia.sailendra-and-mataram-java": (110.2, -7.6),
 "myanmar.toungoo-dynasty": (96.48, 17.33), "laos.three-lao-kingdoms": (102.6, 17.97), "malaysia.malacca-sultanate": (102.25, 2.19),
 "brunei.bruneian-sultanate": (114.94, 4.89), "singapore.temasek-and-singapura": (103.85, 1.29),
 "polynesia.chiefdoms-and-island-kingdoms": (-175.2, -21.1), "polynesia.european-contact-and-polynesian-kingdoms": (-157.9, 21.3),
 "micronesia.chiefdoms-and-stone-cultures": (158.33, 6.84),
 # Europe and Mediterranean (shown only where the borders dataset is empty)
 "austria.celtic-kingdom-of-noricum": (14.4, 46.9), "greece.classical-greek-city-states": (23.73, 37.98), "ukraine.cossack-hetmanate": (32.88, 51.34),
 "malta.order-of-st-john": (14.51, 35.9), "montenegro.duklja": (19.1, 42.3),
}
if __name__ == "__main__":
    d = json.load(open("../blocks/data.json")); found = set()
    for t in d["tracks"]:
        for p in t["p"]:
            if p["i"] in U: p["ul"] = list(U[p["i"]]); found.add(p["i"])
            else: p.pop("ul", None)
    miss = sorted(set(U) - found); assert not miss, miss
    d["meta"]["v"] = "4.4"
    json.dump(d, open("../blocks/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
    M = json.load(open("../../data/world_history_timeline_v4_3.json")); k = 0
    def walk(o):
        global k
        if isinstance(o, dict):
            if o.get("id") in U and isinstance(o.get("name"), str):
                lo, la = U[o["id"]]; o["map_location"] = {"lon": lo, "lat": la, "precision": "approximate capital or core area", "reason": "not mapped by Cliopatria"}; k += 1
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(M)
    if isinstance(M.get("meta"), dict): M["meta"]["version"] = "4.4"
    json.dump(M, open("../../data/world_history_timeline_v4_4.json", "w"), ensure_ascii=False, indent=1)
    print(f"unmapped polities located: {len(found)}; master {k}")
