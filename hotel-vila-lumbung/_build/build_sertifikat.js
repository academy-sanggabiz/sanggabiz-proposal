const path = require("path");
const L = require("./lib.js");
const { D, p, makeDoc, save, NAVY, GOLD, MUTED, FONT } = L;
const { Paragraph, TextRun, AlignmentType, BorderStyle, PageOrientation, Table, TableRow, TableCell, WidthType } = D;
const t = (text, o) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: o.after ?? 120 }, children: L.runs(text, { font: FONT, ...o.run }) });
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const kids = [
  t("SERTIFIKAT", { after: 60, run: { bold: true, size: 64, color: NAVY, characterSpacing: 80 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: GOLD, space: 8 } }, children: [new TextRun({ text: "Nomor: [ISI TIM: nomor sertifikat]", font: FONT, size: 20, color: MUTED })] }),
  t("Diberikan kepada", { run: { size: 22, color: MUTED } }),
  t("[ISI TIM: nama peserta]", { after: 40, run: { bold: true, size: 44, color: NAVY } }),
  t("[ISI TIM: jabatan], Hotel Vila Lumbung", { after: 260, run: { size: 22 } }),
  t("atas keikutsertaannya dalam", { run: { size: 22, color: MUTED } }),
  t("Pelatihan Online Account Receivable dan Income Audit Hotel", { after: 80, run: { bold: true, size: 32, color: NAVY } }),
  t("Total 9 jam tatap muka daring dalam tiga sesi, dengan materi pendapatan hotel dan income audit, piutang dan city ledger, invoice, aging, rekonsiliasi pembayaran, dan laporan AR.", { after: 120, run: { size: 19 } }),
  t("Dilaksanakan pada [ISI TIM: tanggal pelaksanaan] Desember 2026", { after: 420, run: { size: 20 } }),
  new Table({ width: { size: 14000, type: WidthType.DXA }, columnWidths: [7000, 7000], rows: [new TableRow({ children: [
    ["Direktur Sanggabiz", "[ISI TIM: nama penandatangan]"], ["Pengajar", "[ISI TIM: nama pengajar]"]].map(([a, b]) => new TableCell({ width: { size: 7000, type: WidthType.DXA }, borders: { top: none, bottom: none, left: none, right: none },
      children: [t(a, { after: 600, run: { size: 19, color: MUTED } }), t(b, { after: 0, run: { bold: true, size: 20 } })] })) })] }),
];
const doc = makeDoc("Contoh Sertifikat", [{ properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1000, bottom: 800, left: 1000, right: 1000 } } }, children: kids }]);
save(doc, path.join(__dirname, "..", "assets", "6 Contoh Sertifikat.docx"));
