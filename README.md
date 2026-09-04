# 北京 C2 速通指南

网页：https://driving-log-d25.pages.dev  
源码：[Gitee](https://gitee.com/mengqiangding/driving-log) · [GitHub](https://github.com/mmqqdd/driving-log)

网站两栏：**教学**、**日常**。科目一按「一章一课 + 一包题」长。科二科三以后套同一套架子。

---

## 架构

### 打开网站时

```
首页
  教学 → 课程 / 练习 / 考试
  日常 → 日历（格子上两个字就是那天在干什么）

顶栏
  教学    日常
```

日常用日历看，不按「故事 / 流程」再拆。流程页留一句链接。科二三四在课程里占位，不摊开项目。

### 训练模块

一节 = 一件容易混的事。看完立刻练。文件一对一，加节不改框架。

```
subjects/k1/           课（给人看）
  index.md             目录：现在练到哪、下一节是哪
  01-xxx.md            正文不超过两屏
  02-xxx.md
  …

public/practice/k1/    题（给 Quiz 抽）
  01.json              只服务 01 那一节
  02.json
  …

.vitepress/theme/Quiz.vue
  随机抽 N 道 · 错了出 why · 「再抽一组」
```

一节课底部只写一行：`<Quiz src="/practice/k1/01.json" />`。题变多，页面不用动。

科二以后原样复制：`subjects/k2/` + `public/practice/k2/`。

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

### 旧入口

| 现在 | 处理 |
|---|---|
| `subjects/k1/01`–`06` | 留下，当训练模块第一版 |
| `kemu1-guide.md`、`practice.md`、`subjects/index.md` | 重定向到 `k1/`，不再当入口 |
| `kb/` | 继续给写课用，不上顶栏 |
| `kemu2.md` / `kemu3.md` / `kemu4.md` | 留文件，导航里先藏 |

---

## 本地

```bash
npm install
npm run dev
```

打开 http://localhost:5173。发布：`git push all main`，再说一声「部署一下」。
