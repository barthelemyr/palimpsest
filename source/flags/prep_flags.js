// Step 1 of the flag sprite: read flag-icons 7.2.3 (MIT) 4x3 SVGs for the codes in codes.json -> imgs.json (data URIs).
// Step 2 is raster.py (Playwright), which draws them into one PNG sprite -> flags.json.
const fs = require('fs'), path = require('path');
const dir = path.join(path.dirname(require.resolve('flag-icons/package.json')), 'flags/4x3');
const codes = JSON.parse(fs.readFileSync('codes.json'));
const out = {};
for (const c of codes) out[c] = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(dir, `${c.toLowerCase()}.svg`)).toString('base64');
fs.writeFileSync('imgs.json', JSON.stringify(out));
console.log(Object.keys(out).length, 'flags');
