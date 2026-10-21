// Shared-arc topology of all Cliopatria outlines + Natural Earth land, with Visvalingam weights.
const fs=require('fs'),{topology}=require('topojson-server'),S=require('topojson-simplify');
const c=JSON.parse(fs.readFileSync('clio_proj.geojson')), l=JSON.parse(fs.readFileSync('land_proj.geojson'));
const p=S.presimplify(topology({c,l},1e6));
fs.writeFileSync('topo_w.json',JSON.stringify(p));
let n=0;p.arcs.forEach(a=>n+=a.length);console.log('arcs',p.arcs.length,'points',n);
