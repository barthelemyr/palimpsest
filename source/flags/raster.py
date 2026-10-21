import json, base64
from playwright.sync_api import sync_playwright
codes=json.load(open('codes.json')); imgs=json.load(open('imgs.json'))
W,H,COLS=48,36,16
html='<canvas id=c></canvas><script>window.go=async(imgs,codes,W,H,COLS)=>{const c=document.getElementById("c");c.width=W*COLS;c.height=H*Math.ceil(codes.length/COLS);const x=c.getContext("2d");x.imageSmoothingQuality="high";for(let i=0;i<codes.length;i++){const im=new Image();im.src=imgs[codes[i]];await im.decode();x.drawImage(im,(i%COLS)*W,Math.floor(i/COLS)*H,W,H);}return c.toDataURL("image/png");}</script>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.set_content(html)
    url=pg.evaluate('([i,c,W,H,C])=>window.go(i,c,W,H,C)',[imgs,codes,W,H,COLS]); b.close()
open('sprite.png','wb').write(base64.b64decode(url.split(',')[1]))
json.dump({"w":W,"h":H,"cols":COLS,"codes":codes,"png":url.split(',')[1],"src":"flag-icons 7.2.3 (MIT, lipis)"},open('flags.json','w'))
print(len(url)/1e3,'KB base64')
