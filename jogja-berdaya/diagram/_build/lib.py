"""Pembantu kecil untuk menyusun SVG dengan teks yang dibungkus otomatis."""
import html

FONT = "Arial, Helvetica, sans-serif"
NAVY, TEAL, BLUE = "#12304F", "#0E8A8A", "#0071CE"
INK, MUTED, LINE = "#1B2A3A", "#5B6B7A", "#C9D3DA"
TEALBG, GRAYBG, YEL, YELBG = "#E6F4F5", "#F3F5F7", "#FFC00C", "#FFF6D6"
RED, REDBG, GRN, GRNBG = "#B83227", "#FCE9E7", "#2E7D4F", "#E5F3EA"


def esc(t):
    return html.escape(str(t), quote=False)


def wrap(txt, fs, maxw, bold=False):
    f = 0.6 if bold else 0.55
    per = max(4, int(maxw / (fs * f)))
    out = []
    for para in str(txt).split("\n"):
        line = ""
        for w in para.split(" "):
            cand = (line + " " + w).strip()
            if len(cand) <= per:
                line = cand
            else:
                if line:
                    out.append(line)
                line = w
        out.append(line)
    return out


class SVG:
    def __init__(self, w):
        self.w, self.p = w, []

    def add(self, s):
        self.p.append(s)

    def rect(self, x, y, w, h, fill="#fff", stroke=None, rx=8, sw=1.2):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}/>')

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1.5, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#ah)"' if arrow else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

    def circle(self, cx, cy, r, fill, stroke=None):
        st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"{st}/>')

    def diamond(self, cx, cy, r, fill):
        self.add(f'<polygon points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="{fill}"/>')

    def text(self, x, y, txt, fs=14, fill=INK, bold=False, anchor="start", maxw=None, lh=1.32):
        """Gambar teks mulai dari garis atas y. Mengembalikan tinggi yang dipakai."""
        lines = wrap(txt, fs, maxw, bold) if maxw else str(txt).split("\n")
        wt = ' font-weight="700"' if bold else ""
        first = y + fs * 0.95
        tsp = "".join(
            f'<tspan x="{x:.1f}" dy="{0 if i == 0 else fs * lh:.1f}">{esc(l)}</tspan>'
            for i, l in enumerate(lines)
        )
        self.add(f'<text x="{x:.1f}" y="{first:.1f}" font-size="{fs}" fill="{fill}"{wt} text-anchor="{anchor}">{tsp}</text>')
        return len(lines) * fs * lh

    def height_of(self, txt, fs, maxw, bold=False, lh=1.32):
        return len(wrap(txt, fs, maxw, bold)) * fs * lh

    def save(self, path, h, title, desc):
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h:.0f}" width="{self.w}" height="{h:.0f}" '
            f'font-family="{FONT}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>'
            f'<rect width="{self.w}" height="{h:.0f}" fill="#FFFFFF"/>'
        )
        open(path, "w", encoding="utf-8").write(head + "".join(self.p) + "</svg>\n")


def header(s, title, sub, h=118):
    s.rect(0, 0, s.w, h, NAVY, rx=0)
    s.text(50, 22, title, 30, "#fff", True, maxw=s.w - 100)
    s.text(50, 66, sub, 15.5, "#CFE6EC", maxw=s.w - 100, lh=1.35)


def section(s, y, num, label):
    s.circle(66, y + 16, 15, TEAL)
    s.text(66, y + 8.5, str(num), 16, "#fff", True, "middle")
    s.text(92, y + 5, label, 20, NAVY, True)
    return y + 42


def card(s, x, y, w, title, body, h=None, fill=GRAYBG, stroke=LINE, tfs=15, bfs=13, tcol=NAVY, pad=14, bar=None):
    th = s.height_of(title, tfs, w - 2 * pad, True)
    bh = s.height_of(body, bfs, w - 2 * pad) if body else 0
    need = pad + th + (8 if body else 0) + bh + pad
    h = max(h or 0, need)
    s.rect(x, y, w, h, fill, stroke)
    if bar:
        s.rect(x, y, 6, h, bar, None, rx=3)
    s.text(x + pad, y + pad, title, tfs, tcol, True, maxw=w - 2 * pad)
    if body:
        s.text(x + pad, y + pad + th + 8, body, bfs, INK, maxw=w - 2 * pad)
    return h


def need(s, w, title, body, tfs=15, bfs=13, pad=14):
    th = s.height_of(title, tfs, w - 2 * pad, True)
    bh = s.height_of(body, bfs, w - 2 * pad) if body else 0
    return pad + th + (8 if body else 0) + bh + pad
