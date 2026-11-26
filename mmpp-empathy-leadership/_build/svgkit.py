"""Alat bantu kecil untuk menulis SVG visual Sanggabiz (warna, teks terbungkus, ikon)."""
from xml.sax.saxutils import escape

INK = "#1D1D1F"
TEAL = "#0E8A8A"
TEAL_H = "#15908F"
TEAL_D = "#0D5C5B"
TEAL_L = "#D7ECEC"
ROW_ALT = "#F2F8F9"
CYAN = "#33BCCF"
BLUE = "#0071CE"
BLUE_L = "#DCEBFA"
GREY = "#D9D9D9"
GREY_T = "#555555"
GREY_F = "#999999"
PINK = "#E2A9F1"
PINK_L = "#F6E5FB"
WHITE = "#FFFFFF"
FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"

# warna per modul, satu keluarga dengan compro
MOD = {"M1": TEAL_D, "M2": BLUE, "M3": TEAL_H, "M4": "#0B4F8A", "M5": CYAN, "M6": "#7B4C9C"}


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{FONT}">\n{body}\n</svg>\n')


def wrap(text, width, size, bold=False):
    per = size * (0.56 if bold else 0.51)
    maxc = max(4, int(width / per))
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if len(t) <= maxc:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text(x, y, s, size=14, bold=False, fill=INK, anchor="start", width=None, lh=1.25,
         italic=False, valign="top"):
    """Teks dengan bungkus otomatis. y = garis atas blok teks (valign top) atau tengah (middle)."""
    lines = wrap(s, width, size, bold) if width else str(s).split("\n")
    total = size * lh * len(lines)
    y0 = y + size * 0.9 if valign == "top" else y - total / 2 + size * 0.9
    fw = ' font-weight="bold"' if bold else ""
    fs = ' font-style="italic"' if italic else ""
    attrs = f'font-size="{size}" fill="{fill}" text-anchor="{anchor}"{fw}{fs}'
    spans = "".join(f'<tspan x="{x}" y="{y0 + i * size * lh:.1f}">{escape(l)}</tspan>'
                    for i, l in enumerate(lines))
    return f'<text {attrs}>{spans}</text>'


def lines_needed(s, width, size, bold=False):
    return len(wrap(s, width, size, bold))


