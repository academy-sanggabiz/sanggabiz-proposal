// Render HTML ke PDF dan PNG dengan Chromium bawaan Playwright.
// Pemakaian: node render.js jobs.json
// jobs.json berisi daftar {html, pdf, png, width, height, format, landscape, scale}
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const ctx = await browser.newContext({
      viewport: { width: j.width || 794, height: j.height || 1123 },
      deviceScaleFactor: j.scale || 2,
    });
    const page = await ctx.newPage();
    await page.goto('file://' + path.resolve(j.html), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    if (j.pdf) {
      const opt = { path: j.pdf, printBackground: true, preferCSSPageSize: true };
      await page.pdf(opt);
    }
    if (j.png) {
      await page.screenshot({ path: j.png, fullPage: !!j.fullPage });
    }
    await ctx.close();
    console.log('ok', j.pdf || j.png);
  }
  await browser.close();
})();
