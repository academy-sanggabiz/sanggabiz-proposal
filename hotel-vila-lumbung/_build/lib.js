// Penolong pembuat docx Sanggabiz. NODE_PATH=$(npm root -g) node build_xxx.js
const fs = require("fs");
const path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Footer, AlignmentType, BorderStyle,
  WidthType, ShadingType, HeightRule, PageNumber, LevelFormat, VerticalAlign, TabStopType, PageOrientation } = D;

const NAVY = "0B396D", GOLD = "FFC00C", INK = "1D1D1F", MUTED = "5C5F66", LINE = "C9D2DE";
const FONT = "Montserrat";

function runs(text, base = {}) {
  const out = [];
  const re = /(\[ISI TIM:[^\]]*\])|(\*\*[^*]+\*\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    if (m[1]) out.push(new TextRun({ text: m[1], ...base, bold: true, shading: { type: ShadingType.CLEAR, fill: "FFF200", color: "auto" }, color: INK }));
    else out.push(new TextRun({ text: m[2].slice(2, -2), ...base, bold: true }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const p = (text, o = {}) => new Paragraph({
  children: runs(text, o.run || {}), alignment: o.align || AlignmentType.LEFT,
  spacing: { after: o.after ?? 110, before: o.before ?? 0, line: o.line ?? 290 }, keepNext: o.keepNext, indent: o.indent, pageBreakBefore: o.pageBreakBefore,
});
const h1 = (text, pb = false) => new Paragraph({ heading: "Heading1", children: [new TextRun({ text })], pageBreakBefore: pb, keepNext: true });
const h2 = (text) => new Paragraph({ heading: "Heading2", children: [new TextRun({ text })], keepNext: true });
const h3 = (text) => new Paragraph({ children: [new TextRun({ text, bold: true, size: 20, color: NAVY })], spacing: { before: 200, after: 90 }, keepNext: true });
const bullet = (text) => new Paragraph({ numbering: { reference: "bul", level: 0 }, children: runs(text), spacing: { after: 70, line: 290 } });
const num = (text, ref = "num") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(text), spacing: { after: 70, line: 290 } });
const caption = (text) => new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, size: 17, color: INK })], spacing: { after: 180 } });
const spacer = (n = 120) => new Paragraph({ spacing: { after: n }, children: [] });

const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(content, width, o = {}) {
  const lines = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, columnSpan: o.span,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    verticalAlign: o.valign || VerticalAlign.TOP, margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children: lines.map((t) => new Paragraph({
      alignment: o.align || AlignmentType.LEFT, spacing: { after: 30, line: 260 },
      children: runs(t, { size: o.size || 17, bold: o.bold, color: o.color || INK }),
    })),
  });
}
function table(widths, header, rows, o = {}) {
  const head = new TableRow({ tableHeader: true, cantSplit: true,
    children: header.map((t, i) => cell(t, widths[i], { fill: NAVY, color: "FFFFFF", bold: true, size: 16 })) });
  const total = widths.reduce((a, b) => a + b, 0);
  const body = rows.map((r, ri) => {
    if (r && r.group) return new TableRow({ cantSplit: true, children: [cell(r.group, total, { fill: "DCE6F2", bold: true, span: widths.length })] });
    return new TableRow({ cantSplit: !o.split, children: r.map((c, i) => cell(c && c.text !== undefined ? c.text : c, widths[i], {
      fill: c && typeof c.bg === "string" ? c.bg : (i === 0 && o.firstFill ? "F2F5FA" : (ri % 2 ? "F7F9FC" : undefined)),
      align: o.align && o.align[i], size: o.size, bold: (c && typeof c === "object" && !Array.isArray(c) && c.bold === true) || (i === 0 && o.firstBold) })) });
  });
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
const fmt = (n) => "Rp " + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

function cover(W, kicker, title, subtitle, stats, foot) {
  const none = { style: BorderStyle.NONE, size: 0, color: NAVY };
  return [
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({
      height: { value: 11800, rule: HeightRule.EXACT },
      children: [new TableCell({ width: { size: W, type: WidthType.DXA }, shading: { fill: NAVY, type: ShadingType.CLEAR, color: "auto" },
        borders: { top: none, bottom: none, left: none, right: none }, margins: { top: 500, bottom: 400, left: 560, right: 560 },
        children: [
          new Paragraph({ spacing: { after: 2400 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(__dirname, "assets", "logo_white.png")), transformation: { width: 150, height: 30 } })] }),
          new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: kicker, font: FONT, bold: true, size: 20, color: GOLD, characterSpacing: 60 })] }),
          new Paragraph({ spacing: { after: 240, line: 400, lineRule: "atLeast" }, children: [new TextRun({ text: title, font: FONT, bold: true, size: 50, color: "FFFFFF" })] }),
          new Paragraph({ spacing: { after: 2200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: GOLD, space: 14 } }, children: [new TextRun({ text: subtitle, font: FONT, size: 24, color: "DCE6F2" })] }),
          new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: foot[0], font: FONT, bold: true, size: 22, color: "FFFFFF" })] }),
          new Paragraph({ children: [new TextRun({ text: foot[1], font: FONT, size: 22, color: "DCE6F2" })] }),
        ] })] })] }),
    spacer(300),
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [Math.floor(W / 3), Math.floor(W / 3), W - 2 * Math.floor(W / 3)],
      rows: [new TableRow({ children: stats.map(([a, b], i) => new TableCell({
        width: { size: Math.floor(W / 3) + (i === 2 ? W - 3 * Math.floor(W / 3) : 0), type: WidthType.DXA },
        borders: { top: { style: BorderStyle.SINGLE, size: 18, color: GOLD }, bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" } },
        margins: { top: 120, bottom: 60, left: 120, right: 160 },
        children: [new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: a, bold: true, size: 26, color: NAVY })] }),
          new Paragraph({ children: [new TextRun({ text: b, size: 17, color: MUTED })] })] })) })] }),
  ];
}
function footer(W, label) {
  return new Footer({ children: [new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 6 } },
    tabStops: [{ type: TabStopType.RIGHT, position: W }],
    children: [new TextRun({ text: "Sanggabiz  |  " + label, size: 14, color: MUTED }), new TextRun({ text: "\t", size: 14 }),
      new TextRun({ children: ["Halaman ", PageNumber.CURRENT], size: 14, color: MUTED })] })] });
}
function makeDoc(title, sections, extraNumbering = []) {
  return new Document({
    creator: "Sanggabiz", title,
    styles: {
      default: { document: { run: { font: FONT, size: 19, color: INK } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 30, bold: true, color: NAVY },
          paragraph: { spacing: { before: 0, after: 200 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: GOLD, space: 6 } } } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 22, bold: true, color: NAVY },
          paragraph: { spacing: { before: 240, after: 110 }, outlineLevel: 1 } },
      ],
    },
    numbering: { config: [
      { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 260 } } } }] },
      ...["num", "num2", "num3", "num4", "num5", "num6", "num7", "num8"].map((r) => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } } } }] })),
      ...extraNumbering ] },
    sections,
  });
}
const save = (doc, file) => Packer.toBuffer(doc).then((b) => { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, b); console.log("ditulis:", file); });

module.exports = { D, p, h1, h2, h3, bullet, num, caption, spacer, cell, table, fmt, cover, footer, makeDoc, save, runs, NAVY, GOLD, INK, MUTED, LINE, FONT };
