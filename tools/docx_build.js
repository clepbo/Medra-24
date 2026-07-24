const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, PageBreak, LevelFormat, TabStopType, ImageRun
} = require('docx');
const LOGO_PNG = '/home/user/Medra-24/brand/png/medra-logo-primary.png';

const md = fs.readFileSync(process.argv[2], 'utf8');
const lines = md.split('\n');

const NAVY = '1B3A5B';
const TEAL = '2E8B9E';
const LIGHT = 'EAF1F5';
const GREY = '666666';
const CONTENT_WIDTH = 9360; // DXA within Letter margins (12240 - 2*1440)

// ---- inline parser: **bold**, *italic*, `code` ----
function parseInline(text, base = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith('**')) runs.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else if (tok.startsWith('`')) runs.push(new TextRun({ text: tok.slice(1, -1), font: 'Consolas', ...base }));
    else runs.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = re.lastIndex;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), ...base }));
  if (runs.length === 0) runs.push(new TextRun({ text: '', ...base }));
  return runs;
}

function splitRow(line) {
  let s = line.trim().replace(/^\|/, '').replace(/\|$/, '');
  return s.split('|').map(c => c.trim());
}

function isTableSep(line) {
  return /^\|?[\s:\-|]+\|?$/.test(line) && line.includes('-');
}

function makeTable(rows) {
  const header = rows[0];
  const body = rows.slice(1);
  const ncol = header.length;
  const colW = Math.floor(CONTENT_WIDTH / ncol);
  const widths = Array(ncol).fill(colW);
  widths[ncol - 1] = CONTENT_WIDTH - colW * (ncol - 1);

  const border = { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' };
  const borders = { top: border, bottom: border, left: border, right: border,
    insideHorizontal: border, insideVertical: border };

  function cell(text, i, opts = {}) {
    const align = /^[-–—✅⚠️]+$/.test(text) || /^\d+%?$/.test(text) ? AlignmentType.CENTER : AlignmentType.LEFT;
    return new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      shading: opts.shade ? { type: ShadingType.CLEAR, fill: opts.shade, color: 'auto' } : undefined,
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({
        alignment: align,
        spacing: { after: 0 },
        children: parseInline(text, opts.run || {})
      })]
    });
  }

  const trs = [];
  trs.push(new TableRow({
    tableHeader: true,
    children: header.map((t, i) => cell(t, i, { shade: NAVY, run: { bold: true, color: 'FFFFFF' } }))
  }));
  body.forEach((r, ri) => {
    const cells = [];
    for (let i = 0; i < ncol; i++) cells.push(cell(r[i] || '', i, { shade: ri % 2 ? LIGHT : 'FFFFFF' }));
    trs.push(new TableRow({ children: cells }));
  });

  return new Table({
    columnWidths: widths,
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    borders,
    rows: trs
  });
}

const children = [];
let i = 0;

function hr() {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 1 } },
    children: [new TextRun('')]
  });
}

