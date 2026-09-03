# 知识库（不上网站）

`kb/**` 整棵不上站。给人看的是 `subjects/k1/` 和考试记录。本页只给写课用。

供货：`raw` → `extracts` → **`atoms`** → 课 + 随堂测。  
精选 500 另走：`raw` → `kb/raw/bank/k1/`（题 + 裁图）→ `kb/questions/`（分类账）。模拟考以后从这份库抽，先不上站。

## 怎么用

用户丢来一个目标（比如「科目一一次过」），按 `make-guide` 走：

```
1. 拆目标          →  kb/goals/<id>.md
2. 收集资料（最难） →  kb/sources-official.md
                     kb/sources-community.md
3. 用户丢来的原包   →  kb/raw/（不上 git、不上网站）
4. 读完蒸馏        →  kb/extracts/
5. 拆成原子        →  kb/atoms/<科>.json
6. 精选题库（可选） →  kb/raw/bank/ + kb/questions/
7. 写成课          →  subjects/k1/（一节一页）
8. 能练的做成练习  →  public/practice/k1/0x.json
```

旧入口 `subjects/kemu1-guide.md`、`practice.md` 只重定向到 `k1/`，不要再写一套正文。

资料分两层，不要混：

| 层 | 放哪 | 能不能当唯一依据 |
|---|---|---|
| **官方公开** | `sources-official.md` | 能。法规、国标、部委文件、12123 |
| **驾校指定** | 也记在 official，标 `school` | 约考认这个，但不是国家标准全文 |
| **UP / 博主** | `sources-community.md` | 不能。只用来讲清楚、记口诀，必须能对回官方 |

## 一条资料最低要有

- `name` / `url` / `kind`（law / standard / app / book / video / blog）
- `trust`：`official` | `school` | `community`
- `use`：这篇能回答目标里的哪一步
- `checked`：哪天核过还在

过不了「说得清为什么收」的，不进库。宁缺毋滥。

## 原子

`kb/atoms/k1.json` 是数组。字段：`id`、`kind`（rule / pit / mnemonic / discard）、`claim`、`why`、`trust`、`source`、`lesson`（01–06 或 null）、`c2`。

蒙题法（看见「应当」就打对等）标 `discard`，不进课、不进练习。`extracts/kemu1-koujue.md` 是同一批原子的可读视图，不要删。

## 练习题从哪来

- **自己写的易混规则**：根据公开法规和原子改写成判断 / 选择，进 `public/practice/k1/`。
- **不抄**驾考宝典、一点通、东方时尚题库原文。完整题库不公开，也不该整包搬进仓库。
- 用户错过的题：压缩成一句「题意 + 为什么错」，写进 `subjects/kemu1.md` 和对应 `subjects/k1/` 课，不要粘贴整道原题。
- 用户收来的「精选 500」：抽进 `kb/raw/bank/k1/k1-500.json`，配图裁进 `images/q002.png`。分类账在 `kb/questions/`。原题和配图不上 git、不上网站。蒙题 tip 标 `discard`。
- 随堂测仍自己写，不把这 500 道抄进 `public/practice/`。
