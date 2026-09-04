---
title: 科目一题库层
updated: 2026-09-03
---

# 科目一题库层

随堂测是自己写的，在 `public/practice/k1/`。  
课里的配图账：`kb/questions/k1-images.md`，文件在 `public/images/k1/`。  

模拟考要从「精选 500」里抽。原文仍在 `kb/raw/bank/`，不上 git。组卷时拷到 `public/practice/exam/`（也 gitignore），页面是 `exam.md`。

```
kb/raw/科目一（技巧口诀+500题）/科目一精选500题＋新规.pdf
    → 抽题 + 裁图
    → kb/raw/bank/k1/k1-500.json
    → kb/raw/bank/k1/images/q002.png
```

第 1 页是使用说明。第 2–501 页一页一题，题号和页码对齐：`k1-q-002` ↔ `images/q002.png`。

## 字段

| 字段 | 含义 |
|---|---|
| `id` | `k1-q-002` |
| `page` | PDF 页码 |
| `type` | `tf` 判断 / `choice` 单选 |
| `new_rule` | 页上有「新规题」 |
| `q` | 题干 |
| `options` | 选项数组。判断题是「正确 / 错误」 |
| `answer` | `A`–`D` |
| `tip` | 页上的口诀。`tip_kind=discard` 的（看见某词就选）以后模拟考不用 |
| `tip_kind` | `discard` / `mnemonic` / `explain` |
| `lesson` | `01`–`09`，对上九节课；对不上是 `other` |
| `ga` | GA 1026 组卷类，模拟考按这个抽比例 |
| `tags` | 更细的标签 |
| `has_image` | 有没有情景图 / 标线 / 标志 / 仪表 |
| `image` | 有图写 `images/q002.png`，没图写 `null` |
| `ocr_ok` | OCR 是否把题干和答案读全 |

## 分类

`lesson` 跟现在九节课走：

| lesson | 节 | 收哪些 |
|---|---|---|
| `01` | 考试须知 | 考试规定、候考厅 |
| `02` | 违法记分 | 12 / 9 / 6 / 3 / 1 |
| `03` | 超速、超员与超重 | 超速、超员、超重、疲劳 |
| `04` | 限速与停车 | 默认限速、能见度、禁停距离、故障标志 |
| `05` | 交通标志与标线 | 颜色、警告禁令、虚实线 |
| `06` | 灯光、手势与仪表 | 灯光、交警手势、仪表、英文 |
| `07` | 通行与让行 | 信号灯、行人、超车、铁路道口 |
| `08` | 准驾与证件 | 准驾、学法减分、随车证件、ABS |
| `09` | 酒驾、逃逸与急救 | 酒驾、逃逸、急救、无争议离开 |
| `other` | — | 还对不上的 |

`ga` 按 GA 1026 小型自动挡组卷（模拟考用）：

| ga | 官方块 | C2 大约 |
|---|---|---|
| `license` | 驾驶证和机动车管理规定 | 20% |
| `traffic` | 道路通行条件及通行规定 | 25% |
| `penalty` | 道路交通安全违法行为及处罚 | 25% |
| `accident` | 道路交通事故处理相关规定 | 10% |
| `vehicle` | 机动车基础知识 | 10% |
| `local` | 地方性法规 | 10% |

## 图

只裁题干和选项之间的情景图 / 标线图 / 标志 / 仪表，不存整页。  
没有这类图的题 `has_image=false`，`image=null`。  
`kb/raw/bank/` 跟 PDF 一样 gitignore，公开站 `/images` 不塞。

## 模拟考怎么用

`scripts/publish-k1-exam.py` 从 `k1-500.json` 抽出能用的题（选项齐全），图压成 jpg。  
`Exam.vue` 抽 100 道：判断约 40、单选约 60，再按 `ga` 比例。  
`why` 用法规意思或口诀，不用 `tip_kind=discard` 的蒙题句。
