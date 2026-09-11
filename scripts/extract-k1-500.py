#!/usr/bin/env python3
"""Extract the 500-question scan into kb/raw/bank/k1/ (local only)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import fitz

ROOT = Path("/Users/mqd/notes/driving-log")
PDF = ROOT / "kb/raw/科目一（技巧口诀+500题）/科目一精选500题＋新规.pdf"
OUT = ROOT / "kb/raw/bank/k1"
IMAGES = OUT / "images"
OCR_DIR = OUT / "ocr"
BANK = OUT / "k1-500.json"
OCR_BIN = ROOT / "scripts/ocr-vision"
RENDER_ZOOM = 1.6

# Skip cover / 注意事项
FIRST_Q_PAGE = 2  # 1-based


def compile_ocr() -> None:
    src = ROOT / "scripts/ocr-vision.swift"
    if OCR_BIN.exists() and OCR_BIN.stat().st_mtime >= src.stat().st_mtime:
        return
    subprocess.check_call(
        ["swiftc", "-O", "-o", str(OCR_BIN), str(src)],
        cwd=ROOT / "scripts",
    )


def ocr_image(path: Path) -> str:
    r = subprocess.run(
        [str(OCR_BIN), str(path)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return ""
    return r.stdout


def row_stats(pix: fitz.Pixmap) -> list[tuple[float, float, float]]:
    """Per-row (white_ratio, color_ratio, mid_ratio)."""
    w, h, n = pix.width, pix.height, pix.n
    samples = pix.samples
    out = []
    for y in range(h):
        base = y * w * n
        white = color = mid = 0
        for x in range(w):
            i = base + x * n
            r, g, b = samples[i], samples[i + 1], samples[i + 2]
            mx, mn = (r if r > g else g), (r if r < g else g)
            if b > mx:
                mx = b
            if b < mn:
                mn = b
            if r > 238 and g > 238 and b > 238:
                white += 1
            elif mx - mn > 28:
                color += 1
            else:
                avg = (r + g + b) / 3
                if 50 < avg < 210:
                    mid += 1
        tot = float(w) or 1.0
        out.append((white / tot, color / tot, mid / tot))
    return out


def find_illustration(pix: fitz.Pixmap) -> tuple[int, int, int, int] | None:
    """Crop box in pixmap pixels, or None if this page is text-only."""
    w, h = pix.width, pix.height
    stats = row_stats(pix)
    scores = []
    for white, color, mid in stats:
        # photos: midtones; schematics: saturated ink on white
        score = color * 4.0 + mid * 1.1 - max(0.0, white - 0.72) * 0.6
        scores.append(score)

    top = int(h * 0.11)
    bot = int(h * 0.70)
    thresh = 0.12
    photo = [False] * h
    for y in range(top, bot):
        photo[y] = scores[y] >= thresh or stats[y][1] >= 0.035

    gap = int(h * 0.035)
    y = top
    while y < bot:
        if photo[y]:
            y += 1
            continue
        z = y
        while z < bot and not photo[z]:
            z += 1
        if z < bot and (z - y) <= gap and y > top:
            for k in range(y, z):
                photo[k] = True
        y = z

    best = None
    y = top
    while y < bot:
        if photo[y]:
            y0 = y
            while y < bot and photo[y]:
                y += 1
            y1 = y
            if y1 - y0 >= int(h * 0.11):
                if best is None or (y1 - y0) > best[0]:
                    best = (y1 - y0, y0, y1)
        else:
            y += 1

    if best is None:
        return None

    _, y0, y1 = best
    while y0 < y1 and stats[y0][0] > 0.92:
        y0 += 1
    while y1 > y0 and stats[y1 - 1][0] > 0.92:
        y1 -= 1
    if y1 - y0 < int(h * 0.10):
        return None
    # tip box sits in the lower third; don't treat orange keywords as a figure
    if y0 > int(h * 0.46):
        return None

    x0, x1 = int(w * 0.07), int(w * 0.93)
    pad = 6
    return (x0, max(0, y0 - pad), x1, min(h, y1 + pad))


def save_crop(page: fitz.Page, box: tuple[int, int, int, int], dest: Path) -> None:
    x0, y0, x1, y1 = box
    clip = fitz.Rect(
        x0 / RENDER_ZOOM,
        y0 / RENDER_ZOOM,
        x1 / RENDER_ZOOM,
        y1 / RENDER_ZOOM,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    cropped = page.get_pixmap(matrix=fitz.Matrix(RENDER_ZOOM, RENDER_ZOOM), clip=clip, alpha=False)
    cropped.save(dest)


def clean_line(s: str) -> str:
    s = s.strip()
    s = s.replace(" ", "")
    return s


JUNK_PREFIX = re.compile(
    r"^(?:"
    r"[］\[\]［【】（）()\\！!、．.•]+|"
    r"单达|单运|单远|单闼|训断|判断|单选|"
    r"野规题|司新规题|新规题|"
    r"团(?=驾驶)"
    r")+"
)


def scrub_stem(q: str) -> str:
    q = (q or "").strip()
    prev = None
    while prev != q:
        prev = q
        q = JUNK_PREFIX.sub("", q)
        q = q.lstrip("］［[]【】（）()\\！!、．.•")
    q = re.sub(r"(是何含义？|交通标志？)不包.*$", r"\1", q)
    q = re.sub(r"(?:感说|不包更新|不包更奖|不包更|店不包更|不包)+$", "", q)
    q = re.sub(r"。不$", "。", q)
    q = re.sub(r"[~～v•]+$", "", q)
    q = re.sub(r"([。？])(?:[\d:：A-Za-z~～_\-\.\^\(\)\'我感说不包]+)$", r"\1", q)
    q = q.replace("判断分", "分")
    q = re.sub(r"(缩写的是什么？)[A-Z]{2,4}$", r"\1", q)
    return q.strip()


def scrub_opt(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"^[~．.\s•]+", "", s)
    s = s.replace("丷", "")
    return s.strip()


def parse_ocr(text: str) -> dict:
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # drop running header / watermark crumbs
    skip_re = re.compile(
        r"^(第\d+页|仅校|驾校合作|此店|不包更新|专用|VIP|精选)$"
    )
    lines = [ln for ln in raw_lines if not skip_re.search(clean_line(ln))]

    joined = "\n".join(lines)
    compact = "".join(clean_line(ln) for ln in lines)

    qtype = "tf" if "判断" in compact[:40] or re.search(r"\n判断\n", joined) else "choice"
    if "单选" in compact[:40]:
        qtype = "choice"
    new_rule = "新规" in compact[:80]

    answer = None
    m = re.search(r"答案\s*([A-D])", joined)
    if m:
        answer = m.group(1)

    tip = ""
    tip_kind = "explain"
    tm = re.search(r"(关键字答题|秒懂技巧)[:：]?\s*(.+)", joined, re.S)
    if tm:
        tip = re.sub(r"\s+", "", tm.group(2))
        tip = re.split(r"第\d+页", tip)[0].strip("：: ")
        kind_label = tm.group(1)
        if kind_label == "关键字答题" or re.search(
            r"直接选|看见.{0,8}就选|选项中看到", tip
        ):
            tip_kind = "discard"
        elif kind_label == "秒懂技巧":
            tip_kind = "mnemonic"

    # stem + options: cut after 答案
    body = re.split(r"答案\s*[A-D]", joined, maxsplit=1)[0]
    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    # drop type tags
    while body_lines and re.fullmatch(r"(单选|判断|新规题|新规)", clean_line(body_lines[0])):
        body_lines.pop(0)

    options, opt_idx = split_options(body_lines, qtype)
    q = "".join(body_lines[:opt_idx] if opt_idx is not None else body_lines)

    q = re.sub(r"\s+", "", q)
    q = re.sub(r"^第\d+[页贞]", "", q)
    q = re.sub(
        r"^(?:单选|单达|单运|单远|单闼|判断|训断|[［\[【（(\\！!]*新规题[］\]】）)!]*)+",
        "",
        q,
    )
    q = re.sub(r"^[圖图＜<]+", "", q)
    q = re.sub(r"[＜<].*$", "", q)
    q = q.lstrip("］［[]【】（）()\\！!、．.")
    q = re.sub(r"[丷].*$", "", q)
    q = re.sub(r"(正确|错误)$", "", q)
    q = scrub_stem(q)
    options = [scrub_opt(o) for o in options]

    if qtype == "tf":
        options = ["正确", "错误"]

    ocr_ok = bool(q) and bool(answer) and (qtype == "tf" or len(options) >= 2)
    return {
        "type": qtype,
        "new_rule": new_rule,
        "q": q,
        "options": options,
        "answer": answer,
        "tip": tip or None,
        "tip_kind": tip_kind if tip else None,
        "ocr_ok": ocr_ok,
    }


LESSON_RULES = [
    (
        "06",
        r"酒|醉驾|酒精|血液|毒驾|逃逸|急救|担架|止血|骨折|伤员|心肺|呼吸|休克|烧伤|水疱",
    ),
    (
        "02",
        r"记[0-9一二三四五六九十]+分|一次记|记分|罚款|拘留|吊销|拘役|有期徒刑|准驾|超员|超载|超重|疲劳|学法减分|伪造|遮挡号牌|买卖分|审验教育|弄虚作假",
    ),
    (
        "04",
        r"远光|近光|转向灯|雾灯|示廓|危险报警|灯光|手势|仪表|标志|禁令|解除|注意|英文|ABS|EPS",
    ),
    (
        "05",
        r"让行|让行人|优先|会车|借道|虚线|实线|标线|停止线|黄灯|红灯|绿灯|信号灯|行人|校车",
    ),
    (
        "03",
        r"限速|时速|公里/小时|公里每小时|最高时速|最低时速|停车|倒车|故障车|警告标志|能见度|跟车|停车距离|雾|车速|两条机动车道",
    ),
    (
        "01",
        r"实习期|审验|申领|驾驶证|身份证|考试|补证|换证|不得申请|身体条件|年龄",
    ),
]

GA_RULES = [
    ("accident", r"事故|逃逸|急救|抢救|现场|伤员|担架"),
    ("penalty", r"记分|一次记|罚款|拘留|吊销|拘役|有期徒刑|处罚|违法"),
    ("license", r"驾驶证|实习|审验|申领|准驾|补证|换证|身份证|不得申请"),
    ("vehicle", r"制动|发动机|仪表|轮胎|转向系|离合器|冷却|机油"),
    ("local", r"北京|本市|本直辖市"),
    ("traffic", r"通行|让行|标线|信号|灯光|限速|停车|倒车|高速|车道|会车|行人"),
]

TAG_RULES = [
    ("酒驾", r"酒|醉|酒精"),
    ("逃逸", r"逃逸"),
    ("急救", r"急救|担架|止血|骨折"),
    ("记分", r"记[0-9一二三四五六九十]+分|一次记"),
    ("超速", r"超速"),
    ("超员", r"超员|超载"),
    ("超重", r"超重"),
    ("疲劳", r"疲劳"),
    ("学法减分", r"学法减分|减分"),
    ("准驾", r"准驾"),
    ("高速", r"高速|城市快速"),
    ("灯光", r"远光|近光|雾灯|灯光"),
    ("手势", r"手势"),
    ("标志", r"标志|禁令"),
    ("标线", r"标线|虚线|实线"),
    ("信号灯", r"信号灯|红灯|黄灯|绿灯"),
    ("让行", r"让行|优先|行人"),
    ("限速", r"限速|时速|公里"),
    ("停车", r"停车|倒车|故障"),
    ("能见度", r"能见度|雾"),
    ("仪表", r"仪表|ABS|感叹号"),
    ("实习审验", r"实习|审验"),
    ("刑罚", r"拘役|有期徒刑"),
]


LETTER_ONLY = re.compile(r"^[A-D][)）．、.]?$")
LETTER_START = re.compile(r"^([A-D])[)）．、.\s]*(.+)$")
NOISE_OPT = re.compile(r"^[vV＜<√✔斤]+$")


def split_options(body_lines: list[str], qtype: str) -> tuple[list[str], int | None]:
    """Return (options, index where options start)."""
    start = None
    for i, ln in enumerate(body_lines):
        c = clean_line(ln)
        if LETTER_ONLY.match(c) or LETTER_START.match(c) or c in ("正确", "错误"):
            start = i
            break
        if NOISE_OPT.match(c) or c.startswith("正确") or c.startswith("错误"):
            start = i
            break
    if start is None:
        return [], None

    raw: list[str] = []
    for ln in body_lines[start:]:
        c = clean_line(ln)
        if LETTER_ONLY.match(c) or NOISE_OPT.match(c):
            continue
        m = LETTER_START.match(c)
        piece = m.group(2) if m else c
        piece = re.sub(r"^(正确|错误).*$", r"\1", piece)
        if piece in ("正确", "错误") and qtype == "tf":
            continue
        if piece:
            raw.append(piece)

    if qtype == "tf":
        return ["正确", "错误"], start
    return normalize_choice_options(raw), start


def normalize_choice_options(raw: list[str]) -> list[str]:
    opts = [re.sub(r"^[vV＜<√✔]+", "", x) for x in raw]
    opts = [x for x in opts if x]
    while len(opts) > 4:
        i = min(range(len(opts)), key=lambda j: len(opts[j]))
        if i == 0:
            opts[0] += opts[1]
            del opts[1]
        else:
            opts[i - 1] += opts[i]
            del opts[i]
    return opts


def classify(q: str, tip: str | None) -> tuple[str, str, list[str]]:
    text = (q or "") + (tip or "")
    lesson = "other"
    for code, pat in LESSON_RULES:
        if re.search(pat, text):
            lesson = code
            break
    ga = "traffic"
    for code, pat in GA_RULES:
        if re.search(pat, text):
            ga = code
            break
    tags = [name for name, pat in TAG_RULES if re.search(pat, text)]
    return lesson, ga, tags


def load_bank() -> list[dict]:
    if BANK.exists():
        return json.loads(BANK.read_text())
    return []


def save_bank(items: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    BANK.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n")


def extract_one(doc: fitz.Document, page_no: int) -> dict:
    """page_no is 1-based."""
    page = doc[page_no - 1]
    mat = fitz.Matrix(RENDER_ZOOM, RENDER_ZOOM)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    qid = f"{page_no:03d}"
    full_png = OCR_DIR / f"p{qid}.png"
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    pix.save(full_png)

    box = find_illustration(pix)
    image_rel = None
    has_image = box is not None
    dest = IMAGES / f"q{qid}.png"
    if has_image:
        save_crop(page, box, dest)
        image_rel = f"images/q{qid}.png"
    elif dest.exists():
        dest.unlink()

    text = ocr_image(full_png)
    (OCR_DIR / f"p{qid}.txt").write_text(text)
    full_png.unlink(missing_ok=True)
    parsed = parse_ocr(text)
    lesson, ga, tags = classify(parsed["q"], parsed["tip"])

    # 如图 / 这种 usually means a figure even if crop missed
    if re.search(r"如图|这种信号|图中|图示|这种标志|图中所示", parsed["q"] or ""):
        if not has_image:
            # keep a conservative center crop so the field is not empty
            w, h = pix.width, pix.height
            fallback = (int(w * 0.10), int(h * 0.16), int(w * 0.90), int(h * 0.55))
            dest = IMAGES / f"q{qid}.png"
            save_crop(page, fallback, dest)
            has_image = True
            image_rel = f"images/q{qid}.png"

    pix = None
    return {
        "id": f"k1-q-{qid}",
        "page": page_no,
        "type": parsed["type"],
        "new_rule": parsed["new_rule"],
        "q": parsed["q"],
        "options": parsed["options"],
        "answer": parsed["answer"],
        "tip": parsed["tip"],
        "tip_kind": parsed["tip_kind"],
        "why": None,
        "lesson": lesson,
        "ga": ga,
        "tags": tags,
        "has_image": has_image,
        "image": image_rel,
        "ocr_ok": parsed["ocr_ok"],
    }


def main() -> None:
    compile_ocr()
    if not PDF.exists():
        sys.exit(f"missing {PDF}")
    doc = fitz.open(PDF)
    items = load_bank()
    done = {it["page"] for it in items}
    start = FIRST_Q_PAGE
    end = doc.page_count  # 501
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None

    pages = only if only else list(range(start, end + 1))
    for page_no in pages:
        if page_no in done and only is None:
            continue
        rec = extract_one(doc, page_no)
        items = [it for it in items if it["page"] != page_no]
        items.append(rec)
        items.sort(key=lambda it: it["page"])
        save_bank(items)
        flag = "IMG" if rec["has_image"] else "   "
        ok = "ok" if rec["ocr_ok"] else "OCR?"
        print(
            f"{rec['id']} {flag} {ok} {rec['type']} L{rec['lesson']} {rec['ga']} {rec['q'][:28]}",
            flush=True,
        )
    doc.close()
    print(f"done {len(items)} -> {BANK}")


if __name__ == "__main__":
    main()
