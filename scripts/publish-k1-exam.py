#!/usr/bin/env python3
"""Copy the local 500-question bank into public/ for the mock exam page."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

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
            {"key": LETTERS[i], "text": str(text).strip()}
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
                "q": item["q"],
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
