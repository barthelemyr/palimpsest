"""v4.2: exact English Wikipedia article for every event and achievement (field 'wikipedia' in the master, 'wp' in the prototype).
Titles chosen by Claude; verify periodically (articles get renamed)."""
import json
EV = {"Austronesian expansion": "Austronesian peoples", "Bantu expansion": "Bantu expansion", "Late Bronze Age collapse": "Late Bronze Age collapse",
 "Axial Age": "Axial Age", "Greco-Persian Wars": "Greco-Persian Wars", "Punic Wars": "Punic Wars", "Silk Road trade": "Silk Road",
 "Spread of Christianity": "Early Christianity", "Plague of Justinian": "Plague of Justinian", "Rise and spread of Islam": "Spread of Islam",
 "Viking expansion": "Viking expansion", "Crusades": "Crusades", "Mongol conquests": "Mongol invasions and conquests", "Black Death": "Black Death",
 "Ming treasure voyages": "Ming treasure voyages", "Fall of Constantinople": "Fall of Constantinople",
 "Conquest of the Americas and epidemics": "European colonization of the Americas", "Atlantic slave trade": "Atlantic slave trade",
 "Protestant Reformation": "Reformation", "Thirty Years' War": "Thirty Years' War", "Industrial Revolution": "Industrial Revolution",
 "American Revolution": "American Revolution", "French Revolution": "French Revolution", "Haitian Revolution": "Haitian Revolution",
 "Abolition of slavery in the Atlantic world": "Abolitionism", "Napoleonic Wars": "Napoleonic Wars",
 "Spanish American wars of independence": "Spanish American wars of independence", "Emancipation of the serfs": "Emancipation reform of 1861",
 "Paraguayan War": "Paraguayan War", "War of the Pacific": "War of the Pacific", "Scramble for Africa": "Scramble for Africa",
 "First World War": "World War I", "Armenian Genocide": "Armenian genocide", "Russian Revolution": "Russian Revolution",
 "1918 influenza pandemic": "Spanish flu", "League of Nations": "League of Nations", "Chinese Civil War": "Chinese Civil War",
 "Great Depression": "Great Depression", "Second World War": "World War II", "The Holocaust": "The Holocaust", "United Nations": "United Nations",
 "Decolonization of Asia and Africa": "Decolonization", "Partition of India": "Partition of India", "Cold War": "Cold War",
 "Universal Declaration of Human Rights": "Universal Declaration of Human Rights", "Korean War": "Korean War", "Vietnam War": "Vietnam War",
 "Antarctic Treaty": "Antarctic Treaty System", "Iranian Revolution": "Iranian Revolution", "HIV/AIDS pandemic": "HIV/AIDS",
 "End of communist rule in Europe": "Revolutions of 1989", "End of apartheid": "Negotiations to end apartheid in South Africa",
 "Breakup of Yugoslavia": "Breakup of Yugoslavia", "Rwandan genocide": "Rwandan genocide",
 "COVID-19 public health emergency of international concern": "COVID-19 pandemic"}
ACH = {"Maize Cultivation": "Maize", "The Wheel": "Wheel", "Writing (cuneiform)": "Cuneiform", "Pyramids": "Egyptian pyramids",
 "Urban sanitation and planning": "Mohenjo-daro", "Code of Hammurabi": "Code of Hammurabi", "Alphabet": "Alphabet", "Olympic Games": "Ancient Olympic Games",
 "Birth of Democracy": "Athenian democracy", "Yoga": "Yoga", "Royal Road and postal relay": "Royal Road", "Papermaking": "Papermaking",
 "Maya Astronomy": "Maya astronomy", "Justinian Code": "Corpus Juris Civilis", "The Concept of Zero": "0", "Algebra (al-Khwarizmi)": "Al-Khwarizmi",
 "Gunpowder": "Gunpowder", "Compass": "Compass", "Renaissance": "Renaissance", "Printing Press": "Printing press", "Hangul alphabet": "Hangul",
 "European arrival in the Americas (Columbus)": "Voyages of Christopher Columbus", "Route to India": "Vasco da Gama",
 "Heliocentric model (Copernicus)": "Copernican heliocentrism", "Laws of Motion & Gravity": "Newton's laws of motion", "Watt's Steam Engine": "Watt steam engine",
 "Classical Music": "Classical period (music)", "Rights of Man": "Declaration of the Rights of Man and of the Citizen", "Metric System": "Metric system",
 "Vaccination": "Vaccination", "Natural Selection": "Natural selection", "Tango": "Tango", "Automobile": "Benz Patent-Motorwagen",
 "Special Relativity": "Special relativity", "Discovery of Insulin": "Insulin", "Penicillin": "Penicillin", "Digital Revolution": "Digital Revolution",
 "Lean Manufacturing": "Lean manufacturing", "First artificial satellite (Sputnik)": "Sputnik 1", "Bullet Train": "Shinkansen", "Moon Landing": "Apollo 11",
 "Smallpox eradication": "Smallpox", "World Wide Web": "World Wide Web", "Wi-Fi Innovation": "Wi-Fi"}
d = json.load(open("proto/data.json")); n = 0
for e in d["ev"]:
    if e["n"] in EV: e["wp"] = EV[e["n"]]; n += 1
for a in d["ach"]:
    if a["n"] in ACH: a["wp"] = ACH[a["n"]]; n += 1
d["meta"]["v"] = "4.2"; json.dump(d, open("proto/data.json", "w"), ensure_ascii=False)
v = json.load(open("world_history_timeline_v4_1.json"))
for k, M in (("events", EV), ("achievements", ACH)):
    for x in v.get(k, []):
        if x.get("name") in M: x["wikipedia"] = "https://en.wikipedia.org/wiki/" + M[x["name"]].replace(" ", "_")
v["version"] = "4.2"; v.setdefault("changelog", []).append({"version": "4.2", "change": "Wikipedia article added to every event and achievement."})
json.dump(v, open("world_history_timeline_v4_2.json", "w"), ensure_ascii=False, indent=1)
print("linked", n, "of", len(d["ev"]) + len(d["ach"]), "| master keys:", [k for k in v if k in ("events", "achievements")])
