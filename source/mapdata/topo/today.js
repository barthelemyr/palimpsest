const fs=require('fs'),{topology}=require('topojson-server'),S=require('topojson-simplify'),{mesh}=require('topojson-client');
const fc=JSON.parse(fs.readFileSync('../ne_countries_proj.geojson'));
let t=topology({c:fc},1e6); t=S.presimplify(t); t=S.simplify(t,0.08);
const m=mesh(t,t.objects.c,(a,b)=>a!==b);
fs.writeFileSync('today_mesh.json',JSON.stringify(m.coordinates));
let n=0;m.coordinates.forEach(l=>n+=l.length);console.log('lines',m.coordinates.length,'pts',n);