def rect(x, y, w, h, fill, rx=10, stroke=None, sw=1.2, dash=None, opacity=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash:
        st += f' stroke-dasharray="{dash}"'
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{op}/>'


def circle(cx, cy, r, fill, stroke=None, sw=2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st}/>'


def line(x1, y1, x2, y2, stroke=GREY, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def arrow(x1, y1, x2, y2, stroke=TEAL_H, sw=3, head=10):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(a - 0.45)
    hy1 = y2 - head * math.sin(a - 0.45)
    hx2 = x2 - head * math.cos(a + 0.45)
    hy2 = y2 - head * math.sin(a + 0.45)
    return (line(x1, y1, x2 - head * 0.6 * math.cos(a), y2 - head * 0.6 * math.sin(a), stroke, sw) +
            f'<polygon points="{x2},{y2} {hx1:.1f},{hy1:.1f} {hx2:.1f},{hy2:.1f}" fill="{stroke}"/>')


def curve(x1, y1, x2, y2, stroke=TEAL_L, sw=3):
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}"/>')


def chip(x, y, w, h, label, fill=PINK, color=INK, size=12, bold=True):
    return rect(x, y, w, h, fill, rx=h / 2) + text(x + w / 2, y + h / 2, label, size, bold, color,
                                                   "middle", width=w - 16, valign="middle")


# ---------- ikon: glif putih di kotak 24 x 24 ----------
_G = {
    "chat": '<path d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#fff"/>',
    "chat2": '<path d="M2 4h12a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H8l-4 3v-3H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#fff"/>'
             '<path d="M18 9h3a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-1v3l-4-3h-5a2 2 0 0 1-2-2v-1h5a3 3 0 0 0 3-3z" fill="#fff" opacity="0.75"/>',
    "heart": '<path d="M12 21s-8-4.8-10-10A5.3 5.3 0 0 1 12 6.5 5.3 5.3 0 0 1 22 11c-2 5.2-10 10-10 10z" fill="#fff"/>',
    "people": '<circle cx="8" cy="7" r="3.5" fill="#fff"/><path d="M1 20c0-4 3-6.5 7-6.5s7 2.5 7 6.5z" fill="#fff"/>'
              '<circle cx="17" cy="8" r="3" fill="#fff" opacity="0.8"/><path d="M14 14.2c1-.5 2-.7 3-.7 3.4 0 6 2.2 6 5.5h-6.5c0-2-.9-3.6-2.5-4.8z" fill="#fff" opacity="0.8"/>',
    "listen": '<path d="M12 3a8 8 0 0 0-8 8v5a3 3 0 0 0 3 3h2v-8H6.2A5.8 5.8 0 0 1 17.8 11H15v8h2a3 3 0 0 0 3-3v-5a8 8 0 0 0-8-8z" fill="#fff"/>',
    "shield": '<path d="M12 2l8 3v6.5c0 5-3.4 9-8 10.5-4.6-1.5-8-5.5-8-10.5V5z" fill="#fff"/>'
              '<path d="M8 12l3 3 5-6" stroke="#000" stroke-opacity="0.25" stroke-width="2" fill="none"/>',
    "target": '<circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="2.4"/>'
              '<circle cx="12" cy="12" r="5" fill="none" stroke="#fff" stroke-width="2.4"/><circle cx="12" cy="12" r="1.8" fill="#fff"/>',
    "clip": '<rect x="5" y="4" width="14" height="18" rx="2" fill="#fff"/><rect x="9" y="2" width="6" height="4" rx="1" fill="#fff" stroke="#000" stroke-opacity="0.25"/>'
            '<path d="M8.5 13l2.5 2.5 4.5-5" stroke="#000" stroke-opacity="0.35" stroke-width="2" fill="none"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2" fill="#fff"/><rect x="3" y="5" width="18" height="5" fill="#000" opacity="0.2"/>'
                '<rect x="7" y="2.5" width="2" height="5" rx="1" fill="#fff"/><rect x="15" y="2.5" width="2" height="5" rx="1" fill="#fff"/>',
    "flag": '<path d="M5 22V3h12l-2 4 2 4H7v11z" fill="#fff"/>',
    "search": '<circle cx="10" cy="10" r="6.5" fill="none" stroke="#fff" stroke-width="2.8"/><path d="M15 15l6 6" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
    "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.8a2.8 2.8 0 1 1 0-5.6 2.8 2.8 0 0 1 0 5.6z" fill="#fff"/>',
    "doc": '<path d="M6 2h9l5 5v15H6z" fill="#fff"/><path d="M9 11h8M9 14.5h8M9 18h5" stroke="#000" stroke-opacity="0.3" stroke-width="1.6"/>',
    "chart": '<rect x="3" y="12" width="4" height="9" fill="#fff"/><rect x="10" y="7" width="4" height="14" fill="#fff"/><rect x="17" y="3" width="4" height="18" fill="#fff"/>',
    "globe": '<circle cx="12" cy="12" r="9.5" fill="none" stroke="#fff" stroke-width="2"/><ellipse cx="12" cy="12" rx="4.2" ry="9.5" fill="none" stroke="#fff" stroke-width="1.8"/>'
             '<path d="M2.5 12h19M4 7h16M4 17h16" stroke="#fff" stroke-width="1.6"/>',
    "check": '<path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "lock": '<rect x="4.5" y="10" width="15" height="11" rx="2" fill="#fff"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="#fff" stroke-width="2.4" fill="none"/>',
    "build": '<rect x="3" y="9" width="18" height="12" fill="#fff"/><path d="M2 9l10-6 10 6z" fill="#fff"/><rect x="10" y="14" width="4" height="7" fill="#000" opacity="0.25"/>',
    "book": '<path d="M3 5c3-1.5 6-1.5 9 0v15c-3-1.5-6-1.5-9 0z" fill="#fff"/><path d="M12 5c3-1.5 6-1.5 9 0v15c-3-1.5-6-1.5-9 0z" fill="#fff" opacity="0.8"/>',
    "star": '<path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z" fill="#fff"/>',
    "handshake": '<path d="M2 9l5-3 5 2 5-2 5 3v5l-3 2-4 3.5a1.5 1.5 0 0 1-2-.1L6 14l-4-2z" fill="#fff"/><path d="M9 12l3 3M11.5 10.5l3 3" stroke="#000" stroke-opacity="0.3" stroke-width="1.5"/>',
    "clock": '<circle cx="12" cy="12" r="9.5" fill="none" stroke="#fff" stroke-width="2.4"/><path d="M12 6.5V12l4 2.5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/>',
    "pencil": '<path d="M4 20l1-5L16 4l4 4L9 19z" fill="#fff"/><path d="M4 20l5-1-4-4z" fill="#000" opacity="0.25"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3" fill="#fff"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4M8 21h8" stroke="#fff" stroke-width="2" fill="none"/>',
}


def icon(name, cx, cy, r, bg):
    s = r * 1.15
    return (circle(cx, cy, r, bg) +
            f'<g transform="translate({cx - s / 2:.1f},{cy - s / 2:.1f}) scale({s / 24:.3f})">{_G[name]}</g>')


def glyph(name, x, y, size):
    return f'<g transform="translate({x},{y}) scale({size / 24:.3f})">{_G[name]}</g>'
