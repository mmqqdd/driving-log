---
title: 电子技巧单元账
updated: 2026-09-04
source: kb/raw/科目一（技巧口诀+500题）/科目一2026最新电子技巧.pdf
trust: community
checked: 2026-09-04
---

# 电子技巧单元账

38 页已经整本渲染、OCR 过。**不要再整本识别。** 对某一单元，先打开这份和 `kemu1-tips.json`。

```
kb/raw/tips/k1/          本地，gitignore
  pages/p01.png–p38.png  整页
  ocr/p01.txt–p38.txt    页 OCR
  images/*.jpg           按单元裁的图（仪表、灯、手势、让行）
  units.json             和 extracts 那份相同

kb/extracts/kemu1-tips.json   进 git：每页 OCR + 121 个单元
```

重出图：`python3 scripts/extract-k1-tips.py`（已有 OCR 和页图会跳过）。

对照哪条进课：`kemu1-80.md`。口诀可读视图：`kemu1-koujue.md`。

## 整本怎么切

| 页脚 | PDF 页 | 单元 | 落到 | 图 |
|---|---|---|---|---|
| 封面 | 0 | 2026 新交规文字版 | — | 整页 |
| 1–19/35 | 1–19 | 技巧 1–80，多数是字 | 见下 | 第 9–13、18–19 页有仪表/灯/实景 |
| 20–22/35 | 20–22 | 交警手势，每种两帧一组 | 06 | 已裁 `g-*.jpg` |
| 23–29/35 | 23–29 | 各种标志汇总 | 05 | 用整页，课里另有图册 |
| 30–34/35 | 30–34 | 标线 | 05 | 用整页 |
| 35/35 | 35 | 10 月 1 日新标 | 05 | 用整页 |
| 仓库末两页 | 36–37 | 色卡（数字 / 动物） | 不上课 | 整页，体检用 |

页脚 `n/35` = PDF 第 `n` 页（封面是第 0 页）。文件名 `p01` = 封面，`p02` = 第 1/35。

## 有独立图的单元

裁在 `kb/raw/tips/k1/images/`。框偏了以整页为准，不要为了修一张图再 OCR。

| 文件 | 是什么 | 课 |
|---|---|---|
| `img-rpm` / `img-speedo` | 转速到 8 / 车速到 240 | 06 |
| `img-brake` / `img-park` | `(!)` 制动 / `(P)` 手刹 | 06 |
| `img-high-beam` / `img-low-beam` | 直远斜近 | 06 |
| `img-fog-front` / `img-fog-rear` | 前绿后黄 | 06 |
| `img-fog-trap` | 题干写后雾灯、图是前雾灯 | 06 |
| `img-position` / `img-master-light` | 示廓成对 / 太阳总开关 | 06 |
| `img-meet-yield` / `img-meet-priority` | 谁胖谁先走 | 05 |
| `img-stop` / `img-yield` | 8 停 3 减 | 05 |
| `g-stop` … `g-right` | 手势两帧一组 | 06 |
| `img-police-scene` | 路口举左手实景 | 06 |
| `img-ignition` 等 | 点火开关、圆方仪表 | discard |
| `img-man-nosign` / `img-man-sign` | 男子和牌子 | discard |

标志汇总、标线没有逐标再裁一遍：一页就是一张图册，课里用 `public/images/k1/signs-*.jpg`。

## 80 条怎么用

能对回法规的上课。看见某词就打对 / 打错的标 `discard`，图可以留着对照，不进课、不进随堂测。

细表仍以 `kemu1-80.md` 为准。JSON 里每条有 `id`（`tip-01`）、`action`、`lesson`、`pdf_page`。
