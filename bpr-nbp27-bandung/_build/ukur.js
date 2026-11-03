// Mengukur posisi elemen HTML (dalam piksel CSS) untuk menyusun PPTX yang sama dengan PDF.
// Pemakaian: node ukur.js masukan.json keluaran.json
// masukan.json: daftar {nama, html, width, height, selectors: {kunci: "selector CSS"}}
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const hasil = {};
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.width, height: j.height } });
    await page.goto('file://' + path.resolve(j.html), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    hasil[j.nama] = await page.evaluate((sel) => {
      const akar = document.querySelector('.sisi').getBoundingClientRect();
      const kotak = (b) => ({ x: b.left - akar.left, y: b.top - akar.top, w: b.width, h: b.height });
      const out = {};
      for (const [kunci, s] of Object.entries(sel)) {
        out[kunci] = [...document.querySelectorAll(s)].map((el) => {
          const o = kotak(el.getBoundingClientRect());
          // kotak teks langsung (tanpa anak elemen), untuk elemen yang berisi ikon dan teks
          let t = null;
          for (const n of el.childNodes) {
            if (n.nodeType === 3 && n.textContent.trim()) {
              const r = document.createRange();
              r.selectNodeContents(n);
              const b = r.getBoundingClientRect();
              t = t ? { l: Math.min(t.l, b.left), t: Math.min(t.t, b.top), r: Math.max(t.r, b.right), b: Math.max(t.b, b.bottom) }
                : { l: b.left, t: b.top, r: b.right, b: b.bottom };
            }
          }
          if (t) o.teks = kotak({ left: t.l, top: t.t, width: t.r - t.l, height: t.b - t.t });
          o.isi = el.textContent.trim();
          return o;
        });
      }
      return out;
    }, j.selectors);
    await page.close();
  }
  fs.writeFileSync(process.argv[3], JSON.stringify(hasil, null, 1));
  await browser.close();
  console.log('ukur selesai');
})();
