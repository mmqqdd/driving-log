#!/usr/bin/env python3
"""Build public/images/k1/ teaching signs + cropped gesture photos."""

from __future__ import annotations

import subprocess
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/images/k1"
TIPS = Path("/tmp/k1-tips")
TIPS_PDF = ROOT / "kb/raw/科目一（技巧口诀+500题）/科目一2026最新电子技巧.pdf"
ICONS_PDF = ROOT / "kb/raw/科目一（技巧口诀+500题）/最新驾考图标.pdf"


def svg(name: str, body: str, w: int = 160, h: int = 160) -> None:
    OUT.joinpath(name).write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">{body}</svg>\n',
        encoding="utf-8",
    )


def octagon(cx=80, cy=80, r=70) -> str:
    pts = []
    for i in range(8):
        from math import cos, pi, sin

        a = pi / 8 + i * pi / 4
        pts.append(f"{cx + r * cos(a):.1f},{cy + r * sin(a):.1f}")
    return " ".join(pts)


def write_svgs() -> None:
    o = octagon()
    svg(
        "stop.svg",
        f'<polygon points="{o}" fill="#d32f2f" stroke="#fff" stroke-width="6"/>'
        '<text x="80" y="96" text-anchor="middle" fill="#fff" '
        'font-size="52" font-family="PingFang SC, Heiti SC, sans-serif" font-weight="700">停</text>',
    )
    svg(
        "yield.svg",
        '<polygon points="80,12 150,148 10,148" fill="#fff" stroke="#d32f2f" stroke-width="14"/>'
        '<text x="80" y="120" text-anchor="middle" fill="#111" '
        'font-size="42" font-family="PingFang SC, Heiti SC, sans-serif" font-weight="700">让</text>',
    )
    svg(
        "no-pass.svg",
        '<circle cx="80" cy="80" r="70" fill="#fff" stroke="#d32f2f" stroke-width="18"/>',
    )
    svg(
        "no-entry.svg",
        '<circle cx="80" cy="80" r="70" fill="#d32f2f"/>'
        '<rect x="28" y="68" width="104" height="24" rx="2" fill="#fff"/>',
    )
    svg(
        "no-long-park.svg",
        '<circle cx="80" cy="80" r="70" fill="#1565c0"/>'
        '<circle cx="80" cy="80" r="62" fill="none" stroke="#d32f2f" stroke-width="10"/>'
        '<line x1="40" y1="40" x2="120" y2="120" stroke="#d32f2f" stroke-width="12"/>',
    )
    svg(
        "no-park.svg",
        '<circle cx="80" cy="80" r="70" fill="#1565c0"/>'
        '<circle cx="80" cy="80" r="62" fill="none" stroke="#d32f2f" stroke-width="10"/>'
        '<line x1="40" y1="40" x2="120" y2="120" stroke="#d32f2f" stroke-width="12"/>'
        '<line x1="120" y1="40" x2="40" y2="120" stroke="#d32f2f" stroke-width="12"/>',
    )
    svg(
        "speed-max.svg",
        '<circle cx="80" cy="80" r="70" fill="#fff" stroke="#d32f2f" stroke-width="16"/>'
        '<text x="80" y="98" text-anchor="middle" fill="#111" font-size="56" '
        'font-family="Arial, sans-serif" font-weight="700">40</text>',
    )
    svg(
        "speed-min.svg",
        '<circle cx="80" cy="80" r="70" fill="#1565c0"/>'
        '<text x="80" y="98" text-anchor="middle" fill="#fff" font-size="56" '
        'font-family="Arial, sans-serif" font-weight="700">50</text>',
    )
    svg(
        "speed-end.svg",
        '<circle cx="80" cy="80" r="70" fill="#fff" stroke="#111" stroke-width="8"/>'
        '<text x="80" y="98" text-anchor="middle" fill="#111" font-size="48" '
        'font-family="Arial, sans-serif" font-weight="700">40</text>'
        '<line x1="28" y1="132" x2="132" y2="28" stroke="#111" stroke-width="8"/>',
    )
    warn = '<polygon points="80,10 150,145 10,145" fill="#f4d03f" stroke="#111" stroke-width="6"/>'
    svg("curve-1.svg", warn + '<path d="M50,115 Q80,40 118,100" fill="none" stroke="#111" stroke-width="8"/>')
    svg(
        "curve-2.svg",
        warn + '<path d="M42,118 L70,70 L100,110 L122,72" fill="none" stroke="#111" stroke-width="8"/>',
    )
    svg(
        "curve-3.svg",
        warn + '<path d="M38,120 L60,75 L88,115 L110,70 L128,105" fill="none" stroke="#111" stroke-width="7"/>',
    )
    svg(
        "warn-ped.svg",
        warn
        + '<rect x="48" y="108" width="64" height="8" fill="#111"/>'
        + '<rect x="56" y="100" width="48" height="6" fill="#111"/>'
        + '<circle cx="80" cy="62" r="8" fill="#111"/>'
        + '<path d="M80,70 L80,92 L68,108 M80,92 L94,108 M70,80 L90,80" fill="none" stroke="#111" stroke-width="5"/>',
    )
    svg(
        "warn-child.svg",
        warn
        + '<circle cx="62" cy="64" r="6" fill="#111"/><circle cx="96" cy="60" r="6" fill="#111"/>'
        + '<path d="M62,70 L62,92 L52,110 M62,92 L74,110 M96,66 L90,92 L80,110 M96,66 L108,92" '
        'fill="none" stroke="#111" stroke-width="4"/>',
    )
    svg(
        "warn-bike.svg",
        warn
        + '<circle cx="58" cy="112" r="10" fill="none" stroke="#111" stroke-width="4"/>'
        + '<circle cx="102" cy="112" r="10" fill="none" stroke="#111" stroke-width="4"/>'
        + '<path d="M58,112 L78,88 L98,112 M78,88 L86,72" fill="none" stroke="#111" stroke-width="4"/>',
    )
    svg(
        "lane-bike.svg",
        '<rect x="8" y="20" width="144" height="120" rx="8" fill="#1565c0"/>'
        '<circle cx="58" cy="100" r="12" fill="none" stroke="#fff" stroke-width="5"/>'
        '<circle cx="108" cy="100" r="12" fill="none" stroke="#fff" stroke-width="5"/>'
        '<path d="M58,100 L80,70 L106,100 M80,70 L90,52" fill="none" stroke="#fff" stroke-width="5"/>'
        '<line x1="24" y1="36" x2="24" y2="128" stroke="#fff" stroke-width="3" stroke-dasharray="8 6"/>'
        '<line x1="136" y1="36" x2="136" y2="128" stroke="#fff" stroke-width="3" stroke-dasharray="8 6"/>',
    )
    svg(
        "meet.svg",
        '<circle cx="80" cy="80" r="70" fill="#fff" stroke="#d32f2f" stroke-width="10"/>'
        '<path d="M80,28 L68,70 L80,62 L92,70 Z" fill="#111"/>'
        '<path d="M80,132 L96,88 L80,98 L64,88 Z" fill="#d32f2f"/>',
    )
    svg(
        "high-beam.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#e8f5e9"/>'
        '<circle cx="48" cy="80" r="18" fill="#2e7d32"/>'
        '<path d="M70,56 L138,56 M70,80 L138,80 M70,104 L138,104" stroke="#2e7d32" stroke-width="8"/>',
    )
    svg(
        "low-beam.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#e8f5e9"/>'
        '<circle cx="48" cy="80" r="18" fill="#2e7d32"/>'
        '<path d="M70,52 L130,78 M70,80 L130,106 M70,108 L130,134" stroke="#2e7d32" stroke-width="8"/>',
    )
    svg(
        "fog-front.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#e8f5e9"/>'
        '<circle cx="52" cy="80" r="16" fill="#2e7d32"/>'
        '<path d="M74,52 C88,68 88,92 74,108 M90,48 C108,68 108,92 90,112 M106,44 C128,68 128,92 106,116" '
        'fill="none" stroke="#2e7d32" stroke-width="6"/>',
    )
    svg(
        "fog-rear.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#fff8e1"/>'
        '<circle cx="52" cy="80" r="16" fill="#f9a825"/>'
        '<path d="M74,52 C88,68 88,92 74,108 M90,48 C108,68 108,92 90,112 M106,44 C128,68 128,92 106,116" '
        'fill="none" stroke="#f9a825" stroke-width="6"/>',
    )
    svg(
        "master-light.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#eceff1"/>'
        '<circle cx="80" cy="80" r="18" fill="none" stroke="#37474f" stroke-width="8"/>'
        '<g stroke="#37474f" stroke-width="8" stroke-linecap="round">'
        '<line x1="80" y1="28" x2="80" y2="44"/><line x1="80" y1="116" x2="80" y2="132"/>'
        '<line x1="28" y1="80" x2="44" y2="80"/><line x1="116" y1="80" x2="132" y2="80"/>'
        '<line x1="44" y1="44" x2="54" y2="54"/><line x1="106" y1="106" x2="116" y2="116"/>'
        '<line x1="116" y1="44" x2="106" y2="54"/><line x1="54" y1="106" x2="44" y2="116"/>'
        "</g>",
    )
    svg(
        "brake.svg",
        '<circle cx="80" cy="80" r="70" fill="none" stroke="#c62828" stroke-width="10"/>'
        '<text x="80" y="102" text-anchor="middle" fill="#c62828" font-size="72" '
        'font-family="Arial, sans-serif" font-weight="700">!</text>',
    )
    svg(
        "park-brake.svg",
        '<circle cx="80" cy="80" r="70" fill="none" stroke="#c62828" stroke-width="10"/>'
        '<text x="80" y="104" text-anchor="middle" fill="#c62828" font-size="72" '
        'font-family="Arial, sans-serif" font-weight="700">P</text>',
    )
    svg(
        "position-light.svg",
        '<rect x="10" y="10" width="140" height="140" rx="16" fill="#e8f5e9"/>'
        '<circle cx="46" cy="80" r="12" fill="#2e7d32"/>'
        '<circle cx="114" cy="80" r="12" fill="#2e7d32"/>'
        '<g stroke="#2e7d32" stroke-width="5" fill="none">'
        '<path d="M28,62 L18,54 M28,80 L14,80 M28,98 L18,106"/>'
        '<path d="M132,62 L142,54 M132,80 L146,80 M132,98 L142,106"/>'
        "</g>",
    )
    svg(
        "crosswalk.svg",
        '<rect x="8" y="20" width="144" height="120" rx="8" fill="#1565c0"/>'
        '<g fill="#fff">'
        '<rect x="28" y="44" width="16" height="72"/>'
        '<rect x="52" y="44" width="16" height="72"/>'
        '<rect x="76" y="44" width="16" height="72"/>'
        '<rect x="100" y="44" width="16" height="72"/>'
        '<rect x="124" y="44" width="8" height="72"/>'
        "</g>",
    )
    svg(
        "warn-triangle.svg",
        '<polygon points="80,12 150,148 10,148" fill="#f4d03f" stroke="#111" stroke-width="6"/>'
        '<text x="80" y="118" text-anchor="middle" fill="#111" font-size="72" '
        'font-family="Arial, sans-serif" font-weight="700">!</text>',
    )
    svg(
        "work.svg",
        warn
        + '<circle cx="72" cy="64" r="7" fill="#111"/>'
        + '<path d="M72,72 L72,96 L60,118 M72,96 L86,118 M64,84 L92,78" fill="none" stroke="#111" stroke-width="5"/>'
        + '<line x1="92" y1="54" x2="108" y2="108" stroke="#111" stroke-width="5"/>'
        + '<rect x="104" y="108" width="14" height="6" fill="#111"/>',
    )
    svg(
        "rocks.svg",
        warn
        + '<path d="M28,128 L62,58 L88,88 L118,50 L138,128 Z" fill="#111"/>'
        + '<circle cx="96" cy="72" r="4" fill="#f4d03f"/>'
        + '<circle cx="108" cy="86" r="3.5" fill="#f4d03f"/>'
        + '<circle cx="118" cy="98" r="3" fill="#f4d03f"/>',
    )
    svg(
        "mountain-road.svg",
        warn
        + '<path d="M86,128 L118,48 L142,128 Z" fill="#111"/>'
        + '<path d="M28,128 L28,108 L70,108 L70,128" fill="#111"/>',
    )
    svg(
        "embankment.svg",
        warn
        + '<path d="M38,88 L70,88 L78,78 L98,78 L106,88 L118,88 L110,100 L46,100 Z" fill="#111"/>'
        + '<path d="M36,112 Q52,104 68,112 Q84,120 100,112 Q116,104 132,112" fill="none" stroke="#111" stroke-width="5"/>',
    )
    svg(
        "ferry.svg",
        warn
        + '<rect x="54" y="62" width="52" height="22" rx="3" fill="#111"/>'
        + '<circle cx="64" cy="70" r="3" fill="#f4d03f"/><circle cx="96" cy="70" r="3" fill="#f4d03f"/>'
        + '<path d="M40,92 L48,84 L112,84 L128,100 L36,100 Z" fill="#111"/>'
        + '<path d="M36,112 Q52,104 68,112 Q84,120 100,112 Q116,104 132,112" fill="none" stroke="#111" stroke-width="4"/>',
    )
    svg(
        "rail.svg",
        warn
        + '<rect x="48" y="70" width="64" height="28" rx="4" fill="#111"/>'
        + '<rect x="70" y="56" width="28" height="18" rx="3" fill="#111"/>'
        + '<circle cx="62" cy="102" r="8" fill="#111"/><circle cx="98" cy="102" r="8" fill="#111"/>'
        + '<circle cx="62" cy="102" r="3" fill="#f4d03f"/><circle cx="98" cy="102" r="3" fill="#f4d03f"/>',
    )
    svg(
        "hump.svg",
        warn + '<path d="M36,118 Q80,48 124,118" fill="none" stroke="#111" stroke-width="10"/>',
    )
    svg(
        "uneven.svg",
        warn
        + '<path d="M30,118 Q52,78 70,118 Q90,78 108,118 Q126,86 138,118" fill="none" stroke="#111" stroke-width="8"/>',
    )


