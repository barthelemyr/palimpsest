// Step 0 of the map build: Natural Earth 1:50m from world-atlas 2.0.2 (ISC) as GeoJSON, with each country's continent.
// Run from mapdata/topo. Inputs: the world-atlas package (countries-50m.json, land-50m.json).
// Outputs: ne_countries.geojson, ne_countries_cont.geojson (adds properties.cont), ../land50.geojson.
const fs = require('fs'), { feature } = require('topojson-client');
const iso = require('i18n-iso-countries'), { countries } = require('countries-list');
const wa = require('path').dirname(require.resolve('world-atlas/package.json'));
const C = JSON.parse(fs.readFileSync(`${wa}/countries-50m.json`)), L = JSON.parse(fs.readFileSync(`${wa}/land-50m.json`));
const fc = feature(C, C.objects.countries);
fs.writeFileSync('ne_countries.geojson', JSON.stringify(fc));
const cont = { type: 'FeatureCollection', features: fc.features.map((f) => {
  const a2 = f.id ? iso.numericToAlpha2(f.id) : null, c = a2 && countries[a2] ? countries[a2].continent : null;
  return { ...f, properties: { ...f.properties, cont: c } }; }) };
fs.writeFileSync('ne_countries_cont.geojson', JSON.stringify(cont));   // build_continents.py fixes the five without an ISO code
fs.writeFileSync('../land50.geojson', JSON.stringify(feature(L, L.objects.land)));
console.log(fc.features.length, 'countries');
