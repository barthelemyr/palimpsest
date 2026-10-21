"""Today's borders overlay: Natural Earth 1:50m admin-0 (public domain), internal borders as one mesh + label anchors."""
import json, base64, gzip, math
from shapely.geometry import shape
from shapely.validation import make_valid
from shapely.ops import polylabel
GRID=20.0
class VS:
    def __init__(s): s.b=bytearray()
    def u(s,v):
        while v>=0x80: s.b.append((v&0x7F)|0x80); v>>=7
        s.b.append(v)
    def i(s,v): s.u((v<<1) if v>=0 else ((-v<<1)-1))
lines=json.load(open('topo/today_mesh.json'))
vs=VS(); vs.u(len(lines)); px=py=0
for l in lines:
    pts=[(round(x*GRID),round(y*GRID)) for x,y in l]
    ded=[pts[0]]+[p for k,p in enumerate(pts[1:],1) if p!=pts[k-1]]
    vs.u(len(ded))
    for x,y in ded: vs.i(x-px); vs.i(y-py); px,py=x,y
SHORT={"United States of America":"United States","Dem. Rep. Congo":"DR Congo","Central African Rep.":"Central African Rep.","Bosnia and Herz.":"Bosnia and Herz.","Russia":"Russia"}
labs=[]
for f in json.load(open('ne_countries_proj.geojson'))['features']:
    g=shape(f['geometry'])
    if not g.is_valid: g=make_valid(g)
    polys=[g] if g.geom_type=='Polygon' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='Polygon']
    if not polys: continue
    lp=max(polys,key=lambda q:q.area)
    if lp.area<4: continue
    c=polylabel(lp,tolerance=max(0.05,math.sqrt(lp.area)/60))
    r=lp.exterior.distance(c) if lp.contains(c) else 0.5
    nm=f['properties']['name']; labs.append([SHORT.get(nm,nm),round(c.x,1),round(c.y,1),round(r,1),round(lp.area)])
labs.sort(key=lambda l:-l[4])
out={"lines":base64.b64encode(gzip.compress(bytes(vs.b),9)).decode(),"labels":labs,"src":"Natural Earth 1:50m admin-0 countries (public domain)"}
s=json.dumps(out,ensure_ascii=False,separators=(",",":")); open('today.json','w').write(s); print(len(labs),'labels',len(s)/1e3,'KB')
