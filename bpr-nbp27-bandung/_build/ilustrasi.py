"""Ilustrasi benda bank untuk kartu tunjuk. Gambar generik, tanpa meniru desain uang kertas atau merek kartu asli."""


def _uang(x, y, w, h, warna1, warna2, gid, rot=0):
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2.2" fill="url(#{gid})" stroke="{warna2}" stroke-width=".8"/>'
            f'<rect x="{x + 2.5}" y="{y + 2.5}" width="{w - 5}" height="{h - 5}" rx="1.4" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".7"/>'
            f'<circle cx="{x + w * .72}" cy="{y + h / 2}" r="{h * .26}" fill="#fff" fill-opacity=".35"/>'
            f'<text x="{x + 5}" y="{y + h / 2 + 3}" font-family="Montserrat" font-weight="800" font-size="{h * .34}" fill="#fff">Rp</text></g>')


def _grad(gid, a, b):
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'


def ilus(nama, w=58, h=44):
    bayang = '<filter id="bb" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="1.4" stdDeviation="1.2" flood-color="#13314F" flood-opacity=".25"/></filter>'
    if nama == "setor":
        isi = (f'<defs>{bayang}{_grad("gs1", "#5FC08F", "#2E8B62")}{_grad("gs2", "#62B6E8", "#2A7DB8")}</defs>'
               '<rect x="8" y="33" width="48" height="9" rx="2.5" fill="#33495A"/><rect x="14" y="35.6" width="36" height="2.6" rx="1.3" fill="#0E1D29"/>'
               f'<g filter="url(#bb)">{_uang(12, 9, 34, 17, "#5FC08F", "#2E8B62", "gs1", -6)}{_uang(17, 14, 34, 17, "#62B6E8", "#2A7DB8", "gs2", 4)}</g>'
               '<path d="M54 6v14m-4.5-4.5L54 20l4.5-4.5" stroke="#15908F" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    elif nama == "tarik":
        isi = (f'<defs>{bayang}{_grad("gt1", "#F3B44B", "#D2841B")}{_grad("gt2", "#5FC08F", "#2E8B62")}</defs>'
               '<rect x="6" y="28" width="46" height="15" rx="3" fill="#3B5467"/><rect x="11" y="31.5" width="36" height="3" rx="1.5" fill="#0E1D29"/>'
               '<rect x="40" y="37" width="7" height="3" rx="1" fill="#7FD3E0"/>'
               f'<g filter="url(#bb)">{_uang(12, 10, 34, 17, "#F3B44B", "#D2841B", "gt1", -3)}{_uang(14, 15, 34, 17, "#5FC08F", "#2E8B62", "gt2", 0)}</g>'
               '<path d="M56 20V6m-4.5 4.5L56 6l4.5 4.5" stroke="#15908F" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    elif nama == "saldo":
        isi = (f'<defs>{bayang}{_grad("gc1", "#ffffff", "#EEF3F6")}</defs>'
               '<g filter="url(#bb)"><path d="M14 4h30v36l-3.75-2.5-3.75 2.5-3.75-2.5-3.75 2.5-3.75-2.5-3.75 2.5-3.75-2.5L14 40z" fill="url(#gc1)" stroke="#C9D6DD" stroke-width=".8"/></g>'
               '<text x="18" y="12" font-family="Montserrat" font-weight="800" font-size="5" fill="#13314F">SALDO</text>'
               '<rect x="18" y="15" width="22" height="1.4" rx=".7" fill="#C9D6DD"/><rect x="18" y="19" width="16" height="1.4" rx=".7" fill="#C9D6DD"/>'
               '<text x="18" y="30" font-family="Montserrat" font-weight="800" font-size="5.6" fill="#15908F">Rp ***</text>'
               '<circle cx="47" cy="30" r="7" fill="#fff" stroke="#13314F" stroke-width="2.4"/><path d="M52 35l6 6" stroke="#13314F" stroke-width="3.2" stroke-linecap="round"/>')
    elif nama == "rekening":
        isi = (f'<defs>{bayang}{_grad("gr1", "#2A7DB8", "#13314F")}</defs>'
               '<g filter="url(#bb)"><rect x="9" y="6" width="30" height="36" rx="3" fill="url(#gr1)"/><rect x="9" y="6" width="5" height="36" rx="2" fill="#0E2740"/></g>'
               '<rect x="18" y="12" width="16" height="2" rx="1" fill="#FFC00C"/><text x="18" y="22" font-family="Montserrat" font-weight="700" font-size="3.5" fill="#fff">TABUNGAN</text>'
               '<rect x="18" y="28" width="12" height="1.4" rx=".7" fill="#7FB1D6"/>'
               '<circle cx="45" cy="31" r="9" fill="#15908F" stroke="#fff" stroke-width="2"/><path d="M45 26.5v9M40.5 31h9" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>')
    elif nama == "buku":
        isi = (f'<defs>{bayang}{_grad("gb1", "#ffffff", "#EEF3F6")}</defs>'
               '<g filter="url(#bb)"><path d="M6 10c7-2 15-2 26 1v30c-11-3-19-3-26-1z" fill="url(#gb1)" stroke="#C9D6DD" stroke-width=".8"/>'
               '<path d="M58 10c-7-2-15-2-26 1v30c11-3 19-3 26-1z" fill="url(#gb1)" stroke="#C9D6DD" stroke-width=".8"/></g>'
               + "".join(f'<rect x="10" y="{16 + i * 5}" width="18" height="1.4" rx=".7" fill="#9FB3BF"/><rect x="36" y="{16 + i * 5}" width="{18 - (i % 2) * 6}" height="1.4" rx=".7" fill="#15908F"/>' for i in range(4))
               + '<rect x="30.6" y="9.5" width="2.8" height="32" fill="#2A7DB8"/>')
    elif nama == "kartu":
        isi = (f'<defs>{bayang}{_grad("gk1", "#34BDCF", "#13314F")}<linearGradient id="gk2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7D774"/><stop offset="1" stop-color="#C99A2E"/></linearGradient></defs>'
               '<g filter="url(#bb)"><rect x="5" y="8" width="54" height="34" rx="4" fill="url(#gk1)"/></g>'
               '<circle cx="50" cy="16" r="10" fill="#fff" fill-opacity=".12"/>'
               '<rect x="11" y="16" width="10" height="8" rx="1.5" fill="url(#gk2)"/><path d="M11 20h10M16 16v8" stroke="#A97E1F" stroke-width=".6"/>'
               '<text x="11" y="33" font-family="Montserrat" font-weight="700" font-size="4.6" fill="#fff" letter-spacing=".6">****  ****  2775</text>'
               '<text x="11" y="38.5" font-family="Inter" font-size="3.4" fill="#D7ECEC">NAMA NASABAH</text>')
    else:
        raise KeyError(nama)
    return f'<svg viewBox="0 0 64 48" width="{w}" height="{h}">{isi}</svg>'