while (i < lines.length) {
  let line = lines[i];
  const t = line.trim();

  if (t === '') { i++; continue; }

  // horizontal rule
  if (t === '---') { children.push(hr()); i++; continue; }

  // headings
  if (t.startsWith('### ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 180, after: 60 },
      children: parseInline(t.slice(4)) }));
    i++; continue;
  }
  if (t.startsWith('## ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 80 },
      children: parseInline(t.slice(3)) }));
    i++; continue;
  }
  if (t.startsWith('# ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 120, after: 120 },
      children: parseInline(t.slice(2)) }));
    i++; continue;
  }

  // table
  if (t.startsWith('|') && i + 1 < lines.length && isTableSep(lines[i + 1])) {
    const rows = [];
    rows.push(splitRow(lines[i]));
    i += 2; // skip header + sep
    while (i < lines.length && lines[i].trim().startsWith('|')) {
      rows.push(splitRow(lines[i])); i++;
    }
    children.push(makeTable(rows));
    children.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun('')] }));
    continue;
  }

  // blockquote
  if (t.startsWith('> ')) {
    const buf = [];
    while (i < lines.length && lines[i].trim().startsWith('>')) {
      buf.push(lines[i].trim().replace(/^>\s?/, '')); i++;
    }
    children.push(new Paragraph({
      spacing: { before: 80, after: 80 },
      indent: { left: 360 },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: TEAL, space: 12 } },
      shading: { type: ShadingType.CLEAR, fill: LIGHT, color: 'auto' },
      children: parseInline(buf.join(' '), { italics: true, color: '333333' })
    }));
    continue;
  }

  // bullet list
  if (/^[-*] /.test(t)) {
    while (i < lines.length && /^\s*[-*] /.test(lines[i])) {
      const raw = lines[i];
      const indent = raw.match(/^\s*/)[0].length;
      const level = indent >= 2 ? 1 : 0;
      children.push(new Paragraph({
        bullet: { level },
        spacing: { after: 40 },
        children: parseInline(raw.trim().replace(/^[-*] /, ''))
      }));
      i++;
    }
    continue;
  }

  // numbered list
  if (/^\d+\. /.test(t)) {
    while (i < lines.length && /^\s*\d+\. /.test(lines[i])) {
      children.push(new Paragraph({
        numbering: { reference: 'num', level: 0 },
        spacing: { after: 40 },
        children: parseInline(lines[i].trim().replace(/^\d+\. /, ''))
      }));
      i++;
    }
    continue;
  }

  // normal paragraph
  children.push(new Paragraph({ spacing: { after: 100 }, children: parseInline(t) }));
  i++;
}

// ---- Cover page ----
const cover = [
  new Paragraph({ spacing: { before: 2200, after: 0 }, alignment: AlignmentType.CENTER,
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(LOGO_PNG),
      transformation: { width: 300, height: 223 } })] }),
  new Paragraph({ spacing: { before: 220, after: 0 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'MEDRA', bold: true, size: 72, color: NAVY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 0 },
    children: [new TextRun({ text: 'Product Requirements Document', size: 32, color: TEAL, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 0 },
    children: [new TextRun({ text: 'A unified medical records & consultation-booking platform for Nigeria', size: 22, italics: true, color: GREY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 2400, after: 0 },
    children: [new TextRun({ text: 'Version 1.0  ·  Draft for review', size: 22, color: '333333' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 40, after: 0 },
    children: [new TextRun({ text: '23 July 2026  ·  Launch market: Abuja, Nigeria', size: 20, color: GREY })] }),
  new Paragraph({ children: [new PageBreak()] })
];

const doc = new Document({
  creator: 'Medra',
  title: 'Medra — Product Requirements Document',
  description: 'PRD for the Medra medical records & booking platform',
  numbering: {
    config: [{
      reference: 'num',
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.START,
        style: { paragraph: { indent: { left: 460, hanging: 260 } } } }]
    }]
  },
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 21, color: '222222' } }
    },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Calibri', size: 32, bold: true, color: NAVY },
        paragraph: { spacing: { before: 240, after: 120 }, keepNext: true } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Calibri', size: 26, bold: true, color: NAVY },
        paragraph: { spacing: { before: 220, after: 80 }, keepNext: true,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D0DCE4', space: 4 } } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Calibri', size: 23, bold: true, color: TEAL },
        paragraph: { spacing: { before: 160, after: 40 }, keepNext: true } }
    ]
  },
  sections: [
    {
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
      children: cover
    },
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } }
      },
      footers: {
        default: new (require('docx').Footer)({
          children: [new Paragraph({ alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: 'Medra — Product Requirements Document v1.0  ·  Confidential', size: 16, color: GREY })] })]
        })
      },
      children
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(process.argv[3], buf);
  console.log('wrote', process.argv[3], buf.length, 'bytes');
});
