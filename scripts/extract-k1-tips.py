#!/usr/bin/env python3
"""电子技巧 PDF → 页图 + OCR + 按单元裁图。识别过的不再重跑。"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "kb/raw/科目一（技巧口诀+500题）/科目一2026最新电子技巧.pdf"
OUT = ROOT / "kb/raw/tips/k1"
PAGES = OUT / "pages"
OCR_DIR = OUT / "ocr"
IMAGES = OUT / "images"
UNITS_JSON = OUT / "units.json"
EXTRACT_JSON = ROOT / "kb/extracts/kemu1-tips.json"
OCR_BIN = ROOT / "scripts/ocr-vision"
ZOOM = 1.6


def compile_ocr() -> None:
    src = ROOT / "scripts/ocr-vision.swift"
    if OCR_BIN.exists() and OCR_BIN.stat().st_mtime >= src.stat().st_mtime:
        return
    subprocess.check_call(["swiftc", "-O", "-o", str(OCR_BIN), str(src)], cwd=ROOT / "scripts")


def ocr_image(path: Path) -> str:
    r = subprocess.run([str(OCR_BIN), str(path)], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def render_pages() -> list[Path]:
    PAGES.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    paths = []
    mat = fitz.Matrix(ZOOM, ZOOM)
    for i, page in enumerate(doc):
        dest = PAGES / f"p{i + 1:02d}.png"
        if not dest.exists():
            pix = page.get_pixmap(matrix=mat, alpha=False)
            pix.save(dest)
            print("render", dest.name)
        paths.append(dest)
    doc.close()
    return paths


def ocr_pages(paths: list[Path]) -> dict[str, str]:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    compile_ocr()
    out = {}
    for path in paths:
        txt = OCR_DIR / (path.stem + ".txt")
        if txt.exists() and txt.stat().st_size > 0:
            out[path.stem] = txt.read_text(encoding="utf-8")
            continue
        text = ocr_image(path)
        txt.write_text(text, encoding="utf-8")
        out[path.stem] = text
        print("ocr", path.name, len(text), "chars")
    return out


def crop(src: Path, dest: Path, box: tuple[float, float, float, float]) -> None:
    """box = 相对 0–1 的 (x0, y0, x1, y1)。"""
    if dest.exists():
        return
    doc = fitz.open(src)
    page = doc[0]
    r = page.rect
    x0, y0, x1, y1 = box
    clip = fitz.Rect(r.x0 + r.width * x0, r.y0 + r.height * y0, r.x0 + r.width * x1, r.y0 + r.height * y1)
    pix = page.get_pixmap(clip=clip, alpha=False, matrix=fitz.Matrix(1.3, 1.3))
    tmp = dest.with_suffix(".png")
    pix.save(tmp)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() in {".jpg", ".jpeg"}:
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-Z", "900", str(tmp), "--out", str(dest)],
            capture_output=True,
            check=False,
        )
        tmp.unlink(missing_ok=True)
    else:
        tmp.rename(dest)
    doc.close()


# 80 条：编号、标题、课、处理。页码是 PDF 0-index（封面=0，第1/35=1）。
TIPS: list[dict] = [
    {"n": 1, "pdf": 1, "title": "12分", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 2, "pdf": 1, "title": "9分", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 3, "pdf": 1, "title": "6分", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 4, "pdf": 2, "title": "3分", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 5, "pdf": 2, "title": "1分", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 6, "pdf": 3, "title": "超速", "lesson": "03", "action": "teach", "kind": "tip"},
    {"n": 7, "pdf": 3, "title": "超载/超员", "lesson": "03", "action": "teach", "kind": "tip"},
    {"n": 8, "pdf": 3, "title": "超重", "lesson": "03", "action": "teach", "kind": "tip"},
    {"n": 9, "pdf": 4, "title": "疲劳驾驶", "lesson": "03", "action": "teach", "kind": "tip"},
    {"n": 10, "pdf": 4, "title": "学法减分", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 11, "pdf": 4, "title": "准驾车型", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 12, "pdf": 5, "title": "英文题", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 13, "pdf": 5, "title": "代罚牟利", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 14, "pdf": 5, "title": "米数题", "lesson": "04", "action": "teach", "kind": "tip"},
    {"n": 15, "pdf": 6, "title": "新规罚款", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 16, "pdf": 6, "title": "逾期/伪造/补领", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 17, "pdf": 6, "title": "刑法题", "lesson": "09", "action": "teach", "kind": "tip"},
    {"n": 18, "pdf": 7, "title": "信号灯", "lesson": "07", "action": "teach", "kind": "tip"},
    {"n": 19, "pdf": 7, "title": "公里数", "lesson": "04", "action": "teach", "kind": "tip"},
    {"n": 20, "pdf": 9, "title": "ABS", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 21, "pdf": 9, "title": "违法题", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 22, "pdf": 9, "title": "口5站3", "lesson": "04", "action": "teach", "kind": "tip"},
    {"n": 23, "pdf": 9, "title": "吊销题", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 24, "pdf": 9, "title": "点火开关", "lesson": None, "action": "discard", "kind": "tip", "note": "有钥匙孔图"},
    {"n": 25, "pdf": 9, "title": "机械仪表圆方", "lesson": None, "action": "discard", "kind": "tip", "note": "有车速/水温表"},
    {"n": 26, "pdf": 10, "title": "转速/车速表", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 27, "pdf": 10, "title": "感叹号制动", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 28, "pdf": 10, "title": "手刹P", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 29, "pdf": 10, "title": "灯光拨杆戒指", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 30, "pdf": 11, "title": "会车让行箭头", "lesson": "05", "action": "teach", "kind": "tip"},
    {"n": 31, "pdf": 11, "title": "灯光总开关", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 32, "pdf": 11, "title": "前绿后黄", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 33, "pdf": 12, "title": "直远斜近", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 34, "pdf": 12, "title": "位置灯成双", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 35, "pdf": 12, "title": "让行箭头相交", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 36, "pdf": 13, "title": "左对右错", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 37, "pdf": 13, "title": "月份题", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 38, "pdf": 13, "title": "应当", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 39, "pdf": 13, "title": "扣留", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 40, "pdf": 13, "title": "报警", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 41, "pdf": 13, "title": "易", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 42, "pdf": 13, "title": "尽快加速迅速", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 43, "pdf": 14, "title": "停车减速谨慎", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 44, "pdf": 14, "title": "近光灯", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 45, "pdf": 14, "title": "远光灯", "lesson": "06", "action": "teach", "kind": "tip"},
    {"n": 46, "pdf": 14, "title": "远近光灯连写", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 47, "pdf": 14, "title": "不能", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 48, "pdf": 14, "title": "不要", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 49, "pdf": 14, "title": "不得", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 50, "pdf": 15, "title": "不用", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 51, "pdf": 15, "title": "不需", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 52, "pdf": 15, "title": "不必", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 53, "pdf": 15, "title": "依次主动观察", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 54, "pdf": 15, "title": "可/可以", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 55, "pdf": 16, "title": "年份题", "lesson": "01", "action": "teach", "kind": "tip"},
    {"n": 56, "pdf": 16, "title": "补领换领", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 57, "pdf": 16, "title": "注销", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 58, "pdf": 16, "title": "避免", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 59, "pdf": 16, "title": "公安", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 60, "pdf": 16, "title": "考试", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 61, "pdf": 17, "title": "安全文明关键词", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 62, "pdf": 17, "title": "开车带证件", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 63, "pdf": 17, "title": "无争议", "lesson": "09", "action": "teach", "kind": "tip"},
    {"n": 64, "pdf": 17, "title": "利用发动机", "lesson": "08", "action": "teach", "kind": "tip"},
    {"n": 65, "pdf": 17, "title": "伤员", "lesson": "09", "action": "teach", "kind": "tip"},
    {"n": 66, "pdf": 17, "title": "开启转向灯", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 67, "pdf": 18, "title": "特殊天气", "lesson": "04", "action": "teach", "kind": "tip"},
    {"n": 68, "pdf": 18, "title": "标线题", "lesson": "05", "action": "teach", "kind": "tip"},
    {"n": 69, "pdf": 18, "title": "标志颜色", "lesson": "05", "action": "teach", "kind": "tip"},
    {"n": 70, "pdf": 18, "title": "酒驾", "lesson": "09", "action": "teach", "kind": "tip"},
    {"n": 71, "pdf": 18, "title": "可可不", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 72, "pdf": 18, "title": "确认安全", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 73, "pdf": 18, "title": "安全带", "lesson": "02", "action": "teach", "kind": "tip"},
    {"n": 74, "pdf": 18, "title": "双引号", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 75, "pdf": 18, "title": "开启远光灯", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 76, "pdf": 18, "title": "安全距离", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 77, "pdf": 18, "title": "确保安全", "lesson": None, "action": "discard", "kind": "tip"},
    {"n": 78, "pdf": 18, "title": "高速题", "lesson": "04", "action": "teach", "kind": "tip"},
    {"n": 79, "pdf": 18, "title": "急救伤员", "lesson": "09", "action": "teach", "kind": "tip"},
    {"n": 80, "pdf": 18, "title": "人山洞自行车", "lesson": None, "action": "discard", "kind": "tip"},
]

# 有独立图的单元：相对页的裁切框。页是 PDF 0-index。
CROPS: list[dict] = [
    {"id": "img-ignition", "pdf": 9, "title": "点火开关四档", "lesson": None, "action": "discard", "kind": "dash", "box": (0.08, 0.42, 0.48, 0.62)},
    {"id": "img-gauge-speed-demo", "pdf": 9, "title": "车速表示例", "lesson": None, "action": "discard", "kind": "dash", "box": (0.06, 0.66, 0.48, 0.92)},
    {"id": "img-gauge-temp", "pdf": 9, "title": "水温表示例", "lesson": None, "action": "discard", "kind": "dash", "box": (0.50, 0.66, 0.92, 0.92)},
    {"id": "img-rpm", "pdf": 10, "title": "发动机转速表到8", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.06, 0.10, 0.48, 0.36)},
    {"id": "img-speedo", "pdf": 10, "title": "车速表到240", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.50, 0.10, 0.92, 0.36)},
    {"id": "img-brake", "pdf": 10, "title": "制动感叹号", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.08, 0.40, 0.28, 0.55)},
    {"id": "img-park", "pdf": 10, "title": "手刹P", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.08, 0.78, 0.28, 0.93)},
    {"id": "img-meet-yield", "pdf": 11, "title": "会车让行红圈", "lesson": "05", "action": "teach", "kind": "sign", "box": (0.06, 0.34, 0.30, 0.50)},
    {"id": "img-meet-priority", "pdf": 11, "title": "会车先行蓝底", "lesson": "05", "action": "teach", "kind": "sign", "box": (0.32, 0.34, 0.56, 0.50)},
    {"id": "img-master-light", "pdf": 11, "title": "灯光总开关", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.08, 0.56, 0.30, 0.72)},
    {"id": "img-fog-front", "pdf": 11, "title": "前雾灯绿", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.06, 0.76, 0.30, 0.94)},
    {"id": "img-fog-rear", "pdf": 11, "title": "后雾灯黄", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.32, 0.76, 0.56, 0.94)},
    {"id": "img-high-beam", "pdf": 12, "title": "远光平射", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.08, 0.16, 0.34, 0.32)},
    {"id": "img-low-beam", "pdf": 12, "title": "近光斜下", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.38, 0.16, 0.64, 0.32)},
    {"id": "img-position", "pdf": 12, "title": "示廓灯成对", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.10, 0.42, 0.36, 0.58)},
    {"id": "img-fog-trap", "pdf": 12, "title": "后雾灯题配前雾灯图", "lesson": "06", "action": "teach", "kind": "dash", "box": (0.52, 0.42, 0.78, 0.58)},
    {"id": "img-stop", "pdf": 19, "title": "八边形停车让行", "lesson": "05", "action": "teach", "kind": "sign", "box": (0.18, 0.16, 0.36, 0.34)},
    {"id": "img-yield", "pdf": 19, "title": "倒三角减速让行", "lesson": "05", "action": "teach", "kind": "sign", "box": (0.58, 0.16, 0.76, 0.34)},
    {"id": "img-man-nosign", "pdf": 19, "title": "人行横道男子无牌", "lesson": None, "action": "discard", "kind": "scene", "box": (0.06, 0.38, 0.46, 0.62)},
    {"id": "img-man-sign", "pdf": 19, "title": "人行横道男子有停牌", "lesson": None, "action": "discard", "kind": "scene", "box": (0.50, 0.38, 0.90, 0.62)},
    {"id": "img-police-scene", "pdf": 19, "title": "路口停止手势实景", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.08, 0.68, 0.92, 0.92)},
    {"id": "g-stop", "pdf": 20, "title": "停止信号一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.10, 0.18, 0.50, 0.37)},
    {"id": "g-straight", "pdf": 20, "title": "直行信号一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.09, 0.42, 0.51, 0.64)},
    {"id": "g-slow", "pdf": 20, "title": "减速慢行一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.10, 0.65, 0.51, 0.90)},
    {"id": "g-wait", "pdf": 21, "title": "左转弯待转一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.09, 0.14, 0.51, 0.37)},
    {"id": "g-change", "pdf": 21, "title": "变道信号一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.09, 0.42, 0.50, 0.63)},
    {"id": "g-left", "pdf": 21, "title": "左转弯一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.09, 0.64, 0.51, 0.89)},
    {"id": "g-right", "pdf": 22, "title": "右转弯一组", "lesson": "06", "action": "teach", "kind": "gesture", "box": (0.10, 0.39, 0.51, 0.63)},
]


def footer_of(pdf_index: int, page_count: int) -> str | None:
    if pdf_index == 0:
        return None
    if 1 <= pdf_index <= 35:
        return f"{pdf_index}/35"
    return f"extra-{pdf_index}"


def page_kind(pdf_index: int) -> str:
    if pdf_index == 0:
        return "cover"
    if 1 <= pdf_index <= 19:
        return "tips"
    if 20 <= pdf_index <= 22:
        return "gestures"
    if 23 <= pdf_index <= 29:
        return "signs"
    if 30 <= pdf_index <= 34:
        return "markings"
    if pdf_index == 35:
        return "new-signs"
    return "colorblind"


def lesson_of_page(pdf_index: int) -> str | None:
    if pdf_index == 0:
        return None
    if pdf_index <= 3:
        return "02" if pdf_index <= 2 else "03"
    if pdf_index in (9, 10, 11, 12):
        return "06"
    if 20 <= pdf_index <= 22:
        return "06"
    if 23 <= pdf_index <= 35:
        return "05"
    return None


def crop_all() -> list[dict]:
    IMAGES.mkdir(parents=True, exist_ok=True)
    items = []
    for spec in CROPS:
        dest = IMAGES / f"{spec['id']}.jpg"
        src = PAGES / f"p{spec['pdf'] + 1:02d}.png"
        if src.exists():
            crop(src, dest, spec["box"])
        items.append({
            "id": spec["id"],
            "kind": spec["kind"],
            "title": spec["title"],
            "pdf_page": spec["pdf"],
            "footer": footer_of(spec["pdf"], 38),
            "lesson": spec["lesson"],
            "action": spec["action"],
            "images": [f"images/{spec['id']}.jpg"],
        })
    return items


def build_catalog(ocr: dict[str, str], crops: list[dict]) -> dict:
    pages = []
    for i in range(38):
        stem = f"p{i + 1:02d}"
        pages.append({
            "pdf_page": i,
            "file": f"pages/{stem}.png",
            "footer": footer_of(i, 38),
            "kind": page_kind(i),
            "lesson": lesson_of_page(i),
            "ocr": ocr.get(stem, ""),
            "ocr_chars": len(ocr.get(stem, "")),
        })
    units = []
    units.append({
        "id": "cover",
        "kind": "cover",
        "title": "封面：2026 新交规全国通用文字版",
        "pdf_page": 0,
        "footer": None,
        "lesson": None,
        "action": "skip",
        "images": ["pages/p01.png"],
    })
    for t in TIPS:
        units.append({
            "id": f"tip-{t['n']:02d}",
            "kind": t["kind"],
            "n": t["n"],
            "title": t["title"],
            "pdf_page": t["pdf"],
            "footer": footer_of(t["pdf"], 38),
            "lesson": t["lesson"],
            "action": t["action"],
            "images": [],
            "note": t.get("note"),
        })
    units.extend(crops)
    sheets = [
        {"id": "sheet-warn", "pdf": 23, "title": "各种标志汇总·警告（一）", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-warn-2", "pdf": 24, "title": "警告标志（二）弯道/险路/渡口", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-warn-3", "pdf": 25, "title": "警告标志（三）铁路/施工/路面", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-ban", "pdf": 26, "title": "禁令标志", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-guide", "pdf": 27, "title": "指示标志", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-guide-2", "pdf": 28, "title": "停车/国省县乡道编号", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-guide-3", "pdf": 29, "title": "诱导标/高速起终点/服务区", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-mark-1", "pdf": 30, "title": "标线：导向/可变导向/人行预告/出入口", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-mark-2", "pdf": 31, "title": "标线：潮汐/车距/路缘黄线/停字", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "sheet-new", "pdf": 35, "title": "10月1日新标", "kind": "sheet", "lesson": "05", "action": "teach"},
        {"id": "colorblind-num", "pdf": 36, "title": "色卡答案·数字", "kind": "colorblind", "lesson": None, "action": "skip"},
        {"id": "colorblind-animal", "pdf": 37, "title": "色卡答案·动物", "kind": "colorblind", "lesson": None, "action": "skip"},
    ]
    for s in sheets:
        units.append({
            **s,
            "footer": footer_of(s["pdf"], 38),
            "images": [f"pages/p{s['pdf'] + 1:02d}.png"],
        })
    return {
        "source": "kb/raw/科目一（技巧口诀+500题）/科目一2026最新电子技巧.pdf",
        "trust": "community",
        "checked": "2026-09-04",
        "note": "OCR 和裁图在 kb/raw/tips/k1/（gitignore）。这份 JSON 进 git，以后对单元不要再整本识别。",
        "pages": pages,
        "units": units,
    }


def slim_for_git(catalog: dict) -> dict:
    """进 git 的副本：保留 OCR 全文和单元，不依赖本地图也能用。"""
    return catalog


def main() -> int:
    if not PDF.exists():
        print("missing", PDF)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    paths = render_pages()
    ocr = ocr_pages(paths)
    crops = crop_all()
    catalog = build_catalog(ocr, crops)
    UNITS_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    EXTRACT_JSON.write_text(json.dumps(slim_for_git(catalog), ensure_ascii=False, indent=2), encoding="utf-8")
    print("pages", len(catalog["pages"]), "units", len(catalog["units"]))
    print("local", UNITS_JSON)
    print("git", EXTRACT_JSON)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
