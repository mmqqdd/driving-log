# 北京 C2 速通指南

网页：https://driving-log-d25.pages.dev  
源码：[Gitee](https://gitee.com/mengqiangding/driving-log) · [GitHub](https://github.com/mmqqdd/driving-log)

顶栏：**首页**、**教学**、**日常**。

教学分三块，不挤在一列：

- **课程** —— 科目一到四。先看后练，每节底下跟测。现在摊开科目一，科二三四占位
- **练习** —— 随机一题一对错。进去再选练哪一科、哪一块
- **考试** —— 按考场规矩整卷。进去再选考哪一科

另有**资料**页：驾校 PDF 教程在页内直接预览，大扫描书按 25MB 上限拆卷。

日常记从报名到拿证的完整过程。日历是入口，不是重点。

教学正文不写驾校品牌。哪家驾校、哪个考场，写在日常和档案里。

---

## 架构

```
首页
  教学 → 课程 / 练习 / 考试
  日常 → 完整过程

顶栏
  首页    教学    日常
```

### 课程怎么长

一节 = 一件容易混的事。看完立刻练。文件一对一，加节不改框架。

```
subjects/k1/           课
  index.md             九章目录
  01-xxx.md            正文不超过两屏，底下跟测
  …

public/practice/k1/    随堂题
  01.json              只服务 01 那一节
  …

.vitepress/theme/Quiz.vue
  随机抽 10 道 · 错了出 why · 「再抽一组」
```

科二以后原样复制：`subjects/k2/` + `public/practice/k2/`。现在科二三四还是占位页 `subjects/kemu2.md`–`kemu4.md`。

### 练习和考试

| 页 | 干什么 |
|---|---|
| `subjects/practice.md` | 练习。先选科、再选块 |
| `exam.md` | 考试。科目一从精选 500 抽 100 题，45 分钟，90 过 |

模拟考题包在 `public/practice/exam/`，从 `kb/raw/bank/` 现抽，不上 git。

### 日常

```
journal/index.md       日历入口
journal/YYYY-MM-DD.md  当天经过。frontmatter 的 doing 两个字会出现在日历上
journal/process.md     从报名到拿证整条线
```

### 知识库怎么给训练供货（不上导航）

```
你丢来 PDF
    → kb/raw/              原件，不上站、不进 git
    → kb/extracts/         压成「能对回法规的几条」
    → kb/atoms/            拆成一条条结构化记忆
    → kb/questions/        500 题分类账；原题和配图在 kb/raw/bank/
    → 拆成一节课 + 一包题
    → 来源账本记一行（官方 / 驾校 / 社区）
```

| 层 | 放哪 | 干什么 |
|---|---|---|
| 原件 | `kb/raw/`（gitignore） | PDF、视频。500 题扫描件只当词典翻，不整包进站 |
| 来源账本 | `kb/sources-official.md` / `sources-community.md` | 官方、驾校，还是社区；能回答哪一步 |
| 目标拆解 | `kb/goals/kemu1.md` | 「北京 C2 科一一次过」拆成硬条件 / 会考什么 / 刷到能上场 |
| 蒸馏 | `kb/extracts/` | 长 PDF 压成能对回法规的口诀，不贴原文 |
| 原子 | `kb/atoms/k1.json` | `id` / `kind` / `claim` / `why` / `trust` / `source` / `lesson` / `c2`。蒙题法标 `discard`，不进课、不进题 |
| 题库层 | `kb/questions/` | 分类和字段。精选 500 的原文 + 裁图在 `kb/raw/bank/k1/`，不上站、不进 git |
| 课 | `subjects/k1/` | 一节一件事，底下跟测。配图 `/images/k1/`，账本 `kb/questions/k1-images.md` |
| 随堂测 | `public/practice/k1/` | 自己写的易混题，`q` / `type` / `answer` / `why` |
| 模拟考 | `exam.md` + `public/practice/exam/k1/` | 从 500 题抽 100；按 `ga` 比例；有图带图；蒙题 tip 不用 |
| 错题本 | `subjects/kemu1.md` | App 里错过的原题，压成「题意 + 为什么错」，不进 JSON |

官方和社区必须分开。口诀可以写进课里，旁边能指回法规或 12123。蒙题法（看见某词就打对）不进课、不进题。

### 一节课的最低标准

- **讲**：这一节只要记住什么（表、口诀、一句为什么）
- **练**：题包至少 16 道，上场抽 10 道，做完再抽一组
- **过**：抽一组全对，或自己点下一节。先不做账号和进度存档
- **长**：先加题，再拆节。一页超过两屏，就把一块拆出去

整本 100 题仍以驾校题库 / 12123 为准。这个站负责：**规则学会、易混题练熟**。

### 科目一：九节

考试须知 → 违法记分 → 超速超员与超重 → 限速与停车 → 交通标志与标线 → 灯光手势与仪表 → 通行与让行 → 准驾与证件 → 酒驾逃逸与急救。

电子技巧 80 条对照账：`kb/extracts/kemu1-80.md`。蒙题不进课。

---

## 本地

```bash
npm install
npm run dev
```

打开 http://localhost:5173。发布：`git push all main`，再说一声「部署一下」。