def crop_png(src: Path, dest: Path, box: tuple[float, float, float, float]) -> None:
    doc = fitz.open(src)
    page = doc[0]
    pw, ph = page.rect.width, page.rect.height
    pix0 = fitz.Pixmap(src)
    sx, sy = pw / pix0.width, ph / pix0.height
    x0, y0, x1, y1 = box
    clip = fitz.Rect(x0 * sx, y0 * sy, x1 * sx, y1 * sy)
    pix = page.get_pixmap(clip=clip, alpha=False, matrix=fitz.Matrix(1.4, 1.4))
    tmp = dest.with_suffix(".png")
    pix.save(tmp)
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-Z", "960", str(tmp), "--out", str(dest)],
        capture_output=True,
        check=False,
    )
    tmp.unlink(missing_ok=True)
    doc.close()
    print(dest.name, dest.stat().st_size // 1024, "KB")


def ensure_tip_pages() -> bool:
    """PDF 0-index 20/21/22 = printed 20/35–22/35 gesture sheets."""
    pages = (20, 21, 22)
    if TIPS_PDF.exists():
        TIPS.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(TIPS_PDF)
        mat = fitz.Matrix(1.5, 1.5)
        for i in pages:
            pix = doc[i].get_pixmap(matrix=mat, alpha=False)
            pix.save(TIPS / f"p{i+1:02d}.png")
        doc.close()
        return True
    return all((TIPS / f"p{i+1:02d}.png").exists() for i in pages)


def crop_gestures() -> None:
    if not ensure_tip_pages():
        print("skip gestures: missing PDF and /tmp/k1-tips")
        return
    p21 = TIPS / "p21.png"
    p22 = TIPS / "p22.png"
    p23 = TIPS / "p23.png"
    # 893x1262 @ 1.5x. Each row is one gesture: left frame + right frame + 口诀.
    # Crop both officers together; x stops before the mnemonic text.
    crop_png(p21, OUT / "police-stop.jpg", (88, 232, 448, 468))
    crop_png(p21, OUT / "police-straight.jpg", (82, 528, 452, 808))
    crop_png(p21, OUT / "police-slow.jpg", (86, 818, 458, 1132))
    crop_png(p22, OUT / "police-wait-turn.jpg", (82, 172, 458, 468))
    crop_png(p22, OUT / "police-change.jpg", (78, 532, 448, 792))
    crop_png(p22, OUT / "police-left.jpg", (82, 802, 458, 1118))
    if p23.exists():
        crop_png(p23, OUT / "police-right.jpg", (86, 488, 458, 798))


def page_to_jpg(page: fitz.Page, dest: Path, inset: float = 10) -> None:
    r = page.rect
    clip = fitz.Rect(r.x0 + inset, r.y0 + inset, r.x1 - inset, r.y1 - inset)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), clip=clip, alpha=False)
    tmp = dest.with_suffix(".png")
    pix.save(tmp)
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-Z", "1400", str(tmp), "--out", str(dest)],
        capture_output=True,
        check=False,
    )
    tmp.unlink(missing_ok=True)
    print(dest.name, dest.stat().st_size // 1024, "KB")


def publish_sign_sheets() -> None:
    """警告 / 禁令图册来自「最新驾考图标」；指示那页来自电子技巧第27/35。"""
    if ICONS_PDF.exists():
        doc = fitz.open(ICONS_PDF)
        for i, name in (
            (4, "signs-warn-1.jpg"),
            (5, "signs-warn-2.jpg"),
            (6, "signs-warn-3.jpg"),
            (7, "signs-warn-4.jpg"),
            (0, "signs-ban-1.jpg"),
            (1, "signs-ban-2.jpg"),
            (2, "signs-ban-3.jpg"),
        ):
            page_to_jpg(doc[i], OUT / name)
        doc.close()
    else:
        print("skip sign sheets: missing 最新驾考图标.pdf")
    if TIPS_PDF.exists():
        doc = fitz.open(TIPS_PDF)
        # 0-index 27 = 印「第27/35」指示标志
        page_to_jpg(doc[27], OUT / "signs-guide.jpg", inset=6)
        doc.close()
    else:
        print("skip signs-guide: missing 电子技巧 PDF")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    write_svgs()
    crop_gestures()
    publish_sign_sheets()
    print("course images ->", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
