# 知识库（不上网站）

给人看的入口是 `kb/index.md` → 网站「资料」。本页只给写攻略用。

## 怎么用

用户丢来一个目标（比如「科目一一次过」），按 `make-guide` 走：

```
1. 拆目标          →  kb/goals/<id>.md
2. 收集资料（最难） →  kb/sources-official.md
                     kb/sources-community.md
3. 用户丢来的原包   →  kb/raw/（不上 git、不上网站）
4. 读完蒸馏        →  kb/extracts/
5. 写成攻略        →  subjects/<id>-guide.md
6. 能练的做成练习  →  public/practice/<id>.json + subjects/practice.md
```

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

## 练习题从哪来

- **自己写的易混规则**：根据公开法规改写成判断 / 选择，进 `public/practice/`。
- **不抄**驾考宝典、一点通、东方时尚题库原文。完整题库不公开，也不该整包搬进仓库。
- 用户错过的题：压缩成一句「题意 + 为什么错」，写进 `subjects/kemuN.md`，不要粘贴整道原题。
- 用户收来的「精选 500」扫描件：只放 `kb/raw/`，提炼口诀进 `extracts/`，原题不进仓库。
