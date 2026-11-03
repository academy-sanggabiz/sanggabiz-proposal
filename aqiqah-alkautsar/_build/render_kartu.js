// Membuat gambar dan PDF kartu saku dari kartu_saku.html. Jalankan: node render_kartu.js
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const html = "file://" + path.join(__dirname, "kartu_saku.html");
  const browser = await chromium.launch();

  // PNG resolusi tinggi untuk ditempel di proposal
  const page = await browser.newPage({ deviceScaleFactor: 4, viewport: { width: 900, height: 700 } });
  await page.goto(html);
  await page.evaluate(() => document.fonts.ready);
  for (const id of ["depan", "belakang"]) {
    await page.locator("#" + id).screenshot({ path: path.join(__dirname, "assets", `kartu-saku-${id}.png`), omitBackground: true });
  }

  // PDF siap cetak, satu sisi per halaman, ukuran A6, 105 x 148 mm
  const pdfPage = await browser.newPage();
  await pdfPage.goto(html);
  await pdfPage.addStyleTag({ content: "body{padding:0;display:block;background:#fff} .card{box-shadow:none;border-radius:0;page-break-after:always}" });
  await pdfPage.evaluate(() => document.fonts.ready);
  await pdfPage.pdf({
    path: path.join(__dirname, "..", "aset", "Kartu Saku CS - 5 Langkah Chat Closing (contoh).pdf"),
    width: "105mm", height: "148mm", printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();
  console.log("kartu saku selesai");
})();
