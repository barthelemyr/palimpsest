"""Step 1 of the map build: project Cliopatria, Natural Earth countries and Natural Earth land to Equal Earth
(units x1000, y pointing down), with antimeridian and pole fixes, as planar GeoJSON for the TopoJSON step.

Inputs (cwd = mapdata/):
  raw/cliopatria_polities_only_v021.geojson   Cliopatria v0.2.1 (unzip cliopatria/cliopatria.geojson.zip)
  topo/ne_countries.geojson                   Natural Earth 1:50m admin-0, from world-atlas 2.0.2 (countries-50m.json via topojson-client)
  land50.geojson                              Natural Earth 1:50m land, from world-atlas 2.0.2 (land-50m.json via topojson-client)
Outputs:
  topo/clio_proj.geojson, ne_countries_proj.geojson, topo/land_proj.geojson

Rewritten on 20 October 2026 (the original one-off run was not saved) and checked against the files used for v0.1:
13,742 of 13,797 Cliopatria shapes and 240 of 241 countries are identical. The other 55 shapes differ only in where
a repaired ring starts (one vertex), and Antarctica's pole edge (one land part) differs slightly: no visible effect."""
import json, sys
sys.argv = sys.argv[:1]
exec(open("build_map.py").read().split("def encode")[0])   # proj, fix_ring, project_geom, clean
from shapely.geometry import mapping

def mp(g): return {"type": "MultiPolygon", "coordinates": [mapping(p)["coordinates"] for p in clean(project_geom(g))]}
def fc(feats): return {"type": "FeatureCollection", "features": feats}

clio = json.load(open("raw/cliopatria_polities_only_v021.geojson"))["features"]
json.dump(fc([{"type": "Feature", "id": i, "properties": {}, "geometry": mp(f["geometry"])} for i, f in enumerate(clio)]), open("topo/clio_proj.geojson", "w"))
ne = json.load(open("topo/ne_countries.geojson"))["features"]
json.dump(fc([{"type": "Feature", "properties": {"name": f["properties"]["name"]}, "geometry": mp(f["geometry"])} for f in ne]), open("ne_countries_proj.geojson", "w"))
land = json.load(open("land50.geojson"))["features"]
parts = [c for f in land for c in mp(f["geometry"])["coordinates"]]
json.dump(fc([{"type": "Feature", "properties": {}, "geometry": {"type": "MultiPolygon", "coordinates": parts}}]), open("topo/land_proj.geojson", "w"))
print(len(clio), "Cliopatria shapes,", len(ne), "countries,", len(parts), "land parts")
