#!/usr/bin/env python3
"""Copy the local 500-question bank into public/ for the mock exam page."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

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

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "kb/raw/bank/k1/k1-500.json"
IMG_SRC = ROOT / "kb/raw/bank/k1/images"
OUT = ROOT / "public/practice/exam/k1"
OUT_IMG = OUT / "images"
BANK = OUT / "bank.json"
LETTERS = "ABCD"


def usable(item: dict) -> bool:
    opts = item.get("options") or []
    if item.get("type") == "tf":
        return len(opts) == 2 and item.get("answer") in {"A", "B"}
    if item.get("type") == "choice":
        return len(opts) == 4 and item.get("answer") in set(LETTERS)
    return False


def why_of(item: dict) -> str | None:
    if item.get("why"):
        return item["why"]
    if item.get("tip_kind") == "discard":
        return None
    tip = (item.get("tip") or "").strip()
    return tip or None


def compress(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["sips", "-s", "format", "jpeg", "-Z", "900", str(src), "--out", str(dest)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0 or not dest.exists():
        shutil.copy2(src, dest.with_suffix(src.suffix))


def main() -> int:
    if not SRC.exists():
        print(f"skip exam pack: missing {SRC}", file=sys.stderr)
        return 0

    raw = json.loads(SRC.read_text())
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    items = []
    images = 0
    for item in raw:
        if not usable(item):
            continue
        opts = [
            {"key": LETTERS[i], "text": scrub_opt(text)}
            for i, text in enumerate(item["options"])
        ]
        image = None
        src_name = Path(item["image"]).name if item.get("image") else None
        src_path = IMG_SRC / src_name if src_name else None
        if item.get("has_image") and src_path and src_path.exists():
            dest = OUT_IMG / (src_path.stem + ".jpg")
            if not dest.exists():
                compress(src_path, dest)
            if dest.exists():
                image = f"/practice/exam/k1/images/{dest.name}"
                images += 1
        items.append(
            {
                "id": item["id"],
                "type": item["type"],
                "q": scrub_stem(item["q"]),
                "options": opts,
                "answer": item["answer"],
                "why": why_of(item),
                "lesson": item.get("lesson"),
                "ga": item.get("ga") or "traffic",
                "image": image,
            }
        )

    BANK.write_text(
        json.dumps(
            {
                "title": "科目一模拟考试",
                "total": 100,
                "minutes": 45,
                "pass": 90,
                "pool": len(items),
                "items": items,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"exam pack {len(items)} items, {images} images -> {BANK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
